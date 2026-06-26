# 甲骨文开放研究项目

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.md">English</a></h3></td>
  </tr>
</table>

本项目是甲骨文资料整理、知识库、知识图谱和 AI Agent 研究助手框架。
它的第一读者是甲骨文学家、考古学家和其他人类研究者；AI 使用的
索引、JSON、CSV 和图边只是辅助资料。

本项目不是自动破译模型。AI 假说、数据集标签、图边和候选映射在
经过来源证据和学术资料复核前，不能写成已确认学术结论。

English summary:
Oracle Bone Script Research is an open research infrastructure project. Its
main purpose is to provide human-readable, source-traceable dossiers for
inspection, comparison, verification, and future research, with AI-readable
support data kept secondary.

## 项目使命 / Mission

用开放资料基础设施降低甲骨文研究门槛，同时保留来源追溯、复核状态、
权利边界和学术谨慎。

Democratize access to oracle bone script research while preserving source
provenance, review status, rights boundaries, and scholarly caution.

## 当前阶段 / Current Stage

本仓库处于正式甲骨文研究开始前的资料整理与预处理阶段。当前重点
不是提出释读结论，而是把来源、图像、拓片、著录、卜辞、馆藏、
时期、构件、异体、后世字形路线和文献线索整理成可追溯、可复核、
可继续研究的档案。

AI 可读辅助资料包括 JSON、CSV、staging 表、manifest、关系图边和
统计。这些文件服务于检索、追溯、比较和验证，不能替代对象内的人类研究档案。

## 人工研究入口顺序 / Human Research Entry Order

1. 先读 `AGENTS.md`，确认仓库规则和研究边界。
2. 打开 `doc/project/`，查看政策、来源、ID 和大文件规则。
3. 打开 `project_registry/`，把本项目 ID 映射到来源引用。
4. 进入 `corpus/` 下的具体对象目录。
5. 先读人类 README、dossier 或 review sheet，再读 JSON packet。
6. 检查图片、gallery、来源索引、路线索引和人工复核表。
7. 统计和图谱只用于寻找下一条证据路线。
8. 只记录已复核结果，不写未确认释读结论。

## 重要入口 / Main Entry Points

- `corpus/001_oracle-characters/`
  保存甲骨单字和未释字候选目录。
- `corpus/002_oracle-bone-inscriptions/`
  保存卜辞和图版目录互证候选资料。
- `corpus/003_graphemic-components/`
  保存构件候选和视觉复核路线。
- `corpus/004_bronze-seal-modern-correspondences/`
  保存金文、小篆、今字和演化对应候选路线。
- `corpus/005_excavation-sites-periods-and-batches/`
  保存馆藏、出土地、时期和批次来源。
- `corpus/006_research-sources-and-bibliography/`
  保存来源对象、文献、下载路线和权利说明。
- `corpus/007_research-topics-and-grammar/`
  保存主题标签候选和语法复核路线。
- `corpus/008_relationship-graph/`
  保存用于路线和覆盖检查的关系图边。
- `corpus/009_statistics-and-derived-features/`
  保存审计、复核队列和预处理统计。
- `research/`
  保存已有公开学术研究和有来源的书目笔记。
- `doc/public/user_research/`
  保存用户和 AI Agent 草稿，复核前不得混入 `research/`。

## 具体待查问题 / Concrete Questions To Check

- 哪个对象已有图片，却还缺人类可读研究档案？
- 哪个来源还缺 checksum、package manifest、字段映射或风险说明？
- 哪个单字候选还缺卜辞语境、馆藏语境、后世字形路线、异体说明或
  释读史路线？
- 哪个卜辞候选还缺全文/OCR、图版号、著录来源、合集/OBM 路线、
  馆藏对象、时期、批次或复核状态？
- 哪条文献记录还缺适用范围、证据等级、提出者、不同意见或引用关系？
- 哪条图边只是路线，不能被当作学术结论？

## 研究边界 / Research Boundary

数据集标签、图边、codepoint 匹配、构件候选、目录互证、字形演化和
对应候选都只是路线证据。它们不是已确认释读、正式构件归属、卜辞
身份、已接受古文字对应或释读结论。

已有学术研究属于 `research/`。用户和 AI Agent 草稿属于
`doc/public/user_research/`；未经人工复核并改写为有来源的学术笔记前，
不得混入 `research/`。

## 校验 / Validation

提交仓库骨架、文档、schema、脚本或生成的预处理结果前运行：

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
git diff --check
```

推送前校验提交信息：

```powershell
python tools/git/check_commit_messages.py --range origin/main..HEAD
```
