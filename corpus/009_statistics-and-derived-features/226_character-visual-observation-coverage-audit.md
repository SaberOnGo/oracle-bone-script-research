# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 6595
- Pixel profile records / 像素 profile 记录: 4401
- Images without direct records / 有图无人工观察: 4401
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 direct records; 0 pixel
   profiles
- undeciphered_candidate: 9408 objects; 9408 with images; 5007 direct records; 4
  401 pixel profiles

## What The Gap Means / 缺口含义

- English: A local derivative proves only that an image was extracted. A pixel p
  rofile is still not a human visual observation; the object-local note routes t
  he next image review.
- 中文: 本地派生件只能证明图像已经抽取。像素 profile 不是人工观察，对象内档案只负责引导下一次图像复核。

## Human Opening Order / 人工开包顺序

- Open the concrete object README and 04_visual-gallery.md.
- Open the image and 02_visual-source-index.csv together.
- Treat a pixel profile as routing evidence, not a human observation.
- Record only visible shape, damage, orientation, contrast, and limits.
- Keep identity, component, reading, and inscription links pending.
- Record the reviewer, date, image path, source route, rights, and risk.
- 先打开具体对象 README 和 04_visual-gallery.md。
- 同时打开图像和 02_visual-source-index.csv。
- 像素 profile 只作路线证据，不等于人工图像观察。
- 只记录形态、残损、方向、对比度和观察边界。
- 字形身份、构件、释读和卜辞关联继续保持待复核。
- 记录复核人、日期、图像路径、来源路线、权利和风险。

## Representative Missing Routes / 代表性缺口路线

- obs-unk-005001: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/001_obs-unk-005001_hust-obc-und-X-005
  001_oracle-character-candidate
- obs-unk-005002: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/002_obs-unk-005002_hust-obc-und-X-005
  002_oracle-character-candidate
- obs-unk-005003: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/003_obs-unk-005003_hust-obc-und-X-005
  003_oracle-character-candidate
- obs-unk-005004: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/004_obs-unk-005004_hust-obc-und-X-005
  004_oracle-character-candidate
- obs-unk-005005: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/005_obs-unk-005005_hust-obc-und-X-005
  005_oracle-character-candidate
- obs-unk-005006: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/006_obs-unk-005006_hust-obc-und-X-005
  006_oracle-character-candidate
- obs-unk-005007: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/007_obs-unk-005007_hust-obc-und-X-005
  007_oracle-character-candidate
- obs-unk-005008: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/008_obs-unk-005008_hust-obc-und-X-005
  008_oracle-character-candidate
- obs-unk-005009: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/009_obs-unk-005009_hust-obc-und-X-005
  009_oracle-character-candidate
- obs-unk-005010: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/010_obs-unk-005010_hust-obc-und-X-005
  010_oracle-character-candidate
- obs-unk-005011: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/011_obs-unk-005011_hust-obc-und-X-005
  011_oracle-character-candidate
- obs-unk-005012: corpus/001_oracle-characters/067_undeciphered-005001-005100_ob
  s-unk-bucket_oracle-character-candidates/012_obs-unk-005012_hust-obc-und-X-005
  012_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into human observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
