# Large Source Material Handling / 大型来源资料处理

English:
Some oracle bone script sources are large because they come from professional databases, scans, PDF collections, image archives, OCR packages, or exported research datasets. Large does not mean useless, and the project should not discard important sources only because they exceed `SIZE_LIMIT`.

The repository rule is: preserve the research trail, but do not turn Git history into raw storage. GitHub warns on regular Git files above 50 MiB, blocks files above 100 MiB, recommends Git LFS for large binaries, and recommends storing programmatically generated files outside Git. See GitHub Docs: [About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage), and [Repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits).

Use this decision order:

1. Register the source package in `project_registry/006_large-source-register/001_large-source-register.csv`.
2. Keep the raw large package in an ignored local archive, institutional storage, object storage, or another external location. Do not commit it directly.
3. Record enough provenance to reproduce or audit it: source URL, provider, access method, download date, file size, checksum, rights status, risk note, and local or external storage hint.
4. Extract the useful research content into smaller records: metadata, bibliographic rows, OCR text, page-level image references, character records, inscription records, graph edges, or statistics.
5. Commit only reviewed derived records that are source-marked and under `SIZE_LIMIT`.
6. If a raw file is between 30 MiB and 40 MiB and must be committed, add it to `project_registry/004_asset-source-and-rights-index/003_size-limit-exceptions.csv` with a mitigation and risk note.
7. If a raw file is 40 MiB or larger, do not commit it to regular Git. Use an external archive, Git LFS, or GitHub Releases only after an explicit project decision and provenance review.

Recommended strategies by material type:

- Database dumps: commit schema, field map, sample rows, import notes, checksum, and split extracted tables; keep the raw dump outside Git.
- PDF or scan collections: commit bibliographic metadata, page index, OCR text when lawful, extracted small images when needed, and source references; keep full scans outside Git unless rights and size allow.
- Image archives: commit thumbnails or individual useful images under `SIZE_LIMIT`; keep high-resolution originals outside Git and record checksums.
- Website exports: commit crawl manifest, URL list, extraction script notes, and normalized records; keep raw crawl caches in ignored temporary or external storage.
- AI-generated intermediates: keep embeddings, OCR caches, vector indexes, model outputs, and unpacked archives in ignored temporary directories unless a reviewed small derivative is intentionally promoted.

简体中文：
有些甲骨文来源资料会很大，因为它们来自专业数据库、扫描图、PDF 集合、图片包、OCR 包或研究数据导出。文件大不代表没有价值，项目不能因为超过 `SIZE_LIMIT` 就简单丢掉重要来源。

本仓库规则是：保留研究链路，但不要把 Git 历史变成原始资料仓库。GitHub 对普通 Git 文件超过 50 MiB 会警告，超过 100 MiB 会阻止；大二进制文件建议使用 Git LFS，程序生成文件建议放在 Git 外部。参考 GitHub Docs：[About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)、[About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)、[Repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits)。

处理顺序：

1. 先在 `project_registry/006_large-source-register/001_large-source-register.csv` 登记来源包。
2. 原始大包放在已忽略的本地归档、机构存储、对象存储或其他外部位置，不要直接提交。
3. 记录足够复现和审计的信息：来源 URL、提供方、访问方式、下载日期、文件大小、校验和、权利状态、风险提示、本地或外部存放线索。
4. 把有研究价值的内容抽取成更小的记录：metadata、书目行、OCR 文本、页级图片引用、甲骨字记录、卜辞记录、图谱边或统计结果。
5. 只提交经过复核、标注来源且低于 `SIZE_LIMIT` 的派生记录。
6. 如果原始文件在 30 MiB 到 40 MiB 之间且确实必须提交，写入 `project_registry/004_asset-source-and-rights-index/003_size-limit-exceptions.csv`，并记录缓解方式和风险提示。
7. 如果原始文件达到或超过 40 MiB，不得提交到普通 Git。只有经过明确项目决策和出处复核后，才考虑外部归档、Git LFS 或 GitHub Releases。

按资料类型建议：

- 数据库导出：提交 schema、字段映射、样例行、导入说明、校验和和拆分后的抽取表；原始 dump 放在 Git 外部。
- PDF 或扫描集合：提交书目 metadata、页码索引、合法范围内的 OCR 文本、必要的小图和来源引用；全文扫描除非权利和尺寸都允许，否则放在 Git 外部。
- 图片包：提交缩略图或低于 `SIZE_LIMIT` 的单张必要图片；高清原图放在 Git 外部并登记校验和。
- 网站导出：提交 crawl manifest、URL 列表、抽取脚本说明和规范化记录；原始抓取缓存放在已忽略临时区或外部存储。
- AI 中间产物：embedding、OCR cache、向量索引、模型输出和解压目录默认放在已忽略临时目录；只有经过复核的小型派生结果才可以提升为正式记录。
