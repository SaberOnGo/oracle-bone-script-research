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
- Source ID / 来源 ID: src-obimd
- Title / 题名: OBIMD: Oracle Bone Inscriptions Multi-modal Dataset
- Provider / 提供方: Key Laboratory of Oracle Bone Inscriptions Information
  Processing Anyang Normal University; Xiamen University; Tencent Youtu Lab;
  University of Cambridge; Scientific Data
- Source type / 来源类型: open_research_dataset
- Scope / 适用范围: Multi-modal OBI dataset with 10077 oracle bone images, 93652
  annotated characters, 21941 syntactically validated sentences, and reading
  sequences.
- Rights status / 权利状态: licensed_for_repository
- Risk note / 风险提示: Dataset card reports CC-BY 4.0 while the GitHub README
  includes narrower academic-use wording; raw files remain large and need rights
  review before import.
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
- Question / 待查问题: Which access or download row has status downloaded;
  downloaded_to_external_archive; which checksum and size rows are ready for
  audit?

### 03. package_and_field_map
- Status / 状态: needs_human_review
- Evidence / 证据文件: 03_package-route-index.csv; 04_field-map-route-index.csv
- Question / 待查问题: Which package, manifest, and field-map rows can support
  asset_metadata; oracle_character; oracle_character_occurrence;
  oracle_character_variant; oracle_inscription without becoming claims?

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

The source brief records `10364` committed assets and `2770` object-local
bundles or routes. Four OBIMD component-candidate objects (`002744`–`002747`)
now have opened-image observations in their own directories.

来源简报记录了 `10364` 个已提交资产和 `2770` 个对象内资料包或路线。
目前有四个 OBIMD 构件候选对象（`002744`–`002747`）已在各自目录中打开图像
并记录观察。

These four observations describe visible marks only. They do not confirm a
component, character identity, reading, variant, inscription, period, or
decipherment. The remaining bundles and review-image objects still require
independent human review.

这四份观察只描述可见痕迹，不确认构件、字形身份、释读、异体、卜辞、时期
或破译。其余资料包和复核图像对象仍需独立人工复核。

Concrete follow-up questions / 具体待查问题：

- Which package manifest row supports each opened image and its checksum?
- Does each image match the candidate UID, or is the match still pending?
- Which catalogue, collection, plate, or excavation record locates the object?
- Which inscription text, OCR, or neighboring-sign context can be cited?
- Which mapping labels are source records rather than accepted relations?
- Which rights wording governs the raw package and each derivative?
- 每幅已打开图像由哪条来源包清单和 checksum 记录支持？
- 图像是否与候选 UID 一致，还是仍待核对？
- 哪条著录、馆藏、图版或出土记录能定位对象？
- 哪条卜辞全文、OCR 或邻字语境可以引用？
- 哪些映射标签只是来源记录，而不是已确认关系？
- 原始包和每个派生件分别适用什么权利说明？

Evidence paths / 证据路径：
`22_source-research-brief.md`; `18_source-access-integrity-review.md`;
`corpus/003_graphemic-components/028_002701-002800_obs-comp-cand-bucket_`
`component-candidates/`

## Package-to-Download Trace Review / 来源包到下载路线复核

Three registered package rows still have no `download_id` in the package
route or source-package manifest:

- `pkg-file-000005` `data.json`, 41,732,948 bytes;
- `pkg-file-000006` `facsimile.zip`, 210,800,641 bytes;
- `pkg-file-000007` `rubbing.zip`, 558,367,972 bytes.

Their package rows contain provider URLs, but the current download log has no
matching access record, checksum, local or external storage path, or extraction
manifest. They must remain provenance gaps before any derivative is created.

已有三条来源包记录在来源包路线和来源包 manifest 中没有 `download_id`：

- `pkg-file-000005` 的 `data.json`，41,732,948 字节；
- `pkg-file-000006` 的 `facsimile.zip`，210,800,641 字节；
- `pkg-file-000007` 的 `rubbing.zip`，558,367,972 字节。

这些包行虽有提供方 URL，但当前下载日志没有对应访问记录、checksum、
本地或外部存放路径，也没有抽取清单。在补齐前不得生成新的派生资料。

Concrete follow-up questions / 具体待查问题：

- Were these three packages actually accessed, and on what date?
- Where are their raw files stored outside regular Git?
- Which checksum and manifest identify each downloaded package?
- What rights wording applies to facsimile and rubbing derivatives?
- 这三个来源包是否实际访问过，访问日期是什么？
- 原始文件存放在普通 Git 之外的什么位置？
- 哪条 checksum 和 manifest 能唯一标识各个下载包？
- facsimile 和 rubbing 派生件适用什么权利说明？

Boundary / 边界：package URLs alone do not prove download, access, or review.
仅有来源包 URL 不证明已经下载、访问或复核。
