# Finding-List Reconciliation / Finding-list 对账

## Purpose / 目的

This is a human-readable audit of the Cambridge University Library
finding-list import. It preserves the source page's subsection labels,
stated counts, observed identifier rows, and unresolved count differences.
It is a preprocessing audit, not a new classification or decipherment
result.

这是 Cambridge University Library finding-list
导入的人工可读对账。它保留来源页面的分区标签、页面声明数量、实际观察到的编号行以及尚未解释的数量差异。它属于预处理审计，不是新的分类、释读或破译结论。

## Source Evidence / 来源证据

- Source ID: `src-cambridge-hopkins`
- Download ID: `dl-cambridge-hopkins-finding-list`
- Source URL:
  `https://www.lib.cam.ac.uk/collections/departments/chinese-collections/`
  `chinese-collections-te-cang-yu-zhuan-cang/finding-list`
- Imported staging rows: `612`
- Page-stated grand total: `609`
- Difference between imported rows and stated grand total: `3`
- Formal inscription records created: `0`
- Rights status: `metadata_only_until_verified`

The page lists a classified table, the Shih tsu, Tzu tsu, and Wu tsu
subsections, and four Unclassified entries. The flat staging file retained
those four rows but previously represented the three ancestor subsections
through the Group 19 value. The row-level reconciliation below keeps the
original flat value and adds the source-page subsection label.

页面列出分类表、Shih tsu、Tzu tsu、Wu tsu 子分区以及四条 Unclassified。扁平 staging
文件保留了这四条记录，但此前用 Group 19 值表示三个祖先子分区。下面的逐行对账同时保留原始扁平值，并补充来源页面分区标签。

## Section Counts / 分区数量

- Section key: `period-I-shih-tsu`
  Label: Shih tsu / 祖先子组（原页标签）
  Declared: `21`; observed: `21`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-I-tzu-tsu`
  Label: Tzu tsu / 子祖（原页标签）
  Declared: `7`; observed: `7`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-I-wu-tsu`
  Label: Wu tsu / 午祖（原页标签）
  Declared: `2`; observed: `2`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-1`
  Label: Period I Group 1 / 第 I 期第 1 组
  Declared: `30`; observed: `30`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-10`
  Label: Period I Group 10 / 第 I 期第 10 组
  Declared: `6`; observed: `6`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-12`
  Label: Period I Group 12 / 第 I 期第 12 组
  Declared: `8`; observed: `8`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-13`
  Label: Period I Group 13 / 第 I 期第 13 组
  Declared: `4`; observed: `4`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-14`
  Label: Period I Group 14 / 第 I 期第 14 组
  Declared: `16`; observed: `16`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-15`
  Label: Period I Group 15 / 第 I 期第 15 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-16`
  Label: Period I Group 16 / 第 I 期第 16 组
  Declared: `18`; observed: `18`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-17`
  Label: Period I Group 17 / 第 I 期第 17 组
  Declared: `20`; observed: `20`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-18`
  Label: Period I Group 18 / 第 I 期第 18 组
  Declared: `17`; observed: `17`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-19`
  Label: Period I Group 19 / 第 I 期第 19 组
  Declared: `13`; observed: `22`
  Status: `declared_count_differs_from_observed_rows`
- Section key: `period-i-group-2`
  Label: Period I Group 2 / 第 I 期第 2 组
  Declared: `4`; observed: `4`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-3`
  Label: Period I Group 3 / 第 I 期第 3 组
  Declared: `33`; observed: `33`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-4`
  Label: Period I Group 4 / 第 I 期第 4 组
  Declared: `12`; observed: `12`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-5`
  Label: Period I Group 5 / 第 I 期第 5 组
  Declared: `5`; observed: `5`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-6`
  Label: Period I Group 6 / 第 I 期第 6 组
  Declared: `48`; observed: `48`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-7`
  Label: Period I Group 7 / 第 I 期第 7 组
  Declared: `5`; observed: `5`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-8`
  Label: Period I Group 8 / 第 I 期第 8 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-i-group-9`
  Label: Period I Group 9 / 第 I 期第 9 组
  Declared: `11`; observed: `11`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-1`
  Label: Period II Group 1 / 第 II 期第 1 组
  Declared: `29`; observed: `28`
  Status: `declared_count_differs_from_observed_rows`
- Section key: `period-ii-group-10`
  Label: Period II Group 10 / 第 II 期第 10 组
  Declared: `4`; observed: `4`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-11`
  Label: Period II Group 11 / 第 II 期第 11 组
  Declared: `3`; observed: `3`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-12`
  Label: Period II Group 12 / 第 II 期第 12 组
  Declared: `2`; observed: `2`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-13`
  Label: Period II Group 13 / 第 II 期第 13 组
  Declared: `2`; observed: `2`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-14`
  Label: Period II Group 14 / 第 II 期第 14 组
  Declared: `2`; observed: `2`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-15`
  Label: Period II Group 15 / 第 II 期第 15 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-16`
  Label: Period II Group 16 / 第 II 期第 16 组
  Declared: `2`; observed: `2`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-17`
  Label: Period II Group 17 / 第 II 期第 17 组
  Declared: `36`; observed: `36`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-18`
  Label: Period II Group 18 / 第 II 期第 18 组
  Declared: `3`; observed: `3`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-19`
  Label: Period II Group 19 / 第 II 期第 19 组
  Declared: `22`; observed: `21`
  Status: `declared_count_differs_from_observed_rows`
- Section key: `period-ii-group-2`
  Label: Period II Group 2 / 第 II 期第 2 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-20`
  Label: Period II Group 20 / 第 II 期第 20 组
  Declared: `2`; observed: `2`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-3`
  Label: Period II Group 3 / 第 II 期第 3 组
  Declared: `6`; observed: `6`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-ii-group-4`
  Label: Period II Group 4 / 第 II 期第 4 组
  Declared: `16`; observed: `21`
  Status: `declared_count_differs_from_observed_rows`
- Section key: `period-ii-group-6`
  Label: Period II Group 6 / 第 II 期第 6 组
  Declared: `3`; observed: `3`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-1`
  Label: Period III Group 1 / 第 III 期第 1 组
  Declared: `7`; observed: `7`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-10`
  Label: Period III Group 10 / 第 III 期第 10 组
  Declared: `17`; observed: `17`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-11`
  Label: Period III Group 11 / 第 III 期第 11 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-12`
  Label: Period III Group 12 / 第 III 期第 12 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-13`
  Label: Period III Group 13 / 第 III 期第 13 组
  Declared: `3`; observed: `3`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-14`
  Label: Period III Group 14 / 第 III 期第 14 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-17`
  Label: Period III Group 17 / 第 III 期第 17 组
  Declared: `9`; observed: `9`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-18`
  Label: Period III Group 18 / 第 III 期第 18 组
  Declared: `5`; observed: `5`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-19`
  Label: Period III Group 19 / 第 III 期第 19 组
  Declared: `6`; observed: `6`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-20`
  Label: Period III Group 20 / 第 III 期第 20 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-3`
  Label: Period III Group 3 / 第 III 期第 3 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iii-group-4`
  Label: Period III Group 4 / 第 III 期第 4 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-1`
  Label: Period IV Group 1 / 第 IV 期第 1 组
  Declared: `9`; observed: `9`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-10`
  Label: Period IV Group 10 / 第 IV 期第 10 组
  Declared: `2`; observed: `2`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-11`
  Label: Period IV Group 11 / 第 IV 期第 11 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-13`
  Label: Period IV Group 13 / 第 IV 期第 13 组
  Declared: `3`; observed: `3`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-16`
  Label: Period IV Group 16 / 第 IV 期第 16 组
  Declared: `2`; observed: `2`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-17`
  Label: Period IV Group 17 / 第 IV 期第 17 组
  Declared: `3`; observed: `3`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-19`
  Label: Period IV Group 19 / 第 IV 期第 19 组
  Declared: `6`; observed: `6`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-20`
  Label: Period IV Group 20 / 第 IV 期第 20 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-3`
  Label: Period IV Group 3 / 第 IV 期第 3 组
  Declared: `3`; observed: `3`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-5`
  Label: Period IV Group 5 / 第 IV 期第 5 组
  Declared: `2`; observed: `2`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-iv-group-9`
  Label: Period IV Group 9 / 第 IV 期第 9 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-v-group-1`
  Label: Period V Group 1 / 第 V 期第 1 组
  Declared: `12`; observed: `12`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-v-group-12`
  Label: Period V Group 12 / 第 V 期第 12 组
  Declared: `12`; observed: `12`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-v-group-13`
  Label: Period V Group 13 / 第 V 期第 13 组
  Declared: `4`; observed: `4`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-v-group-17`
  Label: Period V Group 17 / 第 V 期第 17 组
  Declared: `2`; observed: `2`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-v-group-18`
  Label: Period V Group 18 / 第 V 期第 18 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-v-group-19`
  Label: Period V Group 19 / 第 V 期第 19 组
  Declared: `30`; observed: `30`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-v-group-20`
  Label: Period V Group 20 / 第 V 期第 20 组
  Declared: `1`; observed: `1`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-v-group-6`
  Label: Period V Group 6 / 第 V 期第 6 组
  Declared: `5`; observed: `5`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-v-group-7`
  Label: Period V Group 7 / 第 V 期第 7 组
  Declared: `6`; observed: `6`
  Status: `declared_count_matches_observed_rows`
- Section key: `period-v-group-8`
  Label: Period V Group 8 / 第 V 期第 8 组
  Declared: `not stated`; observed: `21`
  Status: `source_section_has_no_declared_count`
- Section key: `unclassified`
  Label: Unclassified / 未分类（原页标签）
  Declared: `not stated`; observed: `4`
  Status: `source_section_has_no_declared_count`

## Concrete Review Questions / 具体待查问题

- Why does page total `609` differ from imported row count `612`?
- Which page entries explain each section count difference?
- Should the four Unclassified entries receive separate object routes?
- Which source or catalogue page supplies images, plates, OCR, and full text?
- Which missing references can be resolved without a formal `obi-*` ID?

- 页面声明总数 `609` 与导入行数 `612` 的差异由哪些页面条目造成？
- 各分区的声明数量与实际编号行差异应如何由原页面逐条核对？
- 四条 Unclassified 是否需要分别建立馆藏实物核查路线？
- 哪个来源或著录页面能提供图像、图版、OCR 与全文？
- 哪些缺失著录可以在不分配正式 `obi-*` 编号的前提下补齐？

## Boundary / 边界

This object is a Cambridge/Hopkins inscription crosswalk candidate only. It
is metadata for catalog review; it is not a formal obi-* inscription record,
not an object identity claim, not a transcription, not an inscription
reading, and not a decipherment conclusion.
