# Claim Evidence Gate Review / 命题证据门槛复核

## English

This page applies the project claim matrix to
`obs-insc-src-cand-000009` on 2026-08-21. It is a delivery-gate record,
not a reading, translation, character assignment, or scholarly conclusion.

### Evidence states

- `E1` is the Met API object route and registry checksum. It is
  `source_reported` for the museum metadata and does not prove the physical
  catalog history.
- `E2` is `03_visual-assets/001_asset-021414...jpg`, directly checked and
  checksum-bound to the API `primaryImage` route.
- `E3` is `03_visual-assets/002_asset-021415...jpg`, directly checked and
  checksum-bound to `additionalImages[0]`.
- `E4` is the neutral two-view observation in `09_two-view-human-evidence.md`.

### Claim dispositions

- `C1 object identity`: `blocked`. The API gives object `42022` and accession
  `18.56.71`, but a plate, collection history, findspot, and physical-object
  chain remain unverified.
- `C2 direct glyph observation`: `direct_checked`. E2 and E3 support neutral
  notes about bone surface, marks, pores, cracks, wear, and lighting. Neither
  image establishes orientation or reading order.
- `C3 sign, variant, near-form, or component`: `blocked`. No sign regions,
  comparison family, damage-aware alignment, or non-label support is fixed.
- `C4 inscription occurrence and context`: `blocked`. No plate locator,
  occurrence ID, full text, neighbours, line order, or catalog edition is
  available.
- `C5 reading or phonological candidate`: `blocked` by C4, reading history,
  proposer, alternatives, and positive/negative text evidence.
- `C6 semantic or grammatical function`: `blocked` by C5 and missing sentence,
  grammar, archaeological, and disagreement evidence.
- `C7 diachronic correspondence`: `blocked`. No period-provenanced comparison
  forms or bridge argument beyond visual resemblance are fixed.
- `C8 complete proposition and user delivery`: `withheld`. Calibration,
  independent rerun, external scoring, and the C1--C7 blockers are absent.

### Concrete next-source questions

1. Which Met catalog, accession file, or authorized collection record fixes the
   object history, orientation, and any plate or publication number?
2. Which permitted plate or line-addressable transcription identifies each
   visible mark and its neighbouring signs?
3. Which independent source family supplies comparison forms and a dated
   reading history without reusing the same API image or label?
4. Which rights statement permits any future cropped or region-level delivery?

No numerical decipherment probability is estimated. The object remains a
source-record candidate with
`assignment_status=reserved_candidate_not_assigned` and no user-facing
candidate delivery.

## 简体中文

本页把项目命题矩阵应用于 `obs-insc-src-cand-000009`，日期为
2026-08-21。它是交付门槛记录，不是释读、翻译、单字分配或学术结论。

### 证据状态

- `E1` 是大都会 API 对象路线和登记表 checksum。它对博物馆 metadata
  属于 `source_reported`，不证明实物著录史。
- `E2` 是 `03_visual-assets/001_asset-021414...jpg`，已直接打开，且与
  API 的 `primaryImage` 路线绑定。
- `E3` 是 `03_visual-assets/002_asset-021415...jpg`，已直接打开，且与
  `additionalImages[0]` 路线绑定。
- `E4` 是 `09_two-view-human-evidence.md` 中的中性双图观察。

### 命题处置

- `C1 对象身份`：`blocked`。API 给出对象 42022 和馆藏号 `18.56.71`，
  但图版、收藏史、出土地和实物链仍未核实。
- `C2 直接字形观察`：`direct_checked`。E2、E3 支持对骨面、刻痕、孔隙、
  裂纹、磨损和光照的中性记录，但不能确定方向或阅读顺序。
- `C3 同字、异体、近形或构件`：`blocked`。尚无字区、比较家族、考虑残损
  的对齐或非标签支持。
- `C4 卜辞字例与上下文`：`blocked`。尚无图版定位、字例 ID、全文、邻字、
  行序或著录版本。
- `C5 读音或隶定候选`：因 C4、释读史、提出者、替代读法和文本正反证缺失，
  `blocked`。
- `C6 语义或语法功能`：因 C5 以及句子、语法、考古和争议证据缺失，
  `blocked`。
- `C7 历时字形对应`：`blocked`。尚无带时期来源的比较字形，也无超越视觉
  相似的桥梁论证。
- `C8 完整命题与用户交付`：`withheld`。校准、独立复跑、外部评分和 C1--C7
  阻断项均未完成。

### 具体下一来源问题

1. 哪一份大都会著录、入藏档案或获准馆藏记录能固定对象历史、方向以及图版
   或出版编号？
2. 哪一份获准图版或可定位逐行释文能识别可见刻痕及其邻字？
3. 哪个独立来源家族能在不重复 API 图像或标签的前提下提供比较字形和有日期
   的释读史？
4. 哪条权利说明允许未来提交裁切图或区域级派生物？

没有估计任何破译概率。本对象仍是来源记录候选，使用
`assignment_status=reserved_candidate_not_assigned`，没有面向用户的候选
交付。

[matrix]: ../../../../doc/project/005_ai-agent-research-assistant-design/
