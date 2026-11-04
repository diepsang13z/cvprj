"""Generate paper tables/illustrations from saved cloud artifacts; no model execution."""
from pathlib import Path
import csv
import hashlib
import json
from statistics import mean
from collections import Counter
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
matplotlib.rcParams["mathtext.fontset"] = "stix"
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "notebooks/outputs"
M = OUT / "feature_matcher_benchmark/20261101T163603_779942Z"
D = OUT / "accumulated_drift_evaluation/20261103T165349_596427Z"
F = OUT / "failure_aware_pipeline/20261101T183829_171190Z"
B = OUT / "classical_mosaicking_baseline/20261101T153341_784110Z"
load = lambda p: json.loads(p.read_text(encoding="utf-8"))
for folder in (M, D, F, B):
    assert load(folder / "completed.json")["status"] == "success"
r, d = load(F / "report.json"), load(D / "drift_selfconsistent.json")
assert hashlib.sha256((M / "manifest.json").read_bytes()).hexdigest() == d["provenance"]["source_manifest_sha256"]
with (M / "summary.csv").open(encoding="utf-8", newline="") as f:
    pairs = list(csv.DictReader(f))
with (M / "mosaic_summary.csv").open(encoding="utf-8", newline="") as f:
    mosaics = list(csv.DictReader(f))
TABLES, FIGURES = HERE / "tables", HERE / "figures"
TABLES.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)
NAMES = {"sift_bf": "SIFT-BF", "orb_bf": "ORB-BF", "sift_lightglue": "SIFT-LG",
         "superpoint_lightglue": "SP-LG", "xfeat_mnn": "XFeat-MNN",
         "xfeat_lighterglue": "XFeat-LG", "efficientloftr": "ELoFTR"}

def table(name, columns, headers, rows):
    body = [r"\begin{tabular}{" + columns + "}", r"\toprule", " & ".join(headers) + r" \\", r"\midrule"]
    body += [" & ".join(map(str, row)) + r" \\" for row in rows]
    body += [r"\bottomrule", r"\end{tabular}"]
    (TABLES / (name + ".tex")).write_text("\n".join(body) + "\n", encoding="utf-8")

rows = []
for method, label in NAMES.items():
    ps = [x for x in pairs if x["method"] == method]
    ok = [x for x in ps if x["status"] == "success"]
    ms = [x for x in mosaics if x["method"] == method]
    assert len(ps) == 3890 and sum(int(x["frames_requested"]) for x in ms) == 3898
    ate = mean(x["common_ate_px"] for x in d["results"] if x["method"] == method)
    rows.append([label, len(ok), f'{mean(float(x["match_seconds"]) for x in ps):.3f}',
                 f'{mean(float(x["rmse_px"]) for x in ok):.3f}', sum(int(x["frames_stitched"]) for x in ms), f"{ate:.2f}"])
table("benchmark", "lrrrrr", ["Matcher", "Pairs", "Match (s)", "RMSE", "Frames", "C-ATE"], rows)
indicators = {"rmse_px": "RMSE", "photo_bad_frac": "Photo bad fraction", "photo_ncc": "NCC",
              "hull_area_ratio": "Hull area ratio", "overlap_ratio": "Overlap ratio",
              "inlier_ratio": "Inlier ratio", "inliers": "Inlier count", "matches": "Match count"}
rows = []
for key, label in indicators.items():
    a = [x for x in r["rq1"] if x["tier"] == "sift_bf" and x["indicator"] == key]
    assert len(a) == 8
    rows.append([label, f'{mean(x["spearman_vs_step_error"] for x in a):.3f}', f'{mean(x["auc_bad_step"] for x in a):.3f}'])
table("rq1", "lrr", ["Indicator", r"$\rho$", "AUC"], rows)
rows = []
for policy, label in [("classical", "SIFT"), ("learned", "SP-LG"), ("routed", "Routed"), ("routed_fullres", "Routed-FR")]:
    a = [x for x in r["rq2"] if x["policy"] == policy]
    assert sum(x["steps"] for x in a) == 3891
    rows.append([label, sum(x["failed_steps"] for x in a), "--" if policy == "learned" else sum(x["escalations"] for x in a),
                 f'{sum(x["seconds"] for x in a):.2f}', f'{mean(x["step_error_mean_px"] for x in a):.3f}'])
table("routing", "lrrrr", ["Policy", "Failed", "Esc.", "Time (s)", "Error (px)"], rows)
rows = []
for policy in ("none", "drop", "anchor", "split"):
    a = [x for x in r["rq3"] if x["policy"] == policy]
    assert sum(x["frames_requested"] for x in a) == 3899
    assert all(x["frames_placed"] == x["frames_with_step"] + x["submosaics"] for x in a)
    rows.append([policy.title()] + [sum(x[k] for x in a) for k in ("frames_placed", "frames_with_step", "submosaics", "valid_drift_count")])
table("recovery", "lrrrr", ["Policy", "Retained", "Linked", "Pieces", "Valid drift"], rows)
rows, split_rows = [], []
for scan in r["scans"]:
    seq = scan["sequence"]
    short = seq.split("-")[1]
    frames = next(int(x["frames_requested"]) for x in mosaics if x["sequence"] == seq)
    rows.append([short, frames, scan["steps"] + 1, len(d["common_eligible_sets"][seq]), len(scan["reference_invalid_steps"])])
    x = next(x for x in r["rq3"] if x["sequence"] == seq and x["policy"] == "split")
    counts = Counter(z["submosaic_id"] for z in x["records"] if z["placed"])
    split_rows.append([short, x["submosaics"], max(counts.values()), sum(v == 1 for v in counts.values())])
table("sequences", "lrrrr", ["Sequence", "M frames", "F frames", "Common", "Invalid"], rows)
table("split", "lrrr", ["Sequence", "Pieces", "Largest", "Singletons"], split_rows)

# Minimal framework figure, typeset to match the manuscript body.
fig, ax = plt.subplots(figsize=(7.0, 2.30), dpi=300)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax.set(xlim=(-0.15, 9.85), ylim=(0.30, 3.59)); ax.axis("off")

def cell(x, y, w, h, head, sub=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                facecolor="white", edgecolor="black", linewidth=0.7))
    if sub:
        ax.text(x + w/2, y + h/2 + 0.16, head, fontsize=8.4, ha="center", va="center")
        ax.text(x + w/2, y + h/2 - 0.16, sub, fontsize=7.6, ha="center", va="center")
    else:
        ax.text(x + w/2, y + h/2, head, fontsize=8.4, ha="center", va="center")

def link(p1, p2):
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="->", color="black", linewidth=0.7,
                                shrinkA=1, shrinkB=1))

def tag(y, text):
    ax.text(0.05, y, text, fontsize=8.4, ha="left", va="center")

tag(3.46, "(a)")
for i, (head, sub) in enumerate([("UAV frames", "$I_{k-1},\\, I_k$"),
                                 ("Feature matching", "SIFT / ORB-BF"),
                                 ("Homography", "$H_{k-1 \\leftarrow k}$"),
                                 ("Chain accumulation", "$H_{0 \\leftarrow k}$"),
                                 ("Mosaic canvas", "drift $\\Delta$")]):
    cell(0.15 + 2.01*i, 2.70, 1.66, 0.68, head, sub)
for i in range(4):
    link((1.81 + 2.01*i, 3.04), (2.16 + 2.01*i, 3.04))

tag(2.24, "(b)")
cell(0.15, 0.87, 2.30, 0.68, "Risk prediction", "RQ1")
cell(3.05, 1.32, 2.70, 0.68, "Matcher routing", "RQ2")
cell(3.05, 0.42, 2.70, 0.68, "Failure recovery", "RQ3")
cell(6.30, 0.87, 3.40, 0.68, "Evaluation", "error, cost, retention")

link((2.45, 1.21), (3.05, 1.66))
link((2.45, 1.21), (3.05, 0.76))
link((5.75, 1.66), (6.30, 1.44))
link((5.75, 0.76), (6.30, 0.98))

fig.savefig(FIGURES / "baseline.pdf", pad_inches=0)
plt.close(fig)

# Qualitative baseline panels use clean white unmapped canvas and balanced layout.
panel = Image.new("RGB", (1800, 750), "white")
draw = ImageDraw.Draw(panel)
label_font = ImageFont.truetype(
    str(Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSerif.ttf"), 30)
for i, (method, label) in enumerate([("sift", "(a) SIFT-BF: 406/406 frames"), ("orb", "(b) ORB-BF: 406/406 frames")]):
    with Image.open(B / f"mosaic_{method}_406frames.png") as image:
        arr = np.array(image.convert("RGBA"))
        is_black = (arr[:, :, :3] < 15).all(axis=-1)
        arr[is_black] = [255, 255, 255, 255]
        img_white = Image.fromarray(arr).convert("RGB")
        thumb = ImageOps.contain(img_white, (870, 660), method=Image.Resampling.LANCZOS)
        x_offset = i * 900 + (900 - thumb.width) // 2
        y_offset = 60 + (660 - thumb.height) // 2
        panel.paste(thumb, (x_offset, y_offset))
    draw.text((i * 900 + 30, 20), label, fill="black", font=label_font)
panel.save(FIGURES / "baseline_mosaics.jpg", quality=95)
print("Generated 6 data tables and 2 baseline figures; source/denominator assertions passed.")
