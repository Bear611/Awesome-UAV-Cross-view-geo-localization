# Taxonomy

This repository uses a four-category taxonomy for UAV cross-view geo-localization (UAV-CVGL). The first three categories are treated as the core UAV-CVGL scope. The fourth category is a related category for navigation and sensor-fusion work that directly uses visual geo-localization or cross-view map association.

### Retrieval-based UAV CVGL
这类方法把 UAV 图像作为 query，在大规模卫星图像库中检索最相似的 satellite tile、place 或区域。输出通常是 Top-K 检索结果，而不是连续坐标或姿态。重点是大范围搜索能力、跨视角鲁棒表征、尺度/高度/天气泛化和轻量化部署。常用指标包括 R@1、R@5、R@10、AP、mAP、SDM 等。

### Fine Pose Localization / Local Matching
这类方法假设已有局部卫星图、局部地图或候选区域，然后进一步估计 UAV 在局部地图中的精确位置或姿态。输出可以是 heatmap、2D coordinate、meter-level position、homography 或 3-DoF pose，重点是局部对齐精度和实时性。

### Unified Global UAV Visual Localization
这类方法连接全局检索和局部精定位：先从全局卫星图库中找到候选区域，再做局部匹配、坐标细化或姿态估计，最终输出米级位置或 3-DoF pose。它们更接近真实 UAV 自定位系统。

### Navigation-aided UAV Geo-localization
这类方法把 UAV-CVGL 与其他导航信息或连续运动约束结合，例如 VO、SLAM、IMU/INS、Kalman filter、历史轨迹、路径规划、语义地图、OSM/DEM 等。CVGL 通常作为 GNSS-denied 场景下的地图观测、重定位或误差校正模块。
