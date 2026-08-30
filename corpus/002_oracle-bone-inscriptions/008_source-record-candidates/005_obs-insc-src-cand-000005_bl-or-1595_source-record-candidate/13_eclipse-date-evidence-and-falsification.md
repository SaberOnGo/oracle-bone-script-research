# Eclipse Date Evidence And Falsification / 月食年代证据与反证

## Purpose / 目的

This dossier tests whether the `1192 BCE` and `1166 BCE` routes are competing
answers to the same proposition. It binds exact network receipts and timing
inputs. It does not choose a date or authenticate an inscription.

本档案检验 `1192 BCE` 与 `1166 BCE` 两条路线是否在回答同一命题，并
绑定精确网络回执和时间输入。本文不选择年代，也不鉴定刻辞真伪。

## Evidence Receipts / 证据回执

### Goodliffe 2016 route

- Object scope: `Or. 7694/1595 / Yingcang 886`.
- Source claim: the event occurred on 27 December `1192 BCE`.
- Source timing: totality at Anyang was reported as `21:48--23:30`, with
  uncertainty of about 17 minutes.
- Inscription relation: the page says CUL 1 / Yingcang 885 refers to the same
  eclipse, but does not publish an object-to-object proof.
- First checked: `2026-08-14`.
- Snapshot retrieved: `2026-08-30`; HTTP `200`, `text/html`.
- TLS status: not separately recorded by the successful client.
- Ignored receipt: `.working/bl-1595-eclipse-20260830/`
  `goodliffe-2016-scroll.html`.
- Bytes: `135946`.
- SHA-256:
  `7cbe34af8de639913e3146ce3ba0fd99e559efc510158d36088ba6e16460a25b`.

- 对象范围：`Or. 7694/1595 / Yingcang 886`。
- 来源主张：事件发生于公元前 `1192` 年 12 月 27 日。
- 来源时间：安阳所见月全食阶段约为 `21:48--23:30`，误差约 17 分钟。
- 卜辞关系：页面称 CUL 1 /《英藏》885 记录同一次月食，但没有发表两件
  对象之间的证明。

### Liu 2014 route

- Object scope: `Yingcang 885/886` as a paired argument.
- Source claim: within 1400--1148 BCE, only 14 August `1166 BCE` fits the
  time and ganzhi conditions used by the article.
- Source timing premise: the paired records describe an eclipse beginning
  after midnight and ending shortly after sunrise.
- Open material: Cambridge metadata, bilingual abstract, and displayed
  notes, including a note about a damaged `ri` graph on Yingcang 885.
- Closed material: the full pages `15--38`, plates, calculation steps, and
  the article's complete transcription were not obtained.
- First checked: `2026-08-14`.
- Last direct download attempt: `2026-08-30`; HTTP `429`, no content type,
  no local snapshot, and no separately recorded TLS error.

- 对象范围：论文把《英藏》885/886 作为一组论证。
- 来源主张：在公元前 1400--1148 年之间，只有公元前 `1166` 年
  8 月 14 日满足论文采用的时间与干支条件。
- 来源时间前提：两片记录的是午夜后开始、日出后不久结束的月食。
- 已打开材料：Cambridge 书目信息、双语摘要和页面公开注释；其中一条
  注释讨论《英藏》885 上残损的 `日` 字形。
- 未打开材料：全文第 `15--38` 页、图版、计算步骤及完整释文。

### Ma and others 2021 DE422 route

- Scope: five dated eclipse inscriptions accepted by the Xia-Shang-Zhou
  Chronology Project; the page maps `己未夕皿庚申月食` to `1192 BCE`.
- Method: JPL `DE422`, an explicit Delta T model, and Anyang coordinates.
- Delta T for the 1192 case: `28,837` seconds with error `+/-1,042` seconds.
- Anyang local totality: `21:50:46--23:33:29`.
- Partial phase ended: `00:38:26`; penumbral phase ended: `00:50:20`.
- Reported sunrise: `07:14:32`.
- Accessed: `2026-08-30`.
- Ignored receipt: `.working/bl-1595-eclipse-20260830/`
  `ma-et-al-2021-de422.html`.
- Bytes: `56776`.
- SHA-256:
  `959635a3fa40b7ac376f75da3fbe828d4e4f12217a46f1f16a1f0880ff832bed`.

- 范围：夏商周断代工程采用的五条纪日月食；页面把
  `己未夕皿庚申月食` 对应到公元前 `1192` 年。
- 方法：JPL `DE422`、明确的 Delta T 模型和安阳坐标。
- 1192 年案例的 Delta T：`28,837` 秒，误差 `+/-1,042` 秒。
- 安阳当地全食：`21:50:46--23:33:29`。
- 偏食结束：`00:38:26`；半影食结束：`00:50:20`。
- 来源报告日出：`07:14:32`。

## Proposition Audit / 命题审计

The three routes are not the same tested proposition.

三条路线不是同一个受检命题。

The 1192 route tests whether the `己未` to `庚申` record can match an eclipse
visible at Anyang during the night. The checked DE422 route has all phases
ending more than six hours before its reported sunrise.

1192 路线检验 `己未` 至 `庚申` 的记录能否对应安阳夜间可见月食。已打开
的 DE422 路线显示全部食相在其报告日出前六小时以上结束。

The 1166 abstract tests a stronger timing proposition over the paired
Yingcang 885/886 records: beginning after midnight and ending after sunrise.
The current project has neither the full article nor the 885 plate needed to
reconstruct how those constraints were obtained.

1166 摘要检验的是更强命题：把《英藏》885/886 合并后，月食在午夜后
开始、日出后结束。本项目尚无全文和 885 图版，不能复原这些约束如何
从两片材料得出。

Therefore the DE422 timing countercheck falsifies only the silent assumption
that both routes use identical inputs. It does not falsify either historical
date by itself.

因此，DE422 时间反查只推翻“两条路线输入完全相同”这一静默假定，不能
单独推翻任一历史年代。

## Calendar And Dependency Controls / 历法与依赖控制

The astronomical year for `1192 BCE` is `-1191`; for `1166 BCE` it is
`-1165`. A rerun must record this conversion and must not compare a negative
astronomical year directly with an unconverted BCE label.

公元前 `1192` 年的 astronomical year 是 `-1191`；公元前 `1166` 年是
`-1165`。复算必须记录这一换算，不得把负天文年直接与未换算 BCE 标签
比较。

Goodliffe, the British Library display, Commons, and Google Arts and Culture
share a British Library object ancestry. They are one evidence family. The
2021 paper partly tests the chronology-project date rather than supplying an
independent paleographic identification.

Goodliffe、大英图书馆展示、Commons 和 Google Arts and Culture 共享
大英图书馆对象祖先，只能算一个证据家族。2021 年论文部分检验断代工程
给定年代，不提供独立文字学身份确认。

The catalogue's twentieth-century addition warning remains a separate hard
risk. Neither an astronomical fit nor a source count resolves authenticity.

馆藏目录的 twentieth-century addition 警示仍是独立硬风险。天文吻合或
来源票数都不能解决真伪问题。

## Strongest Alternative / 最强替代解释

The strongest alternative is that 885 and 886 contain complementary timing
information, or that Liu's transcription and syntax derive a dawn condition
not used by the 1192 route. Another possibility is that one route silently
maps a different line or side. These alternatives remain live until both
plates and the full argument are opened.

最强替代解释是：885 与 886 提供互补时间信息，或 Liu 的释文和句法得出
1192 路线没有采用的黎明条件。另一可能是某条路线静默映射了不同辞条或
不同面。两张图版和全文打开前，这些替代解释都保留。

## Decision / 裁决

- Object identity: limited candidate; plate crosswalk remains open.
- Date comparison: `withhold`.
- Reading and syntax: `withhold`.
- Calibrated probability: not available.
- Current source-route observation: the two public date routes currently use
  different object scopes and timing premises.

- 对象身份：有限候选；图版交叉仍待核。
- 年代比较：`withhold`。
- 释读与句法：`withhold`。
- 校准概率：不可用。
- 当前来源路线观察：两条公开年代路线采用不同对象范围与时间前提。

## Decisive Next Sources / 下一决定性来源

1. Open Liu 2014 pages `15--38` through a permitted route.
2. Open Yingcang 885 and 886 plus Heji 40610 with exact plate locators.
3. Bind every timing premise to a specific line, side, and graph reading.
4. Recompute both dates only after the proposition inputs are identical.
5. Keep the modern-addition risk in every later adjudication.

1. 通过许可路线打开 Liu 2014 第 `15--38` 页。
2. 打开《英藏》885、886 和《合集》40610 的确切图版。
3. 把每项时间前提绑定到具体辞条、面和字形释读。
4. 只有命题输入完全一致后，才复算两个年代。
5. 后续每次裁决都保留现代增刻风险。

## Boundary / 边界

This is a falsification and source-comparison dossier. It is not a verified
date, transcription, translation, authentication, or decipherment result.

本档案用于反证和来源比较，不是已核实年代、释文、翻译、真伪鉴定或
破译结果。

[goodliffe]: https://scroll.in/article/801747/
[liu]: https://doi.org/10.1017/eac.2014.10
[ma-2021]: https://html.rhhz.net/Jwk_twyjyjs/html/20210415.htm
