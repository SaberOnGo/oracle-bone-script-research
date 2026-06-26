# Record Model And ID System / 记录模型与 ID 体系

English:
The repository uses stable project-local IDs plus short external reference
IDs. The local ID gives stable repository identity; the external ID provides
provenance and links to existing catalogs, databases, plates, source packages,
or object records.

简体中文：
本仓库使用“稳定本项目 ID + 简短外部来源 ID”。本项目 ID 保证仓库
内部身份稳定；外部 ID 用于追溯现有字编、著录、数据库、图版、来源
包或馆藏对象记录。

## Path Examples / 路径示例

```text
001_000001-000100_obs-char-bucket_oracle-characters/
001_obs-char-000001_xxt-jgw-0001_oracle-character/
001_asset-000001_xxt-jgw-0001_glyph-image.png
```

## Current ID Families / 当前 ID 类型

- `obs-char-*`: promoted oracle-character candidate records.
- `obs-unk-*`: undeciphered or unpromoted oracle-character candidates.
- `obs-comp-cand-*`: graphemic component candidates.
- `obs-insc-cw-cand-*`: inscription catalog-crosswalk candidates.
- `obs-evo-cand-*`: evolution/correspondence candidates.
- `asset-*`: committed visual or source assets.

简体中文：

- `obs-char-*`：已提升的甲骨单字候选记录。
- `obs-unk-*`：未释或尚未提升的甲骨字候选。
- `obs-comp-cand-*`：构件候选。
- `obs-insc-cw-cand-*`：卜辞目录互证候选。
- `obs-evo-cand-*`：字形演化/对应候选。
- `asset-*`：已提交的视觉或来源资产。

## Rule / 规则

English:
Do not encode modern readings as path identity. Many oracle characters do not
have reliable modern equivalents, and readings may change after review. Store
full source trails in object metadata and `project_registry/`.

简体中文：
不要把现代释读写成路径身份。很多甲骨字没有可靠的现代字对应，释读
也可能在复核后变化。完整来源链应写入对象 metadata 和
`project_registry/`。

## Candidate Boundary / 候选边界

English:
A record ID or object directory is not a scholarly conclusion. IDs allow
stable routing, review, graph linking, and evidence collection. Formal
readings, component structures, inscription identities, and paleographic
correspondences require separate human review and stronger evidence.

简体中文：
记录 ID 或对象目录不是学术结论。ID 的作用是稳定寻址、复核、图谱
关联和证据收集。正式释读、构件结构、卜辞身份和古文字对应关系都
需要单独的人工复核和更强证据。
