# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 6491
- Images without direct records / 有图无观察: 4505
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 with direct visual reco
  rds
- undeciphered_candidate: 9408 objects; 9408 with images; 4903 with direct visua
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

- obs-unk-004897: corpus/001_oracle-characters/065_undeciphered-004801-004900_ob
  s-unk-bucket_oracle-character-candidates/097_obs-unk-004897_hust-obc-und-X-004
  897_oracle-character-candidate
- obs-unk-004898: corpus/001_oracle-characters/065_undeciphered-004801-004900_ob
  s-unk-bucket_oracle-character-candidates/098_obs-unk-004898_hust-obc-und-X-004
  898_oracle-character-candidate
- obs-unk-004899: corpus/001_oracle-characters/065_undeciphered-004801-004900_ob
  s-unk-bucket_oracle-character-candidates/099_obs-unk-004899_hust-obc-und-X-004
  899_oracle-character-candidate
- obs-unk-004900: corpus/001_oracle-characters/065_undeciphered-004801-004900_ob
  s-unk-bucket_oracle-character-candidates/100_obs-unk-004900_hust-obc-und-X-004
  900_oracle-character-candidate
- obs-unk-004901: corpus/001_oracle-characters/066_undeciphered-004901-005000_ob
  s-unk-bucket_oracle-character-candidates/001_obs-unk-004901_hust-obc-und-X-004
  901_oracle-character-candidate
- obs-unk-004902: corpus/001_oracle-characters/066_undeciphered-004901-005000_ob
  s-unk-bucket_oracle-character-candidates/002_obs-unk-004902_hust-obc-und-X-004
  902_oracle-character-candidate
- obs-unk-004903: corpus/001_oracle-characters/066_undeciphered-004901-005000_ob
  s-unk-bucket_oracle-character-candidates/003_obs-unk-004903_hust-obc-und-X-004
  903_oracle-character-candidate
- obs-unk-004904: corpus/001_oracle-characters/066_undeciphered-004901-005000_ob
  s-unk-bucket_oracle-character-candidates/004_obs-unk-004904_hust-obc-und-X-004
  904_oracle-character-candidate
- obs-unk-004905: corpus/001_oracle-characters/066_undeciphered-004901-005000_ob
  s-unk-bucket_oracle-character-candidates/005_obs-unk-004905_hust-obc-und-X-004
  905_oracle-character-candidate
- obs-unk-004906: corpus/001_oracle-characters/066_undeciphered-004901-005000_ob
  s-unk-bucket_oracle-character-candidates/006_obs-unk-004906_hust-obc-und-X-004
  906_oracle-character-candidate
- obs-unk-004907: corpus/001_oracle-characters/066_undeciphered-004901-005000_ob
  s-unk-bucket_oracle-character-candidates/007_obs-unk-004907_hust-obc-und-X-004
  907_oracle-character-candidate
- obs-unk-004908: corpus/001_oracle-characters/066_undeciphered-004901-005000_ob
  s-unk-bucket_oracle-character-candidates/008_obs-unk-004908_hust-obc-und-X-004
  908_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
