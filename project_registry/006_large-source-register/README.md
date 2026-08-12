# Large Source Register / 大型来源登记表

English:
This registry records important source packages that are too large, too
generated, or too risky for direct regular Git storage. It is a human review
entry for provenance, rights, storage, and reviewed derivatives.

简体中文：
本登记表记录过大、生成性太强，或不适合直接进入普通 Git 的重要来源
包。它是人工复核来源链、权利、存放位置和已复核派生记录的入口。

## Human Review Entry Order / 人工复核入口顺序

English:
Review a large source package in this order:

1. Open `001_large-source-register.csv` and find the source package row.
2. Open `002_source-download-log.csv` for access or download evidence.
3. Check size, checksum, rights status, risk note, and storage hint.
4. Follow manifest, field-map, extraction-note, and exception paths.
5. Open reviewed derivatives before trusting any corpus or graph route.
6. Record missing evidence as concrete next checks.

简体中文：
复核大型来源包时，先打开 `001_large-source-register.csv` 找到来源包行，
再打开 `002_source-download-log.csv` 核查访问或下载证据。随后核对大小、
checksum、rights status、risk note 和存放线索，并追踪 manifest、字段
映射、抽取说明和例外登记路径。

## Files / 文件

- `001_large-source-register.csv` records source packages and storage trails.
- `002_source-download-log.csv` records access/download status and checksums.
- `001_large-source-register.csv` 记录来源包和存放链路。
- `002_source-download-log.csv` 记录访问/下载状态和 checksum。

## Concrete Questions To Check / 具体待查问题

- Which source package id and source object does this row support?
- Where is the access or download record?
- Is the checksum present and tied to the correct package?
- What are the rights status, risk note, and allowed review use?
- Is the raw package outside regular Git, or is an exception recorded?
- Which package manifest or file list proves what was extracted?
- Which reviewed derivatives can a human researcher open directly?
- Which missing files, fields, licenses, or review steps remain?
- 该行支持哪个 source package id 和来源对象？
- 访问或下载记录在哪里？
- checksum 是否存在，并且对应正确来源包？
- rights status、risk note 和允许的复核用途是什么？
- 原始包是否在普通 Git 外部，或是否已有例外登记？
- 哪个 package manifest 或文件清单证明抽取了什么？
- 哪些已复核派生记录可以被人类研究者直接打开？
- 还缺哪些文件、字段、许可或复核步骤？

## Required Evidence / 必需证据

English:
Each large-source record should preserve source id, source name, access route,
local or external storage hint, expected size, checksum, rights status, risk
note, reviewed derivatives, and review status. Reviewed derivatives may
include metadata rows, field maps, OCR text, image routes, object-local review
sheets, graph edges, statistics, or bibliography records.

简体中文：
每条大型来源记录应保留来源 ID、来源名称、访问路径、本地或外部存放
线索、预期大小、checksum、rights status、risk note、已复核派生记录
和复核状态。已复核派生记录可以包括 metadata 行、字段映射、OCR 文本、
图像路线、对象内复核表、图谱边、统计或书目记录。

## Package Scope And File Snapshots / 来源包范围与分文件快照

English:
`large-src-000003` records an EVOBC unified/raw-image package scope that has
not been identified or downloaded. It does not mean that no EVOBC material
was accessed. The download log separately records five downloaded snapshots:
the arXiv abstract page, repository README, two JSON files, and one workbook.
Three dataset-file snapshots are also linked through the package-file
manifest. Those individual files do not prove acquisition of a unified raw
image package.

简体中文：
`large-src-000003` 登记的是尚未识别、尚未下载的 EVOBC 统一原始图像包
范围，并不表示从未访问任何 EVOBC 资料。下载日志另行记录了 5 个已下载
快照：arXiv 摘要页、仓库 README、两个 JSON 文件和一个工作簿。其中 3 个
数据文件快照也通过来源包文件清单关联。单独取得这些文件，不能证明已经
取得统一原始图像包。

## Research Boundary / 研究边界

English:
Large-source registration preserves a source trail. It is not permission to
commit oversized raw files to regular Git. It is not a decipherment conclusion,
not a component assignment, not an inscription identity claim, and not an
accepted paleographic correspondence.

简体中文：
大型来源登记保存来源链。它不等于允许把超大原始文件提交到普通 Git。
它不是释读结论，不是构件归属结论，不是卜辞或馆藏对象同一性结论，
也不是已接受的古文字对应。
