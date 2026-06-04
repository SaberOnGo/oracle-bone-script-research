# Character ID Assignment Log / 甲骨字 ID 分配记录

English:
Record why each `obs-char-*` ID was assigned. No IDs have been assigned yet.

The `obs-cand-*` IDs used in `005_hust-obc-validation-class-staging.csv` are staging IDs only. They reserve no formal `obs-char-*` identity and exist only to make downloaded HUST-OBC metadata reviewable and traceable.

The `obimd-main-cand-*` IDs used in `006_obimd-main-character-staging.csv` are staging IDs only. They preserve OBIMD main-character UID metadata and must be cross-checked before any formal project character ID is assigned.

The `obs-char-*` values listed in `009_hust-obc-obs-char-promotion-review-queue.csv` are reserved suggestions only. They are not formal assignments and must not be copied into `001_all-oracle-characters-index.csv` until cross-source review creates an accepted record.

The `000_hust-obc-promotion-bucket-manifest.csv` files under the `obs-char` bucket directories are partitions of the same HUST-OBC promotion queue. They do not create individual character records and do not change the formal assignment status.

简体中文：
记录每个 `obs-char-*` ID 的分配原因。当前尚未分配实际数据 ID。

`005_hust-obc-validation-class-staging.csv` 中使用的 `obs-cand-*` 只是暂存 ID。它们不占用正式 `obs-char-*` 身份，只用于让已下载的 HUST-OBC metadata 可以被复核和追溯。

`006_obimd-main-character-staging.csv` 中使用的 `obimd-main-cand-*` 只是暂存 ID。它们保留 OBIMD main-character UID metadata，必须经过交叉复核后才能分配正式项目甲骨字 ID。

`009_hust-obc-obs-char-promotion-review-queue.csv` 中列出的 `obs-char-*` 值只是保留建议。它们不是正式分配，只有跨来源复核形成已接受记录后，才能写入 `001_all-oracle-characters-index.csv`。

`obs-char` bucket 目录下的 `000_hust-obc-promotion-bucket-manifest.csv` 文件是同一 HUST-OBC 提升复核队列的分桶切片。它们不创建单字记录，也不改变正式 ID 分配状态。
