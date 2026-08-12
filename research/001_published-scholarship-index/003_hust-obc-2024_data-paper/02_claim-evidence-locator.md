# Claim-Evidence Locator / 说法—证据定位表

This locator paraphrases short facts. It does not reproduce article tables or
figures. Locations use stable section names on the official HTML page.

本表只转述短事实，不复制论文表格或图。定位采用官方 HTML 的稳定章节名。

## Dataset Scale / 数据规模

- Claim: 140,053 images in total.
- Breakdown: 77,064 images in 1,588 deciphered categories; 62,989 images in
  9,411 undeciphered categories.
- State: `source-reported`.
- Locator: `Abstract`; `Data Records`; Table 3 and Figure 7 context.
- Boundary: these are paper-reported dataset counts, not the number of local
  repository assets or distinct historically attested characters.
- 说法：共 140,053 张图；已释部分 77,064 张、1,588 类；未释部分
  62,989 张、9,411 类。
- 状态：`source-reported`。
- 定位：`Abstract`、`Data Records`、表 3 与图 7 附近。
- 边界：这是论文报告的数据集计数，不是本仓库资产数，也不是历史上不同
  单字的数量。

## Undeciphered Categories / 未释类别

- Claim: the 9,411 undeciphered categories may contain duplicates because
  annotations are unavailable; the paper says merging awaits decipherment.
- State: `source-reported`.
- Locator: `Data Records`, paragraph following the total counts.
- Boundary: “may contain duplicates” is not permission to merge any two local
  candidates. 未释类别“可能存在重复”不授权合并任何本地候选。

## Sources And Integration / 来源与整合

- Claim: inputs came from books, websites, and databases.
- Locator: `Methods` > `Data acquisition`; Table 3.
- Claim: the pipeline reduced 1,781 collected deciphered categories to 1,588
  after feature-assisted similarity comparison and integration.
- Locator: `Methods` > `Data integration`; Figure 6 context.
- State: `source-reported`.
- Boundary: similarity-assisted merging is a dataset construction decision,
  not proof of variant identity, synonymy, or accepted paleography.

## Expert Review / 专家复核

- Claim: scholars from Anyang Normal University reviewed the preliminary
  dataset using books and HWOBC database fonts as references.
- State: `source-reported`.
- Locator: `Methods` > `Validation`, final paragraph.
- Boundary: the paper does not expose an item-level adjudication log for every
  local image. That evidence remains `unresolved`.

## GuoXueDaShi Boundary / 国学大师资料边界

- Claim: the paper keeps unreliable GuoXueDaShi material in a separate folder.
- State: `source-reported`.
- Locator: `Usage Notes`; also the source discussion under `Methods`.
- Boundary: the separate folder is a caution route. It does not prove that all
  other labels are correct or that each GuoXueDaShi item is wrong.
- 该独立目录是风险路线，不证明其他标签全部正确，也不证明其中每项必错。

## Technical Result / 技术结果

- Claim: ResNet-50 reached 94.6% classification accuracy and macro F1 0.914.
- State: `source-reported`.
- Locator: `Technical Validation`, paragraph before Table 4.
- Boundary: the reported result does not support “A means B” at 94.6%.
- Classification accuracy does not equal a decipherment probability.
- 边界：94.6% 分类准确率不等于释读概率，也不支持“甲就是乙”的
  94.6% 学术置信度。

## Independently Checked Routes / 独立核查路线

- DOI, title, venue, article number, publication date, official HTML, and
  visible section names were independently checked on 2026-08-12.
- Logged HTML and PDF sizes and SHA-256 values were independently checked
  against the repository download log.
- The prior downloaded bytes are no longer at the logged temporary paths;
  byte-level revalidation is `unresolved` until a matching re-download exists.
