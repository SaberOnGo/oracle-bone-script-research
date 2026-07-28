# Graph Generation Tools / 图谱生成工具

English:
These tools generate relationship graph edges for preprocessing review.
They connect candidate characters, assets, components, inscriptions,
sources, topics, and evolution routes so human researchers can find the next
evidence trail. A graph edge is not a decipherment conclusion.

简体中文：
本目录工具生成预处理复核使用的关系图边。它们连接候选单字、资产、
构件、卜辞、来源、主题和演化路线，帮助研究者找到下一条证据链。

## Purpose / 用途

English:
Graph edges are review routes. They are not confirmed readings, component
assignments, inscription identities, accepted correspondences, or a
decipherment conclusion. Open the object-local dossier or source note before
using any edge as evidence.

简体中文：
图边只是复核路线。它们不是已确认释读、构件归属、卜辞身份、已接受
对应关系，也不是释读结论。使用任何图边作为证据前，必须先打开对象
内档案或来源说明。

## Human Review Entry Order / 人工复核入口顺序

1. Open the human README or dossier for the source object.
2. Check the source registry, rights note, checksum, and manifest.
3. Open the relevant graph edge JSONL file.
4. Follow edge route fields back to concrete object directories.
5. Compare with visual galleries, source indexes, and review sheets.
6. Record any reviewed outcome in human-gated review files.
7. Keep unreviewed graph links as candidate routes only.

人工复核时，先打开来源对象的人类 README 或档案，再核对来源登记、
权利说明、checksum 和 manifest。随后打开相关 JSONL 图边文件，并沿
路线字段回到具体对象目录，结合图像 gallery、来源索引和复核表核查。
未经人工复核的图边只能保持候选路线状态。

## Edge Families / 图边家族

- character-source:
  HUST-OBC candidate source and validation-class routes.
- character-asset:
  character candidates to co-located local glyph image assets.
- character-component:
  character or component candidates to OBIMD component routes.
- character-inscription:
  character or topic routes to inscription crosswalk candidates.
- cross-source-id:
  HUST, OBIMD, and EVOBC codepoint lookup routes.
- evolution/correspondence:
  EVOBC evolution and later-script correspondence candidate routes.
- topic-source:
  Cambridge/Hopkins topic candidates to source and period routes.

## Current Builders / 当前生成器

- `build_hust_obc_candidate_graph_edges.py`
  writes HUST-OBC candidate source and class edges.
- `build_obimd_component_graph_edges.py`
  writes OBIMD component candidate metadata edges.
- `build_evobc_evolution_graph_edges.py`
  writes EVOBC era and source-code route edges.
- `build_cambridge_hopkins_inscription_graph_edges.py`
  writes inscription crosswalk edges to sources and catalogs.
- `build_character_asset_graph_edges.py`
  writes character-to-local-glyph-asset candidate edges.
- `build_component_asset_graph_edges.py`
  writes component-to-local-image-asset candidate edges.
- `build_cross_source_id_graph_edges.py`
  writes HUST/OBIMD/EVOBC lookup-route edges.
- `build_cambridge_hopkins_topic_graph_edges.py`
  writes topic, period, and inscription-crosswalk route edges.
- `build_character_source_graph_edges.py`
  writes character-candidate to registered-source provenance routes.

## Concrete Questions To Check / 具体待查问题

- Which edge file contains the route for this candidate object?
- Which source row, package manifest, and checksum support the edge?
- Which object-local dossier or review sheet should be opened first?
- Does the edge point to a local image, route-only image, or metadata row?
- Does the edge merely link codepoints, or does it have reviewed evidence?
- Which component, inscription, or evolution link remains candidate-only?
- Which graph edge must not be treated as a scholarly conclusion?

- 哪个图边文件包含该候选对象的路线？
- 哪条来源行、package manifest 和 checksum 支撑这条图边？
- 应先打开哪个对象内档案或人工复核表？
- 图边指向本地图像、仅路线图像，还是 metadata 行？
- 图边只是连接 codepoint，还是已有复核证据？
- 哪条构件、卜辞或演化路线仍只是候选？
- 哪条图边不能被当作学术结论？

## Boundaries / 边界

English:
The graph files support search, tracing, comparison, coverage checks, and
review routing. They do not promote source rows, decide rights, import formal
corpus records, confirm identity, assign components, accept correspondences,
or make decipherment conclusions.

简体中文：
图谱文件服务于检索、追溯、比较、覆盖检查和复核路线。它们不提升
来源行、不裁定权利、不导入正式语料、不确认身份、不归属构件、
不接受对应关系，也不是释读结论。

## Regeneration / 重新生成

Run the relevant builder after changing graph input tables or object-local
source routes. Then run:

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
git diff --check
```
