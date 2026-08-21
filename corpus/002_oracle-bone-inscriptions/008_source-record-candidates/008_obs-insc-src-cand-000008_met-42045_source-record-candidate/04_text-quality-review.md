# Text and OCR quality review / 文字与 OCR 质量复核

## Current text state / 当前文字状态

- Museum API text fields: object title and object name only.
- Full inscription: `待查：需要权利允许的逐行释文来源`。
- OCR: `待查：需要可定位、可复核的 OCR 路线`。
- Source string: none supplied by the API.
- Project transcription: not created.
- Project translation: not created.

The visible marks in the images are not transcribed here. Low contrast,
surface wear, image orientation, and the absence of a plate edition make any
manual character count premature.

图像中的刻痕没有在本页转写。低反差、表面磨损、图像方向和缺少图版版本，
使当前进行人工字数统计仍不合适。

## Quality checks / 质量检查

The two files are JPEG source images from the API routes. Their byte hashes
and 2667 x 4000 dimensions are recorded in the object route page. No text
quality score is assigned because no transcription exists.

两张文件是 API 路线的 JPEG 来源图像。对象路线页记录了字节校验和和
2667×4000 尺寸。由于没有释文，本项目不赋予文字质量分数。

## Concrete next checks / 具体待查问题

1. Find a rights-cleared catalog or plate edition for accession `67.43.14`.
2. Compare its line order with both API image views.
3. Record each uncertain sign with image coordinates before OCR.
4. Keep any museum or published transcription source-reported until checked.

1. 查找馆藏号 `67.43.14` 的权利明确著录或图版版本。
2. 将其行序与两张 API 图像逐项核对。
3. 在 OCR 前先用图像坐标记录每个不确定字形。
4. 任何博物馆或出版释文在核对前都保持为来源报告。
