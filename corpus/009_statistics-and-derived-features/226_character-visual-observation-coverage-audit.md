# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 2435
- Images without direct records / 有图无观察: 8561
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 with direct visual reco
  rds
- undeciphered_candidate: 9408 objects; 9408 with images; 847 with direct visual
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

- obs-unk-000741: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/041_obs-unk-000741_hust-obc-und-L-000
  741_oracle-character-candidate
- obs-unk-000742: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/042_obs-unk-000742_hust-obc-und-L-000
  742_oracle-character-candidate
- obs-unk-000743: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/043_obs-unk-000743_hust-obc-und-L-000
  743_oracle-character-candidate
- obs-unk-000744: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/044_obs-unk-000744_hust-obc-und-L-000
  744_oracle-character-candidate
- obs-unk-000745: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/045_obs-unk-000745_hust-obc-und-L-000
  745_oracle-character-candidate
- obs-unk-000746: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/046_obs-unk-000746_hust-obc-und-L-000
  746_oracle-character-candidate
- obs-unk-000747: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/047_obs-unk-000747_hust-obc-und-L-000
  747_oracle-character-candidate
- obs-unk-000748: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/048_obs-unk-000748_hust-obc-und-L-000
  748_oracle-character-candidate
- obs-unk-000749: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/049_obs-unk-000749_hust-obc-und-L-000
  749_oracle-character-candidate
- obs-unk-000750: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/050_obs-unk-000750_hust-obc-und-L-000
  750_oracle-character-candidate
- obs-unk-000751: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/051_obs-unk-000751_hust-obc-und-L-000
  751_oracle-character-candidate
- obs-unk-000752: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/052_obs-unk-000752_hust-obc-und-L-000
  752_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
