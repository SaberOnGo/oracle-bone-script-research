# Asset Source And Rights Index / 资产来源与权利索引

English:
This registry is the human review entry for image, rubbing, hand-copy,
screenshot, and downloaded-asset provenance. It keeps asset source index rows,
rights review log rows, size-limit exceptions, technical profile rows, and
visual profile rows together before any image is used for formal research.

简体中文：
本注册表是图片、拓片、摹本、截图和下载资产出处的人工复核入口。它把
asset source index、rights review log、尺寸例外、technical profile 和
visual profile 放在一起，供正式研究前核查。

## Human Review Entry Order / 人工复核入口顺序

English:

1. Open `001_asset-source-index.csv` and identify the asset row.
2. Open `002_asset-rights-review-log.csv` for rights status and risk note.
3. Open an active rights override and conflict note, if present.
4. Check file size, checksum, source provenance, and public-commit decision.
5. If the source package exceeds `SIZE_LIMIT`, open the large-source register.
6. Check technical profile rows before using the image file itself.
7. Treat visual profile rows as algorithmic metadata, not glyph analysis.
8. Open the object-local dossier or review sheet before drawing conclusions.

简体中文：

1. 先打开 `001_asset-source-index.csv`，确认资产行。
2. 打开 `002_asset-rights-review-log.csv`，核查权利状态和风险提示。
3. 如存在生效的权利覆盖表和冲突复核页，先打开它们。
4. 核对文件大小、checksum、source provenance 和公开提交决定。
5. 如果来源包超过 `SIZE_LIMIT`，继续打开 large-source register。
6. 使用图像文件前，先核查 technical profile 行。
7. visual profile 只是算法 metadata，不是字形分析。
8. 得出任何结论前，先打开对象内 dossier 或人工复核表。

## Files / 文件

English:

- `001_asset-source-index.csv`: asset source index and object route.
- `002_asset-rights-review-log.csv`: rights review log and risk notes.
- `003_size-limit-exceptions.csv`: reviewed `SIZE_LIMIT` exceptions.
- `004_asset-image-technical-profile.csv`: technical profile metadata.
- `005_asset-image-visual-profile.csv`: deterministic visual profile metadata.
- `006_obimd-rights-conflict-review.md`: human conflict review and boundary.
- `006_obimd-rights-status-override.csv`: effective rights override ledger.

简体中文：

- `001_asset-source-index.csv`：资产来源索引和对象路线。
- `002_asset-rights-review-log.csv`：权利复核记录和风险提示。
- `003_size-limit-exceptions.csv`：已复核的 `SIZE_LIMIT` 例外。
- `004_asset-image-technical-profile.csv`：图像技术 profile metadata。
- `005_asset-image-visual-profile.csv`：确定性视觉 profile metadata。
- `006_obimd-rights-conflict-review.md`：人工权利冲突复核和边界。
- `006_obimd-rights-status-override.csv`：生效权利状态覆盖表。

## Concrete Questions To Check / 具体待查问题

English:

- Which source, catalog, package, object, or URL produced this asset?
- Which checksum, file size, and technical profile identify the file?
- Which rights status and risk note limit public repository use?
- Is the raw package outside regular Git or listed as a size exception?
- Which object-local dossier lets a human compare the image with context?
- Which visual profile value is only a route for later manual inspection?

简体中文：

- 该资产来自哪个来源、著录、来源包、对象或 URL？
- 哪个 checksum、文件大小和 technical profile 能定位文件？
- 哪个 rights status 和 risk note 限制公开仓库使用？
- 原始包是否在普通 Git 外部，或是否登记为尺寸例外？
- 哪个对象内 dossier 能让人结合上下文比较图像？
- 哪个 visual profile 数值只是后续人工检查路线？

## Current Source Families / 当前来源族

English:
HUST-OBC undeciphered-candidate glyph images are small object-local review
images derived from a registered large source package. The raw zip remains
outside regular Git under the large-source register.

OBIMD component-candidate images are small object-local PNG review assets
derived from the registered `Sub-character Images.zip` package. The raw zip
stays outside regular Git in the ignored external archive. Its rights
statements conflict; open the conflict review and apply the override before
treating any OBIMD asset as reusable.

简体中文：
HUST-OBC 未释字候选图像是从已登记大型来源包抽取的小型对象内复核图。
原始 zip 通过 large-source register 保留在普通 Git 外部。

OBIMD 构件候选图像是从已登记 `Sub-character Images.zip` 来源包抽取的
小型对象内 PNG 复核资产。原始 zip 保留在已忽略外部归档中。其权利说明
存在冲突；把任何 OBIMD 资产当作可复用资料前，必须先打开冲突复核页并
应用覆盖表。

## Research Boundary / 研究边界

English:
Asset registration, rights review, technical profile, and visual profile rows
are source and preprocessing evidence only. They are not rights clearance,
glyph segmentation, component analysis, paleographic interpretation, accepted
readings, or a decipherment conclusion. This is not a decipherment conclusion.

简体中文：
资产登记、权利复核、technical profile 和 visual profile 行只是来源和
预处理证据。它们不是权利清理结论，不是字形切分、构件分析、古文字学
解释、已接受释读或破译结论。它们不是释读结论。
