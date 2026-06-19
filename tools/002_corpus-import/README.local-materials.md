# Character Local Materials Builder / 字对象本地资料生成器

English:
`build_character_local_materials.py` writes human-readable and AI-readable preparation materials inside the same concrete character object directory.

Simplified Chinese:
`build_character_local_materials.py` 会把人类可读资料和 AI 可读资料写入同一个具体字对象目录。

English:
`extract_hust_obc_local_glyph_images.py` extracts selected small HUST-OBC glyph candidate image derivatives from the registered raw zip into each target object directory's `03_visual-assets/` folder. The raw zip stays in ignored `external_local_archive/` storage.

简体中文：
`extract_hust_obc_local_glyph_images.py` 会从已登记的 HUST-OBC 原始 zip 中抽取选定的小型字形候选图派生件，放入目标对象目录下的 `03_visual-assets/`。原始 zip 保留在已忽略的 `external_local_archive/` 归档区。

## Scope / 范围

English:
The builders create `README.md`, `02_visual-source-index.csv`, and selected `03_visual-assets/` files next to the existing `01_*packet.json` file. They do not create a parallel human-readable directory, do not commit raw large source packages, and do not make decipherment or component conclusions.

简体中文：
这些脚本会在已有 `01_*packet.json` 旁边生成 `README.md`、`02_visual-source-index.csv` 和选定的 `03_visual-assets/` 文件。它们不创建并行的“人类看的目录”，不提交大型原始来源包，也不提出释读或构件结论。

## Command / 命令

```powershell
python tools/002_corpus-import/build_character_local_materials.py --root .
python tools/002_corpus-import/extract_hust_obc_local_glyph_images.py --root .
```

## Current Batch / 当前批次

English:
The current batch covers three HUST-OBC promoted candidate object directories and two HUST-OBC undeciphered candidate directories with extracted source-image path references.

简体中文：
当前批次覆盖 3 个 HUST-OBC 提升候选字对象目录，以及 2 个已有来源图像路径引用的 HUST-OBC 未释字候选目录。
