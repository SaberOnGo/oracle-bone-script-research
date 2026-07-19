# Source Registers / 来源登记表

English:
This directory records authoritative or research-grade source systems before any oracle bone data is imported. The first stage prioritizes official institutional databases, museum/library systems, peer-reviewed datasets, and project pages maintained by named research teams.

Do not add general news sites, entertainment sites, unsourced popular articles, or unaudited hobbyist collections as adopted sources. If such a site appears in a scholarly dataset's provenance, mark it as `source_under_review` and cross-check it against stronger sources before using it.

简体中文：
本目录在导入甲骨文资料前先登记权威或研究级来源系统。第一阶段优先采纳官方机构数据库、博物馆/图书馆系统、同行评审数据集，以及由明确研究团队维护的项目页面。

不要把一般新闻网站、娱乐网站、无来源科普文章或未经审计的民间整理站作为正式采纳来源。如果某类网站出现在学术数据集的来源链中，应标记为 `source_under_review`，并先与更强来源交叉核验。

## Files / 文件

- `001_all-sources-index.csv`: adopted and candidate source systems.
- `001_all-sources-index.csv`：已采纳和候选来源系统。
- `002_authoritative-online-source-inventory.csv`: authority tier and first-stage action.
- `002_authoritative-online-source-inventory.csv`：权威等级和第一阶段动作。
- `003_source-download-manifest.csv`: approved lightweight source pages for logged download.
- `003_source-download-manifest.csv`：批准进行日志化下载的轻量来源页面。
- `004_first-stage-source-adoption-notes.md`: human-readable adoption decision notes.
- `004_first-stage-source-adoption-notes.md`：人类可读的来源采纳决策说明。
- `005_open-oracle-strategy-review.md`: reviewed strategy note for Open-Oracle as a project index.
- `005_open-oracle-strategy-review.md`：Open-Oracle 作为项目索引的方法评审说明。
- `006_authoritative-source-expansion-notes.md`: second-pass professional source expansion notes.
- `006_authoritative-source-expansion-notes.md`：第二轮专业来源扩展说明。
- `007_source-field-map.csv`: source-to-project field map for import planning.
- `007_source-field-map.csv`：用于导入规划的来源字段到本项目字段映射。
- `008_first-stage-import-readiness-notes.md`: first-stage import readiness decisions.
- `008_first-stage-import-readiness-notes.md`：第一阶段导入准备决策说明。
- `009_source-package-file-manifest.csv`: file-level manifest for raw packages and small metadata files.
- `009_source-package-file-manifest.csv`：原始包和小型 metadata 文件的文件级清单。
- `010_downloaded-metadata-profile.csv`: reviewed profile metrics extracted from downloaded small metadata.
- `010_downloaded-metadata-profile.csv`：从已下载小型 metadata 中抽取的已复核概要指标。
- `011_core-institutional-access-profile.csv`: official field, scale, and access-boundary profile for core institutional sources.
- `011_core-institutional-access-profile.csv`：核心机构来源的官方字段、规模和访问边界 profile。
- `012_obm-abbreviation-staging.csv`: browser-reviewed OBM appendix abbreviation staging for old catalog books and rubbing/holding sources.
- `012_obm-abbreviation-staging.csv`：经浏览器复核的 OBM 附录简称暂存表，用于旧著录书和拓本/现藏来源简称。
- `013_source-download-status-codebook.csv`: status semantics for source-download logs, including successful payloads, access-restricted pages, client challenges, download errors, HTTP errors, and size-limit skips.
- `013_source-download-status-codebook.csv`：来源下载日志状态语义表，覆盖成功下载、访问限制页、客户端挑战、下载错误、HTTP 错误和尺寸限制跳过。

Derived staging indexes built from logged downloads are stored in their subject corpus areas, not in this source-register directory. For example, EVOBC evolution-chain metadata is staged under `corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/`.

`014_browser-verified-metadata-capture.csv` records controlled-browser metadata
observations without treating them as downloaded page payloads or
checksum-backed source content.

## Human Research Reading Order / 人类研究阅读顺序

This register supports a human research file, not a route-only inventory.
Read the source object together with the actual glyph image, rubbing,
inscription, catalog, provenance, and bibliography evidence.

本目录服务于人类研究档案，不是只有访问路线的清单。应把来源对象与
字形图片、拓片、卜辞、著录、出处和书目证据放在一起阅读。

### Human Research Slots / 人类研究槽位

- Glyph image and rubbing: which image or rubbing can a researcher open?
  字形图片与拓片：研究者能够打开并核查哪一份实物图像或拓片？
- Meaning or reading: what reading history is recorded, and who proposed it?
  释义与释读：已有何种释读史，提出者是谁，哪些意见仍有争议？
- Components and relations: which components, variants, or near forms are
  recorded as candidates rather than confirmed identity?
  构件与关系：哪些构件、异体或近形只是候选关系，尚未确认？
- Inscription and catalog: which full text, OCR, plate, catalog number, or
  Heji reference can be checked against the source?
  卜辞与著录：哪一份全文、OCR、图版、著录号或合集号可以回查？
- Excavation and provenance: what findspot, collection, period, or batch is
  directly evidenced, and what remains to be checked?
  出土与出处：出土地、馆藏、时期或批次哪些有直接证据，哪些待查？
- Scholarship and dispute: which bibliography, citation relation, proposer,
  different opinion, or dispute record must be preserved?
  学术与争议：哪些书目、引用关系、提出者、不同意见或争议记录必须保留？
- Next check: what concrete source page, scan, image, or catalog leaf should
  a human researcher open next?
  下一步核查：研究者下一次应打开哪一个具体网页、扫描件、图像或著录页？

These slots are preparation-stage research prompts. They do not establish a
confirmed reading, component assignment, inscription identity, or decipherment.
这些槽位只是预处理阶段的研究问题，不构成已确认释读、构件归属、
卜辞身份或破译结论。

从已登记下载文件生成的派生暂存索引放在对应主题语料区，而不是放在本来源登记目录中。例如，EVOBC 字形演化 metadata 暂存在 `corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/`。
