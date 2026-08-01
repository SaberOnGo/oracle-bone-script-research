# External Package Integrity Review / 外部来源包完整性复核

This page records integrity evidence for raw OBIMD packages kept outside
regular Git. It records download identity and archive structure only; it does
not approve extraction, corpus import, character identity, or reading.

本页记录普通 Git 之外保存的 OBIMD 原始来源包完整性证据。它只记录下载身份
和归档结构，不批准抽取、语料导入、字形身份或释读。

## Review Boundary / 复核边界

- Raw packages remain in `external_local_archive/source_packages/obimd/`.
- No bulk image extraction has been committed to the repository.
- ZIP member names are source-package evidence, not catalog or plate identity.
- 原始包仍保存在上述外部归档目录。
- 未将批量图像抽取件提交到仓库。
- ZIP 成员名只是来源包证据，不是著录或图版身份。

## Integrity Records / 完整性记录

### data.json

- Download ID / 下载 ID: `dl-obimd-data-json`
- Size / 大小: 41,732,948 bytes
- SHA-256: `b504b0d4e7a0126d494c161f5445c5ee4225659ff5e94182685fce35d261aa19`
- External path / 外部路径: `external_local_archive/source_packages/obimd/data.json`
- JSON check / JSON 检查: top-level list, 10,077 items
- Integrity status / 完整性状态: parsed successfully; raw records only

### facsimile.zip

- Download ID / 下载 ID: `dl-obimd-facsimile`
- Size / 大小: 210,800,641 bytes
- SHA-256: `b1544e34ee1a6a34fc0a83475a227fd2141a67293f795eaa3c52760fedb50b0e`
- External path / 外部路径:
  `external_local_archive/source_packages/obimd/facsimile.zip`
- ZIP check / ZIP 检查: `testzip()` returned no bad member
- Member count / 成员数: 10,078, including `facsimile/`
- Integrity status / 完整性状态: downloaded and ZIP-verified

### rubbing.zip

- Download ID / 下载 ID: `dl-obimd-rubbing`
- Size / 大小: 558,367,972 bytes
- SHA-256: `4d07dca94e94c2d17edd7fa25be72b5673161c0c2d03dac4d2c094e5341b7747`
- External path / 外部路径:
  `external_local_archive/source_packages/obimd/rubbing.zip`
- ZIP check / ZIP 检查: `testzip()` returned no bad member
- Member count / 成员数: 10,078, including `rubbing/`
- Integrity status / 完整性状态: downloaded and ZIP-verified

## Handling Decision / 处理决定

The three raw packages exceed `SIZE_LIMIT` and remain external. The repository
stores route rows, checksums, sizes, package IDs, ZIP or JSON checks, and this
human review page. It does not store the raw package bytes or infer a reading.

三个原始包都超过 `SIZE_LIMIT`，继续保存在外部归档。仓库只保存路线、checksum、
大小、包 ID、ZIP 或 JSON 检查结果和本页人工记录，不保存原始大包，也不推断释读。

## Research Slots / 人类研究槽位

- Component marks remain candidate observations until a human compares them.
- Scholarship, bibliography, proposer, and dispute routes remain to be opened.
- Variant, near-form, and other relations remain candidate source relations.
- 构件痕迹在人工比较前仍只是候选观察。
- 学术、书目、提出者和争议路线仍需打开核查。
- 异体、近形和其他关系仍只是候选来源关系。

## Concrete Next Checks / 具体待查问题

- Which image members match a reviewed object UID and source row?
- Which catalog, plate, collection, findspot, and period record can be cited?
- Which rights wording governs a selected derivative?
- Which OCR, inscription, or neighboring-sign context is available?
- 哪些图像成员与已复核对象 UID 和来源行相符？
- 哪条著录、图版、馆藏、出土地和时期记录可以引用？
- 选定派生件适用哪一版权利说明？
- 哪条 OCR、卜辞或邻字语境可以核查？

## Boundary / 边界

- not a rights decision
- not extraction approval
- not corpus import approval
- not a confirmed character identity
- not an accepted reading
- not a decipherment conclusion
- 不是权利结论
- 不是抽取批准
- 不是语料导入批准
- 不是已确认字形身份
- 不是已接受释读
- 不是破译结论
