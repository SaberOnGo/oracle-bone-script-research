# Repository Structure And Naming Rules / 仓库结构与命名规则

English:
Use stable, ASCII-friendly paths with numeric prefixes. Paths should include project-local IDs and one short external reference ID, while complete provenance lives in metadata and registry CSV files.

简体中文：
路径使用稳定、兼容 ASCII、带数字前缀的命名。路径中包含本项目 ID 和一个简短外部来源 ID；完整出处写入 metadata 和 registry CSV。

## Patterns / 模式

```text
001_000001-000100_obs-char-bucket_oracle-characters/
001_obs-char-000001_xxt-jgw-0001_oracle-character/
001_asset-000001_xxt-jgw-0001_glyph-image.png
```

Do not use modern readings, liding forms, pinyin, or English meaning as primary path identity.

不要把现代释读、隶定字、拼音或英文意义作为路径主身份。

Temporary working directories are a special case. Use short conventional names such as `tmp/`, `_tmp/`, `scratch/`, `.working/`, or `.cache/` only for ignored local artifacts. Do not use them as permanent research record paths.

临时工作目录是特殊情况。`tmp/`、`_tmp/`、`scratch/`、`.working/`、`.cache/` 等短名称只用于已忽略的本地临时产物，不得作为永久研究记录路径。
