# Source Provenance Fact Matrix / 来源追溯事实矩阵

This human matrix gives a fast review path for the required provenance facts
before any source material is reused.

本矩阵把来源对象必须核查的出处事实集中在同一页，供研究者在复用任何材料前快速打开、核对和记录缺口。

## Human Review Order / 人工复核顺序
- Open `12_source-provenance-fact-matrix.md` first.
- Then open `10_source-evidence-dossier.md` for route detail.
- Use `13_source-provenance-fact-matrix-index.json` only as an index.
- Then use structured route files only as supporting route evidence.
- Do not treat this matrix as a rights or scholarship decision.
- 先读本矩阵，再读来源证据档案。
- 结构化路线文件只作辅助路线证据。
- 本矩阵不作权利结论，也不作学术结论。

## Source / 来源
- Source ID / 来源 ID: src-nlc-oracle-world
- Title / 题名: 甲骨世界 / Oracle Bones Database
- Rights status / 权利状态: metadata_only_until_verified
- Review status / 复核状态: reviewed

## Provenance Fact Matrix / 出处事实矩阵

### Fact 01: Source identity / 来源身份
- Status / 状态: present
- Evidence files / 证据文件: 01_source-packet.json; 10_source-evidence-dossier.md
- Next check / 下一步核查: Check source_id, title, provider, URL, scope, and
  authority tier.

### Fact 02: Access or download record / 访问或下载记录
- Status / 状态: present
- Evidence files / 证据文件: 02_download-route-index.csv
- Next check / 下一步核查: Check URL, access status, HTTP status, and local route
  notes.

### Fact 03: Checksum evidence / 校验和证据
- Status / 状态: present
- Evidence files / 证据文件: 02_download-route-index.csv
- Next check / 下一步核查: Confirm SHA-256 rows before reusing any downloaded file.

### Fact 04: File size evidence / 文件大小证据
- Status / 状态: present
- Evidence files / 证据文件: 02_download-route-index.csv; 03_package-route-index.csv
- Next check / 下一步核查: Compare download sizes with package manifest file sizes.

### Fact 05: Rights status / 权利状态
- Status / 状态: present
- Evidence files / 证据文件: 01_source-packet.json; 03_package-route-index.csv
- Next check / 下一步核查: Treat rights status as a review note, not a license grant.

### Fact 06: Risk note / 风险提示
- Status / 状态: present
- Evidence files / 证据文件: 01_source-packet.json; 07_material-access-index.md
- Next check / 下一步核查: Keep the visible risk note beside any future derivative.

### Fact 07: Package manifest / 来源包清单
- Status / 状态: present
- Evidence files / 证据文件: 03_package-route-index.csv
- Next check / 下一步核查: Open package rows before treating files as reusable
  derivatives.

### Fact 08: Field map / 字段映射
- Status / 状态: present
- Evidence files / 证据文件: 04_field-map-route-index.csv
- Next check / 下一步核查: Review source fields before moving data into corpus
  objects.

### Fact 09: Derived paths / 派生路径
- Status / 状态: present
- Evidence files / 证据文件: 06_human-source-review-sheet.md;
  07_material-access-index.md; 08_source-processing-status.md;
  10_source-evidence-dossier.md; 05_metadata-profile-route-index.csv
- Next check / 下一步核查: Open human files first, then use structured support
  indexes only as routes.

### Fact 10: Review status / 复核状态
- Status / 状态: present
- Evidence files / 证据文件: 01_source-packet.json; 08_source-processing-status.md
- Next check / 下一步核查: Record unresolved items as concrete human follow-up
  questions.

## Human Research Slots / 人类研究槽位
Glyph image and rubbing slot: check whether this source has a visible glyph
image, rubbing, photograph, or plate image that can later support a concrete
character dossier.

Inscription and catalog slot: check inscription text, OCR, plate number, catalog
number, Heji number, page, and text quality before linking forms to
inscriptions.

Provenance slot: check findspot, collection, museum object, period, group,
batch, and excavation note before using the source for archaeological context.

Relation slot: treat variant, near-form, component, bronze, seal,
modern-character, and evolution relations as candidate comparison evidence until
reviewed.

Scholarship slot: keep bibliography, proposer, editor, citation relation,
disagreement, dispute, and scope limits visible beside later human notes.

字形图像槽：核查本来源是否有字形图像、拓片、照片或图版。
卜辞著录槽：核查卜辞全文、OCR、图版号、著录号、合集号、页码和文本质量。
出土背景槽：核查出土地、馆藏、博物馆对象、时期、组类、批次和考古记录。
关系比较槽：异体、近形、构件、金文、小篆、今字和演化关系只能作为候选比较证据。
学术争议槽：保留书目、提出者、整理者、引用关系、不同意见、争议和适用范围限制。

## Concrete Next Checks / 具体待查问题
- Which access or download rows have dates, sizes, and checksums?
- Which package manifest rows describe reusable derived records?
- Which field maps can safely feed concrete corpus directories?
- Which rights or redistribution risk blocks public promotion?
- Which derived files should a human reviewer open first?
- 哪些访问或下载记录已有日期、大小和 checksum？
- 哪些来源包 manifest 行说明了可复核派生记录？
- 哪些字段映射可以安全进入具体语料对象目录？
- 哪些权利或再分发风险阻止公开提升？
- 人工复核者应先打开哪些派生文件？

## Boundary / 边界
- not a rights decision
- not corpus import approval
- not a confirmed source promotion
- not a reading
- not a component assignment
- not an inscription identity
- not a decipherment conclusion
- 不是权利结论
- 不是语料导入批准
- 不是来源提升结论
- 不是释读、构件归属、卜辞身份或破译结论
