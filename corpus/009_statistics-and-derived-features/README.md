# Statistics And Derived Features / 统计与派生特征

简体中文：
本目录保存可由 `tools/004_statistics-generation/` 重建的统计和审计报告。
统计只用来帮助研究者找到该打开的档案和来源，不是研究结论。

English:
This directory holds statistics and audit reports that can be rebuilt by
`tools/004_statistics-generation/`. Statistics help researchers decide which
dossier or source to open next; they are not research conclusions.

## 2026-11-02 清理 / Cleanup

按[架构重置][reset]第 1 步，约 200 个 AI 队列、scaffold、handoff、
route pack、assignment plan 文件已从工作树删除，它们是 Agent 工作残留，
不是研究资料。需要时可从 Git 提交 `f8638e9ea77` 恢复。

Per step 1 of the [architecture reset][reset], about two hundred AI queue,
scaffold, handoff, route-pack, and assignment-plan files were removed from the
working tree. They remain recoverable from commit `f8638e9ea77`.

现存统计中，`090` 至 `097`、`186` 至 `191`、`213` 至 `235` 描述的是
旧模板目录结构。它们作为历史审计保留，迁移第 6 步会按学术关系图谱重建。

Files `090`--`097`, `186`--`191`, and `213`--`235` describe the former
template structure. They stay as historical audits until step 6 rebuilds the
statistics from the scholarly graph.

## 现存文件 / Current Files

| 文件 | 内容 |
| --- | --- |
| `001`、`002` | 旧路线边的边类型与度数汇总（历史；学术图谱汇总见 `corpus/008_relationship-graph/100_scholarly-graph/000_edge-summary.csv`） |
| `007` | 来源覆盖汇总（含 OBIMD 有效权利状态） |
| `090`--`097` | 预处理状态、数据质量、来源流水线审计（历史） |
| `186`--`191` | 对象资料覆盖与项目 ID 映射审计（历史） |
| `213`--`219` | 各语料区阶段缺口人读说明（历史） |
| `220`--`235` | 研究深度、关联、视觉观察、演化对应审计（历史） |
| `230` | 2026-08-07 预处理闭合报告（历史回执） |

[reset]: ../../doc/project/007_architecture-reset-and-human-first-knowledge-base/
