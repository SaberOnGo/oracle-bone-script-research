# First-stage Import Readiness Notes / 第一阶段导入准备说明

## English

This note converts downloaded source evidence into import-readiness decisions.
It does not import raw image packages, PDFs, or full website exports into Git.
It records fields that may later become structured records and the checks
required before promotion into the corpus.

Immediate import priorities:

1. `src-xiaoxuetang-jiaguwen` and `src-xiaoxuetang-obm` remain the preferred
   backbone for the first 1,500+ character heads and Heji provenance. Current
   downloads are access-restricted, so manual export, API discovery, or
   controlled browsing is required before bulk import.
2. `src-hust-obc` can seed candidate lists for 1,588 deciphered and 9,411
   undeciphered classes. Its mappings are AI-dataset evidence, not final
   philological authority.
3. `src-obimd` is the current source for inscription-context import design:
   image, sentence, character, bounding-box, reading-order, and missing-marker
   fields.
4. `src-cambridge-hopkins` supports inscription-level external-ID crosswalks
   linking Yingguo, CUL, Chalfant, and Heji references.
5. `src-obid-ancientbooks` is a professional discovery and catalog-prefix
   reference, but bulk copying needs access and redistribution review.
6. `src-tsinghua-oracle-bones` supports collection provenance and institution
   context.
7. `src-nlc-oracle-world` has official PDF evidence for collection scale and
   field design, but item-level import still needs a stable query endpoint and
   rights review.
8. `src-evobc` and `src-gbedobc` remain for graph/evolution experiments after
   the primary character and inscription backbones are stronger.

Recommended next data-building sequence:

1. Build a small importer that emits source-marked CSV/JSONL from human-
   reviewed rows, not raw image imports.
2. Stage HUST-OBC character classes as `dataset_candidate`, never accepted
   decipherment.
3. Use OBIMD fields to design occurrences, bounding boxes, reading order,
   sentence groups, and missing/special markers.
4. Use Cambridge-Hopkins rows for an inscription crosswalk with `y`, `c`, `h`,
   and `j` identifiers.
5. Use NLC field-design evidence to reserve holding, source, diviner, period,
   excavation, material, topic, rubbing, join, and catalog fields.
6. Add review gates before promoting any dataset-derived class into the corpus.

Rights and quality boundary:

- Dataset labels and model outputs are evidence leads, not conclusions.
- Raw images stay outside regular Git until provenance, rights, size handling,
  and a derived-record plan are reviewed.
- `GuoXueDaShi` remains `source_under_review` and is not primary authority.
- Commercial or access-controlled platforms are for discovery and citation
  trails; bulk copying requires explicit review.

## 简体中文

本说明把已经下载的来源证据转成“可导入准备”判断。不把原始图片包、PDF 或完整
网站导出直接导入 Git，而是记录以后可转成结构化记录的字段，以及提升到正式语料前
必须完成的复核。

当前优先事项：

1. `src-xiaoxuetang-jiaguwen` 和 `src-xiaoxuetang-obm` 仍是前 1,500+ 字头及合集
   出处的首选骨干。当前下载受访问限制，批量导入前需要人工导出、API 探索或受控浏览。
2. `src-hust-obc` 可为 1,588 个已释类别和 9,411 个未释类别建立候选清单，但这些映射
   只是 AI 数据集证据，不是最终文字学权威。
3. `src-obimd` 适合设计卜辞语境导入字段，包括图像、句子、字符、边界框、阅读顺序和
   缺字或特殊标记。
4. `src-cambridge-hopkins` 可制作卜辞级外部编号 crosswalk，连接 Yingguo、CUL、
   Chalfant 和合集编号。
5. `src-obid-ancientbooks` 可作专业发现界面和目录前缀参考，但批量复制前必须复核
   访问和再分发条款。
6. `src-tsinghua-oracle-bones` 可支持馆藏出处和机构背景记录。
7. `src-nlc-oracle-world` 已有官方 PDF 证据，可核对馆藏规模和字段设计；单条记录导入
   仍需稳定查询入口及权利复核。
8. `src-evobc` 和 `src-gbedobc` 留待甲骨字和卜辞骨干更稳定后用于图谱和演化实验。

建议的数据建设顺序：

1. 先建立小型导入原型，从人工复核行生成带来源标记的 CSV/JSONL，不直接导入原始图片。
2. 用 HUST-OBC 建立标为 `dataset_candidate` 的字类 staging，不标为已接受释读。
3. 用 OBIMD 字段设计出现记录、边界框、阅读顺序、句组和缺字或特殊标记。
4. 用 Cambridge-Hopkins 行设计含 `y`、`c`、`h`、`j` 编号的卜辞 crosswalk。
5. 用 NLC 字段证据预留馆藏号、来源号、贞人、时期、出土地、材质、主题、拓片、缀合
   和著录字段。
6. 任何数据集派生字类进入语料前都要先通过人工复核门槛。

权利和质量边界：

- 数据集标签和模型输出只是证据线索，不是结论。
- 原始图片在来源链、权利状态、大小处理和派生记录方案复核前，留在普通 Git 之外。
- `GuoXueDaShi` 仍标为 `source_under_review`，不能作为一手权威。
- 商业或受控访问平台只用于发现和引用追踪；批量复制必须经过明确复核。
