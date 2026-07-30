# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 3959
- Images without direct records / 有图无观察: 7037
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 with direct visual reco
  rds
- undeciphered_candidate: 9408 objects; 9408 with images; 2371 with direct visua
  l records

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

- obs-unk-002365: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/065_obs-unk-002365_hust-obc-und-L-002
  365_oracle-character-candidate
- obs-unk-002366: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/066_obs-unk-002366_hust-obc-und-L-002
  366_oracle-character-candidate
- obs-unk-002367: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/067_obs-unk-002367_hust-obc-und-L-002
  367_oracle-character-candidate
- obs-unk-002368: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/068_obs-unk-002368_hust-obc-und-L-002
  368_oracle-character-candidate
- obs-unk-002369: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/069_obs-unk-002369_hust-obc-und-L-002
  369_oracle-character-candidate
- obs-unk-002370: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/070_obs-unk-002370_hust-obc-und-L-002
  370_oracle-character-candidate
- obs-unk-002371: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/071_obs-unk-002371_hust-obc-und-L-002
  371_oracle-character-candidate
- obs-unk-002372: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/072_obs-unk-002372_hust-obc-und-L-002
  372_oracle-character-candidate
- obs-unk-002373: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/073_obs-unk-002373_hust-obc-und-L-002
  373_oracle-character-candidate
- obs-unk-002374: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/074_obs-unk-002374_hust-obc-und-L-002
  374_oracle-character-candidate
- obs-unk-002375: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/075_obs-unk-002375_hust-obc-und-L-002
  375_oracle-character-candidate
- obs-unk-002376: corpus/001_oracle-characters/040_undeciphered-002301-002400_ob
  s-unk-bucket_oracle-character-candidates/076_obs-unk-002376_hust-obc-und-L-002
  376_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
