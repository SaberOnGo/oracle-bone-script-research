# Relationship Graph / 关系图谱

English:
This directory stores graph edge records for review routes among characters,
assets, components, variants, inscriptions, sources, topics, and later-form
correspondence candidates. These files support tracing, comparison, coverage
checks, and statistics. They are not scholarship conclusions.

简体中文：
本目录保存单字、图片、构件、异体、卜辞、来源、专题和后世字形
候选对应之间的图边记录。它们用于追溯、比较、覆盖率检查和统计，
不是学术结论。

## Human Research Entry Order / 人工研究入口顺序

English:

1. Start from the related human dossier or source-object README.
2. Open the graph edge only after the source and object route is known.
3. Check the edge source file, source register, and object-local dossier.
4. Verify the evidence path, external id, rights note, and review status.
5. Compare related `character-source` and `character-asset` edges.
6. Compare candidate `character-component` and `character-variant` edges.
7. Compare `character-inscription` and inscription crosswalk routes.
8. Compare `cross-source-id` and `evolution/correspondence` routes.
9. Record only reviewed route outcomes in human-facing notes.

简体中文：

1. 先打开相关的人类档案或来源对象 README。
2. 确认来源和对象路线后，再查看图边文件。
3. 核对图边来源文件、来源登记和对象本地档案。
4. 核对证据路径、外部编号、权利说明和复核状态。
5. 比较相关的 `character-source` 和 `character-asset` 图边。
6. 比较候选 `character-component` 和 `character-variant` 图边。
7. 比较 `character-inscription` 和卜辞 crosswalk 路线。
8. 比较 `cross-source-id` 与 `evolution/correspondence` 路线。
9. 只把已经复核的路线结果写入人类可读笔记。

## Current Graph Files / 当前图边文件

| File | Human review use |
| --- | --- |
| `004_graph-edges.jsonl` | Early route edges kept for audit comparison. |
| `005_hust-obc-candidate-graph-edges.jsonl` | HUST-OBC metadata routes. |
| `006_obimd-component...` | OBIMD component/codepoint routes. |
| `007_evobc-evolution-graph-edges.jsonl` | EVOBC routes; candidate status is explicit. |
| `008_cambridge-hopkins...` | Inscription crosswalk routes. |
| `009_character-asset-graph...` | Character to local asset routes. |
| `010_cross-source-id-graph-edges.jsonl` | Cross-source id lookup routes. |
| `011_component-asset-graph...` | Component to local asset routes. |
| `012_cambridge-hopkins-topic...` | Topic/crosswalk review routes. |
| `013_character-source-graph...` | Character-to-source routes. |
| `014_character-variant-graph-edges.jsonl` | Candidate variant review routes. |
| `015_character-inscription-candidate...` | H2 candidate occurrence routes. |
| `016_character-component-candidate...` | Cross-source component candidates. |
| `017_evobc-evolution-correspondence-candidate...` | EVOBC later-era candidate routes. |

## Edge Dossier Content / 图边档案内容

English:
Each edge should let a reviewer recover the edge type, subject id, object id,
source row or source file, local dossier path, evidence path, review status,
missing evidence, and next source to check.

简体中文：
每条图边都应让复核者找到图边类型、主体编号、客体编号、来源行或
来源文件、本地档案路径、证据路径、复核状态、缺失证据和下一步
待查来源。

## OBIMD Rights Resolution / OBIMD 权利状态解析

The OBIMD staging tables and older graph edges may preserve the historical
source-declared value `licensed_for_repository`. That value is retained for
provenance comparison only. It is not a redistribution grant and must not be
used as the current publication decision.

OBIMD graph consumers must resolve the effective status through the active
[OBIMD rights resolution note](obimd-rights-resolution.md), which points to
the override ledger and the source-object decision.

The effective status is `metadata_only_until_verified`; the current public
decision is no public redistribution or derivative promotion until the
conflicting terms are reconciled. This applies to component, variant, asset,
and package routes. A graph edge remains a candidate review route and cannot
authorize copying an image, raw package, or derived asset.

OBIMD staging 表和较早的图边可能保留来源历史字段
`licensed_for_repository`。该字段只用于来源对照，不是再分发许可，
也不能当作当前公开发布决定。

所有 OBIMD 图谱使用者都必须通过
[OBIMD 权利解析说明](obimd-rights-resolution.md)解析当前状态；该说明
再指向覆盖表和来源对象决定页。

当前有效状态是 `metadata_only_until_verified`；在冲突条款完成对账前，
不得公开再分发或提升派生件。该规则适用于构件、异体、资产和来源包路线。
图边仍只是候选复核路线，不能授权复制图像、原始包或派生资产。

## Concrete Questions To Check / 具体待查问题

English:

- Which edge points to a character without a human dossier route?
- Which `character-source` edge lacks a reviewed source object?
- Which `character-asset` edge lacks a rights or risk note?
- Which `character-component` edge is only a candidate review route?
- Which `character-variant` edge is only a candidate review route?
- Which `character-inscription` edge lacks inscription context?
- Which inscription edge lacks a plate, text, or catalog route?
- Which `cross-source-id` edge has conflicting external ids?
- Which `evolution/correspondence` edge is only a dataset route?
- Which edge must not be cited as accepted scholarship?

The `014_character-variant-graph-edges.jsonl` file is derived from the
OBIMD sub-character/main-character staging table. Its rows are dataset
hierarchy routes only. They require visual comparison, source checking, and
scholarly review before any variant relation is promoted.

`014_character-variant-graph-edges.jsonl` 来自 OBIMD 子字符/主字符
staging 表。每行只是数据集层级路线，必须经过字形图像比较、来源核对
和学术复核，才能考虑提升为异体关系。

简体中文：

- 哪条图边指向还没有人类档案路线的单字？
- 哪条 `character-source` 图边缺少已复核的来源对象？
- 哪条 `character-asset` 图边缺少权利或风险说明？
- 哪条 `character-component` 图边只是候选复核路线？
- 哪条 `character-variant` 图边只是候选复核路线？
- 哪条 `character-inscription` 图边缺少卜辞上下文？
- 哪条卜辞图边缺少图版、文本或著录路线？
- 哪条 `cross-source-id` 图边存在外部编号冲突？
- 哪条 `evolution/correspondence` 图边只是数据集路线？
- 哪条图边绝不能当作已接受的学术结论引用？

## Research Boundary / 研究边界

English:
Graph edges are review route records. They are not a decipherment conclusion,
not a component assignment, not a variant judgment, not an inscription identity,
not a topic assignment, and not an accepted correspondence. Any claim based on
an edge must return to the image, rubbing, plate, catalog, source register,
and published discussion before it can enter formal research notes.

简体中文：
图边只是复核路线记录。它们不是释读结论，不是构件归属，不是异体
判断，不是卜辞身份确认，不是专题归属，也不是已接受的字形对应。
任何基于图边的判断，都必须回到实物图像、拓片、图版、著录、来源
登记和已发表讨论，之后才能进入正式研究笔记。

## Regeneration Notes / 再生成说明

English:
Generated or refreshed edge files must keep source provenance, stable ids,
evidence paths, review status, and candidate boundaries. Temporary extraction,
OCR, unpacked, and cache files must stay in ignored working directories.

简体中文：
重新生成或刷新图边文件时，必须保留来源追溯、稳定编号、证据路径、
复核状态和候选边界。临时抽取、OCR、解包和缓存文件必须留在已忽略
的工作目录中。
