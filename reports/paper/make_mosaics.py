"""Render experiment mosaics by replaying the homographies stored in the notebook-05 scan files.

No matcher is re-run: every H comes from scan_<sequence>.json
(stamp 20261014T070805_406984Z), so the pictures match the numbers in report.json.
Drift of each rebuilt chain is asserted against report.json before anything is written.

Run:  python reports/paper/make_mosaics.py
Out:  reports/paper/figures/mosaic_{village_sift,village_routed,grass_sift,grass_loftr}.jpg
"""
from pathlib import Path
import json
import sys
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "notebooks" / "outputs" / "05_failure_aware"
FIG = Path(__file__).resolve().parent / "figures"
FIG.mkdir(exist_ok=True)

CHEAP, STRONG, DIAGNOSTIC = "sift_bf", "superpoint_lightglue", "efficientloftr"
TAU_NCC, TAU_RATIO = 0.93, 0.30          # village threshold from the RQ2 budget rule
SCALE = 0.32                              # frames are 1920x1080


def risk(row):
    return (row.get("status") != "success"
            or row["photo_ncc"] < TAU_NCC
            or row["inlier_ratio"] < TAU_RATIO)


def marker_error(H_a, H_b, size):
    pts = np.float32([[0, 0], [size[0], 0], [size[0], size[1]], [0, size[1]],
                      [size[0] / 2, size[1] / 2]]).reshape(-1, 1, 2)
    return float(np.linalg.norm(cv2.perspectiveTransform(pts, H_a)
                                - cv2.perspectiveTransform(pts, H_b), axis=2).mean())


def chain_from_steps(chosen, steps):
    """Accumulated H per frame index; stops at the first step without a homography."""
    chain = [np.eye(3)]
    for step in range(1, steps + 1):
        pick = chosen.get(step)
        if pick is None or pick.get("status") != "success" or "H_original" not in pick:
            break
        chain.append(chain[-1] @ np.array(pick["H_original"], float))
    return chain


def reference_chain(scan):
    chain = [np.eye(3)]
    for step in range(1, scan["steps"] + 1):
        chain.append(chain[-1] @ np.array(scan["reference"][str(step)]["H_original"], float))
    return chain


def window_files(sequence, start, steps):
    files = sorted((ROOT / "data" / sequence / "rgb").glob("*.jpg"))
    return files[start:start + steps + 1]


def render(files, chain, size, max_width=1700):
    corners = np.concatenate([
        cv2.perspectiveTransform(
            np.float32([[0, 0], [size[0], 0], [size[0], size[1]], [0, size[1]]]).reshape(-1, 1, 2), H)
        for H in chain]).reshape(-1, 2)
    span = corners.max(0) - corners.min(0)
    scale = min(SCALE, max_width / max(span))
    shift = np.array([[1, 0, -corners[:, 0].min()], [0, 1, -corners[:, 1].min()], [0, 0, 1]], float)
    width, height = int(span[0] * scale), int(span[1] * scale)

    total = np.zeros((height, width, 3), np.float32)
    weight = np.zeros((height, width, 1), np.float32)
    for file, H in zip(files, chain):
        image = cv2.imread(str(file))
        if image is None:
            raise SystemExit(f"cannot read {file}")
        small = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        H_scaled = shift @ H @ np.diag([1 / scale, 1 / scale, 1.0])
        warp = cv2.warpPerspective(small, H_scaled, (width, height)).astype(np.float32)
        mask = cv2.warpPerspective(np.ones(small.shape[:2], np.float32), H_scaled, (width, height))[..., None]
        total += warp * mask
        weight += mask
    canvas = np.where(weight > 0, total / np.maximum(weight, 1e-6), 255).clip(0, 255).astype(np.uint8)
    rows_used, cols_used = np.where(weight[..., 0] > 0)
    return canvas[rows_used.min():rows_used.max() + 1, cols_used.min():cols_used.max() + 1]


def save(canvas, path):
    cv2.imwrite(str(path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 88])
    print(f"  {path.name}: {canvas.shape[1]}x{canvas.shape[0]}")


def contact_sheet(items, path, columns=4, cell=520):
    """items = [(label, canvas), ...] -> labelled grid, fragments scaled to a common cell."""
    rows = (len(items) + columns - 1) // columns
    bar, pad = 26, 8
    sheet = np.full((rows * (cell + bar + pad) + pad, columns * (cell + pad) + pad, 3), 255, np.uint8)
    for i, (label, canvas) in enumerate(items):
        scale = min(cell / canvas.shape[1], cell / canvas.shape[0])
        thumb = cv2.resize(canvas, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        row, col = divmod(i, columns)
        y = pad + row * (cell + bar + pad)
        x = pad + col * (cell + pad)
        sheet[y:y + thumb.shape[0], x:x + thumb.shape[1]] = thumb
        cv2.putText(sheet, label, (x, y + thumb.shape[0] + 18), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)
    save(sheet, path)


def comparison(canvases, path, labels):
    """Two/three mosaics side by side as a paper figure (vector PDF wrapping the rasters)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(canvases), figsize=(7.0, 3.0))
    for ax, canvas, label in zip(np.atleast_1d(axes), canvases, labels):
        ax.imshow(canvas[..., ::-1])
        ax.set_title(label, fontsize=7.5)
        ax.axis("off")
    fig.tight_layout(pad=0.25)
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"  {path.name}")


def main():
    report = json.loads((OUT / "report.json").read_text(encoding="utf-8"))
    rq2 = {(r["sequence"], r["policy"], r.get("tau_ncc")): r for r in report["rq2"]}
    rq3 = {(r["sequence"], r["policy"]): r for r in report["rq3"]}
    first_frame = Path(report["inputs"][0]["path"]).name
    scans = {s: json.loads((OUT / f"scan_{s}.json").read_text(encoding="utf-8"))
             for s in ("phantom3-village-kfs", "phantom3-grass-kfs")}
    frames, sizes, flags = {}, {}, {}
    for name, scan in scans.items():
        files = window_files(name, scan["start"], scan["steps"])
        assert len(files) == scan["steps"] + 1 and scan["sequence"] == name, name
        frames[name], sizes[name] = files, cv2.imread(str(files[0])).shape[1::-1]
        flags[name] = [step for step in range(1, scan["steps"] + 1) if risk(scan["rows"][CHEAP][str(step)])]
    assert frames["phantom3-village-kfs"][0].name == first_frame, first_frame

    village, grass = "phantom3-village-kfs", "phantom3-grass-kfs"

    def chain_of(sequence, tier, chosen=None):
        scan = scans[sequence]
        picked = chosen or {step: scan["rows"][tier][str(step)] for step in range(1, scan["steps"] + 1)}
        chain = chain_from_steps(picked, scan["steps"])
        drift = marker_error(chain[-1], reference_chain(scan)[len(chain) - 1], sizes[sequence])
        return chain, drift

    # (1) village: cheap matcher only, (2) grass: same cheap matcher ---- both vs their RQ2 rows
    canvases = {}
    for sequence, tier, policy_key, label in (
            (village, CHEAP, "classical", "village_sift"),
            (grass, CHEAP, "classical", "grass_sift")):
        chain, drift = chain_of(sequence, tier)
        expected = rq2[(sequence, policy_key, None)]["final_drift_px"]
        assert abs(drift - expected) < 1e-6, (label, drift, expected)
        print(f"{label}: {len(chain) - 1} steps, drift {drift:.2f} px == report.json")
        canvases[label] = (render(frames[sequence][:len(chain)], chain, sizes[sequence]), drift)
        save(canvases[label][0], FIG / f"mosaic_{label}.jpg")

    # (3) grass: EfficientLoFTR everywhere (the known-broken case)
    chain, drift = chain_of(grass, DIAGNOSTIC)
    expected = rq3[(grass, "none")]["drift_final_px"]
    assert abs(drift - expected) < 1e-6, (drift, expected)
    print(f"grass_loftr: {len(chain) - 1} steps, drift {drift:.2f} px == report.json")
    canvases["grass_loftr"] = (render(frames[grass][:len(chain)], chain, sizes[grass]), drift)
    save(canvases["grass_loftr"][0], FIG / "mosaic_grass_loftr.jpg")

    # (4) village: routed (strong matcher on flagged steps only)
    scan = scans[village]
    chosen = {step: (scan["rows"][STRONG][str(step)] if step in flags[village] else scan["rows"][CHEAP][str(step)])
              for step in range(1, scan["steps"] + 1)}
    chain, drift = chain_of(village, None, chosen)
    routed = rq2[(village, "routed", 0.93)]
    assert abs(drift - routed["final_drift_px"]) < 1e-6, (drift, routed["final_drift_px"])
    assert len(flags[village]) == routed["escalations"] == 7, len(flags[village])
    print(f"village_routed: drift {drift:.2f} px, {len(flags[village])} escalations == report.json")
    canvases["village_routed"] = (render(frames[village][:len(chain)], chain, sizes[village]), drift)
    save(canvases["village_routed"][0], FIG / "mosaic_village_routed.jpg")

    # comparison figures used in the paper
    comparison([canvases["village_sift"][0], canvases["village_routed"][0]], FIG / "fig_mosaic_village.pdf",
               [f"(a) SIFT only: drift {canvases['village_sift'][1]:.0f} px",
                f"(b) Routed $\\tau$=0.93: drift {canvases['village_routed'][1]:.0f} px"])
    comparison([canvases["grass_sift"][0], canvases["grass_loftr"][0]], FIG / "fig_mosaic_grass.pdf",
               [f"(a) SIFT 640 px: drift {canvases['grass_sift'][1]:.0f} px",
                f"(b) EfficientLoFTR: drift {canvases['grass_loftr'][1]:.0f} px"])

    # (5) village: split policy -> one canvas per fragment, assembled as a contact sheet
    roots = [0] + flags[village]
    assert len(roots) == rq3[(village, "split")]["submosaics"] == 8, roots
    print(f"village_split: fragment roots (frame index) {roots} == report.json")
    items = []
    for piece, root in enumerate(roots):
        stop = roots[piece + 1] - 1 if piece + 1 < len(roots) else scan["steps"]
        frag = [np.eye(3)]
        for step in range(root + 1, stop + 1):
            frag.append(frag[-1] @ np.array(scan["rows"][CHEAP][str(step)]["H_original"], float))
        files = frames[village][root:stop + 1]
        assert len(files) == len(frag), (len(files), len(frag))
        items.append((f"fragment {piece + 1}: frames {root}-{stop}",
                      render(files, frag, sizes[village], max_width=520)))
    contact_sheet(items, FIG / "mosaic_village_split.jpg")


if __name__ == "__main__":
    sys.exit(main())
