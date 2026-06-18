# Fine Pose Localization / Local Matching

| 论文 | 分类原因 | 基于 abstract 优化的研究内容 | 数据/benchmark 介绍 |
|---|---|---|---|
| STHN Deep Homography Estimation for UAV Thermal Geo-localization with Satellite Imagery | 命中关键词 `STHN`，结合题名/摘要判断。 | 研究热红外/可见光与卫星图之间的跨模态定位；强调图像/区域对齐以提升精度；缓解跨域、跨模态或环境变化；面向 GNSS-denied 导航或连续定位。 | 数据集：摘要未明确，通常是局部地图、卫星裁剪、热红外-卫星配对或自采 UAV 数据；指标：AP、mAP、CE、ATE、RPE、homography、IoU |
| Comparative Studies of Descriptor-Based Image Matching Techniques for AAV Applications (1) | 命中关键词 `Descriptor-Based Image Matching`，结合题名/摘要判断。 | 研究跨视角视觉定位；强调图像/区域对齐以提升精度；处理高度变化、尺度差异或视场不一致；面向 GNSS-denied 导航或连续定位。 | 数据集：University-1652、DenseUAV、ALTO；指标：AP、mAP、CE、ATE、RPE、localization error、homography、IoU |
| SAVL Scene-Adaptive UAV Visual Localization Using Sparse Feature Extraction and Incremental Descriptor Mapping | 命中关键词 `SAVL`，结合题名/摘要判断。 | 研究跨视角视觉定位；强调图像/区域对齐以提升精度；面向 GNSS-denied 导航或连续定位。 | 数据集：DenseUAV；指标：AP、mAP、CE、ATE、IoU |
| Fine-Grained Cross-View Geo-Localization Using a Correlation-Aware Homography Estimator | 摘要强调局部对齐、homography、姿态或候选区域内精定位。 | 研究跨视角视觉定位；强调图像/区域对齐以提升精度；关注轻量化、速度或端侧部署；面向 GNSS-denied 导航或连续定位。 | 数据集：VIGOR、KITTI；指标：AP、mAP、CE、ATE、RPE、FPS、localization error、homography、IoU |
| SliceMatch Geometry-Guided Aggregation for Cross-View Pose Estimation | 摘要强调局部对齐、homography、姿态或候选区域内精定位。 | 研究跨视角视觉定位；关注轻量化、速度或端侧部署。 | 数据集：VIGOR；指标：AP、mAP、CE、ATE、localization error、homography、IoU |
| View Consistent Purification for Accurate Cross-View Localization | 摘要强调局部对齐、homography、姿态或候选区域内精定位。 | 研究跨视角视觉定位；强调图像/区域对齐以提升精度。 | 数据集：KITTI；指标：AP、mAP、CE、ATE、localization error、homography、IoU |
| Long-range UAV Thermal Geo-localization with Satellite Imagery | 命中关键词 `Long-range UAV Thermal`，结合题名/摘要判断。 | 研究热红外/可见光与卫星图之间的跨模态定位；缓解跨域、跨模态或环境变化；面向 GNSS-denied 导航或连续定位。 | 数据集：Boson-nighttime；指标：AP、mAP、CE、ATE、IoU |
| UASTHN Uncertainty-Aware Deep Homography Estimation for UAV Satellite-Thermal Geo-Localization | 命中关键词 `STHN`，结合题名/摘要判断。 | 研究热红外/可见光与卫星图之间的跨模态定位；强调图像/区域对齐以提升精度；缓解跨域、跨模态或环境变化；面向 GNSS-denied 导航或连续定位。 | 数据集：摘要未明确，通常是局部地图、卫星裁剪、热红外-卫星配对或自采 UAV 数据；指标：AP、mAP、CE、ATE、localization error、homography、IoU |
| Visual Localization with Google Earth Images for Robust Global Pose Estimation of UAVs | 命中关键词 `Google Earth`，结合题名/摘要判断。 | 研究跨视角视觉定位；面向 GNSS-denied 导航或连续定位。 | 数据集：摘要未明确，通常是局部地图、卫星裁剪、热红外-卫星配对或自采 UAV 数据；指标：AP、mAP、CE、ATE、RPE、homography、IoU |
