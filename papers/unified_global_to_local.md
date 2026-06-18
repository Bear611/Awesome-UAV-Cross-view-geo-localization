# Unified Global-to-Local UAV Visual Localization

| 论文 | 分类原因 | 基于 abstract 优化的研究内容 | 数据/benchmark 介绍 |
|---|---|---|---|
| 基于紧耦合GNSS-视觉-惯性的平滑一致状态估计系统 | 摘要同时包含全局候选检索与局部匹配/坐标细化。 | 研究跨视角视觉定位；关注轻量化、速度或端侧部署；面向 GNSS-denied 导航或连续定位。 | 数据集：摘要未明确，通常包含卫星图库和局部定位标注；指标：AP、mAP、CE、ATE、IoU |
| Leveraging Map Retrieval and Alignment for Robust UAV Visual Geo-Localization | 命中关键词 `Map Retrieval and Alignment`，结合题名/摘要判断。 | 研究跨视角视觉定位；通过检索候选卫星图实现位置估计；强调图像/区域对齐以提升精度；处理高度变化、尺度差异或视场不一致；面向 GNSS-denied 导航或连续定位。 | 数据集：摘要未明确，通常包含卫星图库和局部定位标注；指标：AP、mAP、CE、ATE、homography、IoU |
| One-to-Many Retrieval Between UAV Images and Satellite Images for UAV Self-Localization in Real-World Scenarios | 命中关键词 `One-to-Many Retrieval`，结合题名/摘要判断。 | 研究跨视角视觉定位；通过检索候选卫星图实现位置估计；强调图像/区域对齐以提升精度；处理高度变化、尺度差异或视场不一致。 | 数据集：University-1652、SUES-200、DenseUAV、UAV-VisLoc；指标：AP、mAP、SDM、CE、ATE、localization error、IoU |
| Simple, Effective and General A New Backbone for Cross-view Image Geo-localization | 摘要同时包含全局候选检索与局部匹配/坐标细化。 | 研究跨视角视觉定位；强调图像/区域对齐以提升精度。 | 数据集：摘要未明确，通常包含卫星图库和局部定位标注；指标：AP、CE、ATE、IoU |
| A Hierarchical Absolute Visual Localization System for Low-Altitude Drones in GNSS-Denied Environments | 命中关键词 `Hierarchical Absolute Visual Localization`，结合题名/摘要判断。 | 研究跨视角视觉定位；通过检索候选卫星图实现位置估计；强调图像/区域对齐以提升精度；处理高度变化、尺度差异或视场不一致；面向 GNSS-denied 导航或连续定位。 | 数据集：摘要未明确，通常包含卫星图库和局部定位标注；指标：AP、mAP、CE、ATE、IoU |
| R2PLoc A Region-to-Point UAV Visual Geo-Localization Framework Leveraging Hierarchical Semantic Representation | 命中关键词 `R2PLoc`，结合题名/摘要判断。 | 研究跨视角视觉定位；通过检索候选卫星图实现位置估计；强调图像/区域对齐以提升精度；关注轻量化、速度或端侧部署；处理高度变化、尺度差异或视场不一致。 | 数据集：University-1652、SUES-200、DenseUAV、UAV-VisLoc；指标：AP、mAP、CE、ATE、homography |
| Cross-Attention Between Satellite and Ground Views for Enhanced Fine-Grained Robot | 摘要同时包含全局候选检索与局部匹配/坐标细化。 | 研究跨视角视觉定位；强调图像/区域对齐以提升精度；面向 GNSS-denied 导航或连续定位。 | 数据集：VIGOR、CVUSA、CVACT；指标：AP、mAP、CE、ATE、IoU |
