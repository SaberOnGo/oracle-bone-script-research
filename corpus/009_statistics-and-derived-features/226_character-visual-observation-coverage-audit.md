# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 4895
- Images without direct records / 有图无观察: 6101
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 with direct visual reco
  rds
- undeciphered_candidate: 9408 objects; 9408 with images; 3307 with direct visua
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

- obs-unk-003301: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/001_obs-unk-003301_hust-obc-und-L-003
  301_oracle-character-candidate
- obs-unk-003302: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/002_obs-unk-003302_hust-obc-und-L-003
  302_oracle-character-candidate
- obs-unk-003303: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/003_obs-unk-003303_hust-obc-und-L-003
  303_oracle-character-candidate
- obs-unk-003304: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/004_obs-unk-003304_hust-obc-und-L-003
  304_oracle-character-candidate
- obs-unk-003305: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/005_obs-unk-003305_hust-obc-und-L-003
  305_oracle-character-candidate
- obs-unk-003306: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/006_obs-unk-003306_hust-obc-und-L-003
  306_oracle-character-candidate
- obs-unk-003307: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/007_obs-unk-003307_hust-obc-und-L-003
  307_oracle-character-candidate
- obs-unk-003308: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/008_obs-unk-003308_hust-obc-und-L-003
  308_oracle-character-candidate
- obs-unk-003309: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/009_obs-unk-003309_hust-obc-und-L-003
  309_oracle-character-candidate
- obs-unk-003310: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/010_obs-unk-003310_hust-obc-und-L-003
  310_oracle-character-candidate
- obs-unk-003311: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/011_obs-unk-003311_hust-obc-und-L-003
  311_oracle-character-candidate
- obs-unk-003312: corpus/001_oracle-characters/050_undeciphered-003301-003400_ob
  s-unk-bucket_oracle-character-candidates/012_obs-unk-003312_hust-obc-und-L-003
  312_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
