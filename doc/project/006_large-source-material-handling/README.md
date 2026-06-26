# Large Source Material Handling / 大型来源资料处理

English:
Large source material includes database exports, scan sets, PDF collections,
image archives, OCR packages, and research datasets. A large source package may
be essential evidence, but regular Git must not become raw storage.

简体中文：
大型来源资料包括数据库导出、扫描集合、PDF 集合、图片包、OCR 包和
研究数据集。大型 source package 可能是重要证据，但普通 Git 不能
变成原始资料仓库。

## Human Review Entry Order / 人工复核入口顺序

English:
Review a large source in this order:

1. Open `project_registry/006_large-source-register/` first.
2. Confirm the source package id, provider, access method, and storage hint.
3. Check file size, checksum, rights status, risk note, and review status.
4. Open package manifests, field maps, and extraction notes if they exist.
5. Inspect reviewed derived records before any corpus or graph import.
6. Record missing evidence as concrete next checks.

简体中文：
复核大型来源资料时，先打开大型来源登记，确认来源包 ID、提供方、
访问方式和存放线索，再核对大小、checksum、权利状态、风险提示和
复核状态。导入 corpus 或图谱前，先查看已复核派生记录。

## Rule / 规则

English:
The repository `SIZE_LIMIT` is 30 MiB per file. Files above that limit need a
recorded exception. Files at or above 40 MiB must not be committed to regular
Git. Important oversized sources should be kept in ignored local storage or an
approved external archive, with auditable manifests and reviewed derivatives
in Git.

简体中文：
本仓库 `SIZE_LIMIT` 为单文件 30 MiB。超过此限制的文件必须登记例外。
达到或超过 40 MiB 的文件不得提交到普通 Git。重要超大来源应保存在
已忽略本地存储或获批准的外部归档中，Git 中只保留可审计 manifest
和已复核派生记录。

## Concrete Questions To Check / 具体待查问题

- Which registered source package is being used?
- Where are its download or access record and checksum?
- What is the rights status, risk note, and allowed research use?
- Is the raw package outside regular Git, or is an exception recorded?
- Which manifest lists files extracted from the package?
- Which field map explains CSV, JSON, HTML, OCR, PDF, or image fields?
- Which reviewed derived records can a human researcher open directly?
- Which missing pages, images, fields, or permissions still need review?
- 使用的是哪一个已登记 source package？
- 它的下载或访问记录和 checksum 在哪里？
- 权利状态、风险提示和允许的研究用途是什么？
- 原始包是否在普通 Git 外部，或是否已有例外登记？
- 哪个 manifest 列出从来源包抽取的文件？
- 哪个字段映射解释 CSV、JSON、HTML、OCR、PDF 或图片字段？
- 哪些已复核派生记录可以被人类研究者直接打开？
- 哪些页码、图像、字段或许可仍需复核？

## Derived Records / 派生记录

English:
Prefer reviewed derived records over raw packages in Git. Useful derivatives
include bibliographic rows, page indexes, OCR text within rights limits,
object-local image routes, character or inscription staging rows, source field
maps, graph edges, statistics, and human review sheets. Each derivative must
point back to its source package, manifest row, checksum, and review status.

简体中文：
Git 中优先保存已复核派生记录，而不是原始大包。可提交的派生记录包括
书目行、页码索引、权利允许范围内的 OCR 文本、对象内图片路线、单字
或卜辞暂存行、来源字段映射、图谱边、统计和人工复核表。每个派生
记录都必须能追溯到 source package、manifest 行、checksum 和复核
状态。

## Strategies By Material Type / 按资料类型建议

- Database exports: keep schema, field map, sample rows, and checksums.
- PDF or scan sets: keep bibliography, page index, legal OCR, and routes.
- Image archives: keep selected review images or thumbnails under the limit.
- Website exports: keep crawl manifest, URL list, and normalized records.
- AI intermediates: keep caches and vector indexes in ignored storage.
- 数据库导出：保留 schema、字段映射、样例行和 checksum。
- PDF 或扫描集合：保留书目、页码索引、合法 OCR 和路线。
- 图片包：保留低于限制的精选复核图像或缩略图。
- 网站导出：保留 crawl manifest、URL 列表和规范化记录。
- AI 中间产物：cache 和向量索引应留在已忽略存储区。

## Research Boundary / 研究边界

English:
Large-source registration proves that a source trail exists. It is
not a decipherment conclusion. It is not a component assignment,
inscription identity claim, or accepted paleographic correspondence.

简体中文：
大型来源登记只能证明存在来源链。它不是释读结论，不是构件归属结论，
不是卜辞或馆藏对象同一性结论，也不是已接受的古文字对应。
