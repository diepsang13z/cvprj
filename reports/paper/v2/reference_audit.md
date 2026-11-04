# Reference Verification and Bibliographic Audit

This document records verification provenance, primary sources, Google Scholar status, and metadata reconciliation for all 17 references cited in IEEE paper v2.

## 1. Verification Methodology and Repository Metadata Variations
- **Primary Publisher and Open-Access Repositories:** All 17 citations are verified against primary records from Crossref API, IEEE Xplore, CVF Open Access (CVPR/ICCV), ACM Digital Library, MDPI, Wiley Online Library, and ISPRS Archives.
- **Repository Pagination Variations (CVF vs. Crossref):** Conference proceedings exhibit differing pagination schemes between CVF Open Access and Crossref/IEEE indexing. For conference entries, we adopt canonical CVF Open Access proceedings pagination:
  - `lindenberger2023` (LightGlue): CVF records pp. 17627--17638; Crossref indexes pp. 17581--17592.
  - `sun2021` (LoFTR): CVF records pp. 8922--8931; Crossref records pp. 8918--8927. We preserve this disagreement and use CVF pagination, without inferring its cause.
  - `ivashechkin2021` (VSAC): CVF records pp. 15243--15252; Crossref indexes pp. 15223--15232.
  - `detone2018` (SuperPoint): CVF records pp. 224--236; Crossref returns the anomalous range `337--33712`, which is not copied into the bibliography.
  - `barath2023` (CVPR 2023, pp. 21360--21370), `wang2024` (CVPR 2024, pp. 21666--21675), and `xfeat2024` (CVPR 2024, pp. 2682--2691) match across CVF and Crossref records.
- **Google Scholar Query Status:** Programmatic HTTP queries with standard headers (`scholar.google.com/scholar?q=...`) returned direct title and citation matches for the initial 4 sequential queries (`lowe2004`, `rublee2011`, `fischler1981`, `detone2018`). Subsequent automated queries encountered Google Scholar's anti-bot rate-limiting (HTTP 200 presenting a CAPTCHA traffic challenge). Publisher and open-access repositories therefore serve as the authoritative reference source.
- **Verification Limitations:** Bibliographic metadata and cited contributions are verified against primary publisher and CVF records. Proprietary paywalled bodies were not OCR-scraped where official abstracts, methodologies, and open-access preprints sufficed.

## 2. Detailed Audit Table and Claim Evidence

| Key | Primary Source URL / DOI | Scholar Status | Metadata Reconciliation Notes | Cited Claim Support in Paper |
| :--- | :--- | :--- | :--- | :--- |
| `lowe2004` | https://doi.org/10.1023/B:VISI.0000029664.99615.94 | Verified (Direct hit) | Consistent across Crossref/publisher | Classical scale-invariant feature extraction baseline (SIFT). |
| `rublee2011` | https://doi.org/10.1109/ICCV.2011.6126544 | Verified (Direct hit) | Consistent across Crossref/publisher | Lightweight binary keypoint detector and descriptor (ORB). |
| `fischler1981` | https://doi.org/10.1145/358669.358692 | Verified (Direct hit) | Consistent across Crossref/publisher | Robust parametric model fitting and consensus algorithm (RANSAC). |
| `detone2018` | https://doi.org/10.1109/CVPRW.2018.00060 | Verified (Direct hit) | Adopted CVF canonical pages (224--236) | Self-supervised interest point detection and description (SuperPoint). |
| `lindenberger2023` | https://doi.org/10.1109/ICCV51070.2023.01616 | Throttled (CVF/Crossref verified) | Adopted CVF pages (17627--17638); fixed DOI | Graph neural network matcher with adaptive depth and early exit. |
| `sun2021` | https://doi.org/10.1109/CVPR46437.2021.00881 | Throttled (CVF/Crossref verified) | Adopted CVF pages (8922--8931) | Detector-free local feature matching with Transformers (LoFTR). |
| `wang2024` | https://doi.org/10.1109/CVPR52733.2024.02047 | Throttled (CVF/Crossref verified) | Corrected authors & DOI from v1 mismatch | Efficient LoFTR: aggregated attention + two-stage correlation. |
| `xfeat2024` | https://doi.org/10.1109/CVPR52733.2024.00259 | Throttled (CVF/Crossref verified) | Corrected authors (G. Potje et al.) & DOI from v1 mismatch | Accelerated lightweight feature matching for edge platforms. |
| `map2dfusion` | https://doi.org/10.1109/IROS.2016.7759672 | Throttled (Crossref verified) | Reconciled author given name initial (Shuhui Bu) | Monocular visual SLAM tracking with local bundle adjustment. |
| `hwang2026` | https://doi.org/10.3390/app16042133 | Throttled (MDPI/Crossref verified) | Corrected published title & complete author roster | Real-time CPU sequential homography via inlier count gates. |
| `li2023` | https://doi.org/10.3390/rs15082127 | Throttled (MDPI/Crossref verified) | Corrected complete author list (R. Li, P. Gao, et al.) | Incremental video mosaic with keyframe rematching against drift. |
| `kharismawati2025` | https://doi.org/10.1002/ppj2.70033 | Throttled (Wiley/Crossref verified) | Corrected author initials (D. E. Kharismawati) | DroneZaic pipeline: motion clustering into independent submosaics. |
| `chen2022` | https://doi.org/10.3390/rs14051068 | Throttled (MDPI/Crossref verified) | Corrected published title & complete author roster | Seamline dynamic programming & half-projective warp in UAV video. |
| `kim2025` | https://doi.org/10.5194/isprs-archives-XLVIII-2-W11-2025-169-2025 | Throttled (ISPRS/Crossref verified) | Corrected author roster (S. Kim & T. Kim) | Robust UAV mosaicking combining SIFT with LightGlue. |
| `zaffar2024` | https://doi.org/10.1109/CVPR52733.2024.01680 | Throttled (CVF/Crossref verified) | Corrected author roster (M. Zaffar, L. Nan, J. Kooij) | Uncertainty estimation in image matching & place recognition. |
| `barath2023` | https://doi.org/10.1109/CVPR52729.2023.02046 | Throttled (CVF/Crossref verified) | Corrected complete author list & DOI (`02046` vs `01695`) | Benchmark of robust estimators and correspondence filters. |
| `ivashechkin2021` | https://doi.org/10.1109/ICCV48922.2021.01496 | Throttled (CVF/Crossref verified) | Adopted CVF pages (15243--15252); fixed DOI | VSAC: independent inliers & sequential hypothesis verification. |

## 3. Discrepancy Inventory Corrected from v1
1. **XFeat (`xfeat2024`):** In v1, authors were listed as *P. Potlapalli, P. Lindenberger, and M. Pollefeys* with incorrect page range (19163--19172) and mismatched DOI. Primary publisher metadata resolves authors as *Guilherme Potje, Felipe Cadar, André Araujo, Renato Martins, Erickson R. Nascimento*, CVPR 2024, pp. 2682--2691, DOI `10.1109/CVPR52733.2024.00259`.
2. **Efficient LoFTR (`wang2024`):** In v1, authors were cited as *Q. Wang, J. Zhang, K. Han, X. Peng, and C. Shen*, with DOI `10.1109/CVPR52733.2024.02035` (belonging to an unrelated paper). Canonical CVF metadata resolves authors as *Yifan Wang, Xingyi He, Sida Peng, Dongli Tan, Xiaowei Zhou*, CVPR 2024, pp. 21666--21675, DOI `10.1109/CVPR52733.2024.02047`, proposing aggregated attention with adaptive token selection and a two-stage correlation layer.
3. **SuperPoint (`detone2018`):** [CVF proceedings](https://openaccess.thecvf.com/content_cvpr_2018_workshops/w9/html/DeTone_SuperPoint_Self-Supervised_Interest_CVPR_2018_paper.html) supply pp. 224--236 and the IEEE workshop venue. The anomalous Crossref page field is not adopted.
4. **LightGlue (`lindenberger2023`):** V1 DOI `10.1109/ICCV51070.2023.00812` identifies another work. Crossref resolves the cited work to `10.1109/ICCV51070.2023.01616`; [CVF proceedings](https://openaccess.thecvf.com/content/ICCV2023/html/Lindenberger_LightGlue_Local_Feature_Matching_at_Light_Speed_ICCV_2023_paper.html) supply pp. 17627--17638.
5. **LoFTR (`sun2021`):** [CVF proceedings](https://openaccess.thecvf.com/content/CVPR2021/html/Sun_LoFTR_Detector-Free_Local_Feature_Matching_With_Transformers_CVPR_2021_paper.html) list pp. 8922--8931, whereas Crossref lists pp. 8918--8927. CVF pagination is adopted; the cause of the discrepancy is not established.
6. **Hwang et al. 2026 (`hwang2026`):** In v1, title was altered to *"Real-time 2D orthomosaic mapping using CPU-based incremental homography matrix estimation with UAV video"* and authors truncated to *D. Hwang, S. Lee, and J. Park*. Actual published article is *"Real-Time 2D Orthomosaic Mapping from UAV Video via Feature-Based Image Registration"*, by *Se-Yun Hwang, Seunghoon Oh, Jae-Chul Lee, Soon-Sub Lee, Changsoo Ha*, Appl. Sci. 2026, vol. 16, no. 4, Art. no. 2133, DOI `10.3390/app16042133`.
7. **Li et al. 2023 (`li2023`):** In v1, author list was given as *X. Li, Y. Liu, C. Wang, and Z. Zhang*. Publisher records resolve authors as *Ronghao Li, Pengqi Gao, Xiangyuan Cai, Xiaotong Chen, Jiangnan Wei, Yinqian Cheng, Hongying Zhao*, Remote Sens. 2023, vol. 15, no. 8, Art. no. 2127, DOI `10.3390/rs15082127`.
8. **Barath et al. 2023 (`barath2023`):** In v1, authors were listed as *D. Barath, L. Cavalli, and M. Pollefeys* with DOI `...01695` (which was an unrelated 3D point cloud sampling paper). Correct metadata: *Daniel Barath, Dmytro Mishkin, Michal Polic, Wolfgang Förstner, Jiří Matas*, CVPR 2023, pp. 21360--21370, DOI `10.1109/CVPR52729.2023.02046`.
9. **VSAC (`ivashechkin2021`):** In v1, DOI was `...00595` (an unrelated paper). Canonical CVF metadata resolves authors as *Maksym Ivashechkin, Daniel Barath, Jiří Matas*, ICCV 2021, pp. 15243--15252, DOI `10.1109/ICCV48922.2021.01496`.
10. **Zaffar et al. 2024 (`zaffar2024`):** In v1, authors were *M. Zaffar, L. S. F. Ribeiro, S. Ehsan, M. Milford*. Correct authors: *Mubariz Zaffar, Liangliang Nan, Julian F. P. Kooij*, CVPR 2024, pp. 17743--17753, DOI `10.1109/CVPR52733.2024.01680`.
11. **Chen et al. 2022 (`chen2022`):** In v1, title was altered to *"UAV video stitching based on optimal seamline and half-projective warp"*. Correct title is *"UAV Image Stitching Based on Optimal Seam and Half-Projective Warp"*, by *Jun Chen, Zixian Li, Chengli Peng, Yong Wang, Wenping Gong*, Remote Sens. 2022, vol. 14, no. 5, Art. no. 1068, DOI `10.3390/rs14051068`.
12. **Kim & Kim 2025 (`kim2025`):** In v1, authors were given as *J. Kim and S. Kim*. Correct authors: *Sunghyeon Kim and Taejung Kim*, ISPRS Archives 2025, pp. 169--175, DOI `10.5194/isprs-archives-XLVIII-2-W11-2025-169-2025`.
13. **DroneZaic (`kharismawati2025`):** In v1, authors were listed as *M. Kharismawati and D. Kazic*. Correct authors: *Dewi Endah Kharismawati and Toni Kazic*, The Plant Phenome Journal 2025, vol. 8, no. 1, Art. no. e70033, DOI `10.1002/ppj2.70033`.

## 4. Additional primary claim checks

- [Efficient LoFTR](https://openaccess.thecvf.com/content/CVPR2024/html/Wang_Efficient_LoFTR_Semi-Dense_Local_Feature_Matching_with_Sparse-Like_Speed_CVPR_2024_paper.html): aggregated attention with adaptive token selection and a two-stage correlation layer, not QuadTree aggregation.
- [VSAC](https://openaccess.thecvf.com/content/ICCV2021/html/Ivashechkin_VSAC_Efficient_and_Accurate_Estimator_for_H_and_F_ICCV_2021_paper.html): independent inliers and adaptive sequential hypothesis verification; CVF pp. 15243--15252.
- [Zaffar et al.](https://openaccess.thecvf.com/content/CVPR2024/html/Zaffar_On_the_Estimation_of_Image-matching_Uncertainty_in_Visual_Place_Recognition_CVPR_2024_paper.html): image-retrieval uncertainty, learned uncertainty, geometric verification and a reference-pose baseline; not a UAV drift detector.
- [HEB](https://openaccess.thecvf.com/content/CVPR2023/html/Barath_A_Large-Scale_Homography_Benchmark_CVPR_2023_paper.html): reference homographies for robust-estimator and correspondence-filter evaluation.
- [XFeat](https://openaccess.thecvf.com/content/CVPR2024/html/Potje_XFeat_Accelerated_Features_for_Lightweight_Image_Matching_CVPR_2024_paper.html): author order and pp. 2682--2691 checked against the displayed proceedings BibTeX.
