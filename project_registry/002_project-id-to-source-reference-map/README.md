# Project ID To Source Reference Map / 本项目 ID 到来源引用映射

English:
This directory stores CSV maps from project-local IDs to external source IDs. It is the compact source trail for humans and AI Agents. Each map records the canonical object path, primary external reference, complete external reference list, source IDs, rights status, review status, and update date.

简体中文：
本目录保存本项目本地 ID 到外部来源 ID 的 CSV 映射，是人类和 AI Agent 使用的简明来源追溯表。每个映射表记录规范对象路径、首选外部引用、完整外部引用列表、来源 ID、权利状态、复核状态和更新日期。

## Files / 文件

- `001_oracle-character-id-source-map.csv`: oracle-character and undeciphered-character candidate IDs.
- `002_oracle-inscription-id-source-map.csv`: inscription and inscription-crosswalk candidate IDs.
- `003_asset-id-source-map.csv`: committed visual/source asset IDs.
- `004_component-id-source-map.csv`: graphemic component candidate IDs.
- `005_evolution-candidate-id-source-map.csv`: EVOBC evolution/correspondence candidate IDs.
- `006_collection-object-id-source-map.csv`: museum and collection object candidate IDs.

## How To Use / 使用方式

English:
Open the relevant map when you need to move from a project-local ID such as `obs-char-*`, `obs-comp-cand-*`, `obs-insc-cw-cand-*`, or `obs-evo-cand-*` to the corresponding object directory and external source trail.

简体中文：
当需要从 `obs-char-*`、`obs-comp-cand-*`、`obs-insc-cw-cand-*` 或 `obs-evo-cand-*` 等本项目 ID 找到对应对象目录和外部来源链时，先打开相应映射表。

## Boundary / 边界

English:
Rows in these maps are source-routing records, not scholarly conclusions. A mapped candidate ID can point to an object-local research entrance, but it does not by itself confirm a character reading, component structure, inscription identity, evolution chain, or modern-character correspondence.

简体中文：
这些映射行是来源路径记录，不是学术结论。已映射的候选 ID 可以指向对象内研究入口，但它本身并不确认字的释读、构件结构、卜辞身份、演化链或现代字对应关系。
