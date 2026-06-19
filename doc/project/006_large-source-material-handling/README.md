# Large Source Material Handling / 大型来源资料处理

English:
Some oracle bone script sources are large because they come from professional databases, scans, PDF collections, image archives, OCR packages, or exported research datasets. Large does not mean useless, and the project should not discard important sources only because they exceed `SIZE_LIMIT`.

简体中文：
有些甲骨文来源资料会很大，因为它们来自专业数据库、扫描图、PDF 集合、图片包、OCR 包或研究数据导出。文件大不代表没有价值，项目不能因为超过 `SIZE_LIMIT` 就简单丢弃重要来源。

## Rule / 规则

English:
Preserve the research trail, but do not turn Git history into raw storage. GitHub warns on regular Git files above 50 MiB, blocks files above 100 MiB, recommends Git LFS for large binaries, and recommends storing programmatically generated files outside Git. See GitHub Docs: [About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage), and [Repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits).

简体中文：
保留研究链路，但不要把 Git 历史变成原始资料仓库。GitHub 对普通 Git 文件超过 50 MiB 会警告，超过 100 MiB 会阻止；大二进制文件建议使用 Git LFS，程序生成文件建议放在 Git 外部。参见 GitHub 文档：[About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)、[About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)、[Repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits)。

## Decision Order / 处理顺序

1. Register the source package in `project_registry/006_large-source-register/001_large-source-register.csv`.
2. Keep the raw large package in an ignored local archive, institutional storage, object storage, Git LFS, GitHub Releases, or another external location after project approval. Do not commit it directly to regular Git.
3. Record enough provenance to reproduce or audit it: source URL, provider, access method, download date, file size, checksum, rights status, risk note, and local or external storage hint.
4. Extract useful research content into smaller records: metadata, bibliographic rows, OCR text, page-level image references, character records, inscription records, graph edges, or statistics.
5. Commit only reviewed derived records that are source-marked and under `SIZE_LIMIT`.
6. If a raw file is between 30 MiB and 40 MiB and must be committed, add it to `project_registry/004_asset-source-and-rights-index/003_size-limit-exceptions.csv` with mitigation and risk notes.
7. If a raw file is 40 MiB or larger, do not commit it to regular Git.

处理顺序：

1. 先在 `project_registry/006_large-source-register/001_large-source-register.csv` 登记来源包。
2. 原始大包经项目批准后放在已忽略的本地归档、机构存储、对象存储、Git LFS、GitHub Releases 或其他外部位置，不要直接提交到普通 Git。
3. 记录足够复现和审计的信息：来源 URL、提供方、访问方式、下载日期、文件大小、checksum、权利状态、风险提示、本地或外部存放线索。
4. 把有研究价值的内容抽取成更小的记录：metadata、书目行、OCR 文本、页级图片引用、甲骨字记录、卜辞记录、图谱边或统计结果。
5. 只提交经过复核、标注来源且低于 `SIZE_LIMIT` 的派生记录。
6. 如果原始文件在 30 MiB 到 40 MiB 之间且确实必须提交，写入 `project_registry/004_asset-source-and-rights-index/003_size-limit-exceptions.csv`，并记录缓解方式和风险提示。
7. 如果原始文件达到或超过 40 MiB，不得提交到普通 Git。

## Strategies By Material Type / 按资料类型建议

- Database dumps: commit schema, field map, sample rows, import notes, checksum, and split extracted tables; keep the raw dump outside Git.
- 数据库导出：提交 schema、字段映射、样例行、导入说明、checksum 和拆分后的抽取表；原始 dump 放在 Git 外部。
- PDF or scan collections: commit bibliographic metadata, page index, lawful OCR text, small extracted images when needed, and source references; keep full scans outside Git unless rights and size allow.
- PDF 或扫描集合：提交书目 metadata、页码索引、合法范围内的 OCR 文本、必要小图和来源引用；全文扫描除非权利和尺寸都允许，否则放在 Git 外部。
- Image archives: commit thumbnails or individual useful images under `SIZE_LIMIT`; keep high-resolution originals outside Git and record checksums.
- 图片包：提交缩略图或低于 `SIZE_LIMIT` 的必要单图；高清原图放在 Git 外部并登记 checksum。
- Website exports: commit crawl manifest, URL list, extraction script notes, and normalized records; keep raw crawl caches in ignored temporary or external storage.
- 网站导出：提交 crawl manifest、URL 列表、抽取脚本说明和规范化记录；原始抓取缓存放在已忽略临时区或外部存储。
- AI-generated intermediates: keep embeddings, OCR caches, vector indexes, model outputs, and unpacked archives in ignored temporary directories unless a reviewed small derivative is intentionally promoted.
- AI 中间产物：embedding、OCR cache、向量索引、模型输出和解压目录默认放在已忽略临时目录；只有经过复核的小型派生结果才可以提升为正式记录。

## Boundary / 边界

English:
Large-source registration proves that a source trail exists. It does not prove that a reading, component assignment, inscription identity, or correspondence is correct.

简体中文：
大型来源登记只能证明存在来源链，不证明某个释读、构件归属、卜辞身份或字形对应是正确的。
