# Character Local Materials Builder / 字对象本地资料生成器

English:
`build_character_local_materials.py` writes human-readable and AI-readable preparation materials inside the same concrete character object directory.

Simplified Chinese:
`build_character_local_materials.py` 会把人类可读资料和 AI 可读资料写入同一个具体字对象目录。

## Scope / 范围

English:
The builder creates `README.md` and `02_visual-source-index.csv` next to the existing `01_*packet.json` file. It does not create a parallel human-readable directory, does not commit raw large source packages, and does not make decipherment or component conclusions.

简体中文：
该脚本会在已有 `01_*packet.json` 旁边生成 `README.md` 和 `02_visual-source-index.csv`。它不创建并行的“人类看的目录”，不提交大型原始来源包，也不提出释读或构件结论。

## Command / 命令

```powershell
python tools/002_corpus-import/build_character_local_materials.py --root .
```

## Current Batch / 当前批次

English:
The current batch covers three HUST-OBC promoted candidate object directories and two HUST-OBC undeciphered candidate directories with extracted source-image path references.

简体中文：
当前批次覆盖 3 个 HUST-OBC 提升候选字对象目录，以及 2 个已有来源图像路径引用的 HUST-OBC 未释字候选目录。
