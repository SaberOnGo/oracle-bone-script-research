# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 3555
- Images without direct records / 有图无观察: 7441
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 with direct visual reco
  rds
- undeciphered_candidate: 9408 objects; 9408 with images; 1967 with direct visua
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

- obs-unk-001961: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/061_obs-unk-001961_hust-obc-und-L-001
  961_oracle-character-candidate
- obs-unk-001962: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/062_obs-unk-001962_hust-obc-und-L-001
  962_oracle-character-candidate
- obs-unk-001963: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/063_obs-unk-001963_hust-obc-und-L-001
  963_oracle-character-candidate
- obs-unk-001964: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/064_obs-unk-001964_hust-obc-und-L-001
  964_oracle-character-candidate
- obs-unk-001965: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/065_obs-unk-001965_hust-obc-und-L-001
  965_oracle-character-candidate
- obs-unk-001966: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/066_obs-unk-001966_hust-obc-und-L-001
  966_oracle-character-candidate
- obs-unk-001967: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/067_obs-unk-001967_hust-obc-und-L-001
  967_oracle-character-candidate
- obs-unk-001968: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/068_obs-unk-001968_hust-obc-und-L-001
  968_oracle-character-candidate
- obs-unk-001969: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/069_obs-unk-001969_hust-obc-und-L-001
  969_oracle-character-candidate
- obs-unk-001970: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/070_obs-unk-001970_hust-obc-und-L-001
  970_oracle-character-candidate
- obs-unk-001971: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/071_obs-unk-001971_hust-obc-und-L-001
  971_oracle-character-candidate
- obs-unk-001972: corpus/001_oracle-characters/036_undeciphered-001901-002000_ob
  s-unk-bucket_oracle-character-candidates/072_obs-unk-001972_hust-obc-und-L-001
  972_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
