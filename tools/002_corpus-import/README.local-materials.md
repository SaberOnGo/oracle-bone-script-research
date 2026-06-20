# Object-Local Materials Builders / 对象内资料生成器

English:
These builders write human-readable and AI-readable preparation materials inside the same concrete `corpus` object directory. They do not create parallel "human-readable" directories, do not promote dataset labels into scholarship, and do not commit large raw source packages.

Simplified Chinese:
这些生成器会把人类可读资料和 AI 可读资料写入同一个具体 `corpus` 对象目录。它们不会创建并行的“人类可读”目录，不会把数据集标签提升为学术结论，也不会提交大型原始来源包。

## Generated Object Files / 生成的对象内文件

English:
Depending on the object type, a generated object directory contains a human README, an AI packet, source/provenance indexes, visual or code indexes, human review sheets, and small reviewed image derivatives when source rights and size rules allow them.

Simplified Chinese:
根据对象类型不同，生成后的对象目录会包含人类 README、AI packet、来源/出处索引、图像或代码索引、人工复核表，以及在来源权利和大小规则允许时保存的小型复核图像派生件。

## Commands / 命令

```powershell
python tools/002_corpus-import/build_character_local_materials.py --root .
python tools/002_corpus-import/extract_hust_obc_local_glyph_images.py --root .
python tools/002_corpus-import/build_hust_obc_undeciphered_local_materials.py --root .
python tools/002_corpus-import/build_obimd_component_candidate_materials.py --root .
python tools/002_corpus-import/build_cambridge_hopkins_inscription_crosswalk_materials.py --root .
python tools/002_corpus-import/build_evobc_evolution_candidate_materials.py --root .
python tools/002_corpus-import/build_collection_object_candidate_materials.py --root .
```

## Current Coverage / 当前覆盖范围

English:
The HUST-OBC local-material batch covers all 1,588 promoted candidate character directories and all 9,408 undeciphered candidate directories. Each concrete object directory now keeps its AI packet, README, visual/source index, visual gallery, human review sheet, and a small source-marked local review image together under the same `corpus/001_oracle-characters/` object path.

Simplified Chinese:
HUST-OBC 对象内资料批次覆盖 1,588 个已提升候选字目录和全部 9,408 个未释字候选目录。每个具体对象目录现在都把 AI packet、README、图像/来源索引、图像图库、人工复核表和带来源标记的小型本地复核图像放在同一个 `corpus/001_oracle-characters/` 对象路径内。

English:
The OBIMD component batch covers all 2,747 OBIMD subcharacter candidates and 10,364 object-local PNG review assets extracted from the registered `Sub-character Images.zip` source package. Each `obs-comp-cand-*` directory contains a README, candidate packet, source index, glyph-codepoint index, glyph-codepoint gallery, local component image assets, visual index, visual gallery, and human visual review sheet. These are review candidates only, not confirmed components or component assignments.

Simplified Chinese:
OBIMD 构件批次覆盖全部 2,747 个 OBIMD subcharacter 候选，以及从已登记 `Sub-character Images.zip` 来源包抽取的 10,364 个对象内 PNG 复核资产。每个 `obs-comp-cand-*` 目录包含 README、候选 packet、来源索引、glyph-codepoint 索引、glyph-codepoint gallery、本地构件图像资产、视觉索引、视觉 gallery 和人工视觉复核表。这些只是不作结论的待复核候选，不是已确认构件或构件归属。

English:
The Cambridge/Hopkins inscription crosswalk batch covers all 612 catalog crosswalk candidates. Each `obs-insc-cw-cand-*` directory contains a README, candidate packet, crosswalk source index, catalog-reference index, human review sheet, plate/text route index, and plate/text route gallery. These are catalog-review and evidence-route candidates only, not formal `obi-*` inscription records, object identity claims, transcriptions, readings, or decipherment conclusions.

Simplified Chinese:
Cambridge/Hopkins 卜辞目录互证批次覆盖 612 个目录 crosswalk 候选。每个 `obs-insc-cw-cand-*` 目录包含 README、候选 packet、crosswalk 来源索引、目录引用索引、人工复核表、图版/文本路线索引和图版/文本路线图。这些只是目录复核与证据路线候选，不是正式 `obi-*` 卜辞记录、馆藏对象同一性结论、释文、卜辞读法或释读结论。

English:
The EVOBC evolution-category batch covers all 13,714 EVOBC dataset categories. Each `obs-evo-cand-*` directory contains a README, candidate packet, source index, era/source code index, human review sheet, image-reference route index, and image-reference route gallery. These are evidence-route candidates only, not accepted paleographic correspondences, evolution-chain conclusions, modern-character identity confirmations, or decipherment conclusions.

Simplified Chinese:
EVOBC 字形演化类别批次覆盖 13,714 个 EVOBC 数据集类别。每个 `obs-evo-cand-*` 目录包含 README、候选 packet、来源索引、时代码/source 码索引、人工复核表、图像引用路线索引和图像引用路线图。这些只是证据路线候选，不是已接受的古文字对应关系、字形演化链结论、现代字身份确认或释读结论。

## Validation / 校验

English:
The collection-object candidate batch covers 56 museum or collection object candidates from IHP Museum, Smithsonian/NMAA, Penn Museum, and The Met staging rows. Each `coll-obj-cand-*` directory contains a README, AI packet, source index, visual asset or thumbnail-route index, visual gallery, and human review sheet. Public-domain Met and Smithsonian assets are shown through object-local gallery links; IHP thumbnails and Penn images remain metadata-only until rights and object-level review are complete.

Simplified Chinese:
馆藏对象候选批次覆盖 56 个来自史语所历史文物陈列馆、Smithsonian/NMAA、Penn Museum 和 The Met 暂存行的对象。每个 `coll-obj-cand-*` 目录包含 README、AI packet、来源索引、图像资产或缩略图入口索引、图像 gallery 和人工复核表。Met 与 Smithsonian 的公版图片通过对象内 gallery 链接显示；IHP 缩略图和 Penn 图像在权利与对象级复核完成前仍保持 metadata-only。

English:
Object-local material checks are part of `tools/validation/check_repository_skeleton.py` and the unit test suite. They verify co-location, required files, source routes, candidate status, and the absence of parallel human-readable directories.

Simplified Chinese:
对象内资料检查已接入 `tools/validation/check_repository_skeleton.py` 和单元测试。检查内容包括对象内共置、必需文件、来源路径、候选状态，以及不存在并行的人类可读目录。
