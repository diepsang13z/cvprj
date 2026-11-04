"""Check bilingual citation coverage, included assets and TeX build diagnostics.

This checks internal consistency, not bibliographic truth or model reproducibility.
See reference_audit.md for external source verification.
"""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
bib = (HERE / "references.bib").read_text(encoding="utf-8")
keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib)
assert len(keys) == len(set(keys)), "Duplicate bibliography keys"
assert keys, "Bibliography is empty"
sets = []
for stem in ("main", "main_vi"):
    source = (HERE / (stem + ".tex")).read_text(encoding="utf-8")
    assert r"\documentclass[conference]{IEEEtran}" in source
    assert r"\bibliographystyle{IEEEtran}" in source
    included = re.findall(r"\\input\{([^}]+)\}", source)
    for name in included:
        path = HERE / (name if name.endswith(".tex") else name + ".tex")
        assert path.is_file(), f"Missing input: {path}"
        source += "\n" + path.read_text(encoding="utf-8")
    used = {key.strip() for group in re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}", source) for key in group.split(",")}
    assert used == set(keys), f"{stem}: missing refs={used-set(keys)}, uncited={set(keys)-used}"
    sets.append(used)
    for asset in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", source):
        assert (HERE / asset).is_file(), f"Missing figure {asset}"
    assert not re.search(r"TODO|PLACEHOLDER|citation needed", source, re.I)
    logpath = HERE / (stem + ".log")
    assert logpath.is_file(), f"Build {stem}.tex with --keep-logs first"
    log = logpath.read_text(encoding="utf-8", errors="replace")
    bad = [line for line in log.splitlines() if re.search(r"(?:Citation|Reference).*undefined|There were undefined references|Missing character:|Overfull \\[hv]box|^!", line)]
    assert not bad, f"{stem} build diagnostics: {bad}"
    assert (HERE / (stem + ".pdf")).is_file()
    print(f"{stem}: {len(used)} references; assets present; no unresolved citations, missing glyphs or overflow")
assert sets[0] == sets[1]
print("PASS: English/Vietnamese reference sets agree. External accuracy remains source-audit dependent.")
