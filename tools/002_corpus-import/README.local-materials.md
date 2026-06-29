# Object-Local Materials Builders / 对象内资料生成器

English:
These builders prepare object-local research folders for human review first.
Each concrete `corpus` object keeps its object-local dossier, images,
source/provenance index, review sheet, and structured support packet together.
The support packet helps retrieval and audit work; it does not replace the
dossier.

Simplified Chinese:
这些生成器优先服务人工复核。每个具体 `corpus` 对象目录内同时放置对象内
档案、图像、来源/出处索引、复核表和结构化辅助 packet。packet
只辅助检索、追溯和校验，不能替代人类可读档案。

## Human Review Entry Order / 人工复核入口顺序

English:
Use a generated object folder in this order:

1. Open the README or object-local dossier first.
2. Inspect the glyph image, visual gallery, or route gallery.
3. Check the source/provenance index and any rights or risk notes.
4. Read the human review sheet for missing items and next checks.
5. Use the support packet only after the human evidence route is clear.

Simplified Chinese:
使用生成后的对象目录时，建议按以下顺序复核：

1. 先打开 README 或对象内档案。
2. 再检查字形图片、visual gallery 或 route gallery。
3. 核对 source/provenance index 以及权利、风险提示。
4. 阅读人工复核表中的缺失项和下一步待查来源。
5. 人工证据路线清楚后，再用辅助 packet 辅助检索。

## Current Object Families / 当前对象范围

English:
The current builders prepare review material for these families:

- Character and undeciphered-character dossiers.
- HUST-OBC promoted and undeciphered candidate folders.
- OBIMD component-candidate folders and visual review routes.
- Cambridge/Hopkins inscription crosswalk candidates.
- EVOBC evolution-category evidence-route candidates.
- Museum or collection object candidates.
- Source-object folders and bibliography-related entry routes.
- Topic-candidate folders for grammar or source-review follow-up.

Simplified Chinese:
当前生成器覆盖以下对象类型：

- 单字与未释字对象内档案。
- HUST-OBC 已提升候选字和未释字候选目录。
- OBIMD 构件候选目录及视觉复核路线。
- Cambridge/Hopkins 卜辞目录互证候选。
- EVOBC 字形演化类别证据路线候选。
- 博物馆或馆藏对象候选。
- 来源对象目录和书目相关入口路线。
- 语法或来源复核后续用的 topic 候选目录。

## Concrete Questions To Check / 具体待查问题

English:
When reviewing a generated object folder, answer concrete questions:

- Which source package, page, plate, catalog number, or export row produced it?
- Is the visible image local, linked, missing, or blocked by rights review?
- Does the folder show an object-local dossier before AI-only data?
- Are all candidate labels marked as candidates rather than conclusions?
- Are missing inscriptions, findspots, periods, or collection fields named?
- Can the next researcher trace every derived file back to a source record?

Simplified Chinese:
复核生成后的对象目录时，应回答具体问题：

- 该对象来自哪个来源包、页码、图版、著录号或导出行？
- 可见图像是本地文件、外部链接、缺失，还是因权利复核暂缓？
- 目录是否先呈现对象内档案，而不是只呈现 AI 数据？
- 所有候选标签是否都仍标为候选，而非结论？
- 缺失的卜辞、出土地、时期或馆藏字段是否被具体点名？
- 后续研究者能否从每个派生文件追溯到来源记录？

## Builder Inventory / 生成器清单

English:
Run these scripts from the repository root when the source inputs are ready:

- `build_character_local_materials.py`
- `build_character_human_research_dossiers.py`
- `extract_hust_obc_local_glyph_images.py`
- `build_hust_obc_undeciphered_local_materials.py`
- `build_obimd_component_candidate_materials.py`
- `build_cambridge_hopkins_inscription_crosswalk_materials.py`
- `build_evobc_evolution_candidate_materials.py`
- `build_collection_object_candidate_materials.py`
- `build_source_object_materials.py`
- `build_cambridge_hopkins_topic_materials.py`

Simplified Chinese:
来源输入准备好后，从仓库根目录运行这些脚本：

- `build_character_local_materials.py`
- `build_character_human_research_dossiers.py`
- `extract_hust_obc_local_glyph_images.py`
- `build_hust_obc_undeciphered_local_materials.py`
- `build_obimd_component_candidate_materials.py`
- `build_cambridge_hopkins_inscription_crosswalk_materials.py`
- `build_evobc_evolution_candidate_materials.py`
- `build_collection_object_candidate_materials.py`
- `build_source_object_materials.py`
- `build_cambridge_hopkins_topic_materials.py`

## Research Boundary / 研究边界

English:
These outputs are preparation records. They are not a decipherment conclusion,
not component assignments, not inscription identity claims, and not accepted
evolution correspondences. Dataset labels stay as source labels until a human
researcher checks the object, source trail, image, and relevant scholarship.

Simplified Chinese:
这些输出只是资料整理记录，不是释读结论，不是构件归属结论，不是卜辞或
馆藏对象同一性结论，也不是已接受的字形演化对应。数据集标签在人工复核
对象、来源链、图像和相关研究前，只能作为来源标签保存。

## Validation / 校验

English:
Object-local material checks are part of the repository skeleton validator and
unit tests. They check co-location, required files, source routes, candidate
status, review sheets, and the absence of parallel human-readable directories.

Simplified Chinese:
对象内资料检查已接入仓库 skeleton validator 和单元测试。检查范围包括对象
内共置、必需文件、来源路径、候选状态、复核表，以及不存在并行的人类可读
目录。
