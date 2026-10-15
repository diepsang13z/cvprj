from cloud_runtime import require_cloud
require_cloud()

from failure_core import *

def check_metrics(report, scans):
    """Cloud-only regression: reference replay survives JSON step-key conversion."""
    for scan in scans:
        replay = {step: {"status": "success", "H_original": value["H_original"]}
                  for step, value in scan["reference"].items()}
        reference = [np.array(h, float) for h in scan["reference_chain"]]
        chain = chain_from_steps(replay, reference)
        assert len(chain) == scan["steps"] + 1, scan["sequence"]
        assert max(marker_error(h, ref, scan["size_original"])
                   for h, ref in zip(chain, reference)) < 1e-6, scan["sequence"]
        invalid = sorted(s for s, r in scan["reference"].items() if r["inliers"] < MIN_INLIERS)
        assert invalid == scan["reference_invalid_steps"], scan["sequence"]
    for row in report["rq1"]:
        both = 0 < row["n_bad_steps"] < row["n_steps"]
        assert (row["auc_bad_step"] is not None) == both, row
    for row in report["rq3"]:
        assert 1 <= row["submosaics"] <= row["frames_placed"] <= row["frames_requested"], row
    print("PASS: reference replay, invalid-reference gate, AUC class validity, recovery frame accounting")

def render_report(REPORT, SCANS, TARGET):
    TAU_STAR = choose_tau([r for r in REPORT["rq2"] if r["policy"] == "routed"]) or TAU_NCC
    # Biểu đồ: (trái) chỉ báo vs sai số so với tham chiếu; (phải) drift của 4 chiến lược phục hồi.
    figure, axes = plt.subplots(1, 2, figsize=(15, 5))
    for tier, marker in ((CHEAP, "o"), (STRONG, "s"), (DIAGNOSTIC, "^")):
        for scan in SCANS:
            rows = [r for r in scan["rows"][tier].values() if r["status"] == "success"]
            axes[0].scatter([r["photo_ncc"] for r in rows], [max(r["step_error_px"], 0.05) for r in rows],
                            s=18, marker=marker, alpha=0.75,
                            label=f"{tier} ({scan['sequence'].split('-')[1]})")
    axes[0].axhline(TOLERANCE_PX, ls="--", color="k", lw=1, label=f"ngưỡng sai {TOLERANCE_PX:.0f} px")
    axes[0].axvline(TAU_STAR, ls=":", color="tab:red", lw=2, label=f"τ_ncc = {TAU_STAR}")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("tương phản sau khi ghép (photo_ncc)")
    axes[0].set_ylabel("sai số so với tham chiếu của bước (px, log)")
    axes[0].set_title("RQ1: chỉ báo quang học tách được ca ghép sai")
    axes[0].legend(fontsize=7)
    axes[0].grid(alpha=.3)
    for sequence, style in zip(SEQUENCES, ("-", "--")):
        for row in [r for r in REPORT["rq3"] if r["sequence"] == sequence]:
            axes[1].plot(range(len(row["drift_series"])), row["drift_series"], style, lw=1.8,
                         label=f"{sequence.split('-')[1]} · {row['matcher']} · {row['policy']}")
    axes[1].set_xlabel("số bước đã đặt")
    axes[1].set_ylabel("drift tích luỹ so với chuỗi tham chiếu (px)")
    axes[1].set_title("RQ3: bốn chiến lược dưới cùng ngưỡng")
    axes[1].legend(fontsize=7)
    axes[1].grid(alpha=.3)
    plt.tight_layout()
    figure.savefig(TARGET / "summary.png", dpi=110)
    plt.show()

    rq1 = sorted(REPORT["rq1"], key=lambda r: (r["sequence"], r["tier"],
                                               -abs(r["spearman_vs_step_error"] or 0.0)))
    print(f"{'sequence':22} {'matcher':22} {'chỉ báo':16} {'ρ':>7} {'AUC':>6} {'bước':>5} {'sai':>5} {'loại':>5}")
    for row in rq1:
        score = "   n/a" if row["auc_bad_step"] is None else f"{row['auc_bad_step']:6.3f}"
        print(f"{row['sequence']:22} {row['tier']:22} {row['indicator']:16} "
              f"{fmt(row['spearman_vs_step_error'], 7)} {score} {row['n_steps']:5} {row['n_bad_steps']:5} "
              f"{row['n_invalid_reference']:5}")
    print("(cột 'loại' = số bước bị loại vì cặp tham chiếu dưới 100 inlier)")
    print("(AUC 'n/a' = cửa sổ không có đủ cả bước tốt lẫn bước sai để chấm điểm)")

    print()
    header = f"{'sequence':22} {'chính sách':16} {'leo thang':>9} {'giây':>8} {'err TB':>8} {'err p95':>8} {'drift cuối':>11}"
    print(header)
    for row in REPORT["rq2"]:
        label = row["policy"] if row["tau_ncc"] is None else f"{row['policy']}@{row['tau_ncc']}"
        print(f"{row['sequence']:22} {label:16} "
              f"{row['escalation_rate']:9.2f} {row['seconds']:8.1f} {fmt(row['step_error_mean_px'], 8)} "
              f"{fmt(row['step_error_p95_px'], 8)} {fmt(row['final_drift_px'], 11, 1)}")

    print()
    header = f"{'sequence':22} {'matcher':20} {'chiến lược':10} {'frame':>9} {'sub':>4} {'trigger':>8} {'err max':>9} {'drift max':>10}"
    print(header)
    for row in REPORT["rq3"]:
        print(f"{row['sequence']:22} {row['matcher']:20} {row['policy']:10} "
              f"{row['frames_placed']:4}/{row['frames_requested']:<4} "
              f"{row['submosaics']:4} {row['triggers']:8} {fmt(row['step_error_max_px'], 9)} {fmt(row['drift_max_px'], 10)}")
    print("('n/a' = chiến lược không đặt được frame nào, không có gì để đo)")


