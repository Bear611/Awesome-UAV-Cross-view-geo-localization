# 数据集公开状态与纳入规则

本文件只把“有可验证公开访问入口的数据集 / benchmark”放入正式 leaderboard。若数据集未公开、仅论文中构建但找不到公开下载入口，或者只是某篇论文的额外迁移/鲁棒性实验设置，则不进入正式 leaderboard。

| 数据集 / benchmark | 公开状态 | Leaderboard 处理 | 说明 |
|---|---|---|---|
| University-1652 | 公开，可按官方 repo 申请/下载 | 保留 | 官方 repo 提供 dataset link 与 SOTA 表。 |
| SUES-200 | 公开，限学术研究使用 | 保留 | 官方 repo 提供 Google Drive、百度网盘、天翼网盘链接。 |
| DenseUAV | 公开 | 保留原始 self-positioning 榜单 | 只保留原始 Recall@K / SDM@K 设置；删除旋转鲁棒性扩展表。 |
| GTA-UAV / Game4Loc | 公开，低分辨率版本已发布；高分辨率版本标注为 soon | 保留低分辨率/已公开协议榜单 | 只保留原始 Cross-Area / Same-Area 任务；删除 pre-training dataset 对比表。 |
| UAV-VisLoc | 公开 | 保留基于公开 UAV-VisLoc 的改造协议 | 原始数据公开，但不同论文改造 protocol 不与原始任务混排。 |
| World-UAV / UAV-GeoLoc | 公开，Hugging Face 已发布 | 保留 | 可作为公开数据集榜单。 |
| Nardo-Air | 公开，可通过 AnyLoc public release 获取 | 保留 | 属于 aerial/UAV localization 相关真实数据；保留时需注明来自 AnyLoc/FoundLoc 相关评测。 |
| MT-UAV | 未确认公开 | 不纳入 leaderboard | 目前只找到 MM-Geo repo，未找到可验证数据下载说明。 |
| UAV-R2P / UVL-R2P | 未确认公开 | 不纳入 leaderboard | 当前只确认论文构建了 UAV-R2P/UVL-R2P benchmark，未找到公开下载入口。 |
| C2F-UAVLoc | 暂未公开 | 暂不纳入正式 leaderboard | 可以放入 “Emerging / Not yet public benchmark” note；公开后再开正式榜单。 |
