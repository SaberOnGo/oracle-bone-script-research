# Source Rights And Provenance Policy / 来源权利与出处政策

English:
External oracle bone images, scans, paper PDFs, large image sets, and research corpora may be downloaded or committed when they are necessary for research. Because oracle bone materials are scarce, the project should preserve useful source trails instead of discarding material too aggressively.

Every committed item should answer: where did it come from, what external ID identifies it, what rights status is known, what redistribution risk exists, and who reviewed it.

`SIZE_LIMIT` is 30 MiB per file. Downloaded or committed source materials should stay under this limit. If a file exceeds `SIZE_LIMIT`, record an exception and first consider splitting the file, extracting the useful records, downsampling oversized images, or using a more efficient archival format. Files at or above 40 MiB must not be committed to regular Git.

Large but important source packages should be registered in `project_registry/006_large-source-register/` instead of being discarded. Keep the raw package in ignored local storage or an external archive, then commit only provenance records, checksums, extraction notes, and reviewed derived records that fit the repository limits.

AI Agent temporary downloads, OCR intermediates, caches, vector indexes, unpacked archives, and generated experiment outputs must stay in ignored temporary directories such as `tmp/`, `_tmp/`, `scratch/`, `.working/`, or `.cache/`.

简体中文：
研究需要时，本仓库可以下载或提交外部甲骨图片、扫描件、论文 PDF、大规模图片集和研究语料。甲骨文材料本来就稀缺，项目不应因为过度保守而轻易丢失可追溯资料链。

每个提交的资料项都应回答：资料来自哪里、对应哪个外部 ID、已知权利状态是什么、再分发风险是什么、由谁复核过。

`SIZE_LIMIT` 设为单文件 30 MiB。下载或提交的来源材料原则上应低于这个限制。如果文件超过 `SIZE_LIMIT`，必须登记特例，并优先考虑分包、抽取有用记录、对超大图片降采样，或改用更高效的归档格式。达到或超过 40 MiB 的文件不得提交到普通 Git。

超过限制但重要的来源包不应被丢弃，而应登记到 `project_registry/006_large-source-register/`。原始包放在已忽略的本地存储或外部归档中，仓库只提交出处记录、校验和、抽取说明和符合尺寸限制的复核后派生记录。

AI Agent 临时下载、OCR 中间产物、缓存、向量索引、解压目录和实验生成产物必须放在 `tmp/`、`_tmp/`、`scratch/`、`.working/` 或 `.cache/` 等已忽略临时目录。

## Rights Status Values / 权利状态值

- `source_marked_risk_noted`: raw material may be present, with source provenance and risk note.
- `source_marked_risk_noted`：可保存原始材料，但必须标注来源和风险提示。
- `metadata_only_until_verified`: metadata and references are public; raw material is not included yet.
- `metadata_only_until_verified`：公开 metadata 和引用，暂不包含原始材料。
- `public_domain_verified`: source is verified public domain.
- `public_domain_verified`：来源已确认公版。
- `licensed_for_repository`: source is licensed for repository use.
- `licensed_for_repository`：来源已授权本仓库使用。
- `local_private_only`: may only be stored locally and must not be pushed.
- `local_private_only`：只能本地保存，不得推送。
