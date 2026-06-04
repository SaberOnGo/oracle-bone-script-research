---
name: source-provenance-review
description: Use when reviewing source references, external IDs, catalog numbers, asset provenance, rights status, or whether material is safe to commit to this public repository.
---

# Source Provenance Review / 来源出处复核

## Use This Skill When / 何时使用

English:
Use this skill before adding source references, asset metadata, screenshots, rubbings, hand copies, paper notes, or any material with uncertain rights.

简体中文：
在添加来源引用、资产 metadata、截图、拓片、摹本、论文笔记或权利状态不明确的材料前使用本 skill。

## Required Reading / 必读

- `AGENTS.md`
- `doc/project/002_source-rights-and-provenance-policy/README.md`
- `doc/project/006_large-source-material-handling/README.md`
- `license/README.md`
- `project_registry/003_external-source-prefixes/README.md`
- `project_registry/004_asset-source-and-rights-index/README.md`
- `project_registry/006_large-source-register/README.md`

## Review Questions / 复核问题

- What is the source system, catalog, book, paper, museum, or URL?
- 来源系统、著录、图书、论文、博物馆或 URL 是什么？
- What external ID identifies the item?
- 哪个外部 ID 能定位该资料？
- Is this a character ID, inscription ID, plate number, old catalog number, asset ID, or modern Unicode code?
- 这是单字 ID、卜辞 ID、图版号、旧著录号、资产 ID，还是现代 Unicode 编码？
- What will be committed publicly: metadata only, small sample, full asset, or local-only reference?
- 将公开提交哪些内容：仅 metadata、小样例、完整资产，还是只保存本地引用？
- Is the raw source package over `SIZE_LIMIT`, and if so where is it registered and stored outside regular Git?
- 原始来源包是否超过 `SIZE_LIMIT`？如果超过，它登记在哪里、存放在普通 Git 之外的哪里？
- What is the `rights_status`?
- `rights_status` 是什么？
- What risk note should be visible beside this material?
- 这项资料旁边需要显示什么风险提示？

## Rule / 规则

English:
Rights-unclear material may be downloaded or committed when it is useful for research, but it must carry source provenance, rights status, and a visible risk note. If the risk is too high for the public repository, place the raw material in a local-only folder and commit the metadata trail.

Large source packages over `SIZE_LIMIT` should be registered in `project_registry/006_large-source-register/` and stored outside regular Git. AI Agent temporary downloads, OCR caches, unpacked archives, and generated indexes must stay in ignored temporary directories.

简体中文：
权利不明确的材料在研究需要时可以下载或提交，但必须带有来源、权利状态和显式风险提示。如果公开仓库风险过高，则把原始材料放入本地私有目录，只提交 metadata 追溯链。

超过 `SIZE_LIMIT` 的大型来源包应登记到 `project_registry/006_large-source-register/`，并存放在普通 Git 之外。AI Agent 临时下载、OCR 缓存、解压目录和生成索引必须留在已忽略临时目录。
