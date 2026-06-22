# Character ID Assignment Log / 甲骨字 ID 分配记录

English:
Record why each `obs-char-*` ID was assigned. No IDs have been formally
assigned from staging data yet.

The `obs-cand-*` IDs in `005_hust-obc-validation-class-staging.csv` are
staging IDs only. They reserve no formal `obs-char-*` identity and only make
downloaded HUST-OBC metadata reviewable and traceable.

The `obimd-main-cand-*` IDs in `006_obimd-main-character-staging.csv` are
staging IDs only. They preserve OBIMD UID metadata for cross-checking before
any formal project character ID is assigned.

The `obs-char-*` values in `009_hust-obc-obs-char-promotion-review-queue.csv`
are reserved suggestions only. They are not formal assignments and must not
enter `001_all-oracle-characters-index.csv` before cross-source review creates
an accepted record.

The `000_hust-obc-promotion-bucket-manifest.csv` files are bucket slices of
the same HUST-OBC promotion queue. They do not create individual character
records and do not change the formal assignment status.

简体中文:
本文件记录每个 `obs-char-*` ID 的分配原因。目前尚未从暂存数据中正式
分配单字 ID。

`005_hust-obc-validation-class-staging.csv` 中的 `obs-cand-*` 只是暂存
ID。它们不占用正式 `obs-char-*` 身份，只用于让已下载的 HUST-OBC
metadata 可以被复核和追溯。

`006_obimd-main-character-staging.csv` 中的 `obimd-main-cand-*` 只是
暂存 ID。它们保留 OBIMD UID metadata，必须经过交叉复核后才能分配
正式项目甲骨字 ID。

`009_hust-obc-obs-char-promotion-review-queue.csv` 中列出的
`obs-char-*` 值只是保留建议。它们不是正式分配；只有跨来源复核形成
已接受记录后，才能写入 `001_all-oracle-characters-index.csv`。

`000_hust-obc-promotion-bucket-manifest.csv` 文件是同一 HUST-OBC 提升
复核队列的分桶切片。它们不创建单字记录，也不改变正式 ID 分配状态。
