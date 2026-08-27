# Rigid Image Match and Countercontrol
# 刚体图像匹配与反向对照

Review date / 复核日期: `2026-08-28`

Status / 状态: `diagnostic image correspondence only`

This review asks a narrow question: can an independently photographed member
surface be located again in the official full-composite photograph without
shear, perspective correction, or non-rigid warping? It is not a seam verdict.

本次只问一个窄问题：独立拍摄的成员表面，能否在不使用剪切、透视校正或
非刚性形变的条件下，在官方全器合编照片中再次定位？这不是接缝裁决。

## Method boundary / 方法边界

The diagnostic uses SIFT local features and a RANSAC similarity transform
only. The transform permits uniform scale, rotation, and translation. It does
not permit anisotropic scale, shear, perspective, reflection, or local warp.

诊断使用 SIFT 局部特征和 RANSAC，且仅使用相似变换。变换只允许等比例
缩放、旋转和平移；不允许非等比缩放、剪切、透视、镜像或局部形变。

Software: OpenCV `5.0.0`, NumPy `2.5.2`, Python `3.14`.

For each member face, the matching full-composite face is the test. The other
full-composite face is an opposite-face countercontrol. This `异面反向对照`
checks whether a result merely follows background, watermark, scale bar, or
repeated surface texture.

每个成员面与同面全器图进行测试，同时与另一面全器图作
`opposite-face countercontrol`。异面反向对照用于检查结果是否只追随
背景、水印、比例尺或重复表面纹理。

## Diagnostic decision rule / 诊断判定规则

A row is called `rigid_match` only when it has:

- at least 50 RANSAC inliers;
- inlier ratio at least `0.35`;
- uniform scale between `0.2` and `2.0`;
- median inlier residual no more than `2.5` pixels;
- no passing opposite-face countercontrol.

一行只有同时满足以下条件才记为`刚体匹配`：

- RANSAC 内点不少于 50；
- 内点率不低于 `0.35`；
- 等比例缩放位于 `0.2` 至 `2.0`；
- 内点残差中位数不高于 `2.5` 像素；
- 异面反向对照不通过。

These are diagnostic screening thresholds, not calibrated scientific
probabilities. Rows that fail are `algorithmic inconclusive`, or`算法未定`.
Failure is not evidence that catalog membership or a proposed join is false.

这些只是诊断筛选阈值，不是经过校准的科学概率。未通过的行记为
`algorithmic inconclusive`，即`算法未定`；失败不构成馆藏成员关系或
拟议缀合为假的证据。

## Passing same-face correspondences / 通过的同面对应

Six face rows across three members pass:

- `R038421` front: 96 inliers, ratio `0.3650`, median residual `2.0669` px.
- `R038421` reverse: 110 inliers, ratio `0.6111`, residual `1.2948` px.
- `R039467` front: 105 inliers, ratio `0.7047`, residual `0.5086` px.
- `R039467` reverse: 128 inliers, ratio `0.8050`, residual `1.0771` px.
- `R060751` front: 93 inliers, ratio `0.9029`, residual `1.5178` px.
- `R060751` reverse: 159 inliers, ratio `0.8785`, residual `1.1526` px.

三个成员的六个面通过：

- `R038421` 正面：96 内点，内点率 `0.3650`，残差 `2.0669` 像素。
- `R038421` 反面：110 内点，内点率 `0.6111`，残差 `1.2948` 像素。
- `R039467` 正面：105 内点，内点率 `0.7047`，残差 `0.5086` 像素。
- `R039467` 反面：128 内点，内点率 `0.8050`，残差 `1.0771` 像素。
- `R060751` 正面：93 内点，内点率 `0.9029`，残差 `1.5178` 像素。
- `R060751` 反面：159 内点，内点率 `0.8785`，残差 `1.1526` 像素。

No opposite-face row passes. Some controls produced small or zero-scale
degenerate transforms. Those are rejected even when their apparent residual
is zero, because repeated matches collapsed onto one target coordinate.

没有异面行通过。部分对照产生很小或零缩放的退化变换；即使表面残差为
零也予以否决，因为重复匹配塌缩到同一目标坐标。

## What the passing result means / 通过结果的含义

The result independently supports image-level same-surface correspondence:
the independently photographed faces of `R038421`, `R039467`, and `R060751`
can be relocated in the appropriate official composite face by a rigid
similarity transform.

结果独立支持图像层的同表面对应：`R038421`、`R039467`、`R060751` 的
独立正反面照片，均能用刚性相似变换在对应的官方全器面中重新定位。

For `R060751`, this is useful confirmation that the later literature-cited
member is visibly present in the current official composite photograph. It
does not show that its boundary touches another fragment tooth by tooth.

对 `R060751` 而言，这说明后出文献所引成员确实可在当前官方合编照片中
定位；但不能证明其边缘与另一残片逐齿接触。

`R038421` is itself an earlier multi-piece composite. Matching it as one image
does not independently validate every internal seam inside that older unit.

`R038421` 本身就是较早的多片合编。把它作为一张图匹配成功，不会独立
验证该旧合编内部的每条接缝。

## Inconclusive members / 算法未定成员

The same diagnostic does not pass for `R053740`, `R054970`, or `R062431` on
either face. Their best same-face solutions have too few inliers, a degenerate
scale, or both. This may reflect limited overlap, changed placement, lighting,
surface contrast, or photograph history. No cause is selected without a
calibrated image series.

同一诊断在 `R053740`、`R054970`、`R062431` 的正反面均未通过。同面最佳
解的内点过少、缩放退化，或两者兼有。原因可能是重叠区域有限、摆放变化、
光照、表面对比或拍摄史差异；没有校准图像序列前不选定原因。

Their status remains official catalog membership plus `algorithmic
inconclusive`. It must not be rewritten as negative join evidence.

三者仍是正式馆藏成员关系加`算法未定`，不得改写成缀合反证。

## Falsification and next checks / 证伪与下一步

The current image-level result is falsified if checksum-identical reruns do
not reproduce the six passing rows, if a passing opposite-face control appears,
or if a source image is later shown to have a different face label.

若绑定相同校验和的复跑不能重现六个通过行、出现通过的异面反向对照，
或来源后来证明面别标签不同，则当前图像层结果被证伪。

No seam may be promoted from this diagnostic. Seam review still requires the
2011 plate, 2013 correction/commentary, 2018 paper, calibrated object images,
and boundary-specific positive and negative controls.

本诊断不能提升任何接缝。接缝复核仍须取得 2011 图版、2013 勘误／考释、
2018 论文、校准实物图，以及针对具体边缘的正、负对照。

## Reproducibility record / 可复跑记录

Inputs are the 12 member JPEGs and two full-composite JPEGs bound in file
`95`. Ignored analysis files:

- `rigid_match.py`: `3627` bytes;
  SHA-256
  `6be20389139ec91009c84460326af100dcd95521a1872c2c9ec534b0f3b5774c`.
- `rigid-match-results.json`: `15897` bytes;
  SHA-256
  `fb2d18d3ef9f27214faa9db9b8236a09b1cb1e2c0768cb47dacead5c1f80f81a`.

Both remain under:

`.working/ihp-1222-plate-search-20260828/`

The compact committed metrics are in `97_rigid-match-index.csv`. Images,
overlays, and transformed derivatives remain ignored because the site states
noncommercial and no-derivatives conditions.

精简指标写入 `97_rigid-match-index.csv`。因站方声明非商用、禁止改作，
原图、叠图及变换派生图继续留在忽略区。
