# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 5939
- Images without direct records / 有图无观察: 5057
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 with direct visual reco
  rds
- undeciphered_candidate: 9408 objects; 9408 with images; 4351 with direct visua
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

- obs-unk-004345: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/045_obs-unk-004345_hust-obc-und-L-004
  345_oracle-character-candidate
- obs-unk-004346: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/046_obs-unk-004346_hust-obc-und-L-004
  346_oracle-character-candidate
- obs-unk-004347: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/047_obs-unk-004347_hust-obc-und-L-004
  347_oracle-character-candidate
- obs-unk-004348: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/048_obs-unk-004348_hust-obc-und-L-004
  348_oracle-character-candidate
- obs-unk-004349: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/049_obs-unk-004349_hust-obc-und-L-004
  349_oracle-character-candidate
- obs-unk-004350: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/050_obs-unk-004350_hust-obc-und-L-004
  350_oracle-character-candidate
- obs-unk-004351: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/051_obs-unk-004351_hust-obc-und-L-004
  351_oracle-character-candidate
- obs-unk-004352: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/052_obs-unk-004352_hust-obc-und-L-004
  352_oracle-character-candidate
- obs-unk-004353: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/053_obs-unk-004353_hust-obc-und-L-004
  353_oracle-character-candidate
- obs-unk-004354: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/054_obs-unk-004354_hust-obc-und-L-004
  354_oracle-character-candidate
- obs-unk-004355: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/055_obs-unk-004355_hust-obc-und-L-004
  355_oracle-character-candidate
- obs-unk-004356: corpus/001_oracle-characters/060_undeciphered-004301-004400_ob
  s-unk-bucket_oracle-character-candidates/056_obs-unk-004356_hust-obc-und-L-004
  356_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
