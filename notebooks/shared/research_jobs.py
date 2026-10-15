"""File-based handoff between independent cloud research jobs."""
from cloud_runtime import require_cloud, new_run
require_cloud()
import hashlib
import json
from pathlib import Path
import failure_core as core
from failure_core import *


def configure(root, device):
    global DEVICE
    DEVICE = device
    core.ROOT = Path(root)
    core.DEVICE = device
    core._MATCH_CACHE.clear()
    core._REFERENCE_CACHE.clear()
    torch.set_num_threads(4)
    cv2.setNumThreads(4)
    torch.manual_seed(0)
    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA unavailable; select an appropriate cloud runtime")


def signature():
    return {"max_side": MAX_SIDE, "max_keypoints": MAX_KEYPOINTS,
            "ransac_px": RANSAC_PX, "ratio": RATIO, "min_inliers": MIN_INLIERS,
            "tolerance_px": TOLERANCE_PX, "windows": {s: list(w) for s, w in WINDOWS.items()},
            "seed": 0, "device": core.DEVICE, "torch": torch.__version__,
            "opencv": cv2.__version__, "numpy": np.__version__,
            "accelerator": torch.cuda.get_device_name() if core.DEVICE.startswith("cuda") else platform.processor(),
            "code_sha256": hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest(),
            "jobs_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def scan_job(method, output_root):
    if method not in (CHEAP, STRONG, DIAGNOSTIC):
        raise ValueError(method)
    target = new_run(output_root, "05_scan_" + method)
    payload = {"signature": signature(), "method": method, "scans": [], "inputs": []}
    for sequence, (start, steps) in WINDOWS.items():
        scan = scan_window(sequence, start, steps, methods=(method,))
        payload["inputs"].extend({"path": str(p.relative_to(core.ROOT)),
                                  "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in scan["files"])
        payload["scans"].append({k: v for k, v in scan.items() if k not in ("files", "images")})
    dump(target / "scan.json", payload)
    print(target / "scan.json")
    return target


def load_scans(paths, images=False):
    payloads = [json.loads(Path(p).read_text(encoding="utf-8")) for p in paths]
    if sorted(p["method"] for p in payloads) != sorted((CHEAP, STRONG, DIAGNOSTIC)):
        raise ValueError("Provide exactly one scan.json per research matcher")
    first = payloads[0]
    for p in payloads:
        if p["signature"] != first["signature"] or p["inputs"] != first["inputs"]:
            raise ValueError("Cannot combine scans with different code, environment, config or input hashes")
        if len(p["scans"]) != len(WINDOWS) or {s["sequence"] for s in p["scans"]} != set(WINDOWS):
            raise ValueError("Missing or duplicate sequence in scan artifact")
        for scan in p["scans"]:
            if (scan["start"], scan["steps"]) != WINDOWS[scan["sequence"]]:
                raise ValueError("Scan window differs from configured window")
            if set(scan["rows"]) != {p["method"]}:
                raise ValueError("Scan contains another matcher's rows")
            expected = {str(i) for i in range(1, scan["steps"] + 1)}
            if set(scan["rows"][p["method"]]) != expected or set(scan["reference"]) != expected:
                raise ValueError("Missing step in scan artifact")
    scans = []
    for sequence in WINDOWS:
        parts = [next(s for s in p["scans"] if s["sequence"] == sequence) for p in payloads]
        base = dict(parts[0])
        # Reference times differ across workers; geometry and validity must agree.
        reference_geometry = lambda s: {k: {f: v for f, v in r.items() if f != "seconds"}
                                        for k, r in s["reference"].items()}
        if any(reference_geometry(s) != reference_geometry(base) for s in parts):
            raise ValueError("Reference geometry differs across workers: " + sequence)
        base["reference"] = {int(k): v for k, v in base["reference"].items()}
        base["rows"] = {tier: {int(k): v for k, v in rows.items()}
                        for part in parts for tier, rows in part["rows"].items()}
        base["size_original"] = tuple(base["size_original"])
        base["size_processed"] = tuple(base["size_processed"])
        if images:
            files, loaded, size = frames_of(sequence, base["start"], base["steps"])
            actual = [{"path": str(p.relative_to(core.ROOT)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                      for p in files]
            expected = [r for r in first["inputs"] if sequence in Path(r["path"]).parts]
            if actual != expected or tuple(size) != base["size_original"]:
                raise ValueError("Input images changed since scan: " + sequence)
            base.update(files=files, images=loaded)
            for step, ref in base["reference"].items():
                key = (str(files[step - 1]), str(files[step]))
                core._REFERENCE_CACHE[key] = (np.array(ref["H_original"]), ref["inliers"], ref["matches"], ref["seconds"])
            for method, rows in base["rows"].items():
                for step, row in rows.items():
                    core._MATCH_CACHE[(method, base["size_processed"], str(files[step - 1]), str(files[step]))] = row
        scans.append(base)
    provenance = {"signature": first["signature"], "inputs": first["inputs"],
                  "scan_hashes": sorted(hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths)}
    return scans, provenance


def save_result(output_root, job, provenance, values):
    target = new_run(output_root, job)
    dump(target / "result.json", {"provenance": provenance, **values})
    print(target / "result.json")
    return target


def rq1_job(scan_paths, output_root):
    scans, provenance = load_scans(scan_paths)
    return save_result(output_root, "05_rq1", provenance, {"rq1": rq1_table(scans)})


def recovery_job(scan_paths, rq2_path, policy, output_root):
    if policy not in POLICIES:
        raise ValueError(policy)
    scans, provenance = load_scans(scan_paths, images=True)
    if signature() != provenance["signature"]:
        raise ValueError("Recovery must use the scan environment/configuration")
    rq2 = json.loads(Path(rq2_path).read_text(encoding="utf-8"))
    if rq2["provenance"] != provenance:
        raise ValueError("RQ2 and recovery must use the same scans")
    tau = choose_tau([r for r in rq2["rq2"] if r["policy"] == "routed"]) or TAU_NCC
    rows = []
    for scan, method in zip(scans, (CHEAP, DIAGNOSTIC)):
        rows.extend(run_policies(scan, method, tau, policies=(policy,)))
    return save_result(output_root, "05_rq3_" + policy, provenance,
                       {"rq3": rows, "tau_star": tau,
                        "rq2_sha256": hashlib.sha256(Path(rq2_path).read_bytes()).hexdigest()})


def assemble(scan_paths, rq1_path, rq2_path, recovery_paths, output_root):
    scans, provenance = load_scans(scan_paths)
    rq1 = json.loads(Path(rq1_path).read_text(encoding="utf-8"))
    rq2 = json.loads(Path(rq2_path).read_text(encoding="utf-8"))
    recovery = [json.loads(Path(p).read_text(encoding="utf-8")) for p in recovery_paths]
    for result in [rq1, rq2, *recovery]:
        if result["provenance"] != provenance:
            raise ValueError("Stage provenance mismatch")
    rq2_hash = hashlib.sha256(Path(rq2_path).read_bytes()).hexdigest()
    if any(r["rq2_sha256"] != rq2_hash for r in recovery):
        raise ValueError("Recovery used a different RQ2 result")
    rows = [row for result in recovery for row in result["rq3"]]
    expected = {(s, p) for s in WINDOWS for p in POLICIES}
    if len(rows) != len(expected) or {(r["sequence"], r["policy"]) for r in rows} != expected:
        raise ValueError("Missing or duplicate recovery policy/sequence")
    target = new_run(output_root, "05_failure_aware")
    report = {"stamp": target.name, "scope": "Split cloud RQ1/RQ2/RQ3; not integrated end-to-end",
              "manifest": {**provenance["signature"], "cheap": CHEAP, "strong": STRONG,
                           "diagnostic": DIAGNOSTIC}, "provenance": provenance,
              "inputs": provenance["inputs"], "scans": [], "rq1": rq1["rq1"],
              "rq2": rq2["rq2"], "rq3": rows,
              "tau_chosen": rq2["tau_chosen"], "rq2_fullres_detail": rq2.get("rq2_fullres_detail", [])}
    from research_report import check_metrics, render_report
    check_metrics(report, scans)
    for scan in scans:
        report["scans"].append({"sequence": scan["sequence"], "start": scan["start"], "steps": scan["steps"],
                                "reference_inliers_min": min(r["inliers"] for r in scan["reference"].values()),
                                "rows": scan["rows"]})
        dump(target / f"scan_{scan['sequence']}.json", scan)
    dump(target / "report.json", report)
    render_report(report, scans, target)
    print(target / "report.json")
    return target


def rq2_job(scan_paths, output_root):
    scans, provenance = load_scans(scan_paths, images=True)
    if signature() != provenance["signature"]:
        raise ValueError("RQ2 full-resolution matching must use the scan environment/configuration")
    values = {"rq2": [], "tau_chosen": {}, "rq2_fullres_detail": []}
    for scan in scans:
        sweep = [simulate(scan, "classical"), simulate(scan, "learned")]
        sweep += [simulate(scan, "routed", tau_ncc=tau) for tau in TAU_GRID]
        tau = choose_tau(sweep)
        values["rq2"].extend({"sequence": scan["sequence"], **row} for row in sweep)
        values["tau_chosen"][scan["sequence"]] = tau
        if tau is None:
            continue
        matcher = load_matcher(STRONG, DEVICE)
        flagged = [s for s in range(1, scan["steps"] + 1)
                   if risk(scan["rows"][CHEAP][s], tau, TAU_INLIER_RATIO)]
        full_images, full = LazyImages(scan["files"]), {}
        for step in flagged:
            row = dict(estimate_cached(FULLRES, matcher, full_images, scan["files"], step - 1, step,
                                       scan["size_original"], scan["size_original"], paths=scan["files"]),
                       step=step, tier=FULLRES)
            if row["status"] == "success":
                row["step_error_px"] = marker_error(np.array(row["H_original"], float),
                                                    np.array(scan["reference"][step]["H_original"], float),
                                                    scan["size_original"])
            full[step] = row
        fullres_rows = {s: full[s] if s in full else dict(scan["rows"][STRONG][s], tier=FULLRES)
                        for s in range(1, scan["steps"] + 1)}
        routed = simulate(scan, "routed", tau_ncc=tau, strong_rows=fullres_rows)
        values["rq2"].append({"sequence": scan["sequence"], **routed, "policy": "routed_fullres"})
        values["rq2_fullres_detail"].append({
            "sequence": scan["sequence"], "tau": tau, "flagged_steps": flagged,
            "fullres_step_error_mean_px": float(np.mean([full[s]["step_error_px"] for s in flagged])) if flagged else None,
            "native_px_step_error_mean_px": float(np.mean([scan["rows"][STRONG][s]["step_error_px"] for s in flagged])) if flagged else None})
        del matcher
    return save_result(output_root, "05_rq2", provenance, values)
