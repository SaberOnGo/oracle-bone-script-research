# Oracle Bone Script Research

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
  </tr>
</table>

Oracle Bone Script Research is an open research infrastructure project for
oracle bone script materials. It is a knowledge base, knowledge graph, and AI
Agent research-assistant framework, but its first audience is human
researchers who need to inspect, compare, verify, and continue the work.

This repository is not an automatic decipherment model. It must not present
AI hypotheses, dataset labels, graph edges, or candidate mappings as confirmed
scholarship.

中文摘要：
本项目首先是给甲骨文学家、考古学家和人类研究者阅读、核查、比较、
继续研究的资料库；其次才是给 AI 使用的索引和结构化数据。所有未
复核材料都必须保持候选、来源记录、争议、待查或待复核状态。

## Mission / 项目使命

Democratize access to oracle bone script research while preserving source
provenance, review status, rights boundaries, and scholarly caution.

用开放资料基础设施降低甲骨文研究门槛，同时保留来源追溯、复核状态、
权利边界和学术谨慎。

## Current Stage / 当前阶段

The repository is in the preprocessing and research-infrastructure stage,
before formal oracle-bone research. Current work prepares human-readable
object dossiers, source provenance trails, staging tables, relationship graph
edges, coverage statistics, and review queues.

本仓库处于正式甲骨文研究开始前的资料整理与预处理阶段。当前重点
不是提出释读结论，而是把来源、图像、拓片、著录、卜辞、馆藏、
时期、构件、异体、后世字形路线和文献线索整理成可追溯、可复核、
可继续研究的档案。

AI-readable JSON, CSV, staging tables, manifests, graph edges, and statistics
help people search, trace, compare, and validate the human dossiers. They are
AI-readable support data, not the main research product, and cannot replace
object-local human records.

AI 可读 JSON、CSV、staging 表、manifest、图边和统计只服务检索、
追溯、比较和验证。它们是辅助资料，不是主要研究成果，也不能替代
对象目录内的人类研究档案。

## Human Research Entry Order / 人工研究入口顺序

1. Read `AGENTS.md` for repository rules and research boundaries.
2. Open `doc/project/` for policy, provenance, ID, and large-source rules.
3. Open `project_registry/` to map project IDs to source references.
4. Open a concrete object directory under `corpus/`.
5. Read the human README, dossier, or review sheet before the JSON packet.
6. Inspect images, galleries, source indexes, route indexes, and review sheets.
7. Use statistics and graph files only to find the next evidence route.
8. Record reviewed outcomes without making unverified decipherment claims.

人工阅读时，应先看规则、政策、来源登记和具体对象目录，再看结构化
辅助数据。一个对象目录应同时放人类可读档案和 AI 可读辅助资料。

## Main Entry Points / 主要入口

- `corpus/001_oracle-characters/`
  contains oracle-character and undeciphered-character candidate directories.
- `corpus/002_oracle-bone-inscriptions/`
  contains inscription and plate crosswalk candidate materials.
- `corpus/003_graphemic-components/`
  contains component candidate materials and visual review routes.
- `corpus/004_bronze-seal-modern-correspondences/`
  contains later-script and correspondence candidate routes.
- `corpus/005_excavation-sites-periods-and-batches/`
  contains collection, findspot, period, and batch provenance.
- `corpus/006_research-sources-and-bibliography/`
  contains source objects, bibliography, download routes, and rights notes.
- `corpus/007_research-topics-and-grammar/`
  contains topic-label candidates and grammar-review routes.
- `corpus/008_relationship-graph/`
  contains graph edges for routing and coverage checks.
- `corpus/009_statistics-and-derived-features/`
  contains audits, review queues, and preprocessing statistics.
- `research/`
  is for existing published scholarship and sourced bibliographic notes.
- `doc/public/user_research/`
  is for user and AI Agent drafts before review.

## Concrete Questions To Check / 具体待查问题

- Which object has images but lacks a human-readable research dossier?
- Which source has no checksum, package manifest, field map, or risk note?
- Which character candidate lacks inscription context, collection context,
  later-script route, variant note, or decipherment-history route?
- Which inscription candidate lacks text/OCR, plate number, catalog source,
  Heji/OBM route, collection object, period, batch, or review status?
- Which bibliography item lacks scope, evidence level, proposer, disagreement,
  or citation relationship?
- Which graph edge is only a route and must not be treated as scholarship?
- 哪个对象已有图片，却还缺人类可读研究档案？
- 哪个来源还缺 checksum、package manifest、字段映射或风险说明？
- 哪个单字候选还缺卜辞语境、馆藏语境、后世字形路线、异体说明或
  释读史路线？
- 哪个卜辞候选还缺全文/OCR、图版号、著录来源、合集/OBM 路线、
  馆藏对象、时期、批次或复核状态？
- 哪条文献记录还缺适用范围、证据等级、提出者、不同意见或引用关系？
- 哪条图边只是路线，不能被当作学术结论？

## Research Boundary / 研究边界

Dataset labels, graph edges, codepoint matches, component candidates, catalog
crosswalks, and evolution or correspondence candidates are routing evidence
only. They are not confirmed readings, formal component assignments,
inscription identities, accepted correspondences, or decipherment conclusions.

数据集标签、图边、codepoint 匹配、构件候选、目录互证、字形演化和
对应候选都只是路线证据。不得把它们写成已确认释读、正式构件归属、
卜辞身份、已接受古文字对应或释读结论。

## Validation / 校验

Before committing repository skeleton, docs, schemas, scripts, or generated
preprocessing outputs, run:

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
git diff --check
```

Before pushing, validate commit messages:

```powershell
python tools/git/check_commit_messages.py --range origin/main..HEAD
```
