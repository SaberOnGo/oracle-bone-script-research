# Source Rights And Provenance Policy / 来源权利与出处政策

English:
This policy tells reviewers how to keep source provenance, rights status, risk
note, size evidence, checksum, and review status beside each source material
before formal oracle-bone research begins.

简体中文：
本政策说明正式甲骨文研究开始前，如何把来源系统、出处链、权利状态、
风险提示、大小证据、checksum 和复核状态放在每项资料旁边，供人类
研究者核查。

## Purpose / 用途

English:
The first goal is a human-readable source trail. AI-readable CSV, JSON,
manifest, and graph data only help people search, compare, trace, and audit
that trail.

简体中文：
首要目标是形成给人看的来源追溯链。AI 可读 CSV、JSON、manifest 和
图边只用于帮助研究者检索、比较、追溯和审计。

## Required Provenance / 必需出处信息

English:
Every source item, asset, OCR text, PDF note, image derivative, or database
export should preserve these facts when they are known:

- source provenance and source system;
- external ID, catalog number, page, plate, URL, or object record;
- access route, access date, package name, and provider;
- file name, file size, checksum, and package manifest;
- rights status, risk note, and public-commit decision;
- field map, extraction note, derived paths, and review status.

简体中文：
每项来源资料、资产、OCR 文本、PDF 笔记、图片派生件或数据库导出，
在可知时都应保留下列信息：

- 来源出处和来源系统；
- 外部 ID、著录号、页码、图版号、URL 或馆藏对象记录；
- 访问路线、访问日期、来源包名称和提供方；
- 文件名、文件大小、checksum 和 package manifest；
- 权利状态、风险提示和是否公开提交的决定；
- 字段映射、抽取说明、派生路径和复核状态。

## Rights And Risk Status / 权利与风险状态

English:
Rights status records what is known about reuse. It is not a license grant
unless a reviewed license says so. A visible risk note must explain why the
material is safe enough for public metadata, public small derivatives,
metadata-only routing, or local-private storage.

Allowed status values include:

- `source_marked_risk_noted`;
- `metadata_only_until_verified`;
- `public_domain_verified`;
- `licensed_for_repository`;
- `local_private_only`.

简体中文：
权利状态只记录目前知道的复用情况。除非有已复核许可证，否则它不是
授权声明。显式风险提示必须说明资料为何只能公开 metadata、可公开
小型派生件、只保留 metadata 路线，或必须放在本地私有位置。

## Large And Temporary Materials / 大文件与临时材料

English:
`SIZE_LIMIT` is 30 MiB per file. Files at or above 40 MiB must not be
committed to regular Git. Important large packages must be registered in
`project_registry/006_large-source-register/` with storage hints, checksums,
rights notes, risk notes, manifests, and derived paths.

AI Agent scratch files, OCR caches, temporary downloads, unpacked archives,
vector indexes, and experimental outputs must stay in ignored local areas such
as `tmp/`, `_tmp/`, `scratch/`, `.working/`, or `.cache/`.

简体中文：
`SIZE_LIMIT` 是单文件 30 MiB。达到或超过 40 MiB 的文件不得提交到
普通 Git。重要大型来源包必须登记到
`project_registry/006_large-source-register/`，并记录存放线索、
checksum、权利说明、风险提示、manifest 和派生路径。

AI Agent 草稿、OCR 缓存、临时下载、解压目录、向量索引和实验输出
必须留在已忽略的本地区域，例如 `tmp/`、`_tmp/`、`scratch/`、
`.working/` 或 `.cache/`。

## Concrete Questions To Check / 具体待查问题

- Which source system, catalog, museum, paper, book, or URL supplied it?
- Which external ID, page, plate, object record, or package locates it?
- Is the public repository keeping metadata, a small derivative, or raw data?
- What rights status and risk note are visible beside the material?
- Is there a checksum, file size, package manifest, and field map?
- If the package exceeds `SIZE_LIMIT`, where is the raw package registered?
- Which derived paths let a reviewer audit the extraction route?
- What review status remains pending, and who should check it next?
- 哪个来源系统、著录、博物馆、论文、图书或 URL 提供了它？
- 哪个外部 ID、页码、图版号、馆藏对象记录或来源包能定位它？
- 公开仓库保留的是 metadata、小型派生件，还是原始资料？
- 该资料旁边可见的权利状态和风险提示是什么？
- 是否已有 checksum、文件大小、package manifest 和字段映射？
- 如果来源包超过 `SIZE_LIMIT`，原始包登记在哪里？
- 哪些派生路径能让复核者审计抽取路线？
- 还剩什么复核状态待完成，下一步应由谁检查？

## Review Order / 复核顺序

1. Open the human source note or object-local README first.
2. Check the registry row and source ID map.
3. Check the access log, checksum, file size, and package manifest.
4. Check rights status and the visible risk note.
5. Check derived records, field maps, and exception records.
6. Record concrete missing questions instead of empty placeholders.

复核时先读人类可读来源说明或对象内 README，再核对 registry 行、
来源 ID 映射、访问日志、checksum、文件大小、来源包清单、权利状态、
风险提示、派生记录、字段映射和特例记录。缺失项要写成具体待查问题。

## Research Boundary / 研究边界

English:
Source availability, rights status, route metadata, graph edges, staging rows,
and derived indexes are review routes only. They are not scholarship, not
source promotion, not corpus import approval, and not a rights decision.
They are not a decipherment conclusion and do not confirm a reading.

简体中文：
来源可得性、权利状态、路线 metadata、图边、staging 行和派生索引都
只是复核路线。它们不是学术结论，不是来源提升，不是语料导入批准，
不是权利决定，也不是释读结论。
