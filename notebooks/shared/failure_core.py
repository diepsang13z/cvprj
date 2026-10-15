from cloud_runtime import require_cloud
require_cloud()

import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import cv2
import matplotlib
import numpy as np
import torch
from IPython.display import Markdown, display

# Chỉ ép backend không tương tác khi chạy như script; trong notebook phải hiển thị inline.
try:
    get_ipython  # noqa: B018
    IN_NOTEBOOK = True
except NameError:
    IN_NOTEBOOK = False
if not IN_NOTEBOOK:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path.cwd() if (Path.cwd() / "requirements.txt").exists() else Path.cwd().parent
SEQUENCES = ("phantom3-village-kfs", "phantom3-grass-kfs")
# Cửa sổ chọn theo scan 160 bước (docs/logs/progress): nơi matcher thật sự sai
#   village: SIFT-640 sai 5-11 px ở các bước 86-98, 116-137 -> cửa sổ 80..125
#   grass:   EfficientLoFTR vỡ 5-190 px ngay từ bước đầu    -> cửa sổ 0..45
WINDOWS = {"phantom3-village-kfs": (80, 45), "phantom3-grass-kfs": (0, 45)}
MAX_SIDE = 640
MAX_KEYPOINTS = 2000
RANSAC_PX = 3.0
RATIO = 0.75
DEVICE = "cpu"
MIN_INLIERS = 100          # RDR-0007: ngưỡng hợp lệ của matcher tham chiếu
TOLERANCE_PX = 2.0         # ngưỡng "bước ghép sai": nằm ở mức nền nhiễu của chính SIFT (RDR-0007)
TAU_NCC = 0.95             # TẠM — nhóm chưa chốt bằng RDR
TAU_INLIER_RATIO = 0.30    # TẠM — nhóm chưa chốt bằng RDR
TAU_GRID = (0.90, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99)
ESCALATION_BUDGET = 0.25
ANCHOR_BACK = 3
CHEAP = "sift_bf"
STRONG = "superpoint_lightglue"
DIAGNOSTIC = "efficientloftr"
FULLRES = "superpoint_lightglue@full"
POLICIES = ("none", "drop", "anchor", "split")
print("Root:", ROOT, "| torch", torch.__version__, "| opencv", cv2.__version__)


# Tải ảnh ở độ phân giải làm việc. Mọi homography trả về hệ pixel ảnh ĐÃ resize;
# hàm to_original() đưa về hệ pixel ảnh gốc để so với matcher tham chiếu.
def frames_of(sequence, start, count, max_side=MAX_SIDE):
    folders = list((ROOT / "data" / sequence).rglob("rgb"))
    if len(folders) != 1:
        raise ValueError(f"cần đúng một thư mục rgb: {sequence}")
    files = sorted(folders[0].glob("*.jpg"), key=lambda p: float(p.stem))[start:start + count + 1]
    if len(files) != count + 1:
        raise ValueError(f"{sequence}: chỉ có {len(files)} frame, cần {count + 1}")
    images, size = [], None
    for path in files:
        bgr = cv2.imread(str(path))
        if bgr is None:
            raise ValueError(f"không đọc được {path}")
        size = (bgr.shape[1], bgr.shape[0])
        scale = min(1, max_side / max(bgr.shape[:2]))
        resized = (max(32, int(bgr.shape[1] * scale) // 32 * 32),
                   max(32, int(bgr.shape[0] * scale) // 32 * 32))
        images.append(cv2.cvtColor(cv2.resize(bgr, resized, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB))
    return files, images, size


def to_original(H, processed, original):
    """H ở hệ pixel ảnh resize -> hệ pixel ảnh gốc."""
    D = np.diag([original[0] / processed[0], original[1] / processed[1], 1.0])
    return D @ H @ np.linalg.inv(D)


class LazyImages:
    """Danh sách ảnh gốc chỉ nạp khi thật sự dùng — leo thang full-res chỉ cần vài frame."""

    def __init__(self, files):
        self.files, self.cache = list(files), {}

    def __getitem__(self, index):
        if index not in self.cache:
            bgr = cv2.imread(str(self.files[index]))
            if bgr is None:
                raise ValueError(f"không đọc được {self.files[index]}")
            self.cache[index] = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        return self.cache[index]

    def __len__(self):
        return len(self.files)


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")


def fmt(value, width, digits=2):
    """In số an toàn: giá trị có thể là None (chưa đo được) thì ghi 'n/a'."""
    return "n/a".rjust(width) if value is None else f"{value:{width}.{digits}f}"


# Adapter matcher — giữ nguyên giao diện của notebook 03 để dùng chung.
def tensor(image, device):
    return torch.from_numpy(image.copy()).permute(2, 0, 1).float().to(device) / 255


def load_matcher(method, device, max_points=MAX_KEYPOINTS):
    if method == CHEAP:
        detector = cv2.SIFT_create(nfeatures=max_points)
        matcher = cv2.BFMatcher(cv2.NORM_L2)

        def match(a, b):
            detected = [detector.detectAndCompute(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), None) for img in (a, b)]
            (k0, d0), (k1, d1) = detected
            if d0 is None or d1 is None or len(d1) < 2:
                return np.empty((0, 2), np.float32), np.empty((0, 2), np.float32)
            good = [m for pair in matcher.knnMatch(d0, d1, k=2) if len(pair) == 2
                    for m, n in [pair] if m.distance < RATIO * n.distance]
            return (np.float32([k0[m.queryIdx].pt for m in good]).reshape(-1, 2),
                    np.float32([k1[m.trainIdx].pt for m in good]).reshape(-1, 2))
        return match
    if method == STRONG:
        from lightglue import LightGlue, SuperPoint
        from lightglue.utils import rbd
        extractor = SuperPoint(max_num_keypoints=max_points).eval().to(device)
        matcher = LightGlue(features="superpoint").eval().to(device)
        extractor.requires_grad_(False)
        matcher.requires_grad_(False)

        @torch.inference_mode()
        def match(a, b):
            features = [extractor.extract(tensor(img, device), resize=None) for img in (a, b)]
            if min(f["keypoints"].shape[1] for f in features) == 0:
                return np.empty((0, 2), np.float32), np.empty((0, 2), np.float32)
            index = rbd(matcher({"image0": features[0], "image1": features[1]}))["matches"]
            return (rbd(features[0])["keypoints"][index[:, 0]].cpu().numpy(),
                    rbd(features[1])["keypoints"][index[:, 1]].cpu().numpy())
        return match
    if method == DIAGNOSTIC:
        from transformers import AutoImageProcessor, AutoModelForKeypointMatching
        source = "zju-community/efficientloftr"
        revision = "face1a79050ffa3e9da28720d1cf93aaf2e8f421"
        processor = AutoImageProcessor.from_pretrained(source, revision=revision)
        model = AutoModelForKeypointMatching.from_pretrained(source, revision=revision).eval().to(device)
        model.requires_grad_(False)

        @torch.inference_mode()
        def match(a, b):
            inputs = processor([a, b], do_resize=False, return_tensors="pt").to(device)
            out = processor.post_process_keypoint_matching(
                model(**inputs), [[a.shape[:2], b.shape[:2]]], threshold=0.2)[0]
            return out["keypoints0"].cpu().numpy(), out["keypoints1"].cpu().numpy()
        return match
    raise ValueError(method)


# Matcher tham chiếu (RDR-0007) + hình học + chỉ báo rẻ.
REFERENCE_SIFT = cv2.SIFT_create(nfeatures=4000)
REFERENCE_BF = cv2.BFMatcher(cv2.NORM_L2)
_REFERENCE_CACHE = {}
_MATCH_CACHE = {}


def reference_pair(path_a, path_b):
    """H của cặp (b -> a) ở ẢNH GỐC bằng SIFT 4000 đặc trưng; có cache."""
    key = (str(path_a), str(path_b))
    if key in _REFERENCE_CACHE:
        return _REFERENCE_CACHE[key]
    started = time.perf_counter()
    grays = [cv2.imread(str(p), cv2.IMREAD_GRAYSCALE) for p in (path_a, path_b)]
    if any(g is None for g in grays):
        raise ValueError("reference: không đọc được ảnh")
    detected = [REFERENCE_SIFT.detectAndCompute(g, None) for g in grays]
    (k0, d0), (k1, d1) = detected
    if d0 is None or d1 is None:
        raise ValueError("reference: không đủ đặc trưng")
    good = [m for pair in REFERENCE_BF.knnMatch(d0, d1, k=2) if len(pair) == 2
            for m, n in [pair] if m.distance < RATIO * n.distance]
    if len(good) < 4:
        raise ValueError(f"reference: chỉ {len(good)} match")
    p0 = np.float32([k0[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    p1 = np.float32([k1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    cv2.setRNGSeed(0)
    H, mask = cv2.findHomography(p1, p0, cv2.RANSAC, RANSAC_PX)
    if H is None or not np.isfinite(H).all():
        raise ValueError("reference: RANSAC thất bại")
    _REFERENCE_CACHE[key] = (H / H[2, 2], int(mask.sum()), len(good), time.perf_counter() - started)
    return _REFERENCE_CACHE[key]


def geometry(p0, p1):
    """H ánh xạ p1 -> p0 (frame hiện tại -> frame trước), RANSAC cố định seed."""
    if len(p0) < 4:
        return None, np.zeros(len(p0), bool), None
    cv2.setRNGSeed(0)
    H, mask = cv2.findHomography(p1, p0, cv2.RANSAC, RANSAC_PX)
    if H is None or mask is None or not np.isfinite(H).all() or np.linalg.matrix_rank(H) != 3:
        return None, np.zeros(len(p0), bool), None
    good = mask.ravel().astype(bool)
    if good.sum() < 4:
        return None, good, None
    predicted = cv2.perspectiveTransform(p1[good].reshape(-1, 1, 2), H).reshape(-1, 2)
    rmse = float(np.sqrt(np.mean(np.sum((predicted - p0[good]) ** 2, axis=1))))
    return H, good, rmse if np.isfinite(rmse) else None


def quad_points(shape):
    h, w = shape[:2]
    return np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)


def indicators(a, b, p0, p1, good, H):
    """Sáu chỉ báo rẻ: đếm/tỉ lệ điểm, phân tán không gian, vùng chồng, tương phản sau khi ghép, RMSE."""
    h, w = b.shape[:2]
    inliers = p0[good]
    out = {"matches": int(len(p0)), "inliers": int(good.sum()),
           "inlier_ratio": float(good.sum() / max(len(p0), 1))}
    hull = cv2.convexHull(np.float32(inliers)).reshape(-1, 2) if inliers.shape[0] >= 3 else None
    out["hull_area_ratio"] = float(cv2.contourArea(hull) / (h * w)) if hull is not None else 0.0
    inter, _ = cv2.intersectConvexConvex(quad_points(a.shape), cv2.perspectiveTransform(quad_points(b.shape), H))
    out["overlap_ratio"] = float(inter / float(w * h))
    gray_a = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(np.float32)
    gray_b = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY).astype(np.float32)
    inverse = np.linalg.inv(H)
    warped = cv2.warpPerspective(gray_a, inverse, (w, h))
    mask = cv2.warpPerspective(np.ones_like(gray_a), inverse, (w, h)) > 0.5
    x, y = warped[mask], gray_b[mask]
    x, y = x - x.mean(), y - y.mean()
    out["photo_ncc"] = float((x * y).sum() / (np.sqrt((x * x).sum() * (y * y).sum()) + 1e-9))
    out["photo_bad_frac"] = float(np.mean(np.abs(x - y) > 25))
    return out


def marker_error(H_a, H_b, size):
    pts = np.float32([[0, 0], [size[0], 0], [size[0], size[1]], [0, size[1]],
                      [size[0] / 2, size[1] / 2]]).reshape(-1, 1, 2)
    a = cv2.perspectiveTransform(pts, H_a).reshape(-1, 2)
    b = cv2.perspectiveTransform(pts, H_b).reshape(-1, 2)
    if not (np.isfinite(a).all() and np.isfinite(b).all()):
        raise ValueError("phép chiếu không hữu hạn")
    return float(np.mean(np.linalg.norm(a - b, axis=1)))


def estimate_cached(method, matcher, images, files, index_a, index_b, size_processed, size_original,
                    paths=None):
    """Đo một cặp bằng matcher; cache toàn cục để các chiến lược RQ3 dùng lại kết quả."""
    key = (method, size_processed, str((paths or files)[index_a]), str((paths or files)[index_b]))
    if key in _MATCH_CACHE:
        return _MATCH_CACHE[key]
    started = time.perf_counter()
    p0, p1 = matcher(images[index_a], images[index_b])
    seconds = time.perf_counter() - started
    p0 = np.asarray(p0, np.float32).reshape(-1, 2)
    p1 = np.asarray(p1, np.float32).reshape(-1, 2)
    H, good, rmse = geometry(p0, p1)
    row = {"status": "success" if H is not None else "failed", "seconds": seconds, "rmse_px": rmse}
    if H is not None:
        row.update(indicators(images[index_a], images[index_b], p0, p1, good, H))
        row["H_processed"] = H.tolist()
        row["H_original"] = to_original(H, size_processed, size_original).tolist()
    _MATCH_CACHE[key] = row
    return row


def risk(row, tau_ncc=TAU_NCC, tau_ratio=TAU_INLIER_RATIO):
    """Rủi ro: matcher không ra H, tương phản sau khi ghép kém, hoặc quá ít inlier."""
    if row["status"] != "success":
        return True
    return row["photo_ncc"] < tau_ncc or row["inlier_ratio"] < tau_ratio


# Đo cả cửa sổ: matcher tham chiếu cho từng bước + ba matcher, lưu mọi chỉ báo.
def scan_window(sequence, start, steps, methods=(CHEAP, STRONG, DIAGNOSTIC)):
    files, images, size_original = frames_of(sequence, start, steps)
    size_processed = (images[0].shape[1], images[0].shape[0])
    reference, chain = {}, [np.eye(3)]
    for step in range(1, steps + 1):
        H_ref, inliers, matches, seconds = reference_pair(files[step - 1], files[step])
        reference[step] = {"H_original": H_ref.tolist(), "inliers": inliers, "matches": matches,
                           "seconds": seconds, "valid": inliers >= MIN_INLIERS}
        chain.append(chain[-1] @ H_ref)
    matchers, rows = {}, {}
    for method in methods:
        matchers[method] = load_matcher(method, DEVICE)
        per_step = {}
        for step in range(1, steps + 1):
            row = dict(estimate_cached(method, matchers[method], images, files, step - 1, step,
                                       size_processed, size_original), step=step, tier=method)
            if row["status"] == "success":
                H = to_original(np.array(row["H_processed"]), size_processed, size_original)
                row["step_error_px"] = marker_error(H, np.array(reference[step]["H_original"]), size_original)
            per_step[step] = row
        rows[method] = per_step
        errors = [r["step_error_px"] for r in per_step.values() if r["status"] == "success"]
        print(f"  {method:22} step_err trung vị {np.median(errors):6.2f} | lớn nhất {np.max(errors):8.2f} px | "
              f"{sum(r['seconds'] for r in per_step.values()):6.1f}s | "
              f"lỗi hẳn {sum(1 for r in per_step.values() if r['status'] != 'success')} bước")
    weak = [step for step, value in reference.items() if not value["valid"]]
    if weak:
        print(f"  CẢNH BÁO: {len(weak)}/{steps} bước có tham chiếu dưới {MIN_INLIERS} inlier "
              f"(RDR-0007) -> loại khỏi RQ1, vẫn giữ trong chuỗi RQ2/RQ3: {weak}")
    return {"sequence": sequence, "start": start, "steps": steps, "size_original": size_original,
            "size_processed": size_processed, "files": files, "images": images,
            "reference": reference, "reference_chain": [c.tolist() for c in chain],
            "reference_invalid_steps": weak, "rows": rows}


# RQ1: chỉ báo nào báo được bước ghép sai? (Spearman + AUC so với sai số thật của bước)
INDICATOR_NAMES = ("photo_ncc", "photo_bad_frac", "inlier_ratio", "inliers", "matches",
                   "hull_area_ratio", "overlap_ratio", "rmse_px")


def average_ranks(values):
    """Rank trung bình cho giá trị đồng hạng (đúng chuẩn Spearman; tránh rank giả theo thứ tự xuất hiện)."""
    values = np.asarray(values, float)
    ranks = np.empty(len(values), float)
    ranks[np.argsort(values, kind="mergesort")] = np.arange(1, len(values) + 1)
    unique, inverse, counts = np.unique(values, return_inverse=True, return_counts=True)
    if len(unique) == len(values):
        return ranks
    inverse = inverse.reshape(-1)
    for index, count in enumerate(counts):
        if count > 1:
            ranks[inverse == index] = ranks[inverse == index].mean()
    return ranks


def spearman(x, y):
    """Spearman có xử lý đồng hạng; trả None nếu một biến không đổi (tương quan vô định)."""
    rx = average_ranks(x) - (len(x) + 1) / 2
    ry = average_ranks(y) - (len(y) + 1) / 2
    denominator = np.sqrt((rx * rx).sum() * (ry * ry).sum())
    return float((rx * ry).sum() / denominator) if denominator > 0 else None


def auc(scores, labels):
    """AUC kiểu hạng, không cần sklearn; score lớn hơn = nghi ngờ hơn."""
    scores, labels = np.asarray(scores, float), np.asarray(labels, bool)
    if labels.all() or not labels.any():
        return None      # không có cả hai lớp -> AUC vô nghĩa, ghi None chứ không ghi NaN
    ranks = np.empty(len(scores), float)
    ranks[np.argsort(scores)] = np.arange(1, len(scores) + 1)
    for value, count in zip(*np.unique(scores, return_counts=True)):
        if count > 1:
            ranks[scores == value] = ranks[scores == value].mean()
    n_pos, n_neg = labels.sum(), (~labels).sum()
    return float((ranks[labels].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


# Chiều "nghi ngờ" của từng chỉ báo (điểm cao = dễ là bước ghép sai) khai báo TRƯỚC khi nhìn nhãn,
# theo ý nghĩa vật lý. Bản cũ lấy max(AUC, 1−AUC) sau khi nhìn nhãn = tự chọn chiều có lợi.
INDICATOR_SUSPICION = {"photo_ncc": -1.0, "photo_bad_frac": 1.0, "inlier_ratio": -1.0,
                       "inliers": -1.0, "matches": -1.0, "hull_area_ratio": -1.0,
                       "overlap_ratio": -1.0, "rmse_px": 1.0}


def rq1_table(scans, tolerance_px=TOLERANCE_PX):
    table = []
    for scan in scans:
        invalid = set(scan["reference_invalid_steps"])
        for tier, per_step in scan["rows"].items():
            # Chỉ chấm điểm bước có cả matcher chạy được LẪN tham chiếu đạt ngưỡng RDR-0007.
            rows = [r for step, r in per_step.items() if r["status"] == "success" and step not in invalid]
            if not rows:
                continue
            labels = [r["step_error_px"] > tolerance_px for r in rows]
            for name in INDICATOR_NAMES:
                if name not in rows[0]:
                    continue
                values = [r[name] for r in rows]
                # AUC theo chiều đã khai báo ở trên: < 0.5 nghĩa là chỉ báo tách NGƯỢC chiều kỳ vọng.
                table.append({"sequence": scan["sequence"], "tier": tier, "indicator": name,
                              "n_steps": len(rows), "n_bad_steps": int(sum(labels)),
                              "n_invalid_reference": len(invalid),
                              "spearman_vs_step_error": spearman(values, [r["step_error_px"] for r in rows]),
                              "auc_bad_step": auc([INDICATOR_SUSPICION[name] * v for v in values], labels)})
    return table


# RQ2: mô phỏng chính sách phân luồng trên log đã đo (không chạy lại matcher).
def chain_from_steps(chosen, reference_chain):
    """Chuỗi H tích luỹ; dừng ở bước đầu tiên không có H (row lỗi thiếu H_original) thay vì KeyError."""
    chain = [np.eye(3)]
    for position in range(1, len(reference_chain)):
        pick = chosen.get(position)
        if pick is None or pick.get("status") != "success" or "H_original" not in pick:
            break
        chain.append(chain[-1] @ np.array(pick["H_original"], float))
    return chain


def simulate(scan, policy, strong=STRONG, tau_ncc=TAU_NCC, tau_ratio=TAU_INLIER_RATIO, strong_rows=None):
    rows = scan["rows"]
    strong_rows = strong_rows or rows[strong]
    size_original = scan["size_original"]
    reference_chain = [np.array(c, float) for c in scan["reference_chain"]]
    chosen, seconds, escalations = {}, 0.0, 0
    for step in range(1, scan["steps"] + 1):
        cheap = rows[CHEAP][step]
        if policy == "classical":
            pick, run = cheap, [cheap]
        elif policy == "learned":
            pick, run = strong_rows[step], [strong_rows[step]]
        else:
            if risk(cheap, tau_ncc, tau_ratio):
                pick, run = strong_rows[step], [cheap, strong_rows[step]]
                escalations += 1
            else:
                pick, run = cheap, [cheap]
        seconds += sum(r["seconds"] for r in run)
        chosen[step] = pick
    chain = chain_from_steps(chosen, reference_chain)
    drift = [marker_error(chain[i], reference_chain[i], size_original) for i in range(len(chain))]
    errors = [chosen[s]["step_error_px"] for s in sorted(chosen) if chosen[s]["status"] == "success"]
    return {"policy": policy, "tau_ncc": tau_ncc if policy == "routed" else None,
            "steps": len(chosen), "failed_steps": sum(1 for s in chosen if chosen[s]["status"] != "success"),
            "chained_steps": len(chain) - 1,
            "reference_invalid_steps": len(scan["reference_invalid_steps"]),
            "escalations": escalations, "escalation_rate": escalations / max(len(chosen), 1),
            "seconds": seconds, "step_error_mean_px": float(np.mean(errors)),
            "step_error_p95_px": float(np.percentile(errors, 95)), "step_error_max_px": float(np.max(errors)),
            "final_drift_px": drift[-1], "drift_series": drift}


def choose_tau(sweep, budget=ESCALATION_BUDGET):
    """Ngưỡng LỚN NHẤT mà mọi sequence vẫn nằm trong ngân sách leo thang.

    Leo thang đơn điệu theo τ (τ càng cao càng nhiều bước bị gắn cờ), nên điểm làm việc hợp lý là
    ngưỡng cao nhất còn trong ngân sách — tức là dùng hết ngân sách để bắt lỗi, chứ không phải ít nhất.
    """
    routed = [row for row in sweep if row["policy"] == "routed" and row["tau_ncc"] is not None]
    if not routed:
        return None
    eligible = [tau for tau in {row["tau_ncc"] for row in routed}
                if all(row["escalation_rate"] <= budget for row in routed if row["tau_ncc"] == tau)]
    return max(eligible) if eligible else None


# RQ3: pipeline online — ngưỡng rủi ro + chiến lược phục hồi, chạy thật (không mô phỏng).
class OnlinePipeline:
    def __init__(self, method, matcher, files, images, size_original, policy,
                 tau_ncc=TAU_NCC, tau_ratio=TAU_INLIER_RATIO, anchor_back=ANCHOR_BACK):
        self.method = method
        self.matcher = matcher
        self.files = files
        self.images = images
        self.size_original = size_original
        self.size_processed = (images[0].shape[1], images[0].shape[0])
        self.policy = policy
        self.tau_ncc = tau_ncc
        self.tau_ratio = tau_ratio
        self.anchor_back = anchor_back
        self.cost = 0.0
        self.triggers = self.skips = self.anchored = self.splits = 0
        self.reference_invalid_used = 0     # số lần đo bằng cặp tham chiếu dưới ngưỡng RDR-0007
        self.submosaic_of = {0: 0}
        self.submosaic_root = {0: 0}      # id submosaic -> CHỈ SỐ frame gốc của nó
        self.H_to_root = {0: np.eye(3)}
        self.steps = {}

    def estimate(self, index_a, index_b):
        row = estimate_cached(self.method, self.matcher, self.images, self.files, index_a, index_b,
                              self.size_processed, self.size_original)
        self.cost += row["seconds"]          # tính chi phí kể cả khi lấy từ cache
        return row

    def step_error(self, previous, current, H_original):
        H_ref, inliers, _, _ = reference_pair(self.files[previous], self.files[current])
        if inliers < MIN_INLIERS:
            self.reference_invalid_used += 1
        return marker_error(np.array(H_original, float), np.array(H_ref, float), self.size_original)

    def try_anchor(self, placed, index):
        """Neo vào các frame ĐÃ được đặt gần nhất, trừ frame vừa ghép hỏng.

        Frame chưa đặt không có H về gốc, nên bản cũ (quét mọi frame trước đó) có thể
        chọn một frame như vậy rồi tra H_to_root -> KeyError hoặc drift sai gốc.
        """
        for anchor in reversed(placed[:-1][-self.anchor_back:]):
            candidate = self.estimate(anchor, index)
            if not risk(candidate, self.tau_ncc, self.tau_ratio):
                return dict(candidate, anchor=anchor)
        return None

    def run(self, steps):
        self.steps_total = steps
        placed, submosaic, index = [0], 0, 1
        while index <= steps:
            previous = placed[-1]
            row = self.estimate(previous, index)
            reason, used = "tier", row
            if risk(row, self.tau_ncc, self.tau_ratio):
                self.triggers += 1
                if self.policy == "none":
                    reason = "accept_risky"
                elif self.policy == "drop":
                    used, reason = None, "drop"
                elif self.policy == "split":
                    used, reason = None, "split"
                elif self.policy == "anchor":
                    used = self.try_anchor(placed, index)
                    reason = "anchor" if used else "drop"
            if used is not None and used["status"] == "success":
                root = used["anchor"] if reason == "anchor" else previous
                self.H_to_root[index] = self.H_to_root[root] @ np.array(used["H_original"], float)
                self.submosaic_of[index] = self.submosaic_of[root]
                self.steps[index] = {"reason": reason, "anchor": root,
                                     "step_error_px": self.step_error(root, index, used["H_original"])}
                placed.append(index)
                if reason == "anchor":
                    self.anchored += 1
            elif reason == "split":
                submosaic += 1
                self.splits += 1
                self.H_to_root[index] = np.eye(3)
                self.submosaic_of[index] = submosaic
                self.submosaic_root[submosaic] = index
                placed.append(index)
            else:
                self.skips += 1
            index += 1
        self.placed_total = len(placed)
        return self

    def summary(self):
        placed = sorted(self.steps)          # chỉ các frame có bước ghép được ghi nhận
        errors = [self.steps[i]["step_error_px"] for i in placed]
        drift = {}
        for index in placed:
            root = self.submosaic_root[self.submosaic_of[index]]      # frame gốc, không phải id submosaic
            reference_chain = np.eye(3)
            for step in range(root + 1, index + 1):
                reference_chain = reference_chain @ np.array(reference_pair(self.files[step - 1], self.files[step])[0], float)
            drift[index] = marker_error(self.H_to_root[index], reference_chain, self.size_original)
        return {"policy": self.policy, "matcher": self.method,
                "reference_invalid_used": self.reference_invalid_used,
                "frames_placed": self.placed_total,          # tính cả frame gốc mảnh và frame 0
                "frames_requested": self.steps_total + 1,
                "frames_with_step": len(placed),
                "submosaics": self.splits + 1, "triggers": self.triggers, "skipped": self.skips,
                "anchored": self.anchored, "seconds": self.cost,
                "step_error_mean_px": float(np.mean(errors)) if errors else None,
                "step_error_p95_px": float(np.percentile(errors, 95)) if errors else None,
                "step_error_max_px": float(np.max(errors)) if errors else None,
                "drift_series": [drift[i] for i in sorted(drift)],
                "drift_max_px": float(np.max(list(drift.values()))) if drift else None,
                "drift_final_px": drift[max(drift)] if drift else None}


def run_policies(scan, method, tau_ncc, policies=POLICIES):
    matcher = load_matcher(method, DEVICE)
    out = []
    for policy in policies:
        pipeline = OnlinePipeline(method, matcher, scan["files"], scan["images"],
                                  scan["size_original"], policy, tau_ncc=tau_ncc).run(scan["steps"])
        summary = pipeline.summary()
        out.append({"sequence": scan["sequence"], **summary})
        print(f"  {method:20} {policy:7} đặt {summary['frames_placed']:3}/{scan['steps'] + 1} frame | "
              f"trigger {summary['triggers']:2} | submosaic {summary['submosaics']} | "
              f"step_err max {fmt(summary['step_error_max_px'], 8)} | drift max {fmt(summary['drift_max_px'], 9)} px")
    return out
