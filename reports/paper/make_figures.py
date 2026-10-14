"""Regenerate the paper figures from the notebook-05 artifacts.

Run:  python reports/paper/make_figures.py
Input: notebooks/outputs/05_failure_aware/{report.json,scan_*.json}  (stamp 20261014T070805_406984Z)
Output: reports/paper/figures/{fig_scenes,fig_rq1_rq3,fig_tau}.pdf
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "notebooks" / "outputs" / "05_failure_aware"
FIG = Path(__file__).resolve().parent / "figures"
FIG.mkdir(exist_ok=True)

report = json.loads((OUT / "report.json").read_text(encoding="utf-8"))
scans = {s: json.loads((OUT / f"scan_phantom3-{s}-kfs.json").read_text(encoding="utf-8"))
         for s in ("village", "grass")}

for name in ("village", "grass"):
    src = ROOT / "reports" / "present_02" / "assets" / f"sample_{name}.jpg"
    dst = FIG / f"sample_{name}.jpg"
    if not dst.exists():
        dst.write_bytes(src.read_bytes())

TIERS = {"sift_bf": ("o", "SIFT+BF"), "superpoint_lightglue": ("s", "SP+LightGlue"),
         "efficientloftr": ("^", "EfficientLoFTR")}
SEQ_MARK = {"village": "-", "grass": "--"}

# --- Fig: scenes -------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.3))
for ax, name, label in zip(axes, ("village", "grass"), ("(a) phantom3-village-kfs", "(b) phantom3-grass-kfs")):
    ax.imshow(mpimg.imread(FIG / f"sample_{name}.jpg"))
    ax.set_title(label, fontsize=8)
    ax.axis("off")
fig.tight_layout(pad=0.3)
fig.savefig(FIG / "fig_scenes.pdf")
plt.close(fig)

# --- Fig: RQ1 scatter + RQ3 drift -------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.6))
for seq, scan in scans.items():
    for tier, (marker, label) in TIERS.items():
        rows = scan["rows"][tier]
        xs = [r["photo_ncc"] for r in rows.values() if r.get("status") == "success" and r.get("step_error_px") is not None]
        ys = [max(r["step_error_px"], 0.2) for r in rows.values() if r.get("status") == "success" and r.get("step_error_px") is not None]
        ax1.plot(xs, ys, marker, ms=2.5, ls="none", alpha=0.65,
                 label=f"{label} ({seq})", markeredgecolor="none")
ax1.axhline(2.0, color="k", ls="--", lw=0.8)
ax1.axvline(0.93, color="crimson", ls=":", lw=0.8)
ax1.set_yscale("log")
ax1.set_xlabel("post-registration NCC ($photo\\_ncc$)")
ax1.set_ylabel("step error (px, log)")
ax1.set_title("(a) RQ1: indicator vs. step error", fontsize=8)
ax1.legend(fontsize=4.6, loc="lower left", ncol=2, framealpha=0.85)
ax1.tick_params(labelsize=7)

for r in report["rq3"]:
    if r["policy"] == "anchor" or not r.get("drift_series"):
        continue
    seq = r["sequence"].split("-")[1]
    ls = SEQ_MARK[seq]
    color = {"none": "tab:blue", "drop": "tab:orange", "split": "tab:red"}[r["policy"]]
    ax2.plot(range(len(r["drift_series"])), r["drift_series"], ls, color=color, lw=1.2,
             label=f"{seq}/{r['matcher']}: {r['policy']}")
ax2.set_xlabel("placed frames")
ax2.set_ylabel("drift vs. reference chain (px)")
ax2.set_title("(b) RQ3: recovery under the same trigger", fontsize=8)
ax2.legend(fontsize=4.6, loc="upper left")
ax2.tick_params(labelsize=7)
fig.tight_layout(pad=0.4)
fig.savefig(FIG / "fig_rq1_rq3.pdf")
plt.close(fig)

# --- Fig: tau sweep ----------------------------------------------------------
fig, ax = plt.subplots(figsize=(3.4, 2.4))
rows = [r for r in report["rq2"] if r["sequence"] == "phantom3-village-kfs"]
base = {r["policy"]: r for r in rows if r["policy"] in ("classical", "learned")}
sweep = sorted([r for r in rows if r["policy"] == "routed"], key=lambda r: r["tau_ncc"])
for r in sweep:
    ax.annotate(f"{r['tau_ncc']:.2f}", (r["escalation_rate"] * 100, r["final_drift_px"]),
                textcoords="offset points", xytext=(3, 3), fontsize=5.5)
ax.plot([r["escalation_rate"] * 100 for r in sweep], [r["final_drift_px"] for r in sweep],
        "o-", color="tab:red", ms=3, lw=1.2, label="routed sweep")
ax.axhline(base["classical"]["final_drift_px"], color="tab:blue", ls="--", lw=1.0, label="SIFT everywhere")
ax.axhline(base["learned"]["final_drift_px"], color="tab:green", ls="--", lw=1.0, label="SP+LG everywhere")
ax.axvline(25, color="k", ls=":", lw=0.8)
ax.set_xlabel("escalation rate (% of steps)")
ax.set_ylabel("final drift (px)")
ax.legend(fontsize=5.5, loc="upper left")
ax.tick_params(labelsize=7)
fig.tight_layout(pad=0.3)
fig.savefig(FIG / "fig_tau.pdf")
plt.close(fig)

print("figures written to", FIG)
