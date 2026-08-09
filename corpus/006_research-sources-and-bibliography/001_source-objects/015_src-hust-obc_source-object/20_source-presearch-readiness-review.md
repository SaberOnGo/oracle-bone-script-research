# Source Pre-Research Readiness Review / 来源预研究就绪复核

## English
This human review page tells a researcher what this source object can support
before formal oracle-bone research begins. It gathers the visible source
identity, access evidence, package and field maps, transfer routes, literature
scope, rights boundary, and concrete missing questions in one readable place.

## 简体中文
本页说明正式甲骨文研究开始前，这个来源对象目前能够支持哪些人工核查。它把来源身份、访问证据、来源包和字段映射、转入档案路线、文献范围、权利边界和具体缺失问题集中
到一个人类可读页面。

## Source / 来源
- Source ID / 来源 ID: src-hust-obc
- Title / 题名: HUST-OBC: An open dataset for oracle bone character recognition
  and decipherment
- Provider / 提供方: Huazhong University of Science and Technology research team /
  Scientific Data
- Source type / 来源类型: open_research_dataset
- Scope / 适用范围: Scientific Data dataset with 77064 images of 1588 deciphered
  characters and 62989 images of 9411 undeciphered characters; total 140053
  images.
- Rights status / 权利状态: source_marked_risk_noted
- Risk note / 风险提示: Dataset is directly relevant to 1500+ deciphered and
  undeciphered characters, but raw images are large, non-commercially licensed
  and compiled from diverse sources including an unreliable GuoXueDaShi split.
- Review status / 复核状态: reviewed

## Human Reading Order / 人工阅读顺序
- Read `README.md` and `10_source-evidence-dossier.md` first.
- Check `12_source-provenance-fact-matrix.md` for source facts.
- Check `14_source-to-dossier-transfer-review.md` before transfer.
- Check `16_source-literature-scope-review.md` for scope and disputes.
- Check `18_source-access-integrity-review.md` before reuse.
- Use JSON and CSV only after the human files are clear.
- 先读 `README.md` 和 `10_source-evidence-dossier.md`。
- 再读 `12_source-provenance-fact-matrix.md` 核对来源事实。
- 转入对象档案前先读 `14_source-to-dossier-transfer-review.md`。
- 通过 `16_source-literature-scope-review.md` 核对范围和争议。
- 复用资料前先读 `18_source-access-integrity-review.md`。
- JSON 和 CSV 只能在人类文件清楚之后作为辅助资料使用。

## Readiness Slots / 就绪复核槽位

### 01. visible_source_identity
- Status / 状态: route_present
- Evidence / 证据文件: README.md; 10_source-evidence-dossier.md
- Question / 待查问题: Which source system, title, provider, URL, scope, and
  authority tier can a reviewer cite before opening data rows?

### 02. access_checksum_size
- Status / 状态: needs_human_review
- Evidence / 证据文件: 02_download-route-index.csv;
  18_source-access-integrity-review.md
- Question / 待查问题: Which access or download row has status downloaded; which
  checksum and size rows are ready for audit?

### 03. package_and_field_map
- Status / 状态: needs_human_review
- Evidence / 证据文件: 03_package-route-index.csv; 04_field-map-route-index.csv
- Question / 待查问题: Which package, manifest, and field-map rows can support
  asset_metadata; oracle_character without becoming claims?

### 04. human_dossier_transfer
- Status / 状态: needs_target_dossier_review
- Evidence / 证据文件: 14_source-to-dossier-transfer-review.md
- Question / 待查问题: Which character, inscription, plate, collection, later-form,
  or bibliography dossier can receive only a reviewed route?

### 05. literature_and_dispute_scope
- Status / 状态: needs_human_literature_review
- Evidence / 证据文件: 16_source-literature-scope-review.md
- Question / 待查问题: Which bibliography, database note, proposer, editor, citation
  relation, different opinion, or dispute remains to be opened?

### 06. rights_risk_public_commit
- Status / 状态: needs_rights_boundary_review
- Evidence / 证据文件: 12_source-provenance-fact-matrix.md;
  18_source-access-integrity-review.md
- Question / 待查问题: Which rights status, risk note, size limit, checksum, and
  commit-policy issue blocks public promotion?

### 07. concrete_missing_questions
- Status / 状态: needs_followup_before_formal_research
- Evidence / 证据文件: 20_source-presearch-readiness-review.md
- Question / 待查问题: which human reviewer can close remaining route checks

## Concrete Questions Before Formal Research / 正式研究前待查问题
- Which visible image, rubbing, plate, catalog, or URL is evidence?
- Which checksum, file size, package row, or field map proves it?
- Which target dossier can receive a route without receiving a claim?
- Which bibliography, proposer, alternate view, or dispute is open?
- Which rights, risk, size, or commit-policy issue blocks reuse?
- 哪个图片、拓片、图版、著录或 URL 是可见证据？
- 哪条 checksum、文件大小、来源包或字段映射记录能证明它？
- 哪个目标档案只能接收路线，而不能接收结论？
- 哪条书目、提出者、不同意见或争议仍需打开？
- 哪个权利、风险、大小或提交策略问题阻止复用？

## Boundary / 边界
- not a rights decision
- not corpus import approval
- not a confirmed source promotion
- not an accepted reading
- not a component assignment
- not an inscription identity
- not a correspondence conclusion
- not a decipherment conclusion
- 不是权利结论
- 不是语料导入批准
- 不是来源提升结论
- 不是已接受释读
- 不是构件归属
- 不是卜辞身份确认
- 不是字形对应结论
- 不是破译结论

## Object-Level Visual Review Checkpoint / 对象级图像复核检查点

The current visual audit records `6595` objects with direct visual
observations and `4401` objects with a local derivative but no direct
observation. These are coverage facts, not identity or reading decisions.

当前图像审计记录 `6595` 个对象已有直接视觉观察，另有 `4401` 个对象只有
本地派生件而没有直接观察。这些只是覆盖事实，不是字形身份或释读结论。

Concrete follow-up questions / 具体待查问题：

- Which remaining image route, package member, plate, catalogue, or collection
  record should be opened next?
- Which full inscription, OCR, neighboring sign, or excavation record can be
  cited for that image?
- Which rights statement and checksum govern the derivative and its reuse?
- 下一条应打开哪幅图像、包内文件、图版、著录或馆藏路线？
- 哪条完整卜辞、OCR、邻字或出土记录可以引用？
- 派生件适用哪条权利说明和 checksum，公开复用边界是什么？

Evidence path / 证据路径:
`corpus/009_statistics-and-derived-features/226_character-visual-
observation-coverage-audit.md`
