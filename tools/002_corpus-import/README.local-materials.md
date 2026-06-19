# Character Local Materials Builder / 字对象本地资料生成器

English:
`build_character_local_materials.py` writes human-readable and AI-readable preparation materials inside the same concrete character object directory. The current object-local bundle includes:

- `README.md`: human-readable object entrance and research-boundary note.
- `01_*packet.json`: AI-readable candidate packet already stored in the object directory.
- `02_visual-source-index.csv`: AI-readable visual/source index with source paths, rights status, risk notes, and review status.
- `03_visual-assets/`: selected local review image derivatives and metadata, when extraction is allowed and source-marked.
- `04_visual-gallery.md`: human-readable visual gallery that renders committed local review images directly from the same object directory.

简体中文：
`build_character_local_materials.py` 会把人类可读资料和 AI 可读资料写入同一个具体字对象目录。当前对象内资料包包括：

- `README.md`：人类可读的对象入口和研究边界说明。
- `01_*packet.json`：已经放在对象目录中的 AI 可读候选资料包。
- `02_visual-source-index.csv`：AI 可读的图像和来源索引，记录来源路径、权利状态、风险提示和复核状态。
- `03_visual-assets/`：在允许抽取且带来源标记时保存的本地复核图像派生件和 metadata。
- `04_visual-gallery.md`：人类可读图像页，直接从同一对象目录渲染已提交的本地复核图像。

English:
`extract_hust_obc_local_glyph_images.py` extracts selected small HUST-OBC glyph candidate image derivatives from the registered raw zip into each target object directory's `03_visual-assets/` folder. The raw zip stays in ignored `external_local_archive/` storage.

简体中文：
`extract_hust_obc_local_glyph_images.py` 会从已登记的 HUST-OBC 原始 zip 中抽取选定的小型字形候选图像派生件，放入目标对象目录下的 `03_visual-assets/`。原始 zip 保留在已忽略的 `external_local_archive/` 归档区。

## Scope / 范围

English:
The builders create `README.md`, `02_visual-source-index.csv`, `04_visual-gallery.md`, and selected `03_visual-assets/` files next to the existing `01_*packet.json` file. They do not create a parallel human-readable directory, do not commit raw large source packages, and do not make decipherment or component conclusions.

简体中文：
这些脚本会在已有 `01_*packet.json` 旁边生成 `README.md`、`02_visual-source-index.csv`、`04_visual-gallery.md` 和选定的 `03_visual-assets/` 文件。它们不会创建并行的“人类看的目录”，不会提交大型原始来源包，也不会提出释读或构件结论。

## Command / 命令

```powershell
python tools/002_corpus-import/build_character_local_materials.py --root .
python tools/002_corpus-import/extract_hust_obc_local_glyph_images.py --root .
```

## Current Batch / 当前批次

English:
The current batch covers the first thirteen HUST-OBC promoted candidate buckets, `obs-char-000001` through `obs-char-001300`, plus two HUST-OBC undeciphered candidate directories with extracted source-image path references. These target object directories have co-located README files, visual/source indexes, visual galleries, and committed local review image derivatives inside the same concrete `corpus` object directory.

简体中文：
当前批次覆盖 HUST-OBC 已提升候选字的前十三个分桶，即 `obs-char-000001` 至 `obs-char-001300`，以及 2 个已有来源图像路径引用的 HUST-OBC 未释字候选目录。这些目标对象目录都在同一个具体 `corpus` 对象目录内放置 README、图像和来源索引、图像页，以及已提交的本地复核图像派生件。
