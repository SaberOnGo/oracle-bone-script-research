# Digital Archive Rubbing Crosswalk / 数字典藏拓片交叉复核

## Purpose / 目的

This page compares two institution-managed routes for IHP item 503. It asks
whether museum accession `R044498` and digital rubbing record `188493-0529`
refer to the same source object through `《丙》0529`.

本页比较史语所管理的两条 503 号对象路线，检验馆藏号 `R044498` 与数字
拓片登记号 `188493-0529` 是否通过 `《丙》0529` 指向同一来源对象。

## Opened Institutional Route / 已打开机构路线

A separate Agent acquisition attempt opened the public record on
`2026-08-30`. A later root rerun, using a different access context, received
an access-block page.

另一次 Agent 采集尝试于 `2026-08-30` 打开公开记录；稍后根 Agent 使用
不同访问环境复跑时收到访问阻断页。两次响应差异的原因尚未确认。

The successful record reported:

- title: `甲骨文拓片（登錄號：188493-0529）`;
- material type: `甲骨刻辭`; static image;
- period: late Shang, Period I;
- original rubbing dimensions: `19.23 x 13.79 cm`;
- source: *Xiaotun dierben Yinxu wenzi Bingbian*, plate `0529`;
- digitization and management: Institute of History and Philology;
- image reuse: requires an IHP collection-image authorization request.

成功打开的记录报告：

- 题名：`甲骨文拓片（登錄號：188493-0529）`；
- 类型：`甲骨刻辭`、静态图像；
- 分期：商后期第一期；
- 原拓尺寸：`19.23 x 13.79 cm`；
- 出处：《小屯第二本殷虛文字丙編》图版 `0529`；
- 数字化与管理单位：中央研究院历史语言研究所；
- 图像使用：须申请史语所藏品图像授权。

## Access Receipts / 访问回执

### Successful separate acquisition

- Record URL:
  <https://sinica.digitalarchives.tw/collection_3041293.html>
- Final record host: `ascdc.digitalarchives.tw`.
- Record bytes: `27015`.
- Record SHA-256:
  `00921964c0bbf0e391830f53bbc82c4b5bec50b36fc6243984462a6a9b0919e2`.
- Rubbing URL:
  <https://image.digitalarchives.tw/ImageCache/00/72/70/d9.jpg>
- Rubbing bytes: `69781`; JPEG, RGB, `366 x 500` pixels.
- Rubbing SHA-256:
  `1264db7947ec39474d3c76a19ff58dc5f9ab7bf55499834fbebfcc4ffadb6b48`.
- Storage: inspected in memory; not committed and not retained locally.

### Root rerun failure

The root rerun first failed because the TLS certificate was reported expired.
An explicit certificate-bypass diagnostic then returned the same access-block
HTML for both record and image URLs. It was `36917` bytes with SHA-256
`6465bc25b5527f4605db42effef880065e97ee6553bcfc5a68674480f7215781`.

根 Agent 复跑首先因 TLS certificate 过期而失败。显式绕过证书只用于
诊断，随后记录页和图像页都返回同一访问阻断 HTML。该响应不是拓片，
不得当作成功回执或图像证据。

## Crosswalk Test / 交叉检验

The museum page reports:

- item `503`;
- accession `R044498`;
- title `帶卜辭龜腹甲《丙》0529`;
- object dimensions `17.4 x 13.8 cm`;
- Late Shang, YH127 at Hsiao-t'un, tortoise plastron;
- source phrase `帝令雨` and a short explanatory gloss.

博物馆页报告 503 号、馆藏号 `R044498`、题名
`帶卜辭龜腹甲《丙》0529`、实物尺寸 `17.4 x 13.8 cm`、晚商、
小屯 YH127 坑、龟腹甲，以及来源短语 `帝令雨`。

Both routes share the institution and `《丙》0529`, but neither page lists
the other page's accession number. The result is an
institution-internal crosswalk candidate, not independent confirmation.

两页共享机构和 `《丙》0529`，但都没有列出另一页的登记号。因此当前
结果是机构内交叉候选，不是独立来源确认。

## Counterevidence And Dependency / 反证与依赖

- `19.23 x 13.79 cm` measures the original rubbing.
- `17.4 x 13.8 cm` measures the physical object.
- This is not a dimension conflict, and the values cannot be substituted.
- “Late Shang” and “late Shang, Period I” have different granularity and
  come from the same evidence family; they are not independent dating votes.
- `帝令雨` is museum source prose, not a full transcription, line order,
  reading history, or project translation.
- A public rubbing route does not prove that the displayed plate and museum
  object are geometrically registered.

- `19.23 x 13.79 cm` 是原拓尺寸。
- `17.4 x 13.8 cm` 是实物尺寸。
- 二者不是尺寸冲突，也不得相互替代。
- “晚商”与“商后期第一期”粒度不同，且属于同一证据家族，不能作为
  两票独立断代证据。
- `帝令雨` 是馆方来源说明，不是完整释文、行序、释读史或项目翻译。
- 公开拓片路线不能证明图版与馆藏实物已经完成几何配准。

The museum, digital archive, institutional weekly page, and *Bingbian* route
share IHP, YH127, or plate ancestry. They must remain one dependency-labelled
evidence family unless an external catalog independently confirms the link.

博物馆、数字典藏、馆方周记和《丙编》路线共享史语所、YH127 或图版
祖先。外部著录独立确认前，它们必须保持为同一证据家族。

## Rights Boundary / 权利边界

公开访问不等于再分发许可。数字典藏页要求申请史语所藏品图像授权；
本项目不提交该拓片字节，也不把公开 URL 当成 AI 训练许可。

Authorization route:
<https://copyright.ihp.sinica.edu.tw/ihponlinec/ihponline>

## Decision / 裁决

- C1 object crosswalk: blocked; institution-internal candidate route only.
- C2 image route: separately opened in one acquisition attempt; root rerun
  failed.
- C4 inscription context: source phrase only; incomplete.
- C5--C7: blocked.
- C8 delivery: `withhold`.
- Formal identity, transcription, and reading: not assigned.

- C1 对象交叉：阻断；仅保留机构内交叉候选路线。
- C2 图像路线：一次单独采集尝试成功打开；根 Agent 复跑失败。
- C4 卜辞上下文：只有来源短语，不完整。
- C5--C7：阻断。
- C8 交付：`withhold`。
- 正式身份、释文和释读：未分配。

## Decisive Next Sources / 下一决定性来源

1. Ask IHP to confirm `R044498` to `188493-0529` to `《丙》0529` in writing.
2. Request research and derivative-image permission through the official
   authorization system.
3. Obtain the exact page, rubbing, transcription, commentary, and contrary
   readings for entry 0529 in the revised *Bingbian* publication.
4. Compare object and rubbing with rigid, non-deforming registration only.

1. 请史语所书面确认 `R044498`、`188493-0529`、`《丙》0529` 的关系。
2. 通过官方系统申请研究使用和派生图像许可。
3. 取得新版《丙编》0529 条的页码、拓片、摹写、释文、考释和异说。
4. 只能使用刚性、无变形配准比较实物与拓片。

## Boundary / 边界

This is a source crosswalk and rights dossier. It is not a confirmed object
identity, plate identity, full transcription, reading, or decipherment.

本档案是来源交叉和权利档案，不是已确认实物身份、图版身份、完整释文、
释读或破译结果。
