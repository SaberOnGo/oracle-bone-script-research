# 对象档案标准 / Object Dossier Standard

- 状态 / Status: `proposed_normative_standard`
- 适用对象 / Applies to: 单字、卜辞、甲骨实物、来源、文献、案件

本标准规定"一份给人读的档案"必须是什么样子。它取代各对象目录中现有
的 7 到 9 份模板 Markdown。

This standard defines what one human-readable dossier must look like. It
replaces the seven to nine template Markdown files per object directory.

## 1. 通则 / General Rules

1. 一个对象，一份人读档案 `README.md`，一份机读记录 `record.json`，
   一个资产目录。不再有 `05_human-research-dossier.md`、
   `08_character-context-evidence-dossier.md`、
   `10_archaeology-paleography-review.md`、
   `12_human-research-readiness-review.md` 等并列文件。
2. 档案只写关于该对象的事实、来源和问题。流程说明、复核清单、字段
   解释写在 `skills/` 和 `schemas/`，不写进档案。
3. 边界声明全仓库只写一次（`corpus/README.md`）。档案开头只保留一行
   状态行。
4. 没有内容的章节直接省略。禁止用"待查：需核对……"占位。缺失项统一
   写进最后一节"待查项"，每项是一个具体问题加一个具体来源。
5. 每条事实后面带来源标记：`〔来源 src-xxx 行 N〕`、
   `〔文献 lit-xxx p.N〕` 或 `〔图 images/xxx.png〕`。没有来源的句子
   只能出现在"观察"或"假说"小节，并以"观察："或"假说："开头。
6. 中文为主，英文可以是段末摘要或配套文件。中文必须是通顺的研究
   文字，不是字段名的翻译。
7. 甲骨字形只以图呈现。文中需要指称一个甲骨字时，用项目 ID 或
   `〔图 N〕`；今字只在"隶定与今字候选"一节出现，并带状态。不得把
   扩展区 Unicode 或来源文件名中的字符当作字形写进正文。
8. 80 字符换行只适用于中文和英文散文。路径、URL、ID、表格行、代码块
   不换行。
9. 机读记录 `record.json` 的每个字段都必须能在 `README.md` 找到对应
   句子；反之，`README.md` 中每个带来源的事实在 `record.json` 中有
   对应条目。两者由脚本互检。

## 2. 单字档案 / Character Dossier

文件：`README.md`。状态行示例：

```text
状态：已释候选（数据集标签） | 释读史：未收集 | 例句：0 | 更新：2026-11-01
```

章节与最低内容要求：

| 章节 | 必须回答的问题 | 最低来源 |
| --- | --- | --- |
| 1 字形与观察 | 这个字长什么样？有几种写法？笔画、残损如何？ | 本地图片 ≥ 1 |
| 2 隶定与今字候选 | 学界或数据集把它隶定为什么？状态如何？ | 来源行 |
| 3 释读史 | 谁最早释出？依据是什么？谁反对？现状如何？ | 文献 + 页 |
| 4 卜辞例句 | 它出现在哪些卜辞？全文是什么？字位在哪？ | 著录号 + 释文来源 |
| 5 分布 | 出现多少次？哪些分期、组类、辞例、共现字？ | 由例句层统计 |
| 6 异体、近形、构件 | 哪些字与它同字异写？哪些近形易混？含哪些构件？ | 图 + 依据 |
| 7 后世字形 | 金文、小篆、楷书中对应什么？依据是什么？ | 图 + 文献 |
| 8 实物与出土 | 字例所在甲骨出自哪里？藏在哪里？ | 馆藏 / 著录 |
| 9 争议与未决 | 哪些问题学界没有定论？ | 文献 |
| 10 来源与权利 | 本档案用了哪些来源？各自权利状态？ | 登记表 |
| 11 待查项 | 下一步该打开哪个具体来源回答哪个具体问题？ | 具体 |

已释字档案至少要有第 1、2、3、4、10 节才算"存在"。未释字档案至少要
有第 1、4（若有字例）、6、10、11 节。

示例片段（已释字，示意格式；人名、年份、页码均为占位，内容必须按
真实来源填写）：

```text
## 3 释读史

- 1917 年罗振玉《殷虚书契考释》释为"X"，依据是与金文 Y 形近
  〔文献 lit-luo-1917 p.NN〕。
- 1933 年郭沫若提出异议，认为当读为"Z"，依据是辞例"……"
  〔文献 lit-guo-1933 p.NN〕。
- 《甲骨文字诂林》按语采纳罗说〔文献 lit-gulin-1996 p.NNNN〕。
- 当前状态：多数采罗说；郭说仍见引用。

## 4 卜辞例句

| 著录号 | 释文（来源原文） | 字位 | 分期 | 来源 |
| --- | --- | --- | --- | --- |
| 合 14496 | 貞：翌日 □ 于祖乙 | 4 | 一期 | src-xxt-obm 行 N |
```

## 3. 卜辞记录与实物档案 / Inscription Record And Bone Dossier

卜辞以语料行为主（见 `02_target-architecture.md` 第 6 节）。只有当一
片甲骨有拓片图、多条卜辞、争议或案件时才建实物目录。实物目录
`README.md` 章节：

1. 实物身份（馆藏号、著录号、合集号、旧著录号、拼合信息）
2. 图像（拓片、照片、摹本；每张带来源与权利）
3. 卜辞全文（逐条，带片内序号、字位、残缺标记、来源）
4. 分期与组类（依据）
5. 出土与流转（坑位、批次、馆藏史；区分考古出土、著录来源、馆藏
   记录三种性质）
6. 相关字（字位 -> 字 ID）
7. 学术讨论与争议
8. 来源与权利
9. 待查项

现有 `corpus/002_*/008_source-record-candidates/` 的 10 个候选和
`corpus/005_*/002_collection-object-candidates/` 的 58 个候选已经接近
此标准，是合并与改写的首批对象。实物与卜辞来源候选目前分在两处，
同一件实物（如史语所 1215）应合并为一个实物目录。

## 4. 文献与主张 / Literature And Claims

文献档案在 `research/001_published-scholarship-index/`，现有格式
（范围与方法、主张与证据定位、引用网络、限制与争议、复核记录）保留。
新增要求：每条"主张"单独成行，格式固定：

```text
- claim-xxxx | 提出者 | 年份 | 文献 p.N | 命题 | 依据类型 | 状态
```

主张行是 L3 层的原子单位，图谱 `reading_proposed` / `reading_disputed`
边直接引用 `claim-` ID。

## 5. 研究案件 / Research Case

案件文件放在对象目录内（对象局部原则）并在
`doc/public/user_research/cases/index.md` 登记。案件文件章节：

1. 命题（一句话，中英）
2. 结果状态（`working_hypothesis` / `withheld` / `abstained` /
   `ai_adjudicated_candidate`）
3. 候选解释排序与各自支持证据（引用档案具体行）
4. 最强反证
5. 可推翻条件
6. 已做的检验（含盲测、反例搜索）
7. 下一个最有价值的待查来源
8. 版本与变更记录

案件不得引用没有来源标记的句子作为证据。

## 6. 禁止清单 / Forbidden Patterns

以下内容出现在对象档案中即视为缺陷：

- 同一目录内两份以上人读 Markdown 描述同一对象；
- "本文件不是释读结论"类声明超过一行；
- `project id` / `external id` / `review status` 在同一文件重复出现；
- "待查：需核对……"、"only route record"、"not a decipherment
  conclusion" 等固定句；
- 把 `README.md` 用作文件清单而不是档案正文；
- 用 "Open first / 先打开的材料" 列表代替内容；
- 在路径、ID、URL 中间换行。

The forbidden list: multiple human Markdown files per object, repeated
disclaimers, repeated ID fields, fixed "pending" sentences, README as a file
list, "open first" lists instead of content, and line breaks inside paths or
identifiers.
