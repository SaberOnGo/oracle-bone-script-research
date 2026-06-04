# First-stage Import Readiness Notes

## English

This note converts the currently downloaded source evidence into import-readiness decisions. It does not import raw image packages, PDFs, or full website exports into Git. It records which source fields can later become structured records, and what must be reviewed before promotion into the corpus.

Immediate import priorities:

1. `src-xiaoxuetang-jiaguwen` and `src-xiaoxuetang-obm` remain the preferred backbone for the first 1,500+ character heads and Heji/source provenance. Current automated downloads are access-restricted, so they need manual export, documented API discovery, or controlled browsing before bulk import.
2. `src-hust-obc` can seed a large candidate list for 1,588 deciphered classes and 9,411 undeciphered classes. Its `deciphered`, `undeciphered`, `chinese_to_ID.json`, and `ID_to_chinese.json` structures are useful, but the mapping is an AI-dataset mapping rather than final philological authority.
3. `src-obimd` is the best current source for inscription-context import design. Its image-level, sentence-level, and character-level hierarchy maps directly to asset metadata, inscription context groups, character occurrences, bounding boxes, reading order, and missing-position markers.
4. `src-cambridge-hopkins` is immediately useful for inscription-level external ID crosswalks because it links Yingguo, CUL, Chalfant, and Heji references.
5. `src-obid-ancientbooks` is useful as a professional discovery interface and catalog-prefix reference, but raw records should not be copied in bulk because access and redistribution terms need caution.
6. `src-tsinghua-oracle-bones` is useful for collection-level provenance and institutional context.
7. `src-evobc` and `src-gbedobc` should be reserved for graph/evolution experiments after the primary oracle-character and inscription backbones are stronger.

Recommended next data-building sequence:

1. Create a small import prototype that can produce source-marked CSV/JSONL records from manually reviewed rows, not raw image imports.
2. Use HUST-OBC metadata to create a candidate character-class staging table, clearly marked as `dataset_candidate` and not as accepted decipherment.
3. Use OBIMD metadata fields to design occurrence records: image reference, bounding box, source label, sublabel, reading order, sentence group, and missing/special markers.
4. Use Cambridge Hopkins rows to design an inscription crosswalk table with `y`, `c`, `h`, and `j` identifiers.
5. Add review gates before promoting any dataset-derived character class into `corpus/001_oracle-characters/`.

Rights and quality boundary:

- Dataset labels and model outputs are evidence leads, not conclusions.
- Raw images remain outside regular Git until source chain, rights status, size handling, and derived-record plan are reviewed.
- `GuoXueDaShi` appears as a HUST-OBC source prefix, but it remains `source_under_review` and must not become a primary authority.
- Commercial or access-controlled platforms may be used for discovery and citation trails, but bulk copying requires explicit review.

## 简体中文

本说明把当前已经下载的来源证据转化为“可导入准备”判断。它不把原始图片包、PDF 全文或网站完整导出导入 Git，只记录哪些来源字段将来可以转成结构化记录，以及哪些内容在提升为正式语料前必须复核。

当前优先级：

1. `src-xiaoxuetang-jiaguwen` 和 `src-xiaoxuetang-obm` 仍是第一批 1,500+ 字头和《合集》出处的首选主干。当前自动下载得到的是访问限制页，因此后续需要人工导出、明确 API 探索或受控浏览后再批量导入。
2. `src-hust-obc` 可以为 1,588 个已释类别和 9,411 个未释类别提供大型候选清单。其 `deciphered`、`undeciphered`、`chinese_to_ID.json`、`ID_to_chinese.json` 结构有价值，但这种映射是 AI 数据集映射，不是最终古文字学权威。
3. `src-obimd` 是目前设计卜辞语境导入的最佳来源。它的图像级、句级、字符级层级可以映射到资产 metadata、卜辞语境组、单字出现、bounding box、阅读顺序和缺字/特殊标记。
4. `src-cambridge-hopkins` 可直接用于设计卜辞级外部 ID crosswalk，因为它连接了 Yingguo、CUL、Chalfant 和 Heji 编号。
5. `src-obid-ancientbooks` 适合作为专业发现界面和目录前缀参考，但由于访问和再分发条款需要谨慎，不应批量复制原始记录。
6. `src-tsinghua-oracle-bones` 适合作为馆藏级来源和机构语境。
7. `src-evobc` 和 `src-gbedobc` 应放在后续图谱/字形演化实验阶段使用，前提是甲骨字和卜辞主干已经更稳固。

建议的数据建设顺序：

1. 先建立一个小型导入原型，从人工复核过的行生成带来源的 CSV/JSONL 记录，而不是直接导入原始图片。
2. 用 HUST-OBC metadata 建立候选字类 staging 表，明确标记为 `dataset_candidate`，不能标记为已接受释读。
3. 用 OBIMD 字段设计 occurrence 记录：图像引用、bounding box、来源 label、sublabel、阅读顺序、句组和缺字/特殊标记。
4. 用 Cambridge Hopkins 行设计卜辞 crosswalk 表，记录 `y`、`c`、`h`、`j` 等外部编号。
5. 在任何数据集派生字类进入 `corpus/001_oracle-characters/` 前增加复核门槛。

权利和质量边界：

- 数据集标签和模型输出是证据线索，不是结论。
- 原始图片在来源链、权利状态、大小处理和派生记录方案复核前，仍然放在普通 Git 之外。
- `GuoXueDaShi` 出现在 HUST-OBC 来源前缀中，但在本项目中仍是 `source_under_review`，不能作为一手权威。
- 商业或访问受控平台可以用于发现和引用链，但批量复制必须经过明确复核。
