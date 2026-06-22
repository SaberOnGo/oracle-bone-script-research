# Tools / 工具

English:
This directory contains validation, corpus import, graph generation,
statistics, Git, and AI context-pack tools. These tools support human
research dossiers; they do not replace object-local review.

简体中文：
本目录保存校验、语料导入、图谱生成、统计、Git 与 AI 上下文包工具。
这些工具服务于人类研究档案，不能替代对象目录内的人工复核材料。

## Human Review Entry Order / 人工复核入口顺序

English:
Use repository tools in this order:

1. Open the related object-local dossier, review sheet, or source note first.
2. Check source provenance, rights status, risk note, and review status.
3. Run corpus import tools only to build staging or object-local materials.
4. Run graph generation only after opening the cited source rows.
5. Read statistics as review signals, not as research conclusions.
6. Build AI context-pack files only from reviewed routes and warnings.
7. Run validation before committing any docs, schemas, scripts, or outputs.

简体中文：
使用仓库工具时，按以下顺序处理：

1. 先打开相关对象目录内的档案、复核表或来源说明。
2. 核对来源追溯、权利状态、风险提示和复核状态。
3. 语料导入工具只用于生成 staging 或对象内资料。
4. 图谱生成前，必须先打开被引用的来源记录。
5. 统计只能作为复核信号，不能当作研究结论。
6. AI 上下文包只能汇集已标明路线和警示的材料。
7. 提交文档、schema、脚本或输出前，必须运行校验。

## Tool Areas / 工具分区

- `001_corpus-validation/` checks corpus and object-local records.
- `002_corpus-import/` prepares source package, staging index, and
  object-local materials.
- `003_graph-generation/` builds graph generation outputs such as
  character-source and cross-source route edges.
- `004_statistics-generation/` builds statistics for coverage, gaps, and
  review queues.
- `005_ai-context-pack-builder/` builds AI context-pack support files.
- `validation/` runs repository-wide skeleton and policy checks.
- `git/` checks commit-message rules before GitHub push.

## Concrete Questions To Check / 具体待查问题

- Which object-local dossier or review sheet does this tool support?
- Which source provenance, checksum, manifest, or field map does it cite?
- Does the output stay inside an approved corpus, registry, or ignored area?
- Is the result a staging route, graph route, statistic, or review queue?
- Which human-readable file should be opened before trusting the output?
- Does any output need rights review, large-source registration, or cleanup?
- 哪个对象目录内档案或复核表需要这个工具支持？
- 它引用了哪条来源追溯、checksum、manifest 或字段映射？
- 输出是否留在允许的语料、登记表或已忽略临时区？
- 结果是 staging 路线、图边路线、统计，还是复核队列？
- 信任输出前，应先打开哪一个人类可读文件？
- 是否还有权利复核、大型来源登记或临时产物清理待完成？

## Research Boundary / 研究边界

English:
Tool outputs are preprocessing and review aids. A passed validator, generated
CSV, JSON route, graph edge, statistic, or AI context-pack is not scholarship,
not corpus import approval, not a rights decision, and not a decipherment
conclusion. This is not a decipherment conclusion.

简体中文：
工具输出只是预处理和复核辅助。通过 validator、生成 CSV、JSON 路线、
图边、统计或 AI 上下文包，都不是学术结论，不是语料导入批准，不是
权利决定，也不是释读结论。这不是释读结论。
