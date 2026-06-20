# Asset Source And Rights Index / 资产来源与权利索引

English:
Track image, rubbing, hand-copy, screenshot, and downloaded-asset provenance here. Rights-unclear assets may be committed when research needs them, but the asset index must show source provenance, rights status, and risk notes.

Single files should stay under `SIZE_LIMIT = 30 MiB`. If a research asset must exceed that limit, record it in `003_size-limit-exceptions.csv`; files at or above 40 MiB must not be committed to regular Git and should be handled through `project_registry/006_large-source-register/`.

`004_asset-image-technical-profile.csv` records technical image metadata for committed image assets, such as format, pixel size, color mode, DPI, ICC profile presence, checksum, and review boundary.

`005_asset-image-visual-profile.csv` records deterministic visual preprocessing metadata for committed image assets, including a conservative luma-threshold candidate region, foreground pixel ratio, and mean luma. These rows are algorithmic metadata only; they are not glyph segmentation, component analysis, or paleographic interpretation.

The HUST-OBC undeciphered-candidate glyph images are small object-local review images extracted from the registered large source package. The 607,933,810-byte raw zip remains outside regular Git under the large-source register; committed images keep per-asset source, checksum, rights-status, and risk-note rows here.

The OBIMD component-candidate images are small object-local PNG review assets extracted from the registered `Sub-character Images.zip` package. The 40,436,910-byte raw zip remains outside regular Git in the ignored external archive; committed PNG derivatives keep per-asset source, checksum, technical profile, visual profile, rights-status, and risk-note rows here.

简体中文：
OBIMD 构件候选图像是从已登记 `Sub-character Images.zip` 来源包抽取的小型对象内 PNG 复核资产。40,436,910 字节的原始 zip 保留在已忽略外部归档中，不进入普通 Git；已提交 PNG 派生件在本目录保留逐项来源、checksum、技术 profile、视觉 profile、权利状态和风险提示记录。

简体中文：
本目录用于追踪图片、拓片、摹本、截图和下载资产的来源。研究需要时可以提交权利状态尚不完全明确的资产，但资产索引必须显示来源、权利状态和风险提示。

单个文件原则上应低于 `SIZE_LIMIT = 30 MiB`。如果研究资产必须超过该限制，应写入 `003_size-limit-exceptions.csv`；达到或超过 40 MiB 的文件不得提交到普通 Git，应通过 `project_registry/006_large-source-register/` 处理。

`004_asset-image-technical-profile.csv` 记录已提交图像资产的技术 metadata，例如格式、像素尺寸、颜色模式、DPI、ICC profile、校验和以及复核边界。

`005_asset-image-visual-profile.csv` 记录已提交图像资产的确定性视觉预处理 metadata，包括保守亮度阈值候选区域、前景像素比例和平均亮度。这些记录只是算法 metadata，不是字形切分、构件分析或古文字学释读。

HUST-OBC 未释字候选图像是从已登记大型来源包抽取的小型对象内复核图。607,933,810 字节的原始 zip 仍按大型来源登记保留在普通 Git 之外；已提交图像在本目录保留逐项来源、checksum、权利状态和风险提示记录。
