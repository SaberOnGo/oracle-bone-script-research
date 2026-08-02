# Character Visual Observation Coverage / 单字图像观察覆盖审计

This report separates a local image from a human visual observation.
It is a preprocessing audit, not a character identity or reading claim.
本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。

## Human Reading Result / 人类阅读结果

- Character object directories / 单字对象目录: 10996
- Objects with local images / 有本地图像: 10996
- Direct visual records / 有直接观察记录: 6103
- Images without direct records / 有图无观察: 4893
- Objects without local images / 无本地图像: 0
- Status / 状态: needs_human_visual_observation_review

## Counts By Object Type / 按对象类型计数

- oracle_character: 1588 objects; 1588 with images; 1588 with direct visual reco
  rds
- undeciphered_candidate: 9408 objects; 9408 with images; 4515 with direct visua
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

- obs-unk-004509: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/009_obs-unk-004509_hust-obc-und-X-004
  509_oracle-character-candidate
- obs-unk-004510: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/010_obs-unk-004510_hust-obc-und-X-004
  510_oracle-character-candidate
- obs-unk-004511: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/011_obs-unk-004511_hust-obc-und-X-004
  511_oracle-character-candidate
- obs-unk-004512: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/012_obs-unk-004512_hust-obc-und-X-004
  512_oracle-character-candidate
- obs-unk-004513: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/013_obs-unk-004513_hust-obc-und-X-004
  513_oracle-character-candidate
- obs-unk-004514: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/014_obs-unk-004514_hust-obc-und-X-004
  514_oracle-character-candidate
- obs-unk-004515: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/015_obs-unk-004515_hust-obc-und-X-004
  515_oracle-character-candidate
- obs-unk-004516: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/016_obs-unk-004516_hust-obc-und-X-004
  516_oracle-character-candidate
- obs-unk-004517: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/017_obs-unk-004517_hust-obc-und-X-004
  517_oracle-character-candidate
- obs-unk-004518: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/018_obs-unk-004518_hust-obc-und-X-004
  518_oracle-character-candidate
- obs-unk-004519: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/019_obs-unk-004519_hust-obc-und-X-004
  519_oracle-character-candidate
- obs-unk-004520: corpus/001_oracle-characters/062_undeciphered-004501-004600_ob
  s-unk-bucket_oracle-character-candidates/020_obs-unk-004520_hust-obc-und-X-004
  520_oracle-character-candidate

The complete object list is in:
- `corpus/009_statistics-and-derived-features/227_character-visual-observation-c
  overage.csv`

## Boundary / 边界

This audit does not convert image metadata into observations, identity,
component assignments, readings, evolution, or decipherment.
本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。
