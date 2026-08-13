# Claim-Evidence Locator / 说法—证据定位

Locations use section and table names on the current official article. No
article table or figure is copied here.

定位采用当前官方文章的章节和表名；本档案不复制论文表格或图。

## Scale / 规模

- Claim: 10,077 rubbing images across five Shang phases.
- Breakdown: 9,913 from *Jiaguwen Heji* and 164 from Huayuanzhuang East.
- State: `author-reported`.
- Locator: `Background & Summary`; `Methods` > `Data acquisition`.
- 说法：五期共 10,077 张拓片，其中 9,913 条来自《甲骨文合集》，
  164 条来自殷墟花园庄东地甲骨资料。

- Claim: 93,652 annotated characters and 21,667 missing positions.
- Claim: 21,941 sentence groups and 4,192 non-sentential groups.
- Claim: 115,319 bounding boxes including characters and placeholders.
- Locator: `Background & Summary`; `Data Records`; Table 2 context.
- State: `author-reported`.
- Boundary: these are dataset records, not confirmed distinct inscriptions,
  characters, readings, or locally imported assets.

## Annotation Workflow / 标注流程

- Claim: a tri-modal interface supports rubbing, facsimile, and transcription
  comparison; algorithms provide pre-annotation and shape candidates.
- Claim: non-specialists, trained graduates, and experts have distinct roles.
- Locator: `Methods`; `Pre-annotation`; Figure 5 context.
- State: `author-reported`.
- Boundary: role-based review does not expose a complete public decision log
  for each annotation.

## Data Fields / 数据字段

- Claim: entries use image, group, and character levels.
- Claim: `GroupCategory` distinguishes sentence and non-sentential groups;
  `Position` locates boxes; `OrderNumber` records within-group order.
- Claim: `Label` and `SubLabel` follow a two-level external glyph library.
- Locator: `Data Records`; Table 2.
- State: `author-reported`.

## Technical Validation / 技术验证

- Locator: `Technical Validation`; Tables 3 through 5.
- Tasks: character detection and recognition, sentence clustering, and
  character reordering.
- Reported reordering results: main-character top-1 75.35%; sub-character
  top-1 72.78%.
- State: `author-reported`.
- Boundary: benchmark performance is not a decipherment probability, reading
  confidence, or proof that the annotated sequence is historically final.
- 边界：基准成绩不是释读概率、释读置信度，也不证明标注顺序是最终结论。

## Availability / 可得性

- Locator: `Data availability`; `Code availability`.
- Data route: https://huggingface.co/datasets/KLOBIP/OBIMD
- Code route: https://github.com/libang1991/OBIMD
- Annotation platform: https://www.jgwlbq.org.cn/oracle-bone
- These routes were independently-checked; their content and licences remain
  separately versioned evidence.
