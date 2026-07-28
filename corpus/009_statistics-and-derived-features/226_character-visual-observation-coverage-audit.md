# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 2175
- Images without direct records / 有图无观察: 8821
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 with direct visual reco
  rds
- undeciphered_candidate: 9408 objects; 9408 with images; 587 with direct visual
   records

## What The Gap Means / 缺口含义

- English: A local derivative proves only that an image was extracted. The 14_ma
  terial-visual-observation.md record is the separate human-readable trace of ne
  utral marks seen in that image.
- 中文: 本地派生件只能证明图像已经抽取。14_material-visual-observation.md 才是记录图像中直接可见中性痕迹的人类档案。

## Human Opening Order / 人工开包顺序

- Open the concrete object README and 04_visual-gallery.md.
- Open the image and 02_visual-source-index.csv together.
- Record only visible shape, damage, orientation, contrast, and limits.
- Keep identity, component, reading, and inscription links pending.
- Record the reviewer, date, image path, source route, rights, and risk.
- 先打开具体对象 README 和 04_visual-gallery.md。
- 同时打开图像和 02_visual-source-index.csv。
- 只记录形态、残损、方向、对比度和观察边界。
- 字形身份、构件、释读和卜辞关联继续保持待复核。
- 记录复核人、日期、图像路径、来源路线、权利和风险。

## Representative Missing Routes / 代表性缺口路线

- obs-unk-000481: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/081_obs-unk-000481_hust-obc-und-L-000
  481_oracle-character-candidate
- obs-unk-000482: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/082_obs-unk-000482_hust-obc-und-L-000
  482_oracle-character-candidate
- obs-unk-000483: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/083_obs-unk-000483_hust-obc-und-L-000
  483_oracle-character-candidate
- obs-unk-000484: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/084_obs-unk-000484_hust-obc-und-L-000
  484_oracle-character-candidate
- obs-unk-000485: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/085_obs-unk-000485_hust-obc-und-L-000
  485_oracle-character-candidate
- obs-unk-000486: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/086_obs-unk-000486_hust-obc-und-L-000
  486_oracle-character-candidate
- obs-unk-000487: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/087_obs-unk-000487_hust-obc-und-L-000
  487_oracle-character-candidate
- obs-unk-000488: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/088_obs-unk-000488_hust-obc-und-L-000
  488_oracle-character-candidate
- obs-unk-000489: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/089_obs-unk-000489_hust-obc-und-L-000
  489_oracle-character-candidate
- obs-unk-000490: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/090_obs-unk-000490_hust-obc-und-L-000
  490_oracle-character-candidate
- obs-unk-000491: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/091_obs-unk-000491_hust-obc-und-L-000
  491_oracle-character-candidate
- obs-unk-000492: corpus/001_oracle-characters/021_undeciphered-000401-000500_ob
  s-unk-bucket_oracle-character-candidates/092_obs-unk-000492_hust-obc-und-L-000
  492_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
