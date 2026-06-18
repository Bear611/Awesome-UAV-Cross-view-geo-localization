# Datasets

This page summarizes UAV-CVGL datasets and related auxiliary datasets. A dataset is assigned to a category according to its original design purpose and how it has actually been used in existing papers, rather than theoretical applicability.

这一节只按“数据集被设计出来时服务的任务”和“已有论文实际使用它做过的实验”来判断适用类别；不写理论上可能适用的类别。若某数据集本身不是 UAV 数据集，但被相关论文用作辅助泛化实验，会单独标注为“辅助数据集”。

### UAV-CVGL 核心数据集

| 数据集 / benchmark | 原始设计用途 | 已有论文实际使用它做过的实验 | 对应类别 | 依据说明 |
|---|---|---|---|---|
| University-1652 | Drone-based geo-localization 多视角多源 benchmark，原始任务包括 drone-view target localization 和 drone navigation。 | 大量 UAV/drone-to-satellite 检索实验；University-1652、FSRA、MCCG、MEAN、CDM-Net、MobileGeo、APA-BI、SHAA 等主要报告 R@K/AP。部分新论文在其基础上重新标注或改造后用于端到端定位评估。 | Retrieval-based UAV CVGL；在被重新标注/改造成坐标定位评估时可归入 Unified Global UAV Visual Localization | 原始 benchmark 的主评价是跨视角图像检索；只有当论文明确报告坐标、米级误差或 3-DoF 时，才归入 Unified。 |
| SUES-200 | Multi-height multi-scene drone-satellite cross-view image benchmark，用于评估不同飞行高度下的跨视角匹配。 | MCCG、MEAN、SCOF、SMDT、APA-BI、SHAA、CAMP 等用它做 drone-satellite retrieval/matching，对比 R@K/AP；R2PLoc 等统一式方法也可在其上做定位式评估。 | Retrieval-based UAV CVGL；若论文明确做 region-to-point / coordinate refinement，则对应 Unified Global UAV Visual Localization | 原始设计是多高度检索/匹配 benchmark；统一式类别只来自后续论文的实际任务改造，而不是数据集天然定义。 |
| DenseUAV | 面向 UAV self-positioning 的低空城市密集采样数据集，提出 Recall 与 SDM 等评价。 | Vision-Based UAV Self-Positioning 用于 UAV self-positioning；后续 SMDT、SURFNet、MM-Geo、R2PLoc 等用它做 UAV-satellite 检索和定位距离评价。 | Retrieval-based UAV CVGL；Unified Global UAV Visual Localization | 原始论文既有检索式评价，也引入 SDM 来衡量检索结果与真实位置的距离，因此它比 University-1652 更接近从 retrieval 到 localization 的过渡。 |
| UAV-VisLoc | 大尺度 UAV visual localization 数据集，目标是根据 UAV 下视图在大幅卫星地图上确定真实位置坐标。 | UAV-VisLoc 原始论文用于真实地图定位；One-to-Many Retrieval 和 R2PLoc 使用它研究不完美匹配、one-to-many matching 或 region-to-point 定位。 | Unified Global UAV Visual Localization；也可用于 Retrieval-based UAV CVGL 的候选区域检索阶段 | 原始设计目标是输出真实坐标而不只是检索一个理想对齐 tile；如果论文只报告 Top-K，则按 Retrieval，若报告坐标/距离误差，则按 Unified。 |
| UAV-GeoLoc | 大词汇量 UAV geo-localization 数据集，配合 geometry-transformed 方法研究 UAV 图像到卫星图的跨视角定位。 | UAV-GeoLoc 原始论文用于大规模 UAV geo-localization；相关方法用其评估跨视角检索与几何变换鲁棒性。 | Retrieval-based UAV CVGL；若使用几何变换输出位置细化，则对应 Unified Global UAV Visual Localization | 依据是原始任务仍以 UAV-to-satellite 匹配为核心；几何变换实验决定它是否进入 Unified。 |
| GTA-UAV / Game4Loc | 基于游戏数据构建的大范围连续区域 UAV geo-localization benchmark，包含多高度、多姿态、多场景和部分重叠匹配。 | Game4Loc 明确从 image-level retrieval 扩展到按米评价 localization；MM-Geo、MMGeo 等使用其做多尺度、多模态或组合式 UAV geo-localization 实验。 | Retrieval-based UAV CVGL；Unified Global UAV Visual Localization | 原始论文同时保留检索评价和米级定位评价，因此可对应 Retrieval 与 Unified；不是因为“理论上可用”，而是原始 benchmark 就定义了 partial match 与 distance-based localization。 |
| Boson-nighttime | Long-range UAV Thermal Geo-localization 工作释放的夜间 thermal UAV 与 satellite imagery 数据。 | Long-range UAV Thermal Geo-localization 使用它做热红外 UAV 图像与卫星 RGB 图像匹配/定位实验。 | Fine Pose Localization / Local Matching | 实验重点是热红外-卫星跨模态匹配和定位，不是大规模普通 RGB Top-K 检索。 |
| Thermal-UAV | SCC-Loc 等 thermal geo-localization 工作构建的 thermal UAV 查询、卫星正射图和 DSM/结构信息数据。 | SCC-Loc 用于 thermal UAV localization，结合全局候选、局部匹配和可靠性选择，报告定位误差与阈值命中率。 | Fine Pose Localization / Local Matching；Unified Global UAV Visual Localization | 依据是已有 thermal localization 论文实际把它用于跨模态局部匹配和统一式粗到细定位。 |
| ALTO | 面向 UAV visual place recognition 和 localization 的真实长航迹数据集，包含 GPS-INS、下视 RGB、参考影像和传感器信息。 | ALTO 原始任务包括 VPR、localization、image registration、visual odometry；相关 AAV/UAV matching 论文可用它评估航迹场景下的匹配和导航定位。 | Navigation-aided UAV Geo-localization；Fine Pose Localization / Local Matching | 原始数据包含轨迹和 GPS-INS，不是单帧 satellite tile retrieval benchmark；因此更适合导航辅助和局部注册/匹配类实验。 |

### 辅助 / 跨域评估数据集

| 数据集 / benchmark | 原始设计用途 | 已有论文实际使用它做过的实验 | 对应类别 | 说明 |
|---|---|---|---|---|
| CVUSA / CVACT | Ground-to-satellite cross-view geo-localization 数据集。 | 部分 UAV-CVGL 论文把它们作为跨域泛化或与传统 CVGL 方法对比的辅助实验。 | 不作为 UAV-CVGL 核心类别；仅作为 Retrieval-based 方法的辅助泛化验证 | 查询视角是 ground/street，不是 UAV；不能据此说数据集适用于 UAV 自定位，只能说相关论文用它做泛化对比。 |
| VIGOR | Ground-to-satellite fine-grained geo-localization benchmark。 | Fine-grained homography / local matching 类论文常用它评估坐标细化、局部匹配或 3-DoF 相关能力。 | Fine Pose Localization / Local Matching 的辅助验证 | 不是 UAV 数据集；适用性来自已有 local matching 论文的实际实验，而不是 UAV-CVGL 原生设计。 |
| KITTI | 车载视觉定位、里程计、pose/matching benchmark。 | 一些 fine-grained cross-view localization 或 pose/matching 论文用它做 ground/vehicle 场景的定位泛化实验。 | Fine Pose Localization / Local Matching；Navigation-aided 方法参考 | 不是 UAV-satellite 数据集；只能作为 pose/matching/odometry 模块参考。 |
| University160k | University-1652 的大规模干扰库/扩展评测。 | 用于测试检索模型在更大 gallery 和 distractor 下的检索可扩展性。 | Retrieval-based UAV CVGL | 它的实验目标是大规模 retrieval，不提供完整局部姿态或连续导航评价。 |
