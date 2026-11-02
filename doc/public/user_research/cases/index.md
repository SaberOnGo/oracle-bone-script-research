# 研究案件索引 / Research Case Index

简体中文：
本索引登记全部研究案件。案件文件放在对象目录内，这里只记一行：命题、
当前状态、对象位置和下一个决定性来源。写法见
[Agent 工作协议][protocol]第 5 节。

English:
This index lists every research case. Case files live in their object
directories; this page keeps one line per case. See section 5 of the
[agent operating protocol][protocol].

## 活跃案件 / Active Cases

| 案件 | 命题 | 状态 | 对象位置 | 下一个决定性来源 |
| --- | --- | --- | --- | --- |
| `case-hyz421` | 花东 421 卜辞是否为"避雨"之占 | C4 文本基线成立；释义 `withhold` | `corpus/002_oracle-bone-inscriptions/008_source-record-candidates/007_*` | 韩江苏著作第 350--354 页 |
| `case-h2-heji2` | OBIMD H2 是否即《合集》2 | C1 强对象身份候选 | `corpus/002_oracle-bone-inscriptions/008_source-record-candidates/001_*` | 国图实物条目导出及连接全部编号的书面来源 |
| `case-obs-unk-005708` | HUST 未释类 X/1264 的 50 个成员是否同一字 | C2 视觉观察；混组争议；C8 `withhold` | `corpus/001_oracle-characters/074_*/008_obs-unk-005708_*` | 史语所 `fsnrb188477-3472` 授权完整图版及 `U61812` 字位 |

案件状态以 2026-08-30 运行基线为准，见
`doc/project/005_ai-agent-research-assistant-design/`
`04_current-operating-baseline-2026-08-30-ihp-anchor.md`。

Case states follow the 2026-08-30 operating baseline listed above.

## 盲测记录 / Calibration Rounds

`calibration/` 目录保存已释字盲测，每轮一个文件。目前尚无记录。

The `calibration/` directory holds masked-known rounds, one file per round.
No round has been run yet.

[protocol]: ../../../project/007_architecture-reset-and-human-first-knowledge-base/
