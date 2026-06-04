# Record Model And ID System / 记录模型与 ID 体系

English:
The repository uses project-local stable IDs plus short external reference IDs. The local ID gives stable repository identity; the external ID provides provenance and links to existing catalogs or databases.

简体中文：
本仓库使用“本项目稳定 ID + 简短外部来源 ID”。本项目 ID 保证仓库内部身份稳定；外部 ID 用于追溯现有字编、著录、数据库或图版来源。

## Examples / 示例

```text
001_000001-000100_obs-char-bucket_oracle-characters/
001_obs-char-000001_xxt-jgw-0001_oracle-character/
001_asset-000001_xxt-jgw-0001_glyph-image.png
```

## Rule / 规则

English:
Do not encode modern readings as path identity. Many oracle characters do not have reliable modern equivalents, and readings may change.

简体中文：
不要把现代释读写成路径身份。很多甲骨字没有可靠的现代字对应，释读也可能变化。
