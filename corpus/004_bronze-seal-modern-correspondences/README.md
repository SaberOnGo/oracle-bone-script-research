# Bronze, Seal, And Modern Correspondences / 金文、小篆与今文对应

English:
This directory stores preprocessing infrastructure for cross-period character-form correspondence work across oracle bone script, bronze script, seal script, later script-stage labels, and modern codepoints. Materials here are object-local: each concrete candidate object directory must contain both human-readable review materials and AI-readable structured files.

Simplified Chinese:
本目录保存跨时期字形对应工作的预处理基础设施，范围包括甲骨文、金文、小篆、后续文字阶段标签与现代 codepoint。这里的资料采用对象内组织方式：每一个具体候选对象目录都必须同时包含人类可读复核资料和 AI 可读结构化文件。

Current staging and object areas:

- `000_evolution-registers/001_evobc-evolution-category-staging.csv`: EVOBC evolution-category metadata with 13,714 dataset categories.
- `000_evolution-registers/002_evobc-era-source-codebook-staging.csv`: EVOBC era/source codebook staging table.
- `001_*_obs-evo-cand-bucket_evolution-candidates/`: object-local EVOBC category candidate directories, generated from the staging tables.

当前暂存与对象区域：

- `000_evolution-registers/001_evobc-evolution-category-staging.csv`：EVOBC 字形演化类别 metadata，共 13,714 个数据集类别。
- `000_evolution-registers/002_evobc-era-source-codebook-staging.csv`：EVOBC 时代码/source 码暂存表。
- `001_*_obs-evo-cand-bucket_evolution-candidates/`：由暂存表生成的对象内 EVOBC 类别候选目录。

Boundary / 边界：

EVOBC rows and object-local packets are not formal character correspondences. They preserve dataset-level evidence for later review against stronger paleographic sources, source-chain records, image provenance, and inscription context. Do not use these records as accepted evolution chains, modern-character identity confirmations, or decipherment conclusions.

EVOBC 行和对象内 packet 不是正式字形对应关系。它们只保存数据集层面的证据，供后续与更强的古文字学来源、来源链记录、图像出处和卜辞语境交叉复核。不得把这些记录当作已确认的演化链、现代字身份确认或释读结论。
