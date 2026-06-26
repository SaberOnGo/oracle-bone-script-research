# Repository Structure And Naming Rules / 仓库结构与命名规则

English:
Use stable, short, ASCII-friendly paths with numeric prefixes. Paths should
include a project-local ID and one short external reference ID. Complete
provenance belongs in metadata files and registry CSV files.

简体中文：
路径应稳定、简短、兼容 ASCII，并带数字前缀。路径中应包含本项目
ID 和一个简短外部来源 ID。完整出处应写入 metadata 文件和 registry
CSV。

## Core Patterns / 核心模式

Large bucket directory:

```text
001_000001-000100_obs-char-bucket_oracle-characters/
```

Single oracle character directory:

```text
001_obs-char-000001_xxt-jgw-0001_oracle-character/
```

Asset file:

```text
001_asset-000001_xxt-jgw-0001_glyph-image.png
```

## Path Identity / 路径身份

English:
Do not use modern readings, liding forms, pinyin, or English meaning as
primary path identity. Many oracle characters do not have reliable modern
equivalents, and readings may change after review.

简体中文：
不要把现代释读、隶定字、拼音或英文意义作为路径主身份。很多甲骨字
没有可靠的现代字对应，释读也可能在复核后变化。

## Object-Local Materials / 对象内资料

English:
Concrete corpus object directories should contain both human-readable
materials and AI-readable materials. Do not create a parallel human-readable
directory next to `corpus/` or next to an object directory.

简体中文：
具体 `corpus` 对象目录里应同时放置人类可读资料和 AI 可读资料。不要
在 `corpus/` 旁边或对象目录旁边再创建并行的人类可读目录。

## Temporary Areas / 临时区

English:
Temporary working directories are a special case. Use ignored names such as
`tmp/`, `_tmp/`, `scratch/`, `.working/`, or `.cache/` only for local scratch
files, temporary downloads, OCR intermediates, unpacked archives, caches, and
generated experimental outputs.

简体中文：
临时工作目录只用于已忽略的本地草稿、临时下载、OCR 中间产物、解压
目录、缓存和实验性生成结果。
