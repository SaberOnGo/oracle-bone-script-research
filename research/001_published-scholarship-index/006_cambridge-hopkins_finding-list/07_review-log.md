# Review Log / 复核日志

## 2026-08-13 Current-Route Review / 当前路线复核

- The official Cambridge University Library search-rendered page was opened.
- Title, institution, official URL, opening digitisation statement,
  `Classified Table of Contents`, `KEY`, and period sections were checked.
- The page currently exposes grand total `609` and the `c/h/j/y` key.
- A direct scripted GET returned HTTP `403`; therefore no new raw HTML hash
  is claimed for this date.
- The repository's earlier HTTP `200` download log, size `74132`, and SHA-256
  were checked independently.
- The logged ignored temporary HTML is absent; no source file was restored.

- 已打开 Cambridge University Library 官方路线的搜索呈现页面。
- 已核查题名、机构、URL、数字化说明、分类表、代码表和时期分节。
- 当前页面呈现总数 `609` 及 `c/h/j/y` 代码表。
- 脚本直接请求返回 HTTP `403`，因此本次不声称取得新的原始 HTML
  校验和。
- 已独立检查较早的 HTTP `200` 下载日志、`74132` 字节和 SHA-256。
- 已忽略临时 HTML 当前不存在，本次没有恢复或提交来源文件。

## Review State / 复核状态

- Page identity and logged snapshot metadata: `independently-checked`.
- Counts and key meanings as Cambridge displays them: `source-reported`.
- Causes of `609`/`612` and section differences: `unresolved`.
- Object identity, image direction, text, reading, and reuse: `unresolved`.
- Effective rights: `metadata_only_until_verified`.

## Concrete Next Questions / 具体下一步问题

1. Why does the page state `609` while the parser retains `612` rows?
2. Did the page change around Period V Group 8, or did the parser fail to
   capture `[10]` from the section heading?
3. Which exact rows explain each of the four declared-versus-observed
   section differences?
4. Which CUL object ID and image direction correspond to each `c` number?
5. Which edition page or plate verifies each `h`, `j`, and `y` reference?
6. Do repeated numbers represent the same face, another face, a join, a
   duplicate, a correction, or only a typographic repetition?
7. What terms govern each linked image, OCR text, and 3D asset?
8. Who compiled or revised the web finding list, and when?
9. Where are explicit scholarly proposals, objections, and reading histories
   for the individual rows recorded?

1. 页面 `609` 与解析保留 `612` 行的原因是什么？
2. 第 V 期第 8 组是否发生网页修订，还是解析器漏取了标题 `[10]`？
3. 哪些具体行解释四处分节声明数与观察数差异？
4. 每个 `c` 号对应哪个 CUL 对象 ID 和图像方向？
5. 每个 `h`、`j`、`y` 号由哪个版本页码或图版验证？
6. 重号表示同一面、另一面、缀合、重复、勘误，还是排印重复？
7. 每个图像、OCR 文本和 3D 资产分别适用什么条款？
8. 谁在何时编制或修订了该网页目录？
9. 单行相关的明确提出、反对意见和释读史记录在哪里？

