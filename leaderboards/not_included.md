# 未纳入 Leaderboard 的情况

| 数据集 / 论文情况 | 不纳入原因 |
|---|---|
| DenseUAV Rotation Robustness 设置 | 这是 UAV-GeoLoc/UAVPlace 论文中的旋转扰动实验，不是 DenseUAV 原始 benchmark 主协议；按当前规则删除。 |
| GTA-UAV Pre-Training Dataset 对比 | 这是 Game4Loc 原论文中的预训练数据迁移分析，不是独立数据集榜单；按当前规则删除。 |
| MT-UAV | 目前未找到可验证公开下载入口；因此不进入 leaderboard，仅在 dataset note 中说明未公开/未确认公开。 |
| UAV-R2P / UVL-R2P | 目前未找到可验证公开下载入口；因此不进入 leaderboard。 |
| C2F-UAVLoc | 暂未公开；公开前不进入正式 leaderboard，可作为 emerging benchmark 说明。 |
| CVUSA、CVACT、VIGOR、KITTI、Oxford RobotCar | 这些不是 UAV-satellite 原生数据集，虽然被部分论文用于辅助泛化或 fine pose 参考，但本版按 UAV-CVGL 核心榜单规则不纳入。 |
| UAV-VisLoc 原始论文 | 本地论文中可靠读到的是数据集定义和规模，未读到可直接比较的原始 leaderboard 数值；后续 Game4Loc/MM-Geo 的改造实验已单独列出。 |
| Thermal-UAV、Boson-nighttime、ALTO、AerialVL 等 | 本地可读结果不够完整，或者任务指标与本节主榜单不具可比性；若后续需要，可按各自原论文指标单独补表。 |
| 只报告“提升 x%”但未给完整表格的论文 | 不把相对提升换算成绝对数值，避免制造结果。 |
