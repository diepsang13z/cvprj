"""Audit the paper tables against the experiment artifacts.

Fails if a tabulated number drifts from report.json, or if the Direction column
of Table I disagrees with the pre-declared INDICATOR_SUSPICION in the notebook.

Run:  python reports/paper/check_tables.py
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "notebooks" / "outputs" / "05_failure_aware"
PAPER = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "notebooks" / "05_failure_aware_pipeline.ipynb"

VILLAGE = "phantom3-village-kfs"
GRASS = "phantom3-grass-kfs"


def declared_directions():
    """{indicator: 'uparrow'|'downarrow'} from the notebook's INDICATOR_SUSPICION literal."""
    source = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code = "\n".join("".join(cell["source"]) for cell in source["cells"] if cell["cell_type"] == "code")
    block = re.search(r"INDICATOR_SUSPICION\s*=\s*\{(.*?)\}", code, re.S).group(1)
    pairs = re.findall(r'"([a-z_]+)"\s*:\s*(-?1\.0)', block)
    assert len(pairs) == 8, pairs
    return {name: ("uparrow" if float(sign) > 0 else "downarrow") for name, sign in pairs}


def tables(tex):
    text = (PAPER / tex).read_text(encoding="utf-8")
    blocks = text.split("\\begin{table}")
    return {key: next(b for b in blocks if f"\\label{{{key}}}" in b)
            for key in ("tab:rq1", "tab:rq2", "tab:rq3")}


def variants(value, digits, vietnamese):
    plain = f"{value:.{digits}f}"
    return {plain, plain.replace(".", ","), plain.replace(".", "{,}")} if vietnamese else {plain}


def check_tex(name, vietnamese):
    blocks = tables(name)
    rq1_rows = {}
    for line in blocks["tab:rq1"].splitlines():
        found = re.match(r"\\texttt\{([^}]+)\}\s*&\s*\$(\\uparrow|\\downarrow)\$", line)
        if found:
            rq1_rows[found.group(1).replace("\\_", "_")] = found.group(2).lstrip("\\")

    directions = declared_directions()
    assert set(rq1_rows) == set(directions), (set(rq1_rows) ^ set(directions))
    for indicator, arrow in rq1_rows.items():
        assert arrow == directions[indicator], f"{name}: {indicator} direction {arrow} != declared {directions[indicator]}"

    report = json.loads((OUT / "report.json").read_text(encoding="utf-8"))
    wanted = 0
    for row in report["rq1"]:
        if (row["sequence"], row["tier"]) != (VILLAGE, "sift_bf"):
            continue
        escaped = row["indicator"].replace("_", "\\_")
        line = next(l for l in blocks["tab:rq1"].splitlines() if f"\\texttt{{{escaped}}}" in l)
        for value, digits in ((row["auc_bad_step"], 3), (row["spearman_vs_step_error"], 3)):
            assert any(text in line.replace("$", "") for text in variants(value, digits, vietnamese)), \
                f"{name}: {row['indicator']} {value:.3f} not in '{line.strip()}'"
            wanted += 1

    rq2 = {(r["policy"], r.get("tau_ncc")): r for r in report["rq2"] if r["sequence"] == VILLAGE}
    for policy, tau in (("classical", None), ("learned", None), ("routed", 0.93), ("routed_fullres", 0.93)):
        row = rq2[(policy, tau)]
        for value, digits in ((row["seconds"], 1), (row["step_error_mean_px"], 2), (row["final_drift_px"], 1)):
            assert any(text in blocks["tab:rq2"] for text in variants(value, digits, vietnamese)), \
                f"{name}: RQ2 {policy} {value:.{digits}f} not in table"
            wanted += 1

    rq3 = {(r["sequence"], r["policy"]): r for r in report["rq3"]}
    for key in ((VILLAGE, "none"), (VILLAGE, "drop"), (VILLAGE, "anchor"), (VILLAGE, "split"),
                (GRASS, "none"), (GRASS, "drop"), (GRASS, "split")):
        row = rq3[key]
        frames = f"{row['frames_placed']}/{row['frames_requested']}"
        assert frames in blocks["tab:rq3"], f"{name}: RQ3 {key} {frames} not in table"
        wanted += 1
        if row["drift_max_px"] is not None:
            assert any(text in blocks["tab:rq3"] for text in variants(row["drift_max_px"], 1, vietnamese)), \
                f"{name}: RQ3 {key} drift {row['drift_max_px']:.1f} not in table"
            wanted += 1
        pieces = str(row["submosaics"])
        assert re.search(rf"&\s*{pieces}\s*&", blocks["tab:rq3"]), f"{name}: RQ3 {key} pieces {pieces} not in table"

    print(f"{name}: {wanted} giá trị khớp report.json, 8 chiều chỉ báo khớp INDICATOR_SUSPICION")


def check_dashes():
    compounds = {"satellite--thermal", "tinh--nhiệt"}
    for name in ("main.tex", "main_vi.tex"):
        text = (PAPER / name).read_text(encoding="utf-8")
        assert "---" not in text, f"{name}: còn em dash '---'"
        assert "\u2014" not in text, f"{name}: còn ký tự em dash"
        body = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("%"))
        stray = []
        for token in re.findall(r"\S*--\S*", body):
            if any(token.startswith(c) for c in compounds) or token.split("--")[0][-1:].isdigit():
                continue
            stray.append(token)
        assert not stray, f"{name}: en dash ngoài khoảng số/tên ghép: {stray}"
    print("dash check: sạch (không còn em dash; en dash chỉ dùng cho khoảng số và tên ghép)")


if __name__ == "__main__":
    check_tex("main.tex", vietnamese=False)
    check_tex("main_vi.tex", vietnamese=True)
    check_dashes()
    sys.exit(0)
