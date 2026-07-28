# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 2415
- Images without direct records / 有图无观察: 8581
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 with direct visual reco
  rds
- undeciphered_candidate: 9408 objects; 9408 with images; 827 with direct visual
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

- obs-unk-000721: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/021_obs-unk-000721_hust-obc-und-L-000
  721_oracle-character-candidate
- obs-unk-000722: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/022_obs-unk-000722_hust-obc-und-L-000
  722_oracle-character-candidate
- obs-unk-000723: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/023_obs-unk-000723_hust-obc-und-L-000
  723_oracle-character-candidate
- obs-unk-000724: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/024_obs-unk-000724_hust-obc-und-L-000
  724_oracle-character-candidate
- obs-unk-000725: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/025_obs-unk-000725_hust-obc-und-L-000
  725_oracle-character-candidate
- obs-unk-000726: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/026_obs-unk-000726_hust-obc-und-L-000
  726_oracle-character-candidate
- obs-unk-000727: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/027_obs-unk-000727_hust-obc-und-L-000
  727_oracle-character-candidate
- obs-unk-000728: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/028_obs-unk-000728_hust-obc-und-L-000
  728_oracle-character-candidate
- obs-unk-000729: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/029_obs-unk-000729_hust-obc-und-L-000
  729_oracle-character-candidate
- obs-unk-000730: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/030_obs-unk-000730_hust-obc-und-L-000
  730_oracle-character-candidate
- obs-unk-000731: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/031_obs-unk-000731_hust-obc-und-L-000
  731_oracle-character-candidate
- obs-unk-000732: corpus/001_oracle-characters/024_undeciphered-000701-000800_ob
  s-unk-bucket_oracle-character-candidates/032_obs-unk-000732_hust-obc-und-L-000
  732_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
