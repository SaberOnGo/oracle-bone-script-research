# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 2555
- Images without direct records / 有图无观察: 8441
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 with direct visual reco
  rds
- undeciphered_candidate: 9408 objects; 9408 with images; 967 with direct visual
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

- obs-unk-000861: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/061_obs-unk-000861_hust-obc-und-L-000
  861_oracle-character-candidate
- obs-unk-000862: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/062_obs-unk-000862_hust-obc-und-L-000
  862_oracle-character-candidate
- obs-unk-000863: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/063_obs-unk-000863_hust-obc-und-L-000
  863_oracle-character-candidate
- obs-unk-000864: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/064_obs-unk-000864_hust-obc-und-L-000
  864_oracle-character-candidate
- obs-unk-000865: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/065_obs-unk-000865_hust-obc-und-L-000
  865_oracle-character-candidate
- obs-unk-000866: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/066_obs-unk-000866_hust-obc-und-L-000
  866_oracle-character-candidate
- obs-unk-000867: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/067_obs-unk-000867_hust-obc-und-L-000
  867_oracle-character-candidate
- obs-unk-000868: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/068_obs-unk-000868_hust-obc-und-L-000
  868_oracle-character-candidate
- obs-unk-000869: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/069_obs-unk-000869_hust-obc-und-L-000
  869_oracle-character-candidate
- obs-unk-000870: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/070_obs-unk-000870_hust-obc-und-L-000
  870_oracle-character-candidate
- obs-unk-000871: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/071_obs-unk-000871_hust-obc-und-L-000
  871_oracle-character-candidate
- obs-unk-000872: corpus/001_oracle-characters/025_undeciphered-000801-000900_ob
  s-unk-bucket_oracle-character-candidates/072_obs-unk-000872_hust-obc-und-L-000
  872_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
