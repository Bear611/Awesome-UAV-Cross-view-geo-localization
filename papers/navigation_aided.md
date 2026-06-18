# Navigation-aided / Sensor-fusion UAV Geo-localization

This is a related category. General UAV navigation, SLAM, or path planning papers should be included only when they are directly related to visual geo-localization, map association, or GNSS-denied relocalization.


| 论文 | 分类原因 | 基于 abstract 优化的研究内容 | 数据/benchmark 介绍 |
|---|---|---|---|
| Visible-to-Infrared Image Translation for Matching Tasks | 摘要把定位与导航、轨迹、状态估计或路径规划结合。 | 研究热红外/可见光与卫星图之间的跨模态定位；强调图像/区域对齐以提升精度；缓解跨域、跨模态或环境变化。 | 数据集：摘要未明确或非 UAV-CVGL benchmark；指标：AP、mAP、CE、ATE、IoU |
| Bridging the appearance gap Multi-experience localization for long-term visual teach and repeat | 摘要把定位与导航、轨迹、状态估计或路径规划结合。 | 研究跨视角视觉定位；缓解跨域、跨模态或环境变化。 | 数据集：摘要未明确或非 UAV-CVGL benchmark；指标：AP、mAP、CE、ATE、latency、localization error、IoU |
| Notes on Kalman Filter | 命中关键词 `Kalman`，结合题名/摘要判断。 | 研究跨视角视觉定位；面向 GNSS-denied 导航或连续定位。 | 数据集：摘要未明确或非 UAV-CVGL benchmark；指标：AP、mAP、CE、ATE、IoU |
| Rethinking Cross-view Object Geo-Localization Towards Many-to-Many Real-world Localization | 摘要把定位与导航、轨迹、状态估计或路径规划结合。 | 研究跨视角视觉定位；强调图像/区域对齐以提升精度。 | 数据集：VIGOR；指标：AP、mAP、CE、ATE、IoU |
| ST-D3QN Advancing UAV Path Planning With an Enhanced Deep Reinforcement Learning Framework in Ultra-Low Altitudes | 摘要把定位与导航、轨迹、状态估计或路径规划结合。 | 研究 UAV 路径规划与定位协同；处理高度变化、尺度差异或视场不一致。 | 数据集：摘要未明确或非 UAV-CVGL benchmark；指标：AP、mAP、CE、ATE、IoU |
| Toward Integrating Semantic-aware Path Planning and Reliable Localization for UAV Operations | 命中关键词 `Semantic-aware Path Planning`，结合题名/摘要判断。 | 研究 UAV 视觉跟踪或目标跟踪；强调图像/区域对齐以提升精度；关注轻量化、速度或端侧部署。 | 数据集：摘要未明确或非 UAV-CVGL benchmark；指标：AP、mAP、CE、ATE、IoU |
| FoundLoc Vision-based Onboard Aerial Localization in the Wild | 摘要把定位与导航、轨迹、状态估计或路径规划结合。 | 研究跨视角视觉定位；面向 GNSS-denied 导航或连续定位。 | 数据集：摘要未明确或非 UAV-CVGL benchmark；指标：AP、mAP、CE、ATE、IoU |
| Beyond Matching to Tiles Bridging Unaligned Aerial and Satellite Views for Vision-Only UAV Navigation | 命中关键词 `Beyond Matching to Tiles`，结合题名/摘要判断。 | 研究跨视角视觉定位；强调图像/区域对齐以提升精度；关注轻量化、速度或端侧部署；面向 GNSS-denied 导航或连续定位。 | 数据集：University-1652；指标：AP、mAP、CE、ATE、localization error、IoU |
| Matching 2D Images in 3D Metric Relative Pose from Metric | 摘要把定位与导航、轨迹、状态估计或路径规划结合。 | 研究跨视角视觉定位；强调图像/区域对齐以提升精度；处理高度变化、尺度差异或视场不一致。 | 数据集：摘要未明确或非 UAV-CVGL benchmark；指标：AP、mAP、CE、ATE、IoU |
| MultiLoc Multi-view Guided Relative Pose Regression for Fast and Robust Visual Re-Localization | 摘要把定位与导航、轨迹、状态估计或路径规划结合。 | 研究跨视角视觉定位；通过检索候选卫星图实现位置估计；强调图像/区域对齐以提升精度；处理高度变化、尺度差异或视场不一致；缓解跨域、跨模态或环境变化。 | 数据集：摘要未明确或非 UAV-CVGL benchmark；指标：AP、mAP、CE、ATE |
