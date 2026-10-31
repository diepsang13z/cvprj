# UAV Aerial Mosaicking Experiments

## Mandatory Execution Policy

**Experiments must run exclusively on Google Colab hosted runtimes.** Local execution on personal machines is strictly forbidden for both classical algorithms (CPU) and learned deep models (GPU), per project rules (`RULES.md §8`).

Each notebook includes its own Google Colab environment check and setup cell.

---

## Notebook Structure

The experiment suite is organized into 5 focused, sequential, and fully self-contained notebooks. Each notebook contains all required data loaders, algorithms, and execution cells inline, allowing team members to open and run any single `.ipynb` file on Google Colab independently without external Python module dependencies.

| Notebook | Focus & Objective | Inputs | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **`classical_mosaicking_baseline.ipynb`** | SIFT and ORB feature matching and mosaicking on original full-resolution imagery. | Raw sequence frames in `data/` | Mosaic images, homography metrics, execution logs |
| **`deep_matching_pilot.ipynb`** | LightGlue matcher paired with SIFT or SuperPoint extractors on full-resolution imagery. | Raw sequence frames in `data/` | Pairwise matching metrics, homography matrices, mosaic |
| **`feature_matcher_benchmark.ipynb`** | Standardized 640px benchmark evaluating 7 feature matching configurations. | Sequence frames (scaled to 640px) | `manifest.json`, pairwise matches (`pairs/`), mosaic, HTML report |
| **`accumulated_drift_evaluation.ipynb`** | UAV trajectory/plane verification and accumulated homography drift measurement. | GPS/IMU metadata and output runs from benchmark | `trajectory_check.json`, `drift_selfconsistent.json` |
| **`failure_aware_mosaicking_pipeline.ipynb`** | Complete Failure-Aware Mosaicking research pipeline answering RQ1, RQ2, and RQ3. | Sequence scan windows (village 80-125, grass 0-45) | `scan_<method>.json`, RQ1/RQ2 results, recovery comparisons, `report.json` |

Supported method identifiers for 03 & 04:
`sift_bf`, `orb_bf`, `sift_lightglue`, `superpoint_lightglue`, `xfeat_mnn`, `xfeat_lighterglue`, `efficientloftr`.

---

## Collaborative Team Workflow (4 Members)

To avoid Colab VRAM exhaustion and git merge conflicts on `.ipynb` files, team members execute tasks independently on their own cloud runtimes and exchange only result artifacts (`.json`, `.csv`, images):

### Phase 1: Benchmark & Failure Scans (Parallel Cloud Runs)
- **Member A:** Run `sift_bf` and `orb_bf` in `feature_matcher_benchmark`; run SIFT window scan in `failure_aware_mosaicking_pipeline`.
- **Member B:** Run `sift_lightglue` and `superpoint_lightglue` in `feature_matcher_benchmark`; run SuperPoint+LightGlue scan in `failure_aware_mosaicking_pipeline`.
- **Member C:** Run `xfeat_mnn`, `xfeat_lighterglue`, and `efficientloftr` in `feature_matcher_benchmark`; run EfficientLoFTR scan in `failure_aware_mosaicking_pipeline`.
- **Member D:** Run trajectory verification in `accumulated_drift_evaluation`; evaluate accumulated drift using run outputs from A, B, and C.

### Phase 2: RQ Analysis & Report Synthesis (Fast CPU Execution)
Once the 3 scan files (`scan_sift_bf.json`, `scan_superpoint_lightglue.json`, `scan_efficientloftr.json`) are collected:
1. Provide the 3 file paths in `failure_aware_mosaicking_pipeline`.
2. Execute **Phase 2 (RQ1)**: Computes Spearman rank correlation and ROC-AUC for cheap failure indicators.
3. Execute **Phase 3 (RQ2)**: Simulates two-stage risk-based matcher routing and identifies optimal threshold $\tau$.
4. Execute **Phase 4 (RQ3)**: Evaluates the 4 recovery policies (`none`, `drop`, `anchor`, `split`) under shared threshold $\tau$.
5. Execute **Phase 5 (Assembly)**: Synthesizes final `report.json` and updates IEEE paper figures.

---

## Cloud Runtime Setup Guide

1. Open Google Colab. Clone the repository and set working directory to root:
   ```bash
   git clone -b dieps13z/work https://github.com/diepsang13z/cvprj.git
   cd cvprj
   pip install -r requirements_learned.txt
   ```
2. Mount Google Drive on Colab (default persistent output root: `/content/drive/MyDrive/uav_runs`).
3. Keep `DEVICE = "cpu"` or `"cuda"` consistent across all jobs within the same benchmark comparison.
4. Each run automatically generates a distinct UTC-timestamped folder to prevent overwriting prior runs or historical baseline data in `notebooks/outputs/`.
