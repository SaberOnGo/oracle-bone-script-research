#!/usr/bin/env python3
"""Build object-local visual materials for all HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import textwrap
import zipfile
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageStat
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required to profile HUST-OBC glyph images.") from exc


RAW_ZIP = Path("external_local_archive/source_packages/hust-obc/dl-hust-obc-figshare-raw.zip")
UNDECIPHERED_INDEX = Path(
    "corpus/001_oracle-characters/000_character-registers/003_undeciphered-oracle-characters-index.csv"
)
ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
ASSET_RIGHTS_REVIEW_LOG = Path("project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv")
ASSET_ID_SOURCE_MAP = Path("project_registry/002_project-id-to-source-reference-map/003_asset-id-source-map.csv")
ASSET_IMAGE_TECHNICAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv"
)
ASSET_IMAGE_VISUAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/005_asset-image-visual-profile.csv"
)

EXPECTED_RAW_SHA256 = "0d00a4de8dd9ce7b7495d7b26f3c80098ee9975b91615211dde02e569bf0ad9d"
FIGSHARE_SOURCE_URL = "https://ndownloader.figshare.com/files/48465988"
UPDATED_AT = "2026-06-20"
LUMA_THRESHOLD = 140
MAX_HUMAN_LINE_LENGTH = 80

RISK_NOTE = (
    "HUST-OBC glyph candidate image extracted from registered large source package for "
    "preparation-stage object-local visual review; rights signals conflict between "
    "Figshare package metadata and the Scientific Data article page."
)
BOUNDARY_CAUTION = (
    "Source-marked candidate image only; not an accepted glyph identity, not an "
    "accepted reading, not a component conclusion, and not a decipherment conclusion."
)


# These notes are intentionally limited to candidates whose local image was
# opened and inspected in the current preparation batch.  They are direct
# visual records, not readings, component assignments, or decipherment claims.
MATERIAL_VISUAL_OBSERVATIONS = {
    "obs-unk-001601": (
        "The narrow image shows a dark upper cluster with short descending "
        "marks, a long slanting stroke at the left, and a thin vertical "
        "stroke extending below the cluster.",
        "图像较窄；上部可见深色密集笔画和数个向下短痕，左侧有长斜笔画，"
        "密集区域下方还有细长竖向笔画。",
    ),
    "obs-unk-001602": (
        "The image shows an angular, diamond-like lower contour with a pointed "
        "bottom, crossed by a central vertical stroke and a compact upper mark.",
        "图像下部可见带尖底的菱角状轮廓，中间有竖向笔画贯穿，"
        "上部另有紧密短痕。",
    ),
    "obs-unk-001603": (
        "The image contains a dense central cluster of crossing strokes, small "
        "paired marks near the lower left, and a long descending stroke ending "
        "in a small rounded mark.",
        "图像中央是密集交叉笔画；左下附近有成对小痕迹，右下方向有长向下笔画，"
        "末端接近小型圆弧状痕迹。",
    ),
    "obs-unk-001604": (
        "The image has a narrow vertical middle, two fork-like upper strokes, "
        "and paired curved marks at the lower end; the small image limits detail.",
        "图像中部为窄长竖向结构，上部可见两处分叉状笔画，下端有成对弯曲痕迹；"
        "图像较小，细部仍受限制。",
    ),
    "obs-unk-001605": (
        "The image repeats the dense crossing-stroke pattern seen in the local "
        "candidate image for obs-unk-001603, with paired lower-left marks and a "
        "long descending stroke ending in a small rounded mark.",
        "图像呈现与 obs-unk-001603 本地候选图相同的密集交叉笔画样式；"
        "左下有成对小痕迹，右下有长向下笔画并接近小型圆弧状痕迹。",
    ),
    "obs-unk-001606": (
        "The image has a dense angular cluster at the left, a taller open "
        "contour at the right, and several short lower projections; the image "
        "does not establish whether the two sides form one unit.",
        "图像左侧是密集的折角笔画，右侧有较高的开放轮廓，下方还有数个短向下痕迹；"
        "仅凭此图不能确定左右是否构成一个整体。",
    ),
    "obs-unk-001607": (
        "Two neighboring forms are visible: the left has a rounded upper loop "
        "and a long curved lower contour, while the right has a smaller upper "
        "arch and a descending stem.",
        "图像中可见两个相邻形体：左侧有圆弧状上部和较长下部曲线，右侧有较小上拱和"
        "向下延伸的主干。",
    ),
    "obs-unk-001608": (
        "The image shows a tall forked form on the left with descending branched "
        "strokes, plus a separated narrow upright form on the right with a small "
        "upper loop.",
        "图像左侧是高而分叉的形体，并有向下分枝笔画；右侧另有窄长竖向形体，"
        "上部带有小型环状痕迹。",
    ),
    "obs-unk-001609": (
        "The small dark image contains a compact upper cluster and a lower field "
        "of crossing strokes; edge detail and individual stroke breaks need a "
        "higher-resolution source check.",
        "小型深色图像包含紧密上部簇和下部交叉笔画；边缘细节及单条笔画的断续情况"
        "仍需用更高分辨率来源复核。",
    ),
    "obs-unk-001610": (
        "The high-contrast silhouette has two pointed upper peaks, a broad dark "
        "lower body, and a narrow central opening or lighter gap; filled areas "
        "limit stroke-level observation.",
        "高对比度剪影可见两个尖状上部、宽大的深色下部和窄小中央空隙或浅色缺口；"
        "填黑区域限制了逐笔观察。",
    ),
    "obs-unk-001611": (
        "The narrow image has a curved upper cluster, a short descending central "
        "stroke, and paired horizontal or curved marks forming a compact lower "
        "section.",
        "窄长图像上部有弯曲密集笔画，中部有短向下笔画，下部由成对横向或弯曲痕迹"
        "组成紧凑区域。",
    ),
    "obs-unk-001612": (
        "The image shows a tall angular contour on the right with internal "
        "diagonal marks, plus detached narrow strokes along the left edge.",
        "图像右侧有高而折角的轮廓，内部可见斜向笔画；左侧边缘另有分离的窄长痕迹。",
    ),
    "obs-unk-001613": (
        "A dark compact form occupies the left side, with an uneven outer edge and "
        "small interior openings; a separate long vertical stroke stands on the "
        "right.",
        "图像左侧是深色紧凑形体，外缘不规则，内部有小型空隙；右侧另有一条较长竖向"
        "笔画。",
    ),
    "obs-unk-001614": (
        "The image has a small cross-like mark above a narrow stem, a broad lower "
        "section divided into two rectangular openings, and a detached rounded "
        "mark at the right.",
        "图像上部有小型交叉状痕迹，下接窄长主干；下部较宽并分成两个方形空隙，右侧"
        "另有分离的圆弧状痕迹。",
    ),
    "obs-unk-001615": (
        "The image is dominated by a long descending diagonal stroke with a bent "
        "upper end; a compact lower cluster and a small detached lower mark are "
        "also visible.",
        "图像主要由一条上端弯折、向下延伸的长斜笔画构成；下部有紧凑笔画簇，另有小型"
        "分离痕迹。",
    ),
    "obs-unk-001616": (
        "The sparse image shows one long curved stroke descending from the upper "
        "left to a central junction, with two shorter strokes extending below.",
        "稀疏图像可见一条从左上向中央交点下行的长弯曲笔画，交点下方还有两条较短"
        "笔画。",
    ),
    "obs-unk-001617": (
        "The image contains a dense central composite with a narrow upright stroke "
        "at the left, curved interior marks, and several short lower projections.",
        "图像中央是密集组合形体，左侧有窄长竖向笔画，内部有弯曲痕迹，下方还有数个"
        "短向下痕迹。",
    ),
    "obs-unk-001618": (
        "The local image shows the same visible upper cluster and compact lower "
        "section as the image recorded for obs-unk-001611; this is a visual "
        "comparison only, not an identity claim.",
        "本地图像呈现与 obs-unk-001611 图像相同的上部密集笔画和下部紧凑区域；这只是"
        "视觉比较，不是身份确认。",
    ),
    "obs-unk-001619": (
        "The image shows a dense upright composite with small stacked marks near "
        "the top, a central vertical axis, branching lower strokes, and a short "
        "detached stroke to the right.",
        "图像是密集竖向组合形体；上部有小型叠置痕迹，中部有竖向主轴，下部有分枝"
        "笔画，右侧还有短的分离笔画。",
    ),
    "obs-unk-001620": (
        "The local image shows the same dense upright composite, stacked upper "
        "marks, branching lower strokes, and detached right stroke as the image "
        "recorded for obs-unk-001619; no identity claim is made.",
        "本地图像呈现与 obs-unk-001619 图像相同的密集竖向组合形体、上部叠置痕迹、"
        "下部分枝笔画和右侧分离笔画；本记录不作身份确认。",
    ),
    "obs-unk-001621": (
        "The image has two short upper strokes, a long curved right-side contour, "
        "and a compact lower cluster with a small enclosed or looped mark.",
        "图像上部有两条短笔画，右侧有长弯曲轮廓，下部是紧凑笔画簇，并带有小型"
        "封闭或环状痕迹。",
    ),
    "obs-unk-001622": (
        "The local image shows a dense central composite with a narrow upright "
        "stroke at the left, curved interior marks, and short lower projections; "
        "it is visually similar to obs-unk-001617 only.",
        "本地图像是密集中央组合形体，左侧有窄长竖向笔画，内部有弯曲痕迹，下方有短"
        "向下笔画；这里只记录其与 obs-unk-001617 的视觉相似。",
    ),
    "obs-unk-001623": (
        "The image stacks several angular zigzag strokes above a central vertical "
        "axis, with multiple short horizontal strokes and a broader lower bar.",
        "图像上部叠置数个折线状笔画，中部有竖向主轴，下部可见多条短横向笔画和较宽"
        "底部横痕。",
    ),
    "obs-unk-001624": (
        "The small dark image contains irregular upright and diagonal strokes on "
        "both sides of a dense center; lower edge detail is limited by the image "
        "resolution.",
        "小型深色图像在密集中央两侧可见不规则竖向和斜向笔画；受图像分辨率限制，"
        "下缘细节仍不清楚。",
    ),
    "obs-unk-001625": (
        "The local image shows the same dense upright composite, stacked upper "
        "marks, branching lower strokes, and detached right stroke seen in the "
        "image recorded for obs-unk-001619; this is a comparison route only.",
        "本地图像呈现与 obs-unk-001619 图像相同的密集竖向组合形体、上部叠置痕迹、"
        "下部分枝笔画和右侧分离笔画；这里只记录比较路线。",
    ),
    "obs-unk-001626": (
        "The image has a rounded upper contour, a long horizontal middle stroke, "
        "a narrow descending stem, and a small rectangular mark at the bottom.",
        "图像上部有圆弧状轮廓，中部有较长横向笔画，下接窄长主干，底部有小型方形"
        "痕迹。",
    ),
    "obs-unk-001627": (
        "The compact dark image shows several pointed upper projections, a dense "
        "central field, and a short horizontal lower stroke.",
        "紧凑深色图像可见数个尖状上部笔画、密集中央区域和短横向下部笔画。",
    ),
    "obs-unk-001628": (
        "The image has a tall triangular outer contour, crossing interior strokes, "
        "and a rounded lower enclosure with an open or light center.",
        "图像有高而近三角形的外部轮廓，内部笔画交叉，下部有圆弧状封闭轮廓，"
        "中央留有开放或浅色区域。",
    ),
    "obs-unk-001629": (
        "Two upward-curving strokes meet near the top of a compact central form; "
        "the lower part has a rounded contour and a short horizontal mark.",
        "两条向上弯曲笔画在紧凑中央形体上部附近相接；下部有圆弧状轮廓和短横痕。",
    ),
    "obs-unk-001630": (
        "The high-contrast image shows two tall pointed strokes, a central vertical "
        "line, and a broad rounded lower contour; dark fill limits individual "
        "stroke breaks.",
        "高对比度图像可见两条高而尖的笔画、中央竖线和宽大的圆弧状下部轮廓；"
        "深色填充限制了单条笔画断续的观察。",
    ),
    "obs-unk-001631": (
        "The image shows crossed and stacked upper strokes, a broad central "
        "horizontal mark, and a lower angular or rounded enclosure with short "
        "vertical and diagonal extensions.",
        "图像上部可见交叉和叠置笔画，中部有较宽横向痕迹，下部有近方角或圆弧状的"
        "围合形体，并带有短竖向和斜向延伸笔画。",
    ),
    "obs-unk-001632": (
        "The image has a repeated row of small rounded or pointed marks at the "
        "left, a dense angular block at the right, and a short detached diagonal "
        "mark below.",
        "图像左侧有一列重复出现的圆弧或尖角状小痕迹，右侧是密集的折角形笔画块，"
        "下方另有一条短的分离斜向痕迹。",
    ),
    "obs-unk-001633": (
        "The compact image has a tall upright or diagonal stroke through a group "
        "of crossing angular marks; two short rectangular or block-like marks are "
        "detached near the lower right.",
        "紧凑图像中有一条高的竖向或斜向主笔画穿过交叉折角笔画簇；右下方另有两条"
        "分离的短方块状痕迹。",
    ),
    "obs-unk-001634": (
        "The image contains an open curved outer contour, a dense central vertical "
        "and diagonal cluster, and several short lower projections; the small scale "
        "limits separation of individual strokes.",
        "图像有开放的弯曲外轮廓，中央是密集的竖向和斜向笔画簇，下部有数个短的"
        "外伸笔画；图像尺寸限制了单条笔画的分离观察。",
    ),
    "obs-unk-001635": (
        "The image is dominated by a tall roof-like or angular outer contour, with "
        "a central upright stroke, short side marks, and a small lower extension.",
        "图像主体是高而近屋顶形或折角形的外部轮廓，内部有中央竖向笔画、两侧短痕和"
        "小型下部延伸。",
    ),
    "obs-unk-001636": (
        "Two tall pointed upright strokes rise above a central gap or stem; a broad "
        "rounded lower band or enclosure is visible beneath them.",
        "两条高而尖的竖向笔画位于中央空隙或主干两侧；其下方可见较宽的圆弧状横带"
        "或围合形体。",
    ),
    "obs-unk-001637": (
        "The small image repeats the open curved outer contour, dense central "
        "vertical and diagonal strokes, and short lower projections seen for "
        "obs-unk-001634; this is a visual comparison only.",
        "小型图像呈现与 obs-unk-001634 相同的开放弯曲外轮廓、中央密集竖斜笔画和"
        "短下部外伸痕迹；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001638": (
        "The image shows a tall dense composite with side contours, crossing middle "
        "strokes, and small rounded or rectangular marks near the lower end.",
        "图像是高而密集的组合形体，两侧有外轮廓，中部笔画交叉，下端附近可见小型"
        "圆弧或方块状痕迹。",
    ),
    "obs-unk-001639": (
        "Several pointed or forked upper strokes sit above a dense central field; "
        "the lower area contains short diagonal and horizontal projections.",
        "数条尖状或分叉的上部笔画位于密集中央区域之上；下部可见短的斜向和横向外伸"
        "笔画。",
    ),
    "obs-unk-001640": (
        "The image has two crossing upper strokes, a broad lower body, and several "
        "small detached rounded marks beneath the main form.",
        "图像上部有两条交叉笔画，主体下部较宽，下方另有数个分离的小型圆弧状痕迹。",
    ),
    "obs-unk-001641": (
        "The image contains a compact upper crossing, a dense central vertical "
        "cluster, and a broad lower curved enclosure with short side extensions.",
        "图像上部有紧凑的交叉笔画，中部是密集竖向笔画簇，下部有较宽的圆弧状围合形体"
        "和短的两侧外伸笔画。",
    ),
    "obs-unk-001642": (
        "A rounded elongated upper contour with an inner horizontal mark sits above "
        "a long middle stroke, a descending stem, and a short lower base.",
        "上部是带内部横痕的长圆弧轮廓，下接较长的中部横痕、下降主干和短底部横痕。",
    ),
    "obs-unk-001643": (
        "The image shows two long curved upright strokes; several short diagonal "
        "marks branch from the left side of the darker central area.",
        "图像可见两条较长的弯曲竖向笔画；较深中央区域左侧分出数条短斜向痕迹。",
    ),
    "obs-unk-001644": (
        "The tall form has a rounded or capped upper section, stacked horizontal "
        "marks through the middle, and a narrow lower stem with short projections.",
        "高形图像上部有圆弧或帽状部分，中部叠置多条横向痕迹，下部是窄长主干并带有"
        "短外伸笔画。",
    ),
    "obs-unk-001645": (
        "The image is broadly symmetrical, with a forked upper section, a small "
        "central enclosure or diamond-like mark, and stacked rectangular lower marks.",
        "图像整体近于对称，上部有分叉形笔画，中部有小型围合或菱形状痕迹，下部叠置"
        "方块状痕迹。",
    ),
    "obs-unk-001646": (
        "A broad pointed outer contour frames crossing interior strokes and several "
        "short diagonal marks toward the lower left.",
        "较宽的尖顶外轮廓包围交叉的内部笔画，左下方可见数条短斜向痕迹。",
    ),
    "obs-unk-001647": (
        "The small image repeats the open curved outer contour, dense central "
        "vertical and diagonal strokes, and short lower projections seen for "
        "obs-unk-001634; this is a visual comparison only.",
        "小型图像呈现与 obs-unk-001634 相同的开放弯曲外轮廓、中央密集竖斜笔画和"
        "短下部外伸痕迹；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001648": (
        "The small image repeats the open curved outer contour, dense central "
        "vertical and diagonal strokes, and short lower projections seen for "
        "obs-unk-001634; this is a visual comparison only.",
        "小型图像呈现与 obs-unk-001634 相同的开放弯曲外轮廓、中央密集竖斜笔画和"
        "短下部外伸痕迹；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001649": (
        "Two long diagonal strokes form an open angular body, with a descending "
        "right-side contour and a short horizontal base near the bottom.",
        "两条较长斜向笔画构成开放的折角形主体，右侧有下降轮廓，底部附近有短横向"
        "基线。",
    ),
    "obs-unk-001650": (
        "The high-contrast image contains a dense angular central field, crossing "
        "outer strokes, and small short projections around the main form; dark fill "
        "limits stroke separation.",
        "高对比度图像有密集折角状中央区域，外部笔画相互交叉，主体周围有短外伸痕迹；"
        "深色填充限制了单条笔画的分离观察。",
    ),
    "obs-unk-001651": (
        "The image has a peaked upper contour and two slanting side strokes with "
        "short branching marks along the lower portions.",
        "图像上部有尖顶状轮廓，两侧有斜向笔画，下部各可见短的分枝痕迹。",
    ),
    "obs-unk-001652": (
        "The compact diagonal form has an angular upper section, a narrow middle "
        "stem, a curved lower base, and a small detached mark at the lower left.",
        "紧凑的斜向形体上部折角明显，中部有窄长主干，下部有弯曲底部，左下方另有"
        "小型分离痕迹。",
    ),
    "obs-unk-001653": (
        "The image shows a dense upright composite with a small rounded upper mark, "
        "stacked middle strokes, and a detached curved stroke at the right.",
        "图像是密集竖向组合形体，上部有小型圆弧状痕迹，中部笔画叠置，右侧另有"
        "分离的弯曲笔画。",
    ),
    "obs-unk-001654": (
        "The image repeats the dense upright composite, rounded upper mark, stacked "
        "middle strokes, and detached curved right stroke seen for obs-unk-001653; "
        "this is a visual comparison only.",
        "图像呈现与 obs-unk-001653 相同的密集竖向组合形体、上部圆弧痕迹、中部叠置"
        "笔画和右侧分离弯曲笔画；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001655": (
        "The small image repeats the open curved outer contour, dense central "
        "vertical and diagonal strokes, and short lower projections seen for "
        "obs-unk-001634; this is a visual comparison only.",
        "小型图像呈现与 obs-unk-001634 相同的开放弯曲外轮廓、中央密集竖斜笔画和"
        "短下部外伸痕迹；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001656": (
        "A rounded elongated upper contour with an inner horizontal mark sits above "
        "a long middle stroke, a descending stem, and a short lower base; this is a "
        "visual comparison with obs-unk-001642 only.",
        "带内部横痕的长圆弧上部轮廓下接长中部横痕、下降主干和短底部横痕；这里只作"
        "与 obs-unk-001642 的视觉比较。",
    ),
    "obs-unk-001657": (
        "The image has several pointed upper projections, a dense central field, "
        "and a broad lower rounded or vertical cluster.",
        "图像上部有数个尖状外伸笔画，中部区域密集，下部有较宽的圆弧或竖向笔画簇。",
    ),
    "obs-unk-001658": (
        "The dark form contains a pointed or angular left-side projection, a broad "
        "central horizontal stroke, and short lower and right-side extensions.",
        "深色形体左侧有尖状或折角外伸笔画，中部有较宽横向笔画，下部和右侧有短的"
        "外伸痕迹。",
    ),
    "obs-unk-001659": (
        "The compact diagonal form repeats the angular upper section, narrow middle "
        "stem, curved lower base, and small detached lower-left mark seen for "
        "obs-unk-001652; this is a visual comparison only.",
        "紧凑斜向形体呈现与 obs-unk-001652 相同的上部折角、窄长主干、弯曲底部和"
        "左下分离小痕迹；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001660": (
        "The image separates into a left group with curved upper strokes and a long "
        "descending mark, and a smaller right group with short forked strokes.",
        "图像可分为左侧的弯曲上部笔画和长下降痕迹，以及右侧较小的短分叉笔画簇。",
    ),
    "obs-unk-001661": (
        "The small image repeats the open curved outer contour, dense central "
        "vertical and diagonal strokes, and short lower projections seen for "
        "obs-unk-001634; this is a visual comparison only.",
        "小型图像呈现与 obs-unk-001634 相同的开放弯曲外轮廓、中央密集竖斜笔画和"
        "短下部外伸痕迹；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001662": (
        "The image has a compact upper angular form, a central descending stem, and "
        "three small rounded or circular marks arranged below the main body.",
        "图像上部是紧凑的折角形体，中部有下降主干，主体下方排列三个小型圆弧或圆形"
        "痕迹。",
    ),
    "obs-unk-001663": (
        "The tall image shows a narrow upright central section, crossing side marks, "
        "and a broad lower block with short vertical divisions.",
        "高形图像有窄长中央竖向部分，两侧笔画交叉，下部是较宽的块状形体并有短竖向"
        "分隔痕迹。",
    ),
    "obs-unk-001664": (
        "A rounded elongated upper contour with an inner horizontal mark sits above "
        "a long middle stroke, a descending stem, and a short lower base.",
        "上部是带内部横痕的长圆弧轮廓，下接较长的中部横痕、下降主干和短底部横痕。",
    ),
    "obs-unk-001665": (
        "The image has a narrow pointed upper form, a long central descending stroke, "
        "and a lower angular zigzag or triangular enclosure.",
        "图像上部是窄长尖状形体，中部有长下降笔画，下部有折线或三角形围合痕迹。",
    ),
    "obs-unk-001666": (
        "The image contains a short upper horizontal cluster, a long diagonal middle "
        "stroke, and several short lower side projections.",
        "图像上部有短横向笔画簇，中部有长斜向笔画，下部两侧有数个短外伸痕迹。",
    ),
    "obs-unk-001667": (
        "Two tall upright strokes frame a compact angular central form; the lower "
        "portion contains short crossing and descending marks.",
        "两条高的竖向笔画夹住紧凑折角形中央形体；下部有短交叉和下降痕迹。",
    ),
    "obs-unk-001668": (
        "A broad upper horizontal bar sits above a dense central crossing and a long "
        "diagonal lower extension.",
        "较宽的上部横条位于密集中部交叉笔画之上，下方有长斜向外伸笔画。",
    ),
    "obs-unk-001669": (
        "The image has a peaked upper contour, a compact middle form, and several "
        "closely spaced horizontal strokes along the lower edge.",
        "图像上部有尖顶状轮廓，中部形体紧凑，下缘有数条彼此接近的横向笔画。",
    ),
    "obs-unk-001670": (
        "The image separates into a left group with curved upper strokes and a long "
        "descending mark, and a smaller right group with short forked strokes; this "
        "is a visual comparison with obs-unk-001660 only.",
        "图像可分为左侧的弯曲上部笔画和长下降痕迹，以及右侧较小的短分叉笔画簇；"
        "这里只作与 obs-unk-001660 的视觉比较。",
    ),
    "obs-unk-001671": (
        "The small image repeats the open curved outer contour, dense central "
        "vertical and diagonal strokes, and short lower projections seen for "
        "obs-unk-001634; this is a visual comparison only.",
        "小型图像呈现与 obs-unk-001634 相同的开放弯曲外轮廓、中央密集竖斜笔画和"
        "短下部外伸痕迹；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001672": (
        "The image has a forked upper section, a small central enclosure or diamond-"
        "like mark, and a stacked lower block with short side extensions.",
        "图像上部有分叉形笔画，中部有小型围合或菱形状痕迹，下部叠置块状形体并带有"
        "短的两侧外伸笔画。",
    ),
    "obs-unk-001673": (
        "The small image repeats the open curved outer contour, dense central "
        "vertical and diagonal strokes, and short lower projections seen for "
        "obs-unk-001634; this is a visual comparison only.",
        "小型图像呈现与 obs-unk-001634 相同的开放弯曲外轮廓、中央密集竖斜笔画和"
        "短下部外伸痕迹；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001674": (
        "The image has a compact upper angular form, a central descending stem, and "
        "three small rounded or circular marks arranged below the main body.",
        "图像上部是紧凑的折角形体，中部有下降主干，主体下方排列三个小型圆弧或圆形"
        "痕迹。",
    ),
    "obs-unk-001675": (
        "The image repeats the compact upper angular form, descending stem, and three "
        "small lower rounded marks seen for obs-unk-001674; this is a visual "
        "comparison only.",
        "图像呈现与 obs-unk-001674 相同的上部折角形体、下降主干和下方三个小型圆弧"
        "痕迹；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001676": (
        "The committed review image is nearly blank and does not show an observable "
        "glyph. No stroke, component, or identity observation can be made from "
        "this derivative.",
        "已提交的复核图像近乎纯白，未显示可观察字形。不能依据该派生图像记录笔画、"
        "构件或对象身份。",
    ),
    "obs-unk-001677": (
        "The image shows a compact four-lobed or crossing form with pointed outer "
        "projections and a darker central intersection.",
        "图像是紧凑的四瓣或交叉形体，外缘有尖状外伸笔画，中央交叉处颜色较深。",
    ),
    "obs-unk-001678": (
        "The image repeats the compact four-lobed or crossing form, pointed outer "
        "projections, and darker central intersection seen for obs-unk-001677; this "
        "is a visual comparison only.",
        "图像呈现与 obs-unk-001677 相同的紧凑四瓣或交叉形体、尖状外伸笔画和较深的"
        "中央交叉处；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001679": (
        "The upper body contains two crossing curved strokes; a long diagonal or "
        "descending stroke extends below, with a short detached mark near the base.",
        "上部主体有两条交叉弯曲笔画；下方伸出长斜向或下降笔画，底部附近另有短的"
        "分离痕迹。",
    ),
    "obs-unk-001680": (
        "The image contains a tall angular composite at the left and a separate slim "
        "upright curved form at the right; the two groups are visibly distinct.",
        "图像左侧是高的折角组合形体，右侧另有窄长竖向弯曲形体；两组形体在图像中可"
        "明显区分。",
    ),
    "obs-unk-001681": (
        "The image shows a dense rectangular upper block, a narrow central stem, and "
        "several short branching marks toward the lower edge.",
        "图像上部是密集的方块状笔画块，中部有窄长主干，下缘有数条短分枝痕迹。",
    ),
    "obs-unk-001682": (
        "A short horizontal or arched upper contour sits above a broad curved lower "
        "form with a small interior opening.",
        "短横向或弧状上部轮廓位于较宽的弯曲下部形体之上，内部留有小型开放区域。",
    ),
    "obs-unk-001683": (
        "The compact image has a rounded central body, pointed or branched side marks, "
        "and a smaller rounded lower contour.",
        "紧凑图像有圆弧状中央主体，两侧有尖状或分枝痕迹，下部另有较小的圆弧轮廓。",
    ),
    "obs-unk-001684": (
        "The tall form has a broad outer contour, crossing diagonal interior strokes, "
        "and a rounded lower enclosure.",
        "高形图像有较宽外轮廓，内部斜向笔画交叉，下部有圆弧状围合形体。",
    ),
    "obs-unk-001685": (
        "The image is a dense upright composite with a short crossing upper mark, a "
        "central vertical axis, and small lower side projections.",
        "图像是密集竖向组合形体，上部有短交叉痕迹，中部有竖向主轴，下部有小型两侧"
        "外伸笔画。",
    ),
    "obs-unk-001686": (
        "The image repeats the dense upright composite, crossing upper mark, central "
        "axis, and small lower projections seen for obs-unk-001685; this is a visual "
        "comparison only.",
        "图像呈现与 obs-unk-001685 相同的密集竖向组合形体、上部交叉痕迹、中央主轴和"
        "下部小型外伸笔画；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001687": (
        "The image has a peaked upper contour, a compact central curved form, and "
        "several small rounded or detached marks near the lower right.",
        "图像上部有尖顶状轮廓，中部是紧凑弯曲形体，右下方附近有数个小型圆弧或分离"
        "痕迹。",
    ),
    "obs-unk-001688": (
        "The upper body contains two crossing curved strokes; a long diagonal or "
        "descending stroke extends below, with a short detached mark near the base.",
        "上部主体有两条交叉弯曲笔画；下方伸出长斜向或下降笔画，底部附近另有短的"
        "分离痕迹。",
    ),
    "obs-unk-001689": (
        "The image shows a dense upright upper block, a broad lower rectangular or "
        "rounded body, and a short detached mark near the lower edge.",
        "图像上部是密集竖向笔画块，下部有较宽的方块或圆弧状主体，下缘附近另有短的"
        "分离痕迹。",
    ),
    "obs-unk-001690": (
        "The image has a central crossing form, a short arrow-like projection at the "
        "left, a descending lower stroke, and a detached rectangular mark at the right.",
        "图像中央有交叉形体，左侧有短箭头状外伸笔画，下方有下降笔画，右侧另有分离"
        "的方块状痕迹。",
    ),
    "obs-unk-001691": (
        "The committed review image is nearly blank and does not show an observable "
        "glyph. No stroke, component, or identity observation can be made from "
        "this derivative.",
        "已提交的复核图像近乎纯白，未显示可观察字形。不能依据该派生图像记录笔画、"
        "构件或对象身份。",
    ),
    "obs-unk-001692": (
        "The image has a peaked upper contour, a compact central curved form, and "
        "several small rounded or detached marks near the lower right.",
        "图像上部有尖顶状轮廓，中部是紧凑弯曲形体，右下方附近有数个小型圆弧或分离"
        "痕迹。",
    ),
    "obs-unk-001693": (
        "The tall image shows a narrow upright central section, crossing side marks, "
        "and a broad lower block with short vertical divisions.",
        "高形图像有窄长中央竖向部分，两侧笔画交叉，下部是较宽的块状形体并有短竖向"
        "分隔痕迹。",
    ),
    "obs-unk-001694": (
        "The image repeats the narrow upright central section, crossing side marks, "
        "and broad lower block seen for obs-unk-001693; this is a visual comparison "
        "only.",
        "图像呈现与 obs-unk-001693 相同的窄长中央竖向部分、两侧交叉笔画和较宽下部块"
        "状形体；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001695": (
        "The image shows crossed and stacked upper strokes, a broad central "
        "horizontal mark, and a lower angular or rounded enclosure with short "
        "vertical and diagonal extensions.",
        "图像上部可见交叉和叠置笔画，中部有较宽横向痕迹，下部有近方角或圆弧状的"
        "围合形体，并带有短竖向和斜向延伸笔画。",
    ),
    "obs-unk-001696": (
        "The image has a curved outer contour at the left, a compact upper horizontal "
        "cluster, and a dense central-lower form with short interior divisions.",
        "图像左侧有弯曲外轮廓，上部有紧凑横向笔画簇，中下部是密集形体并带有短的"
        "内部分隔痕迹。",
    ),
    "obs-unk-001697": (
        "The image is a dense upright composite with a short crossing upper mark, a "
        "central vertical axis, and small lower side projections.",
        "图像是密集竖向组合形体，上部有短交叉痕迹，中部有竖向主轴，下部有小型两侧"
        "外伸笔画。",
    ),
    "obs-unk-001698": (
        "The image repeats the dense upright composite, crossing upper mark, central "
        "axis, and small lower projections seen for obs-unk-001697; this is a visual "
        "comparison only.",
        "图像呈现与 obs-unk-001697 相同的密集竖向组合形体、上部交叉痕迹、中央主轴和"
        "下部小型外伸笔画；这里只记录视觉比较，不作身份确认。",
    ),
    "obs-unk-001699": (
        "The image has several forked or branching upper strokes, a long descending "
        "central mark, and short curved side projections.",
        "图像上部有数条分叉或分枝笔画，中部有长下降痕迹，两侧有短弯曲外伸笔画。",
    ),
    "obs-unk-001700": (
        "The tall image contains a pointed outer contour, crossing interior strokes, "
        "and a narrow lower extension with short diagonal marks.",
        "高形图像有尖状外轮廓，内部笔画交叉，下部有窄长延伸形体和短斜向痕迹。",
    ),
    "obs-unk-000101": (
        "A narrow upright image has two detached short marks on the left and a "
        "long angular stroke that bends inward on the right.",
        "狭长直立图像左侧有两处分离短痕，右侧有一条向内折转的长折笔。",
    ),
    "obs-unk-000102": (
        "A compact vertical form has two thin left-side strokes, a crossed central "
        "bar, an angular upper-right mark, and a curved lower-right stroke.",
        "紧凑直立形体左侧有两条细笔，中部有交叉横笔，右上有折角痕，右下有弯曲笔画。",
    ),
    "obs-unk-000103": (
        "A dense upright image has a dark angular upper enclosure, several short "
        "descending marks, and a separate jagged stroke on the left.",
        "密集直立图像上部有深色折角轮廓和数个向下短痕，左侧另有锯齿状笔画。",
    ),
    "obs-unk-000104": (
        "A small upright image has a horizontal top bar, stacked central strokes, "
        "a rounded lower-left enclosure, and a narrow right extension.",
        "小型直立图像上方有横笔，中部笔画叠置，左下有弧形围合，右侧有窄长伸出。",
    ),
    "obs-unk-000105": (
        "A tall narrow image has a slanted upper cluster with branching side marks "
        "and several long descending strokes.",
        "高而狭长图像上部为斜向密集笔群，两侧有分支短痕，并有数条长下降笔画。",
    ),
    "obs-unk-000106": (
        "A compact image has a pointed upper-left contour, a zigzag central stroke, "
        "and multiple short lower projections.",
        "紧凑图像左上有尖状轮廓，中部有锯齿状笔画，下方有多处短伸出。",
    ),
    "obs-unk-000107": (
        "A compact image has a pointed upper contour, a narrow central crossing, "
        "and several short lower projections.",
        "紧凑图像上方有尖状轮廓，中部有窄的交叉笔，下方有多处短伸出。",
    ),
    "obs-unk-000108": (
        "A narrow image has a rounded left loop, an angular upper-right cluster, "
        "and several separated descending strokes.",
        "狭长图像左侧有弧形环状笔群，右上有折角密集笔群，下方有数个分离下降痕。",
    ),
    "obs-unk-000109": (
        "An open angular form has a long slanting upper stroke, a short vertical "
        "left edge, and two rounded lower marks.",
        "开放折角形体上方有长斜笔，左侧有短竖边，下方有两处弧形短痕。",
    ),
    "obs-unk-000110": (
        "A compact image has a pointed upper-left contour, a zigzag central stroke, "
        "and multiple short lower projections.",
        "紧凑图像左上有尖状轮廓，中部有锯齿状笔画，下方有多处短伸出。",
    ),
    "obs-unk-000111": (
        "A vertical form has a small rounded loop at top, a crossing central stem, "
        "stacked horizontal marks, and a short lower bar.",
        "直立形体顶部有小弧环，中部有交叉主干和叠置横笔，下方有短横笔。",
    ),
    "obs-unk-000112": (
        "A compact image has a pointed upper contour, a narrow central crossing, "
        "and several short lower projections.",
        "紧凑图像上方有尖状轮廓，中部有窄的交叉笔，下方有多处短伸出。",
    ),
    "obs-unk-000113": (
        "A small upright form has a long central vertical stroke, short crossbars "
        "on both sides, and a pointed lower projection.",
        "小型直立形体有长中央竖笔，两侧有短横笔，下方有尖状伸出。",
    ),
    "obs-unk-000114": (
        "An open angular form has a long slanting upper stroke, a short vertical "
        "left edge, and two rounded lower marks.",
        "开放折角形体上方有长斜笔，左侧有短竖边，下方有两处弧形短痕。",
    ),
    "obs-unk-000115": (
        "A compact image has a pointed upper-left contour, a zigzag central stroke, "
        "and multiple short lower projections.",
        "紧凑图像左上有尖状轮廓，中部有锯齿状笔画，下方有多处短伸出。",
    ),
    "obs-unk-000116": (
        "A compact image has an angular upper cluster, a rounded lower enclosure, "
        "and a short left-side projection.",
        "紧凑图像上部有折角笔群，下方有弧形围合，左侧有短伸出。",
    ),
    "obs-unk-000117": (
        "A small upright form has a long central vertical stroke, short crossbars "
        "on both sides, and a pointed lower projection.",
        "小型直立形体有长中央竖笔，两侧有短横笔，下方有尖状伸出。",
    ),
    "obs-unk-000118": (
        "A small dense form has two pointed upper strokes, a narrow central vertical, "
        "and a short lower crossing.",
        "小型密集形体上方有两处尖状笔，中部有窄竖笔，下方有短交叉笔。",
    ),
    "obs-unk-000119": (
        "A horizontal upper bar sits over two vertical stems; both stems end in "
        "forked lower strokes.",
        "上方横笔下有两条竖干，两条竖干下端都以分叉笔收束。",
    ),
    "obs-unk-000120": (
        "A narrow upright form has a long central vertical with several short "
        "horizontal crossings and a stepped lower outline.",
        "狭长直立形体有长中央竖笔，交叉数条短横笔，下方轮廓呈阶梯状。",
    ),
    "obs-unk-000121": (
        "A narrow upright image has a small forked top cluster, a long central "
        "stroke, and several short angled side marks.",
        "狭长直立图像顶部有小分叉笔群，中部有长主笔，两侧有数个短斜痕。",
    ),
    "obs-unk-000122": (
        "An oval enclosure contains a slanting central stroke and a short lower "
        "branch.",
        "椭圆围合内有斜向中央笔画，下方有一处短分支。",
    ),
    "obs-unk-000123": (
        "A compact angular image has two projecting upper strokes, a crossed middle, "
        "and a long lower-right stroke.",
        "紧凑折角图像上方有两处伸出笔，中部交叉，下方右侧有长笔。",
    ),
    "obs-unk-000124": (
        "A rounded vertical contour has two short interior crossbars and a curved "
        "lower extension.",
        "弧形直立轮廓内有两条短横笔，下方有弯曲伸出。",
    ),
    "obs-unk-000125": (
        "A small angular form has a short upper bar, a slanting central stroke, and "
        "a separated lower projection.",
        "小型折角形体上方有短横笔，中部有斜笔，下方有分离伸出。",
    ),
    "obs-unk-000126": (
        "A compact form has three short upper prongs, a central vertical, and a "
        "rounded lower loop above a horizontal base.",
        "紧凑形体上方有三处短尖，中部有竖笔，下方弧环位于横向底笔上方。",
    ),
    "obs-unk-000127": (
        "A narrow upright form has long side strokes, a central crossing, and a "
        "short lower diagonal.",
        "狭长直立形体有长侧笔，中部交叉，下方有短斜笔。",
    ),
    "obs-unk-000128": (
        "Four separated slanting strokes appear as two upper marks and two lower "
        "marks.",
        "四条分离斜笔分为上方两痕和下方两痕。",
    ),
    "obs-unk-000129": (
        "A tall narrow image has two long vertical strokes and a short diagonal "
        "crossing near the upper middle.",
        "高而狭长图像有两条长竖笔，中上部有短斜交叉笔。",
    ),
    "obs-unk-000130": (
        "An arched upper contour encloses a short central crossing with a narrow "
        "lower stem.",
        "拱形上部轮廓围住短中央交叉笔，下方接窄长笔干。",
    ),
    "obs-unk-000131": (
        "A rounded upright form has two interior crossbars and a curved lower "
        "sweep.",
        "弧形直立形体内有两条横笔，下方有弯曲扫笔。",
    ),
    "obs-unk-000132": (
        "A rounded open enclosure has a short top projection, an interior diagonal, "
        "and two narrow lower supports.",
        "弧形开放围合上方有短伸出，内部有斜笔，下方有两条窄支撑。",
    ),
    "obs-unk-000133": (
        "An open angular form has a short left bar, a central crossing, and two "
        "descending right-side strokes.",
        "开放折角形体左侧有短横笔，中部交叉，右侧有两条下降笔。",
    ),
    "obs-unk-000134": (
        "A dense form has two pointed upper clusters, a central crossing, and a "
        "long stepped lower-right stroke.",
        "密集形体上方有两处尖状笔群，中部交叉，右下有长阶梯状笔。",
    ),
    "obs-unk-000135": (
        "A narrow image shows a left vertical cluster, a slanting lower stroke, and "
        "a separate small enclosed mark on the right.",
        "狭长图像左侧有竖向笔群，下方有斜笔，右侧另有小围合痕。",
    ),
    "obs-unk-000136": (
        "A compact form has paired pointed side strokes around a long central "
        "vertical.",
        "紧凑形体两侧有成对尖状笔，围绕一条长中央竖笔。",
    ),
    "obs-unk-000137": (
        "A dense dark form has two rounded upper lobes and a broad curved lower "
        "stroke.",
        "密集深色形体上方有两处弧形隆起，下方有宽大的弯曲笔。",
    ),
    "obs-unk-000138": (
        "A compact form has two pointed upright strokes over a short horizontal base "
        "and a rounded lower mark.",
        "紧凑形体有两条尖状直立笔，下方为短横底笔和弧形痕。",
    ),
    "obs-unk-000139": (
        "An upright form has two pointed upper strokes, several descending diagonals, "
        "and a small rounded lower mark.",
        "直立形体上方有两条尖笔，下方有数条下降斜笔和小弧形痕。",
    ),
    "obs-unk-000140": (
        "A rounded upright contour has two short crossbars and a curved lower "
        "extension.",
        "弧形直立轮廓内有两条短横笔，下方有弯曲伸出。",
    ),
    "obs-unk-000141": (
        "A narrow upright image has an arched upper contour, a dense central "
        "crossing, and a long lower-left projection.",
        "狭长直立图像上方有拱形轮廓，中部密集交叉，下方左侧有长伸出。",
    ),
    "obs-unk-000142": (
        "A narrow upright form has a pointed upper enclosure, a central vertical, "
        "and two angled lower projections.",
        "狭长直立形体上方有尖状围合，中部有竖笔，下方有两处斜向伸出。",
    ),
    "obs-unk-000143": (
        "A narrow upright image has a pointed upper contour, a central crossing, "
        "and paired lower angular strokes.",
        "狭长直立图像上方有尖状轮廓，中部交叉，下方有成对折角笔。",
    ),
    "obs-unk-000144": (
        "An open form has two long upper slants, a narrow central stem, and a "
        "forked lower extension.",
        "开放形体上方有两条长斜笔，中部为窄笔干，下方有分叉伸出。",
    ),
    "obs-unk-000145": (
        "A narrow form has two long upper strokes, a dense center, and a thin "
        "descending lower stroke.",
        "狭长形体上方有两条长笔，中部密集，下方有细长下降笔。",
    ),
    "obs-unk-000146": (
        "A compact upright image has a pointed upper contour, short interior "
        "crossings, and several lower projections.",
        "紧凑直立图像上方有尖状轮廓，内部有短交叉笔，下方有数处伸出。",
    ),
    "obs-unk-000147": (
        "An angular form has a short upper bar, a long left diagonal, and a split "
        "lower-right stroke.",
        "折角形体上方有短横笔，左侧有长斜笔，右下有分开的笔画。",
    ),
    "obs-unk-000148": (
        "A dense dark form has a pointed upper cap, a compact central mass, and "
        "several short lower projections.",
        "密集深色形体上方有尖顶，中部成团，下方有数处短伸出。",
    ),
    "obs-unk-000149": (
        "An open form has two short upper strokes, a central horizontal crossing, "
        "and a rounded lower sweep.",
        "开放形体上方有两条短笔，中部有横向交叉，下方有弧形扫笔。",
    ),
    "obs-unk-000150": (
        "A compact form has separated upper side marks, a central crossing, and a "
        "long lower diagonal.",
        "紧凑形体上部两侧有分离短痕，中部交叉，下方有长斜笔。",
    ),
    "obs-unk-000151": (
        "An open form has two upper slants, separated left marks, and a long curved "
        "stroke on the right.",
        "开放形体上方有两条斜笔，左侧有分离短痕，右侧有长弯笔。",
    ),
    "obs-unk-000152": (
        "A compact form has a long upper crossbar, a central vertical, and a broad "
        "curved lower stroke.",
        "紧凑形体上方有长横笔，中部有竖笔，下方有宽大的弯曲笔。",
    ),
    "obs-unk-000153": (
        "A compact symmetrical form has a pointed upper pair, a horizontal middle "
        "bar, and a rounded lower enclosure.",
        "紧凑对称形体上方有成对尖笔，中部有横笔，下方有弧形围合。",
    ),
    "obs-unk-000154": (
        "A dense horizontal form has several stacked crossbars and a long slanting "
        "lower-right stroke.",
        "密集横向形体有数条叠置横笔，右下有长斜笔。",
    ),
    "obs-unk-000155": (
        "An open form has paired curved upper strokes, a central crossing, and a "
        "pointed lower extension.",
        "开放形体上方有成对弧形笔，中部交叉，下方有尖状伸出。",
    ),
    "obs-unk-000156": (
        "A compact dense form has a long upper bar, crossing central strokes, and a "
        "rounded lower enclosure.",
        "紧凑密集形体上方有长横笔，中部交叉，下方有弧形围合。",
    ),
    "obs-unk-000157": (
        "An open form has a narrow left vertical cluster, a central descending "
        "stroke, and a rounded right loop.",
        "开放形体左侧有窄竖笔群，中部有下降笔，右侧有弧形环。",
    ),
    "obs-unk-000158": (
        "A compact angular form has a pointed upper-left mark, a central crossing, "
        "and a long lower-right stroke.",
        "紧凑折角形体左上有尖状痕，中部交叉，右下有长笔。",
    ),
    "obs-unk-000159": (
        "An open form has a short upper-left cluster, a central vertical, and a "
        "rounded lower-right mark.",
        "开放形体左上有短笔群，中部有竖笔，右下有弧形痕。",
    ),
    "obs-unk-000160": (
        "A narrow form has a short upper bar, a long descending central stroke, and "
        "a rounded lower loop.",
        "狭长形体上方有短横笔，中部有长下降笔，下方有弧形环。",
    ),
    "obs-unk-000161": (
        "A compact symmetrical form has a pointed upper pair, a horizontal middle "
        "bar, and a rounded lower enclosure.",
        "紧凑对称形体上方有成对尖笔，中部有横笔，下方有弧形围合。",
    ),
    "obs-unk-000162": (
        "A narrow form has a curved left loop, a central vertical, and a pointed "
        "right projection.",
        "狭长形体左侧有弧形环，中部有竖笔，右侧有尖状伸出。",
    ),
    "obs-unk-000163": (
        "A dense horizontal form has several stacked crossbars and a long slanting "
        "lower-right stroke.",
        "密集横向形体有数条叠置横笔，右下有长斜笔。",
    ),
    "obs-unk-000164": (
        "An arched upper contour has short interior crossings and a long lower "
        "stem.",
        "拱形上部轮廓内有短交叉笔，下方接长笔干。",
    ),
    "obs-unk-000165": (
        "A narrow upright image has an arched upper contour, a dense central "
        "crossing, and a long lower-left projection.",
        "狭长直立图像上方有拱形轮廓，中部密集交叉，下方左侧有长伸出。",
    ),
    "obs-unk-000166": (
        "A narrow upright image has a pointed upper contour, a central crossing, "
        "and paired lower angular strokes.",
        "狭长直立图像上方有尖状轮廓，中部交叉，下方有成对折角笔。",
    ),
    "obs-unk-000167": (
        "A narrow upright form has a pointed upper enclosure, a central vertical, "
        "and two angled lower projections.",
        "狭长直立形体上方有尖状围合，中部有竖笔，下方有两处斜向伸出。",
    ),
    "obs-unk-000168": (
        "A compact upright image has an arched upper contour, short interior marks, "
        "and several lower projections.",
        "紧凑直立图像上方有拱形轮廓，内部有短痕，下方有数处伸出。",
    ),
    "obs-unk-000169": (
        "A dense angular image has crossing central strokes, short side projections, "
        "and two long lower diagonals.",
        "密集折角图像中部笔画交叉，两侧有短伸出，下方有两条长斜笔。",
    ),
    "obs-unk-000170": (
        "A complex form has a rounded upper cluster, a descending central stroke, and "
        "a jagged lower base.",
        "复杂形体上方有弧形笔群，中部有下降笔，下方底部呈锯齿状。",
    ),
    "obs-unk-000171": (
        "An open form has paired pointed side marks around a narrow central gap and "
        "short lower strokes.",
        "开放形体两侧有成对尖状痕，中部留窄间隙，下方有短笔。",
    ),
    "obs-unk-000172": (
        "A compact angular form has a long central vertical, a horizontal crossing, "
        "and a curved lower-right stroke.",
        "紧凑折角形体有长中央竖笔，中部横向交叉，右下有弯曲笔。",
    ),
    "obs-unk-000173": (
        "An open form has two short upper strokes, a central horizontal crossing, "
        "and a rounded lower sweep.",
        "开放形体上方有两条短笔，中部有横向交叉，下方有弧形扫笔。",
    ),
    "obs-unk-000174": (
        "A rounded upper enclosure has a central crossing and two narrow lower "
        "projections.",
        "弧形上部围合内有中央交叉笔，下方有两处窄伸出。",
    ),
    "obs-unk-000175": (
        "A compact form has a short upper bar, a central angled crossing, and a "
        "curved lower extension.",
        "紧凑形体上方有短横笔，中部斜向交叉，下方有弯曲伸出。",
    ),
    "obs-unk-000176": (
        "A faint partial image shows short horizontal strokes on the left, a narrow "
        "vertical center, and a long lower horizontal stroke.",
        "模糊残缺图像左侧有短横笔，中部有窄竖笔，下方有长横笔。",
    ),
    "obs-unk-000177": (
        "A compact form has several stacked upper bars, a central vertical, and a "
        "curved lower sweep.",
        "紧凑形体上方有数条叠置横笔，中部有竖笔，下方有弯曲扫笔。",
    ),
    "obs-unk-000178": (
        "A dense upright form has two pointed side contours, a narrow central gap, "
        "and long lower projections.",
        "密集直立形体两侧有尖状轮廓，中部留窄间隙，下方有长伸出。",
    ),
    "obs-unk-000179": (
        "An open form has a short left cluster, a central descending stroke, and a "
        "rounded right loop.",
        "开放形体左侧有短笔群，中部有下降笔，右侧有弧形环。",
    ),
    "obs-unk-000180": (
        "A compact symmetrical form has several short upper prongs, a central "
        "vertical, and a long lower point.",
        "紧凑对称形体上方有数处短尖，中部有竖笔，下方有长尖状伸出。",
    ),
    "obs-unk-000181": (
        "A dense angular form has several crossing strokes, a short upper-left "
        "projection, and a pointed lower extension.",
        "密集折角形体有数条交叉笔，左上有短伸出，下方有尖状伸出。",
    ),
    "obs-unk-000182": (
        "An open form has a rounded left loop, a central crossing, and a long "
        "lower-right stroke.",
        "开放形体左侧有弧形环，中部交叉，右下有长笔。",
    ),
    "obs-unk-000183": (
        "A compact form has a pointed upper mark, a central enclosed crossing, and "
        "a long lower-right diagonal.",
        "紧凑形体上方有尖状痕，中部有围合交叉，右下有长斜笔。",
    ),
    "obs-unk-000184": (
        "A dense angular image has crossing central strokes, short side projections, "
        "and two long lower diagonals.",
        "密集折角图像中部笔画交叉，两侧有短伸出，下方有两条长斜笔。",
    ),
    "obs-unk-000185": (
        "A compact form has paired pointed upper strokes, a central crossing, and a "
        "long lower extension.",
        "紧凑形体上方有成对尖笔，中部交叉，下方有长伸出。",
    ),
    "obs-unk-000186": (
        "An open form has paired pointed side marks around a narrow central gap and "
        "short lower strokes.",
        "开放形体两侧有成对尖状痕，中部留窄间隙，下方有短笔。",
    ),
    "obs-unk-000187": (
        "An open angular form has a rounded left loop, a central crossing, and a "
        "long right stem.",
        "开放折角形体左侧有弧形环，中部交叉，右侧有长笔干。",
    ),
    "obs-unk-000188": (
        "A narrow image has three short upper marks, a horizontal crossbar, and a "
        "long descending diagonal.",
        "狭长图像上方有三处短痕，中部有横笔，下方有长下降斜笔。",
    ),
    "obs-unk-000189": (
        "A compact symmetrical form has several short upper prongs, a central "
        "vertical, and a long lower point.",
        "紧凑对称形体上方有数处短尖，中部有竖笔，下方有长尖状伸出。",
    ),
    "obs-unk-000190": (
        "An open form has a rounded left loop, a central crossing, and a long "
        "lower-right stroke.",
        "开放形体左侧有弧形环，中部交叉，右下有长笔。",
    ),
    "obs-unk-000191": (
        "An open form has branched left strokes, stacked upper crossbars, and a long "
        "curved right stroke.",
        "开放形体左侧有分支笔，上方有叠置横笔，右侧有长弯笔。",
    ),
    "obs-unk-000192": (
        "A compact symmetrical form has a rounded upper mark, a central vertical, "
        "and paired lower side strokes.",
        "紧凑对称形体上方有弧形痕，中部有竖笔，下方有成对侧笔。",
    ),
    "obs-unk-000193": (
        "A dense form has two long side strokes, several central crossbars, and a "
        "lower diagonal.",
        "密集形体有两条长侧笔，中部有数条横笔，下方有斜笔。",
    ),
    "obs-unk-000194": (
        "A compact form has two upright side strokes, a central crossing, and a "
        "short lower diagonal.",
        "紧凑形体有两条直立侧笔，中部交叉，下方有短斜笔。",
    ),
    "obs-unk-000195": (
        "Two separated marks are visible: a narrow left cluster and a rounded right "
        "enclosure with an upper diagonal.",
        "图像中可见两处分离痕：左侧为窄笔群，右侧为带上斜笔的弧形围合。",
    ),
    "obs-unk-000196": (
        "A compact form has a long upper bar, crossing central strokes, and a broad "
        "curved lower stroke.",
        "紧凑形体上方有长横笔，中部交叉，下方有宽大的弯曲笔。",
    ),
    "obs-unk-000197": (
        "A compact form has a long upper bar, crossing central strokes, and a broad "
        "curved lower stroke.",
        "紧凑形体上方有长横笔，中部交叉，下方有宽大的弯曲笔。",
    ),
    "obs-unk-000198": (
        "A compact symmetrical form has several short upper prongs, a central "
        "vertical, and a long lower point.",
        "紧凑对称形体上方有数处短尖，中部有竖笔，下方有长尖状伸出。",
    ),
    "obs-unk-000199": (
        "A compact form has a rounded lower enclosure, two short upper strokes, and "
        "a central vertical.",
        "紧凑形体下方有弧形围合，上方有两条短笔，中部有竖笔。",
    ),
    "obs-unk-000200": (
        "A dense upright form has several pointed upper strokes, a narrow central "
        "stem, and multiple short lower projections.",
        "密集直立形体上方有数条尖笔，中部为窄笔干，下方有多处短伸出。",
    ),
    "obs-unk-000201": (
        "A compact form has a pointed upper cluster, a narrow central stem, and "
        "paired lower strokes that spread outward.",
        "紧凑形体上方有尖状笔画组，中部有窄笔干，下方有向外分开的成对笔画。",
    ),
    "obs-unk-000202": (
        "The image repeats the compact pointed upper cluster, narrow central stem, "
        "and paired lower spreading strokes seen for obs-unk-000201; visual "
        "comparison only.",
        "图像与视觉对比的 obs-unk-000201 相似，均见紧凑尖状上部、窄中央笔干和向下分开的成对笔画；不作身份确认。",
    ),
    "obs-unk-000203": (
        "A tall narrow form has a short upper crossbar, two upright side strokes, "
        "and a long descending central stroke with small side marks.",
        "高状窄长形体上部有短横栏，两侧有直向笔画，中央为长下降笔干，并有小型侧痕迹。",
    ),
    "obs-unk-000204": (
        "Two upright side groups flank a narrow center; the lower area contains "
        "short crossing strokes and a slanting extension.",
        "两个直向侧笔组包夹中部窄隙；下部可见短交叉笔和一处斜向外伸痕迹。",
    ),
    "obs-unk-000205": (
        "A dense form has an angular upper contour, crossing middle strokes, and "
        "several short lower projections.",
        "密集形体上部为折角轮廓，中部笔画交叉，下方有多处短外伸痕迹。",
    ),
    "obs-unk-000206": (
        "A closed-looking outer contour encloses dense crossing and diagonal "
        "strokes, with short projections along both sides.",
        "图像外围轮廓较封闭，内部笔画密集交叉并带斜向，两侧均有短的外伸痕迹。",
    ),
    "obs-unk-000207": (
        "An oval outer enclosure contains a central upright stroke with a short "
        "diagonal mark near its lower portion.",
        "图像有大致椭圆的外围围合，内部为中央直笔，下部附近有一处短斜笔。",
    ),
    "obs-unk-000208": (
        "A forked upper stem rises above a trapezoid-like lower block; a short "
        "horizontal mark crosses the middle.",
        "上部为分叉的直向笔干，下方为较宽的梯形块状体，中部有短横笔。",
    ),
    "obs-unk-000209": (
        "A compact form has a rounded cap-like upper contour, a central vertical "
        "axis, and several short horizontal lower strokes.",
        "紧凑形体上部为弧形盖状轮廓，中部有直向中轴，下方排列多条短横笔。",
    ),
    "obs-unk-000210": (
        "Two open upper branches flank a central descending stroke; the lower end "
        "turns into a short hooked mark.",
        "两个开放的上部支分夹住中央下降笔画，下端向一侧转成短钩状痕迹。",
    ),
    "obs-unk-000211": (
        "A forked upper pair sits above a narrow central stem and a broad lower "
        "horizontal bar with short side ends.",
        "上部为分叉成对笔画，下接窄中央笔干，底部为两端较短的宽横栏。",
    ),
    "obs-unk-000212": (
        "The left side is a dense knot of short strokes, while the right side has "
        "a long descending curved stroke and small branches.",
        "图像左侧为短笔画密集的结，右侧有长下降弯曲笔和小型分支。",
    ),
    "obs-unk-000213": (
        "A sparse form shows several upright and diagonal strokes, with small "
        "separated marks near the upper left and lower right.",
        "稀疏形体可见多条直向和斜向笔画，左上及右下附近各有小型分离痕迹。",
    ),
    "obs-unk-000214": (
        "A narrow upright form has three short upper prongs, a central stem, and "
        "stacked lower crossbars forming a tapered base.",
        "窄长直立形体上方有三处短尖，中部有直向笔干，下方叠置横笔，底部逐渐收尖。",
    ),
    "obs-unk-000215": (
        "A symmetrical stacked form has a small upper triangle, a central bar, and "
        "a broad lower V-shaped contour.",
        "对称叠置形体上部有小三角形，中部有横栏，下方有较宽的开叉轮廓。",
    ),
    "obs-unk-000216": (
        "A long slanting stroke stands on the left of a narrow upright group with "
        "two small enclosed or stacked lower marks.",
        "一条长斜笔位于左侧，右侧为窄长直向笔组，下方可见两个小型围合或叠置痕迹。",
    ),
    "obs-unk-000217": (
        "A rounded upper contour sits above a long descending diagonal; the lower "
        "area contains several short horizontal strokes.",
        "上部为弧形轮廓，下接一条长斜下降笔，底部可见多条短横笔。",
    ),
    "obs-unk-000218": (
        "An open angular form has a left loop-like contour, a central crossing, and "
        "a long upright right stroke.",
        "开放形体左侧有环状轮廓，中部交叉，右侧有长直向笔画。",
    ),
    "obs-unk-000219": (
        "A compact form has branched upper strokes, a long central diagonal, and a "
        "short curved lower extension.",
        "紧凑形体上部有分支笔画，中部有长斜笔，下方有短弯曲外伸痕迹。",
    ),
    "obs-unk-000220": (
        "The image repeats the rounded upper contour, long descending diagonal, and "
        "short lower horizontal strokes seen for obs-unk-000217; visual comparison "
        "only.",
        "图像与视觉对比的 obs-unk-000217 相似，均见弧形轮廓、向下长斜笔和底部短横笔；不作身份确认。",
    ),
    "obs-unk-000221": (
        "A forked upper contour rises above a narrow central stem; short lower "
        "branches extend outward on both sides.",
        "分叉的上部轮廓位于窄中央笔干之上；下方两侧各有向外伸出的短分支。",
    ),
    "obs-unk-000222": (
        "A compact crossed form has two long diagonal side strokes, a central "
        "crossing, and short lower projections.",
        "紧凑交叉形体有两条长斜侧笔，中部交叉，下方有短外伸痕迹。",
    ),
    "obs-unk-000223": (
        "A dense closed-looking form has a broad upright left section, angular "
        "central crossings, and short projections on the right.",
        "密集且外围较封闭的形体左侧为宽直立部分，中部有折角交叉，右侧有短外伸痕迹。",
    ),
    "obs-unk-000224": (
        "Two separated upright groups are visible: a narrow left cluster and a "
        "right cluster with crossing upper strokes and a curved lower extension.",
        "图像可见两个分离的直立笔组：左侧为窄笔组，右侧上部交叉并向下接弯曲外伸痕迹。",
    ),
    "obs-unk-000225": (
        "A symmetrical stacked form has a broad upper horizontal bar, central "
        "crossing diagonals, and a long lower horizontal base.",
        "对称叠置形体上部有宽横栏，中部为交叉斜笔，下方有长横向底部。",
    ),
    "obs-unk-000226": (
        "A pointed upper cap sits above a narrow central stem; two lower side "
        "groups contain several short prongs.",
        "尖状上部位于窄中央笔干之上；下方两侧笔组各含数处短尖痕迹。",
    ),
    "obs-unk-000227": (
        "A broad upper horizontal form sits above a central descending stem and "
        "two small lower pendant clusters.",
        "宽大的上部横向形体下接中央下降笔干，底部有两个小型下垂笔组。",
    ),
    "obs-unk-000228": (
        "The image repeats the compact crossed form, long diagonal side strokes, "
        "and short lower projections seen for obs-unk-000222; visual comparison "
        "only.",
        "图像与视觉对比的 obs-unk-000222 相似，均见紧凑交叉形体、长斜侧笔和下方短外伸痕迹；不作身份确认。",
    ),
    "obs-unk-000229": (
        "A dense form contains several upright and curved strokes, with a small "
        "rounded mark on the left and clustered projections on the right.",
        "密集形体含多条直向和弯曲笔画，左侧有小型弧形痕迹，右侧有成组外伸痕迹。",
    ),
    "obs-unk-000230": (
        "Two open upper branches meet a descending central stem; a short "
        "horizontal base closes the lower end.",
        "两个开放的上部支分汇入中央下降笔干；下端由短横向底部收束。",
    ),
    "obs-unk-000231": (
        "A tall narrow dense form has parallel side strokes, a compact central "
        "cluster, and a short lower block.",
        "高而窄的密集形体有平行侧笔，中部为紧凑笔组，下方有短块状部分。",
    ),
    "obs-unk-000232": (
        "An open rounded upper contour contains a short central crossbar and a "
        "long curved stroke descending on the right.",
        "开放的弧形上部轮廓内有短中央横笔，右侧向下接长弯曲笔画。",
    ),
    "obs-unk-000233": (
        "A dense upper cluster has crossing strokes and a rounded lower enclosure "
        "with a short right-side extension.",
        "密集上部笔组含交叉笔画，下方有弧形围合，并带一处右侧短外伸痕迹。",
    ),
    "obs-unk-000234": (
        "A compact upright form has a central descending stem with two diagonal "
        "side branches crossing near the middle.",
        "紧凑直立形体有中央下降笔干，中部附近交叉着两条斜向侧分支。",
    ),
    "obs-unk-000235": (
        "The image repeats the narrow upright form, upper short prongs, and "
        "stacked lower crossbars seen for obs-unk-000214; visual comparison only.",
        "图像与视觉对比的 obs-unk-000214 相似，均见窄长直立形体、上方短尖和下方叠置横笔；不作身份确认。",
    ),
    "obs-unk-000236": (
        "A forked upper section sits above a small central block and a broad "
        "lower horizontal bar.",
        "分叉的上部位于小型中央块状部分之上，下方有宽横向底栏。",
    ),
    "obs-unk-000237": (
        "An open rounded upper enclosure contains dense short strokes; a long "
        "descending stroke turns outward on the lower right.",
        "开放的弧形上部围合内有密集短笔，下方右侧接长下降笔并向外转出。",
    ),
    "obs-unk-000238": (
        "The image repeats the open rounded enclosure and long lower-right "
        "descending stroke seen for obs-unk-000237; visual comparison only.",
        "图像与视觉对比的 obs-unk-000237 相似，均见开放弧形围合和右下长下降笔；不作身份确认。",
    ),
    "obs-unk-000239": (
        "Two small upper groups flank a central gap; the lower area has a long "
        "diagonal stroke and a short hooked extension.",
        "两个小型上部笔组夹住中央空隙；下方有长斜笔和短钩状外伸痕迹。",
    ),
    "obs-unk-000240": (
        "Two separated marks are visible: a narrow left form with a crossbar and "
        "long diagonal, and a small closed-looking right form.",
        "图像可见两个分离痕迹：左侧窄形体带横笔和长斜笔，右侧为小型外围较封闭形体。",
    ),
    "obs-unk-000241": (
        "Several descending strokes hang from an angled upper section and meet a "
        "rounded lower bowl-like contour.",
        "数条下降笔画从倾斜的上部形体垂下，并连接到弧形的下部承托轮廓。",
    ),
    "obs-unk-000242": (
        "The image repeats the forked upper pair, narrow central stem, and broad "
        "lower bar seen for obs-unk-000211; visual comparison only.",
        "图像与视觉对比的 obs-unk-000211 相似，均见分叉上部、窄中央笔干和宽下部横栏；不作身份确认。",
    ),
    "obs-unk-000243": (
        "Two small upper side marks flank a long central diagonal, with a short "
        "lower stroke extending below the crossing.",
        "两个小型上部侧痕迹夹住长中央斜笔，交叉处下方还有一条短笔。",
    ),
    "obs-unk-000244": (
        "Paired curved side contours flank a central angular crossing; short "
        "strokes project from the lower middle.",
        "成对弯曲侧轮廓夹住中央折角交叉，下方中部有短笔向外伸出。",
    ),
    "obs-unk-000245": (
        "A rectangular outer enclosure has a broad upper bar, two upright inner "
        "strokes, and several short lower crossbars.",
        "矩形外围围合有宽上横栏、两条内部直笔和数条下部短横笔。",
    ),
    "obs-unk-000246": (
        "The image repeats the compact pointed upper cluster, narrow central stem, "
        "and paired lower spreading strokes seen for obs-unk-000201; visual "
        "comparison only.",
        "图像与视觉对比的 obs-unk-000201 相似，均见紧凑尖状上部、窄中央笔干和向下分开的成对笔画；不作身份确认。",
    ),
    "obs-unk-000247": (
        "Two forked side branches flank a central descending stroke and meet a "
        "rounded lower bowl-like contour.",
        "两个分叉的侧分支夹住中央下降笔，并在下方连接到弧形承托轮廓。",
    ),
    "obs-unk-000248": (
        "The image repeats the symmetrical stacked form, small upper triangle, "
        "central bar, and broad lower contour seen for obs-unk-000215; visual "
        "comparison only.",
        "图像与视觉对比的 obs-unk-000215 相似，均见对称叠置形体、小上三角、中部横栏和宽下部轮廓；不作身份确认。",
    ),
    "obs-unk-000249": (
        "A narrow upright left stroke stands beside a denser curved right group "
        "with several short lower projections.",
        "窄直立左笔旁边是较密集的右侧弯曲笔组，下方有数处短外伸痕迹。",
    ),
    "obs-unk-000250": (
        "The image repeats the compact crossed form, long diagonal side strokes, "
        "and short lower projections seen for obs-unk-000222; visual comparison "
        "only.",
        "图像与视觉对比的 obs-unk-000222 相似，均见紧凑交叉形体、长斜侧笔和下方短外伸痕迹；不作身份确认。",
    ),
    "obs-unk-000251": (
        "Two long sinuous upright strokes run in parallel, with short branch marks "
        "near the upper left and lower ends.",
        "两条长而曲折的直立笔并行分布，上左及下端附近有短分支痕迹。",
    ),
    "obs-unk-000252": (
        "A rounded outer enclosure contains a dense central angular cluster; a "
        "short horizontal bar crosses the lower portion.",
        "弧形外围围合内有密集中央折角笔组，下部由短横栏横贯。",
    ),
    "obs-unk-000253": (
        "A broad arched upper contour leads into a long descending curved stroke "
        "on the right and a short lower-left mark.",
        "宽弧形上部轮廓向右下连接长弯曲笔，下左另有短痕迹。",
    ),
    "obs-unk-000254": (
        "A short upper crossbar has a rightward branch; below it are a slanting "
        "stem and two stacked lower bars.",
        "短上横栏向右伸出分支；下方有斜向笔干和两层叠置下部横栏。",
    ),
    "obs-unk-000255": (
        "The image repeats the broad arched contour, long descending right stroke, "
        "and short lower-left mark seen for obs-unk-000253; visual comparison only.",
        "图像与视觉对比的 obs-unk-000253 相似，均见宽弧形轮廓、右下长弯曲笔和下左短痕迹；不作身份确认。",
    ),
    "obs-unk-000256": (
        "The tall narrow dense form repeats the parallel side strokes, compact "
        "central cluster, and short lower block seen for obs-unk-000231; visual "
        "comparison only.",
        "高而窄的密集形体与视觉对比的 obs-unk-000231 相似，均见平行侧笔、紧凑中央笔组和短下部块；不作身份确认。",
    ),
    "obs-unk-000257": (
        "The image repeats the compact pointed upper cluster, narrow central stem, "
        "and paired lower spreading strokes seen for obs-unk-000201; visual "
        "comparison only.",
        "图像与视觉对比的 obs-unk-000201 相似，均见紧凑尖状上部、窄中央笔干和向下分开的成对笔画；不作身份确认。",
    ),
    "obs-unk-000258": (
        "The image repeats the compact pointed upper cluster, narrow central stem, "
        "and paired lower spreading strokes seen for obs-unk-000201; visual "
        "comparison only.",
        "图像与视觉对比的 obs-unk-000201 相似，均见紧凑尖状上部、窄中央笔干和向下分开的成对笔画；不作身份确认。",
    ),
    "obs-unk-000259": (
        "Several small branched marks sit above a long horizontal bar; short "
        "upright strokes descend from the right side.",
        "数处小型分支痕迹位于长横栏上方，右侧向下接短直立笔。",
    ),
    "obs-unk-000260": (
        "A compact lower group has three descending upright strokes joined by "
        "diagonal branches and a short upper central mark.",
        "紧凑下部笔组含三条下降直笔，由斜向分支相连，上方中央还有短痕迹。",
    ),
    "obs-unk-000261": (
        "A short upper horizontal stroke leads into a descending central section "
        "and a compact lower block with a rightward curve.",
        "短上横笔向下连接中央部分和紧凑下部块状体，右侧带弯曲外伸。",
    ),
    "obs-unk-000262": (
        "The image repeats the angled upper section, several descending strokes, "
        "and rounded lower contour seen for obs-unk-000241; visual comparison only.",
        "图像与视觉对比的 obs-unk-000241 相似，均见倾斜上部、数条下降笔和弧形下部轮廓；不作身份确认。",
    ),
    "obs-unk-000263": (
        "The image repeats the short upper horizontal, descending central section, "
        "and compact lower block seen for obs-unk-000261; visual comparison only.",
        "图像与视觉对比的 obs-unk-000261 相似，均见短上横笔、中央下降部分和紧凑下部块状体；不作身份确认。",
    ),
    "obs-unk-000264": (
        "The image repeats the forked upper contour, narrow central stem, and "
        "short lower side branches seen for obs-unk-000221; visual comparison only.",
        "图像与视觉对比的 obs-unk-000221 相似，均见分叉上部、窄中央笔干和下方短侧分支；不作身份确认。",
    ),
    "obs-unk-000265": (
        "The image repeats the rectangular enclosure, broad upper bar, inner "
        "upright strokes, and lower crossbars seen for obs-unk-000245; visual "
        "comparison only.",
        "图像与视觉对比的 obs-unk-000245 相似，均见矩形围合、宽上横栏、内部直笔和下部横笔；不作身份确认。",
    ),
    "obs-unk-000266": (
        "The image repeats the compact pointed upper cluster, narrow central stem, "
        "and paired lower spreading strokes seen for obs-unk-000201; visual "
        "comparison only.",
        "图像与视觉对比的 obs-unk-000201 相似，均见紧凑尖状上部、窄中央笔干和向下分开的成对笔画；不作身份确认。",
    ),
    "obs-unk-000267": (
        "A tall outer rectangular form contains a forked upper mark and separated "
        "short interior strokes in its lower half.",
        "高直外围形体内有分叉上部痕迹，下半部含分离的短内部笔画。",
    ),
    "obs-unk-000268": (
        "The image repeats the paired forked branches, descending central stroke, "
        "and rounded lower contour seen for obs-unk-000247; visual comparison only.",
        "图像与视觉对比的 obs-unk-000247 相似，均见成对分叉侧支、中央下降笔和弧形下部轮廓；不作身份确认。",
    ),
    "obs-unk-000269": (
        "The image repeats the symmetrical stacked form, small upper triangle, "
        "central bar, and broad lower contour seen for obs-unk-000215; visual "
        "comparison only.",
        "图像与视觉对比的 obs-unk-000215 相似，均见对称叠置形体、小上三角、中部横栏和宽下部轮廓；不作身份确认。",
    ),
    "obs-unk-000270": (
        "A dense upper horizontal cluster descends into a central stem and a "
        "rounded rectangular lower block.",
        "密集上部横向笔组向下连接中央笔干和弧角矩形下部块状体。",
    ),
    "obs-unk-000271": (
        "The image repeats the narrow upright left stroke and denser curved right "
        "group seen for obs-unk-000249; visual comparison only.",
        "图像与视觉对比的 obs-unk-000249 相似，均见窄直立左笔和较密集弯曲右侧笔组；不作身份确认。",
    ),
    "obs-unk-000272": (
        "Two narrow side strokes frame a central upright and lower block; short "
        "branches project near the lower sides.",
        "两条窄侧笔夹住中央直笔和下部块状体，近下方两侧有短分支外伸。",
    ),
    "obs-unk-000273": (
        "A dense upper horizontal group extends toward a curved right side; a "
        "long lower stroke turns outward below.",
        "密集上部横向笔组向弯曲右侧延伸，下方有长笔向外转出。",
    ),
    "obs-unk-000274": (
        "Two tall side strokes flank a central crossing, with a compact cluster "
        "and short projections along the lower edge.",
        "两条高直侧笔夹住中央交叉，下缘有紧凑笔组和短外伸痕迹。",
    ),
    "obs-unk-000275": (
        "A compact upright form has a rounded left enclosure, a narrow central "
        "stem, and short right-side strokes.",
        "紧凑直立形体左侧有弧形围合，中部为窄笔干，右侧有短笔画。",
    ),
    "obs-unk-000276": (
        "The form has branched upper strokes, a narrow central stem, and stacked "
        "crossing marks along the lower portion.",
        "形体上部有分支笔画，中部为窄笔干，下部排列叠置交叉痕迹。",
    ),
    "obs-unk-000277": (
        "The image repeats the branched upper strokes, narrow stem, and stacked "
        "lower crossing marks seen for obs-unk-000276; visual comparison only.",
        "图像与视觉对比的 obs-unk-000276 相似，均见上部分支、窄笔干和下部叠置交叉痕迹；不作身份确认。",
    ),
    "obs-unk-000278": (
        "A pointed crown-like upper section sits above a rounded rectangular "
        "enclosure containing a small inner oval mark.",
        "尖冠状上部位于弧角矩形围合之上，围合内有小型椭圆痕迹。",
    ),
    "obs-unk-000279": (
        "Several broad angular projections radiate around a central crossing, "
        "with a short lower side extension.",
        "数个宽折角外伸部分围绕中央交叉分布，下方侧面有短外伸痕迹。",
    ),
    "obs-unk-000280": (
        "Four triangular or wedge-like projections meet around a central crossing "
        "to form a compact radial arrangement.",
        "四个三角或楔状外伸部分围绕中央交叉汇合，形成紧凑的放射状排列。",
    ),
    "obs-unk-000281": (
        "Three tall rounded uprights rise from a shared lower contour, with short "
        "crossing strokes near the upper ends.",
        "三条高直弧角笔画从共同下部轮廓升起，上端附近有短交叉笔画。",
    ),
    "obs-unk-000282": (
        "A pointed angular outer contour encloses crossing interior strokes and a "
        "small rounded mark toward the lower center.",
        "尖角外部轮廓内有交叉笔画，下部中央附近有小型弧形痕迹。",
    ),
    "obs-unk-000283": (
        "The image shows a narrow pointed upper contour, a long curved side "
        "stroke, and a short lower extension.",
        "图像呈窄尖上部轮廓、长弯曲侧笔和短下部外伸笔画。",
    ),
    "obs-unk-000284": (
        "Two broad roof-like angular strokes are stacked above a shorter lower "
        "stroke, with an open central gap.",
        "两条宽折角横笔上下叠置于较短下部笔画之上，中部留有开口空隙。",
    ),
    "obs-unk-000285": (
        "A small rounded mark sits above a broad lower bar and two short upright "
        "strokes; the form is compact and dark.",
        "小型弧形痕迹位于宽下横笔和两条短直笔之上，整体紧凑且较深。",
    ),
    "obs-unk-000286": (
        "Four detached rounded or diamond-like marks form a loose cluster around "
        "a smaller central mark.",
        "四个分离的弧形或菱形痕迹围绕较小中央痕迹形成疏松笔组。",
    ),
    "obs-unk-000287": (
        "A rounded outer enclosure contains a compact central crossing and a "
        "small lower mark, with short side projections.",
        "弧角外部围合内有紧凑中央交叉和小型下部痕迹，两侧有短外伸笔画。",
    ),
    "obs-unk-000288": (
        "The image has two stacked horizontal bars, a central enclosed mark, and "
        "a short detached stroke below.",
        "图像有两条叠置横栏、中央围合痕迹和下方短分离笔画。",
    ),
    "obs-unk-000289": (
        "A rounded rectangular outer contour encloses dense crossing strokes and "
        "a small lower projection.",
        "弧角矩形外轮廓内有密集交叉笔画，下部有小型外伸痕迹。",
    ),
    "obs-unk-000290": (
        "A tall rounded enclosure contains several crossing interior strokes and "
        "a narrow lower extension.",
        "高直弧角围合内有数条交叉内部笔画，并向下连接窄外伸部分。",
    ),
    "obs-unk-000291": (
        "Two long curved strokes meet near the upper center; short branches extend "
        "from a narrow lower stem.",
        "两条长弯曲笔画在上部中央附近相接，窄下部笔干有短分支外伸。",
    ),
    "obs-unk-000292": (
        "A compact angular central block has a tall left stroke, a short right "
        "projection, and a narrow lower extension.",
        "紧凑折角中央笔块带有高直左笔、短右侧外伸和窄下部延伸。",
    ),
    "obs-unk-000293": (
        "A small rounded upper mark sits on a long upright stroke above a broad "
        "zigzag lower contour.",
        "小型弧形上部痕迹位于长直笔之上，长直笔下方连接宽折线下部轮廓。",
    ),
    "obs-unk-000294": (
        "The form has a rounded upper mark, a descending central stroke, and a "
        "broad lower contour with a short side projection.",
        "形体有弧形上部痕迹、下降中央笔和宽下部轮廓，侧面带短外伸笔画。",
    ),
    "obs-unk-000295": (
        "A small capped upper mark sits over a narrow stem and a broad angular "
        "lower base.",
        "小型带帽上部痕迹位于窄笔干之上，下方连接宽折角底部。",
    ),
    "obs-unk-000296": (
        "A short upright stroke descends into a pointed lower enclosure, with a "
        "small horizontal mark near the upper junction.",
        "短直笔向下连接尖角下部围合，上部连接处附近有小横向痕迹。",
    ),
    "obs-unk-000297": (
        "A rounded rectangular upper enclosure contains a central vertical mark "
        "and continues into a long lower stem.",
        "弧角矩形上部围合内有中央直笔，并向下连接长笔干。",
    ),
    "obs-unk-000298": (
        "A rounded upper enclosure narrows into a pointed lower stem, with a "
        "small crossing mark inside the upper section.",
        "弧角上部围合向下收束为尖形笔干，上部内部有小交叉痕迹。",
    ),
    "obs-unk-000299": (
        "A rounded horizontal upper form sits above a narrow vertical stem and "
        "a short lower base.",
        "弧形横向上部形体位于窄直笔干之上，下方有短底部笔画。",
    ),
    "obs-unk-000300": (
        "Four short strokes cross around a central point, with rounded ends and "
        "a compact symmetrical arrangement.",
        "四条短笔围绕中央点交叉，端部较圆，整体呈紧凑近对称排列。",
    ),
    "obs-unk-000301": (
        "A tall rounded enclosure contains stacked horizontal strokes and a "
        "compact central mark, with a broad lower bar.",
        "高直弧角围合内有叠置横向笔画和紧凑中央痕迹，下部有宽横笔。",
    ),
    "obs-unk-000302": (
        "A rounded rectangular outer contour contains two horizontal interior "
        "marks and a compact lower enclosure.",
        "弧角矩形外轮廓内有两条横向内部笔画和紧凑下部围合。",
    ),
    "obs-unk-000303": (
        "A narrow upright contour contains a long diagonal interior stroke; two "
        "short strokes project from the lower right.",
        "窄直轮廓内有长斜向内部笔画，右下方有两条短外伸笔画。",
    ),
    "obs-unk-000304": (
        "A curved diagonal outer contour contains crossing interior strokes and a "
        "short upright projection on the right.",
        "弯曲斜向外轮廓内有交叉笔画，右侧有短直立外伸笔画。",
    ),
    "obs-unk-000305": (
        "A narrow upright body has paired slanting side strokes and a short lower "
        "extension; the image is visually similar to obs-unk-000311 only.",
        "窄直主体带有成对斜向侧笔和短下部延伸；仅记录其与 "
        "obs-unk-000311 的视觉相似，不作身份确认。",
    ),
    "obs-unk-000306": (
        "A compact angular enclosure has a crossing central cluster and a short "
        "projection toward the lower right.",
        "紧凑折角围合内有中央交叉笔组，右下方有短外伸笔画。",
    ),
    "obs-unk-000307": (
        "Two pointed or looped upper forms meet around a central crossing, with a "
        "tall narrow stroke on the right.",
        "两个尖角或环状上部形体围绕中央交叉相接，右侧有高直窄笔。",
    ),
    "obs-unk-000308": (
        "The image repeats the rounded upper mark, upright stroke, and zigzag "
        "lower contour seen for obs-unk-000293; visual comparison only.",
        "图像与 obs-unk-000293 均见弧形上部痕迹、直笔和折线下部轮廓；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000309": (
        "The image repeats the rounded upper mark, descending stroke, and broad "
        "lower contour seen for obs-unk-000294; visual comparison only.",
        "图像与 obs-unk-000294 均见弧形上部痕迹、下降笔和宽下部轮廓；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000310": (
        "The image repeats the capped upper mark, narrow stem, and broad angular "
        "base seen for obs-unk-000295; visual comparison only.",
        "图像与 obs-unk-000295 均见带帽上部痕迹、窄笔干和宽折角底部；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000311": (
        "The narrow upright body has paired slanting side strokes and a short "
        "lower extension; it is visually similar to obs-unk-000305 only.",
        "窄直主体带有成对斜向侧笔和短下部延伸；仅记录其与 "
        "obs-unk-000305 的视觉相似，不作身份确认。",
    ),
    "obs-unk-000312": (
        "Several stacked curved horizontal strokes occupy the center, with a "
        "short upper projection and a curved lower side stroke.",
        "数条叠置弧形横笔集中于中央，上部有短外伸笔，下部有弯曲侧笔。",
    ),
    "obs-unk-000313": (
        "A peaked outer contour encloses crossing interior strokes and a tall "
        "right-side extension.",
        "尖顶外轮廓内有交叉内部笔画，右侧有高直外伸笔。",
    ),
    "obs-unk-000314": (
        "A small curved upper mark connects to a descending diagonal stem and a "
        "compact angular lower cluster.",
        "小型弧形上部痕迹连接下降斜笔干和紧凑折角下部笔组。",
    ),
    "obs-unk-000315": (
        "The image repeats the curved upper mark, descending stem, and angular "
        "lower cluster seen for obs-unk-000314; visual comparison only.",
        "图像与 obs-unk-000314 均见弧形上部痕迹、下降笔干和折角下部笔组；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000316": (
        "A rounded upper form sits above a narrow vertical stem and a pointed "
        "lower enclosure with an interior crossing.",
        "弧形上部形体位于窄直笔干之上，下方连接带内部交叉的尖角围合。",
    ),
    "obs-unk-000317": (
        "Layered slanting strokes cluster around a narrow central stem, with a "
        "short pointed extension at the lower end.",
        "叠置斜向笔画围绕窄中央笔干分布，下端有短尖角外伸笔。",
    ),
    "obs-unk-000318": (
        "The image repeats the narrow upright contour, diagonal interior stroke, "
        "and lower-right projections seen for obs-unk-000303; comparison only.",
        "图像与 obs-unk-000303 均见窄直轮廓、斜向内部笔画和右下外伸；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000319": (
        "Stacked rounded or pointed forms sit above a compact lower cluster, with "
        "a detached diagonal stroke on the left.",
        "叠置弧形或尖角形体位于紧凑下部笔组之上，左侧有分离斜向笔。",
    ),
    "obs-unk-000320": (
        "A tall curved outer contour contains short interior horizontal and "
        "vertical strokes, with a long side extension.",
        "高直弯曲外轮廓内有短横向和直向内部笔画，侧面有长外伸笔。",
    ),
    "obs-unk-000321": (
        "A curved diagonal outer contour contains crossing interior strokes and a "
        "short upright projection on the right; visually similar to obs-unk-000304 "
        "only.",
        "弯曲斜向外轮廓内有交叉笔画，右侧有短直立外伸；仅记录其与 "
        "obs-unk-000304 的视觉相似，不作身份确认。",
    ),
    "obs-unk-000322": (
        "A rounded central enclosure has a diagonal left-side stroke, a short "
        "upper projection, and a narrow lower stem.",
        "弧角中央围合带有左侧斜笔、短上部外伸和窄下部笔干。",
    ),
    "obs-unk-000323": (
        "The image repeats the layered slanting strokes and narrow central stem "
        "seen for obs-unk-000317; visual comparison only.",
        "图像与 obs-unk-000317 均见叠置斜向笔画和窄中央笔干；仅作视觉 "
        "比较，不作身份确认。",
    ),
    "obs-unk-000324": (
        "A broad upper bar sits above a pointed lower enclosure, with short side "
        "projections and an open central area.",
        "宽上横笔位于尖角下部围合之上，两侧有短外伸，中部留有开口区域。",
    ),
    "obs-unk-000325": (
        "A rounded rectangular enclosure contains a central vertical stroke, a "
        "crossing middle mark, and a broad upper bar.",
        "弧角矩形围合内有中央直笔、中部交叉痕迹和宽上横笔。",
    ),
    "obs-unk-000326": (
        "The image repeats the rounded enclosure, central vertical stroke, and "
        "broad upper bar seen for obs-unk-000325; visual comparison only.",
        "图像与 obs-unk-000325 均见弧角围合、中央直笔和宽上横笔；仅作 "
        "视觉比较，不作身份确认。",
    ),
    "obs-unk-000327": (
        "Two small rounded or rectangular enclosures are crossed by a central "
        "diagonal stroke and a short lower extension.",
        "两个小型弧角或矩形围合被中央斜笔穿过，下方有短外伸笔画。",
    ),
    "obs-unk-000328": (
        "Several broad angular strokes stack above a compact group of short "
        "horizontal marks and a narrow lower stem.",
        "数条宽折角笔画叠置于短横笔紧凑笔组之上，下方连接窄笔干。",
    ),
    "obs-unk-000329": (
        "A small central crossing is surrounded by four rounded or looped "
        "projections, with a short upper-left extension.",
        "小型中央交叉周围有四个弧形或环状外伸，左上方有短外伸笔。",
    ),
    "obs-unk-000330": (
        "Two tall pointed outer strokes frame a central vertical group above a "
        "broad rounded lower base.",
        "两条高直尖角外笔夹住中央直向笔组，下方连接宽弧形底部。",
    ),
    "obs-unk-000331": (
        "The image repeats the stacked angular strokes, short horizontal marks, "
        "and narrow stem seen for obs-unk-000328; visual comparison only.",
        "图像与 obs-unk-000328 均见叠置折角笔、短横笔和窄笔干；仅作视觉 "
        "比较，不作身份确认。",
    ),
    "obs-unk-000332": (
        "The image repeats the paired pointed upper forms, central crossing, and "
        "right upright stroke seen for obs-unk-000307; visual comparison only.",
        "图像与 obs-unk-000307 均见成对尖角上部形体、中央交叉和右直笔；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000333": (
        "The image repeats the four rounded projections around a central crossing "
        "seen for obs-unk-000329; visual comparison only.",
        "图像与 obs-unk-000329 均见四个弧形外伸围绕中央交叉；仅作视觉 "
        "比较，不作身份确认。",
    ),
    "obs-unk-000334": (
        "Two narrow upright forms stand side by side, each with a small upper "
        "mark and several long lower strokes.",
        "两组窄直形体并列排列，各自带有小型上部痕迹和数条长下部笔画。",
    ),
    "obs-unk-000335": (
        "A rounded rectangular left block contains stacked horizontal marks and "
        "a central vertical stroke; a long side stroke extends rightward.",
        "左侧弧角矩形笔块内有叠置横笔和中央直笔，右侧有长笔外伸。",
    ),
    "obs-unk-000336": (
        "The image repeats the peaked outer contour, crossing interior strokes, "
        "and tall right extension seen for obs-unk-000313; visual comparison only.",
        "图像与 obs-unk-000313 均见尖顶外轮廓、交叉内部笔画和高直右伸；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000337": (
        "A tall arched outer contour contains a narrow central crossing and a "
        "pointed lower extension.",
        "高直拱形外轮廓内有窄中央交叉，下方连接尖角外伸笔。",
    ),
    "obs-unk-000338": (
        "A narrow pointed outer contour encloses a vertical chain of small marks "
        "and a short lower projection.",
        "窄尖外轮廓内有一列直向小型痕迹，下方有短外伸笔。",
    ),
    "obs-unk-000339": (
        "A small rounded upper enclosure sits above a broad lower body with "
        "several short side projections.",
        "小型弧角上部围合位于宽下部形体之上，两侧有数条短外伸笔。",
    ),
    "obs-unk-000340": (
        "The image repeats the rounded rectangular block, stacked marks, central "
        "vertical stroke, and right extension seen for obs-unk-000335; comparison "
        "only.",
        "图像与 obs-unk-000335 均见弧角矩形笔块、叠置痕迹、中央直笔和右伸；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000341": (
        "The image repeats stacked rounded or pointed forms above a compact lower "
        "cluster and a detached left diagonal stroke seen for obs-unk-000319; "
        "visual comparison only.",
        "图像与 obs-unk-000319 均见叠置弧形或尖角形体、紧凑下部笔组和左侧"
        "分离斜笔；仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000342": (
        "The image repeats the rounded rectangular block, stacked marks, central "
        "vertical stroke, and right extension seen for obs-unk-000335; comparison "
        "only.",
        "图像与 obs-unk-000335 均见弧角矩形笔块、叠置痕迹、中央直笔和右伸；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000343": (
        "A broad horizontal upper stroke sits above a compact lower group of "
        "rounded and angular marks.",
        "宽横上部笔画位于弧形和折角痕迹组成的紧凑下部笔组之上。",
    ),
    "obs-unk-000344": (
        "Several tall pointed strokes form a symmetrical upper cluster around a "
        "central vertical line and a narrow lower extension.",
        "数条高直尖角笔形成近对称上部笔组，围绕中央直线并连接窄下部延伸。",
    ),
    "obs-unk-000345": (
        "Stacked horizontal strokes cross a central upright, with short side "
        "projections and a compact lower bar.",
        "叠置横向笔画穿过中央直笔，两侧有短外伸，下方有紧凑横栏。",
    ),
    "obs-unk-000346": (
        "The image repeats the rounded rectangular block, stacked horizontal "
        "marks, central upright, and right extension seen for obs-unk-000335; "
        "comparison only.",
        "图像与 obs-unk-000335 均见弧角矩形笔块、叠置横笔、中央直笔和右伸；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000347": (
        "A small rounded upper mark sits above several short diagonal strokes and "
        "a long narrow right-side extension.",
        "小型弧形上部痕迹位于数条短斜笔之上，右侧有长窄外伸笔。",
    ),
    "obs-unk-000348": (
        "The image repeats the rounded upper mark, diagonal strokes, and right "
        "extension seen for obs-unk-000347; visual comparison only.",
        "图像与 obs-unk-000347 均见弧形上部痕迹、斜向笔画和右侧外伸；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000349": (
        "A broad angular upper stroke crosses a rounded lower cluster, with a "
        "short pointed projection toward the upper left.",
        "宽折角上部笔画穿过弧形下部笔组，左上方有短尖角外伸。",
    ),
    "obs-unk-000350": (
        "Layered angular strokes form a dense upper group above a pointed lower "
        "extension and a short side mark.",
        "叠置折角笔形成密集上部笔组，下方连接尖角延伸并带短侧痕迹。",
    ),
    "obs-unk-000351": (
        "A rounded central enclosure is framed by short side projections and a "
        "broad upper contour.",
        "弧角中央围合由短侧外伸和宽上部轮廓夹持。",
    ),
    "obs-unk-000352": (
        "A compact upper block with a central vertical mark sits above two long "
        "diagonal lower strokes.",
        "带中央直向痕迹的紧凑上部笔块位于两条长斜向下部笔之上。",
    ),
    "obs-unk-000353": (
        "Two small rounded side marks flank a central crossing and narrow lower "
        "stem; a separate long upright stroke stands at the right.",
        "两个小型弧形侧痕迹夹住中央交叉和窄下部笔干，右侧另有长直笔。",
    ),
    "obs-unk-000354": (
        "Two separated upright groups each contain a small upper block, crossing "
        "middle strokes, and a short lower extension.",
        "两组分离直立形体各自含小型上部笔块、中部交叉和短下部延伸。",
    ),
    "obs-unk-000355": (
        "The image repeats the paired rounded side marks, central crossing, and "
        "separate right upright seen for obs-unk-000353; comparison only.",
        "图像与 obs-unk-000353 均见成对弧形侧痕迹、中央交叉和分离右直笔；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000356": (
        "The image repeats the rounded central enclosure, short side projections, "
        "and broad upper contour seen for obs-unk-000351; comparison only.",
        "图像与 obs-unk-000351 均见弧角中央围合、短侧外伸和宽上部轮廓；"
        "仅作视觉比较，不作身份确认。",
    ),
    "obs-unk-000357": (
        "Two short upper side strokes flank a pointed lower enclosure containing "
        "a small interior crossing.",
        "两条短上部侧笔夹住尖角下部围合，围合内有小型交叉痕迹。",
    ),
    "obs-unk-000358": (
        "A curved outer contour encloses a compact radial lower cluster and a "
        "short upper crossing.",
        "弯曲外轮廓内有紧凑放射状下部笔组和短上部交叉。",
    ),
    "obs-unk-000359": (
        "The image repeats the curved contour and compact radial cluster seen for "
        "obs-unk-000358; visual comparison only.",
        "图像与 obs-unk-000358 均见弯曲轮廓和紧凑放射状笔组；仅作视觉比较，"
        "不作身份确认。",
    ),
    "obs-unk-000360": (
        "Several stacked horizontal strokes occupy the upper center, with long "
        "slanting side strokes extending below.",
        "数条叠置横笔集中于上部中央，下方有长斜向侧笔外伸。",
    ),
    "obs-unk-000361": (
        "Two compact angular or rounded clusters are stacked vertically, with a "
        "long narrow stroke extending along the right side.",
        "两个折角或弧形紧凑笔组上下叠置，右侧有长窄笔外伸。",
    ),
    "obs-unk-000362": (
        "A rounded central block has a broad horizontal top, a narrow lower stem, "
        "and a long right-side stroke.",
        "弧角中央笔块带宽上横笔、窄下部笔干和长右侧笔。",
    ),
    "obs-unk-000363": (
        "A dense zigzag central cluster is framed by curved side strokes and short "
        "upper projections.",
        "密集折线中央笔组由弯曲侧笔夹持，上方有短外伸笔。",
    ),
    "obs-unk-000364": (
        "Two stacked horizontal groups are crossed by narrow vertical strokes, "
        "with short side projections.",
        "两组叠置横向笔画被窄直笔穿过，两侧有短外伸笔。",
    ),
    "obs-unk-000365": (
        "Two compact rectangular groups are stacked, each containing a central "
        "crossing and short side marks.",
        "两个紧凑矩形笔组上下叠置，各自含中央交叉和短侧痕迹。",
    ),
    "obs-unk-000366": (
        "A rounded upper enclosure sits above several long diagonal lower strokes "
        "and a short right-side extension.",
        "弧角上部围合位于数条长斜向下部笔之上，右侧有短外伸。",
    ),
    "obs-unk-000367": (
        "The image repeats the rounded upper enclosure and long diagonal lower "
        "strokes seen for obs-unk-000366; visual comparison only.",
        "图像与 obs-unk-000366 均见弧角上部围合和长斜向下部笔；仅作视觉 "
        "比较，不作身份确认。",
    ),
    "obs-unk-000368": (
        "A dense rounded and angular cluster contains several crossing strokes and "
        "short outer projections.",
        "密集弧形和折角笔组内有数条交叉笔画及短外伸痕迹。",
    ),
    "obs-unk-000369": (
        "A tall branching right-side form stands beside a short detached left "
        "mark and a central crossing.",
        "高直分支右侧形体旁有短分离左侧痕迹和中央交叉。",
    ),
    "obs-unk-000370": (
        "A dense angular composite has a short upper projection, crossing middle "
        "strokes, and a curved lower edge.",
        "密集折角组合体带短上部外伸、中部交叉笔画和弯曲下缘。",
    ),
    "obs-unk-000371": (
        "A dense central crossing is framed by short pointed upper projections and "
        "long lower side strokes.",
        "密集中央交叉由短尖角上部外伸和长下部侧笔夹持。",
    ),
    "obs-unk-000372": (
        "A rounded rectangular lower enclosure has two pointed upper projections "
        "and a compact central mark.",
        "弧角矩形下部围合带有两个尖角上部外伸和紧凑中央痕迹。",
    ),
    "obs-unk-000373": (
        "A small pointed upper mark sits above a broad curved enclosure with a "
        "short lower projection.",
        "小型尖角上部痕迹位于宽弯曲围合之上，下方有短外伸笔。",
    ),
    "obs-unk-000374": (
        "Four broad strokes meet around a central crossing and continue into a "
        "pointed lower extension.",
        "四条宽笔围绕中央交叉汇合，并向下连接尖角外伸。",
    ),
    "obs-unk-000375": (
        "A narrow pointed enclosure contains a central vertical stroke and a "
        "short horizontal upper mark.",
        "窄尖围合内有中央直笔和短上部横向痕迹。",
    ),
    "obs-unk-000376": (
        "A short crossing form stands beside a tall narrow enclosure, with a "
        "small lower projection.",
        "短交叉形体旁有高直窄围合，下方带小型外伸笔。",
    ),
    "obs-unk-000377": (
        "A rounded upright enclosure with a descending stem stands beside a "
        "separate curved stroke on the right.",
        "弧角直立围合连接下降笔干，右侧另有分离弯曲笔。",
    ),
    "obs-unk-000378": (
        "A small rounded upper mark connects to a narrow stem and a broad zigzag "
        "lower contour.",
        "小型弧形上部痕迹连接窄笔干和宽折线下部轮廓。",
    ),
    "obs-unk-000379": (
        "A tall rounded rectangular enclosure contains dense crossing interior "
        "strokes and a narrow lower extension.",
        "高直弧角矩形围合内有密集交叉内部笔画和窄下部延伸。",
    ),
    "obs-unk-000380": (
        "A rounded horizontal enclosure contains a central crossing and a short "
        "lower stem, forming a compact near-symmetrical arrangement.",
        "弧形横向围合内有中央交叉和短下部笔干，形成紧凑近对称排列。",
    ),
    "obs-unk-000381": (
        "A square enclosure contains a small central rounded mark; a vertical "
        "stroke extends above and below the enclosure with a short upper bar.",
        "方形围合内有小型中央弧形痕迹，一条直笔上下延伸，"
        "上方另有短横笔。",
    ),
    "obs-unk-000382": (
        "An upper rectangular block sits above a long central stem and a "
        "crossing; the lower section forms a rounded loop with a narrow base.",
        "上部矩形笔块位于长中央笔干和交叉之上，"
        "下部形成弧形环状笔组，下方收小。",
    ),
    "obs-unk-000383": (
        "A tall curved right contour has forked upper projections, a central "
        "band, an enclosed lower opening, and a long leftward foot.",
        "高直弧形右侧轮廓带有分叉上部外伸、中央带状痕迹、"
        "下部围合空隙，并向左伸出长笔。",
    ),
    "obs-unk-000384": (
        "Two long slanting upper strokes converge above paired rounded lower "
        "loops, with a narrow central stem descending between them.",
        "两条长斜笔从上方收合，下方有成对弧形环状笔组，"
        "中间有窄中央笔干。",
    ),
    "obs-unk-000385": (
        "A diagonally oriented composite has a small rounded upper enclosure, "
        "crossing slanting strokes, and a pointed lower extension.",
        "整体呈斜向布局，上部有小型弧角围合，中部有交叉斜笔，"
        "下方连接尖角外伸。",
    ),
    "obs-unk-000386": (
        "A broad rounded enclosure on the left contains several interior "
        "divisions, while a separate curved upright form stands on the right.",
        "左侧宽幅弧形围合内含数个内部分割，右侧另有分离弯曲"
        "直立形体。",
    ),
    "obs-unk-000387": (
        "Two adjacent forms are visible: a curved segmented enclosure on the "
        "left and a narrow rectangular mark with a forked lower extension on "
        "the right.",
        "图像中可见两个相邻形体：左侧是弯曲分格围合，右侧是"
        "窄矩形痕迹并连接分叉形下伸。",
    ),
    "obs-unk-000388": (
        "A separated pair is visible: a narrow upright form with a long lower "
        "stroke on the left, and a pointed curved composite with internal "
        "openings on the right.",
        "图像由分离的左右两部分组成：左侧是窄直立形体和长下笔，"
        "右侧是尖头弯曲组合体并带内部空隙。",
    ),
    "obs-unk-000389": (
        "A small paired rounded mark stands on the left of a larger branching "
        "upright form with a central axis, side projections, and detached upper "
        "marks.",
        "左侧是小型成对弧形痕迹，右侧是较大的分支直立形体，"
        "其中有中央轴和侧外伸，上方附近另有分离痕迹。",
    ),
    "obs-unk-000390": (
        "A tall branching structure has a small rounded upper projection, "
        "layered curved side strokes, a central axis, and a tapered lower end.",
        "高直分支结构带有小型弧形上部外伸、叠置弯曲侧笔、"
        "中央笔轴和逐渐收窄的下端。",
    ),
    "obs-unk-000391": (
        "A tall rounded segmented form on the left has a long descending stem; "
        "a separate slender curved form stands on the right.",
        "左侧高直弧角分格形体向下延伸长笔干，右侧另有窄细"
        "弧形直立形体。",
    ),
    "obs-unk-000392": (
        "A tall branching structure has a rounded upper cap, layered curved side "
        "strokes, a central axis, and a tapered lower end; it is visually similar "
        "to obs-unk-000390 only.",
        "高直分支结构带有弧形上部、叠置弯曲侧笔、中央笔轴和"
        "逐渐收窄的下端；仅作与 obs-unk-000390 的视觉比较。",
    ),
    "obs-unk-000393": (
        "A broad upper U-shaped enclosure is crossed by a central axis; paired "
        "rounded side marks flank the middle and lower sections, with a long "
        "central stem below.",
        "宽大的 U 形向上围合被中央笔轴穿过，中、下部两侧均有"
        "成对弧形痕迹，下方连接长中央笔干。",
    ),
    "obs-unk-000394": (
        "A small rounded central cluster is crossed by a long diagonal stroke; "
        "several short detached slanting marks surround its upper area.",
        "小型弧形中央笔组被一条长斜笔穿过，上方附近分布数条"
        "短分离斜痕。",
    ),
    "obs-unk-000395": (
        "A narrow upright axis has a broad upper cross stroke and a rounded "
        "lower-left enclosure with an interior diagonal; a short upper-right "
        "projection is separate.",
        "窄直立主轴带宽横上笔，下左有带内部斜笔的弧形围合，"
        "上右侧另有短外伸笔。",
    ),
    "obs-unk-000396": (
        "Two neighboring forms are visible: a sparse branching upright mark on "
        "the left and a taller pointed enclosure on the right with a long curved "
        "lower stem.",
        "图像中可见两个相邻形体：左侧是稀疏分枝直立标记，右侧"
        "是更高的尖部围合形体，下方连接长弧形笔干。",
    ),
    "obs-unk-000397": (
        "A dense irregular vertical block stands on the left; a small rounded "
        "upper mark with a descending stem occupies the center, and a separate "
        "curved upright stroke stands on the right.",
        "左侧是密集不规则竖向笔块，中部有小型弧形上部痕迹和"
        "向下延伸笔干，右侧另有分离弧形直笔。",
    ),
    "obs-unk-000398": (
        "A compact upper double-bar enclosure is crossed by a central vertical "
        "stroke; two divergent lower strokes extend beneath it.",
        "紧凑上部双横围合被直立中央笔穿过，下方连接两条向外"
        "分开的笔画。",
    ),
    "obs-unk-000399": (
        "A broad upper cross stroke sits above a lower-left rounded enclosure with "
        "an interior diagonal and a pointed lower extension; the arrangement is "
        "visually similar to obs-unk-000395 only.",
        "宽横上部笔置于左下弧形围合之上，围合内有斜笔并向下"
        "连接尖角外伸；仅作与 obs-unk-000395 的视觉比较。",
    ),
    "obs-unk-000400": (
        "A sparse branching upright mark stands beside a taller pointed enclosure "
        "with a long curved lower stem; it is visually similar to obs-unk-000396 "
        "only.",
        "稀疏分枝直立标记位于较高尖头围合形体旁，后者下方连接"
        "长弧形笔干；仅作与 obs-unk-000396 的视觉比较，不作身份确认。",
    ),
    "obs-unk-000401": (
        "A narrow upright mark has a forked upper stroke beside a dense right "
        "cluster, with a pointed lower extension and several interior strokes.",
        "窄直立痕迹上部有分叉笔画，右侧邻接密集笔组；下方有尖角外伸，"
        "内部可见数条笔画。",
    ),
    "obs-unk-000402": (
        "A compact upper crossing sits above a central descending stroke; the "
        "lower portion forms a rounded loop with a short rightward extension.",
        "紧凑上部交叉笔组下接中央下行笔画；下部形成弧形环状笔组，"
        "并向右有短外伸。",
    ),
    "obs-unk-000403": (
        "A small rounded upper cluster is attached to a tall curved central "
        "stroke, with short right-side projections and a longer lower curve.",
        "小型弧形上部笔组连接高直弯曲中央笔画，右侧有短外伸，"
        "下方接较长弧形笔。",
    ),
    "obs-unk-000404": (
        "The image shows a narrow forked upright form beside a dense right "
        "cluster and a pointed lower extension; it is visually similar to "
        "obs-unk-000401 only.",
        "图像显示窄直立分叉形体与右侧密集笔组相邻，并有尖角下伸；"
        "仅作与 obs-unk-000401 的视觉比较。",
    ),
    "obs-unk-000405": (
        "Two tall curved strokes rise around a rounded lower enclosure; the "
        "enclosure contains small interior marks and remains visually separate "
        "from the outer strokes.",
        "两条高直弯曲笔画围绕下部弧形围合上行；围合内有小型痕迹，"
        "与外侧笔画的连接关系仍只作视觉记录。",
    ),
    "obs-unk-000406": (
        "A tall narrow form has crossing strokes near the upper middle and an "
        "open rounded lower contour with a diagonal interior stroke.",
        "高直窄形体中上部有交叉笔画，下部为开放弧形轮廓，"
        "内部可见斜向笔画。",
    ),
    "obs-unk-000407": (
        "A broad pointed contour slopes downward and contains several interior "
        "partitions, including a small enclosed opening near the lower left.",
        "宽幅尖部轮廓向下倾斜，内部有数处分格，左下附近可见"
        "小型围合空隙。",
    ),
    "obs-unk-000408": (
        "A small rounded cap sits above a slender descending stem; a broad low "
        "base extends horizontally with a pointed projection on the right.",
        "小型弧形上部位于窄长下行笔干之上；下部有宽横基部，"
        "右侧带尖角外伸。",
    ),
    "obs-unk-000409": (
        "A short upper cross stroke sits over a descending central stem; two "
        "rounded lower lobes join a long horizontal base.",
        "短横上部笔位于中央下行笔干之上；下部有两个弧形侧部，"
        "并连接长横基部。",
    ),
    "obs-unk-000410": (
        "A rectangular upper frame with internal divisions sits above a central "
        "stem and a broad rounded lower enclosure with a pointed right edge.",
        "带内部分格的矩形上框位于中央笔干之上；下部为宽弧形围合，"
        "右缘有尖角外伸。",
    ),
    "obs-unk-000411": (
        "A short upper stem leads into paired curved side contours and a rounded "
        "lower enclosure, with a small point at the bottom.",
        "短上部笔干向下连接成对弧形侧轮廓和下部弧形围合，"
        "最下端带小型尖角。",
    ),
    "obs-unk-000412": (
        "A rounded upper loop with an interior diagonal sits above a broad lower "
        "block; short side strokes project from the lower horizontal bar.",
        "弧形上部环状笔组内有斜笔，下方连接宽幅笔块；"
        "下部横笔两侧有短外伸。",
    ),
    "obs-unk-000413": (
        "A compact rectangular frame contains four visible interior openings; "
        "two long lower strokes descend and spread apart beneath it.",
        "紧凑矩形框内可见四处内部空隙；下方有两条长笔向下并"
        "向两侧分开。",
    ),
    "obs-unk-000414": (
        "A rounded cap sits above a slender descending stem and a broad low base "
        "with a pointed right projection; it is visually similar to obs-unk-000408 "
        "only.",
        "弧形上部位于窄长下行笔干之上，下部有宽横基部和右侧尖角外伸；"
        "仅作与 obs-unk-000408 的视觉比较。",
    ),
    "obs-unk-000415": (
        "A short upper cross stroke sits above a descending stem and two rounded "
        "lower lobes joined to a long base; it is visually similar to "
        "obs-unk-000409 only.",
        "短横上部笔位于下行笔干之上，下部有两个弧形侧部并连接长基部；"
        "仅作与 obs-unk-000409 的视觉比较。",
    ),
    "obs-unk-000416": (
        "A detached dark triangular mark is above a broad lower curved enclosure "
        "crossed by horizontal strokes and a diagonal interior line.",
        "分离的深色三角痕迹位于下部宽弧形围合之上；围合内有横向笔画，"
        "并可见一条内部斜笔。",
    ),
    "obs-unk-000417": (
        "A three-lobed upper cluster sits above a rounded enclosure containing a "
        "small central rectangular opening.",
        "三瓣状上部笔组位于弧形围合之上，围合内部有小型中央矩形空隙。",
    ),
    "obs-unk-000418": (
        "A tall oval enclosure contains two narrow interior vertical strokes; a "
        "rounded lower loop or base is attached below it.",
        "高直椭圆围合内有两条窄长内部竖笔；下方连接弧形环状笔组或基部。",
    ),
    "obs-unk-000419": (
        "A broad upper bar contains two rounded divisions above a short central "
        "stem and a small lower rounded rectangular enclosure.",
        "宽幅上横笔内有两处分格，下方连接短中央笔干和小型下部弧角矩形围合。",
    ),
    "obs-unk-000420": (
        "A pointed triangular upper contour sits above a narrow stem and an open "
        "rounded lower form with a short rightward stroke.",
        "尖角三角上部轮廓位于窄长笔干之上；下部为开放弧形形体，"
        "右侧带短向外笔画。",
    ),
    "obs-unk-000421": (
        "Two small rounded rectangular marks sit above a broad pointed contour "
        "with two long descending legs and a central opening.",
        "两个小型弧角矩形痕迹位于宽幅尖角轮廓之上；下部有两条长下行笔，"
        "中间保留空隙。",
    ),
    "obs-unk-000422": (
        "A pointed forked upright form with a long stem stands beside a separate "
        "narrow angular form with a short upper projection.",
        "尖角分叉直立形体连接长笔干，旁边另有窄长折角形体，"
        "上部带短外伸。",
    ),
    "obs-unk-000423": (
        "A broad rounded upper enclosure contains a central crossing and a lower "
        "tapered stem; two small detached marks sit to the left.",
        "宽幅弧形上部围合内有中央交叉，下方接收窄下行笔干；"
        "左侧有两个小型分离痕迹。",
    ),
    "obs-unk-000424": (
        "A broad rounded upper enclosure contains a central crossing and a lower "
        "tapered stem; it is visually similar to obs-unk-000423 only.",
        "宽幅弧形上部围合内有中央交叉，下方接收窄下行笔干；"
        "仅作与 obs-unk-000423 的视觉比较。",
    ),
    "obs-unk-000425": (
        "A rectangular enclosure contains crossing interior strokes, including a "
        "small rounded upper mark and a curved diagonal lower stroke.",
        "矩形围合内有交叉内部笔画，其中包括小型弧形上部痕迹和"
        "弯曲斜向下部笔画。",
    ),
    "obs-unk-000426": (
        "A dense central upright cluster has several short side projections and "
        "a longer curved stroke descending on the right.",
        "密集中央直立笔组带有数个短侧向外伸，右侧连接较长弯曲下行笔。",
    ),
    "obs-unk-000427": (
        "Crossing diagonal strokes form a tall narrow structure with a small "
        "central rounded opening and a pointed lower end.",
        "交叉斜向笔画构成高直窄形体，中部有小型弧形空隙，"
        "下端收成尖角。",
    ),
    "obs-unk-000428": (
        "A forked upper cluster sits above a broad open lower contour with a "
        "small rounded point at the bottom.",
        "分叉上部笔组位于宽幅开放下部轮廓之上，最下端有小型弧形尖点。",
    ),
    "obs-unk-000429": (
        "A sparse upright arrangement has a curved left axis, crossing middle "
        "strokes, and a separate narrow right upright with a rounded top.",
        "稀疏直立排列有弯曲左侧轴线、中部交叉笔画，右侧另有"
        "窄直立形体并带弧形上端。",
    ),
    "obs-unk-000430": (
        "A compact diagonal composite has a small rounded upper mark, a central "
        "slanting stroke, and a pointed lower fork.",
        "紧凑斜向组合体带有小型弧形上部痕迹、中央斜笔和尖角下部叉形。",
    ),
    "obs-unk-000431": (
        "Three tall descending strokes or branches stand together, with crossing "
        "marks through the central area and uneven lower ends.",
        "三个高直下行笔或分枝并列，中部有交叉痕迹，下端长短不一。",
    ),
    "obs-unk-000432": (
        "A small upper rectangular frame sits above crossing diagonal strokes and "
        "a rounded lower loop.",
        "小型上部矩形框位于交叉斜向笔画之上，下方连接弧形环状笔组。",
    ),
    "obs-unk-000433": (
        "A dense star-like cluster on the left stands beside a separate slender "
        "curved descending form on the right.",
        "左侧是密集星状笔组，右侧另有窄长弯曲下行形体。",
    ),
    "obs-unk-000434": (
        "A forked upper cluster sits above a broad open lower contour with a "
        "small rounded point; it is visually similar to obs-unk-000428 only.",
        "分叉上部笔组位于宽幅开放下部轮廓之上，最下端有小型弧形尖点；"
        "仅作与 obs-unk-000428 的视觉比较。",
    ),
    "obs-unk-000435": (
        "A compact four-lobed crossing cluster stands beside a separate narrow "
        "right upright with a short upper diagonal mark.",
        "紧凑四瓣交叉笔组旁边有分离的窄直立右侧形体，"
        "上部带短斜向痕迹。",
    ),
    "obs-unk-000436": (
        "A broad upper crossing has branching side strokes; the lower area "
        "contains a small curved enclosure and a short pointed projection.",
        "宽幅上部交叉笔组带分枝侧笔；下部有小型弧形围合和"
        "短尖角外伸。",
    ),
    "obs-unk-000437": (
        "A pointed upper enclosure sits above a broad rounded lower basin with "
        "several short descending strokes.",
        "尖角上部围合位于宽幅弧形下部笔组之上，下部有数条短下行笔。",
    ),
    "obs-unk-000438": (
        "A broad upper horizontal stroke crosses a narrow central stem; the lower "
        "section forms an angular left contour with a short right projection.",
        "宽幅上横笔穿过窄中央笔干；下部形成折角左侧轮廓，"
        "右侧带短外伸。",
    ),
    "obs-unk-000439": (
        "A short upright stem sits above a small rectangular block and a lower "
        "zigzag contour with several pointed projections.",
        "短直立笔干位于小型矩形笔块之上；下部为带数个尖角外伸的"
        "折线轮廓。",
    ),
    "obs-unk-000440": (
        "A short upright stem sits above a small rectangular block and a broad "
        "lower zigzag contour; it is visually similar to obs-unk-000439 only.",
        "短直立笔干位于小型矩形笔块之上，下部为宽幅折线轮廓；"
        "仅作与 obs-unk-000439 的视觉比较。",
    ),
    "obs-unk-000441": (
        "A dense central crossing is flanked by curved side strokes, with a long "
        "descending curve extending below the cluster.",
        "密集中央交叉笔组两侧有弧形笔画，笔组下方接长弧形下行笔。",
    ),
    "obs-unk-000442": (
        "A short upper stem leads into two long curved descending strokes; a "
        "separate narrow upright form stands on the right.",
        "短上部笔干向下连接两条长弧形笔；右侧另有窄直立形体。",
    ),
    "obs-unk-000443": (
        "A tall curved left contour surrounds a nested central cluster with a "
        "pointed upper cap and a rounded lower opening.",
        "高直弧形左侧轮廓围绕中央嵌套笔组，上端有尖角，下部有弧形空隙。",
    ),
    "obs-unk-000444": (
        "A cross-like upper cluster sits above two rounded horizontal enclosures "
        "and a broad curved lower base.",
        "交叉状上部笔组位于两个弧形横向围合之上，下方连接宽幅弧形基部。",
    ),
    "obs-unk-000445": (
        "A stacked rectangular form with an upper triangular opening stands beside "
        "a taller jagged curved stroke on the right.",
        "带上部三角空隙的叠置矩形形体旁边有更高的右侧折曲笔画。",
    ),
    "obs-unk-000446": (
        "Two neighboring forms are visible: a sparse curved upright with detached "
        "small marks on the left, and a denser branching form on the right.",
        "图像中有两个相邻形体：左侧为稀疏弧形直立笔并带分离小痕迹，"
        "右侧为较密集的分支形体。",
    ),
    "obs-unk-000447": (
        "A broad forked upper contour spans two long descending legs and leaves a "
        "central open space between them.",
        "宽幅分叉上部轮廓向下形成两条长笔，二者之间保留中央空隙。",
    ),
    "obs-unk-000448": (
        "A small upper oval sits above crossing strokes and a lower branching "
        "cluster with short horizontal side projections.",
        "小型上部椭圆痕迹位于交叉笔画之上，下方有分支笔组并带短横侧伸。",
    ),
    "obs-unk-000449": (
        "A broad curved upper contour rises to a hook on the right; lower "
        "horizontal strokes and a descending right mark form the base.",
        "宽幅弧形上部轮廓向右上形成钩状外伸；下部横笔与右侧下行痕迹"
        "共同形成基部。",
    ),
    "obs-unk-000450": (
        "A stacked rectangular lower block has a small upper triangular opening and "
        "a tall curved contour along the right side.",
        "叠置矩形下部笔块上方有小型三角空隙，右侧沿有高直弧形轮廓。",
    ),
    "obs-unk-000451": (
        "A broad upper horizontal enclosure has small upper projections; below it "
        "are paired rounded marks and a central descending stroke.",
        "宽幅上部横向围合带有小型上伸；下方有成对弧形痕迹和中央下行笔。",
    ),
    "obs-unk-000452": (
        "A sparse tall branching form has several forked upper strokes, a short "
        "angled lower foot, and a long curved right extension.",
        "稀疏高直分支形体上部有数处分叉笔，下部有短斜向足部，"
        "右侧连接长弧形外伸。",
    ),
    "obs-unk-000453": (
        "A stacked rectangular form with an upper triangular opening stands beside "
        "a tall curved right contour; it is visually similar to obs-unk-000450 "
        "only.",
        "带上部三角空隙的叠置矩形形体旁有高直右侧弧形轮廓；"
        "仅作与 obs-unk-000450 的视觉比较。",
    ),
    "obs-unk-000454": (
        "A diagonal composite has a small upper diamond-like enclosure and lower "
        "angular strokes extending toward the left.",
        "斜向组合体上部有小型菱角状围合，下部有折角笔画向左外伸。",
    ),
    "obs-unk-000455": (
        "A dense curved branching form on the left stands beside a separate group "
        "of small marks and short horizontal strokes on the right.",
        "左侧为密集弧形分支形体，右侧另有一组小型痕迹和短横笔。",
    ),
    "obs-unk-000456": (
        "A rounded lower enclosure contains two small interior rounded marks; "
        "curved upper strokes and a detached round mark sit above and to the right.",
        "弧形下部围合内有两个小型弧形痕迹；上方弯曲笔画和右侧分离圆痕"
        "共同构成外部笔组。",
    ),
    "obs-unk-000457": (
        "A tall left stem forks at the top and is crossed by a long rightward "
        "diagonal, with a small lower curved opening.",
        "高直左侧笔干上端分叉，并被长斜笔向右穿过；下部有小型弧形空隙。",
    ),
    "obs-unk-000458": (
        "A compact curved form has a broad lower hook, a tall slanting right "
        "stroke, and a small interior upper mark.",
        "紧凑弧形形体带宽幅下部钩状笔、右侧高直斜笔和小型内部上部痕迹。",
    ),
    "obs-unk-000459": (
        "A rectangular U-shaped frame has two descending side strokes and a small "
        "pointed upper projection at the center.",
        "矩形 U 形框有两条下行侧笔，中央上部带小型尖角外伸。",
    ),
    "obs-unk-000460": (
        "A central upright stem is crossed by two upper diagonals and divides into "
        "two long diverging lower strokes.",
        "中央直立笔干被两条上部斜笔交叉，并在下方分成两条长外张笔。",
    ),
    "obs-unk-000461": (
        "Two neighboring narrow rectangular forms each have a short upper cap, "
        "interior vertical strokes, and a pointed lower extension.",
        "两个相邻窄矩形形体各有短上部笔帽、内部竖笔和尖角下伸。",
    ),
    "obs-unk-000462": (
        "Two adjacent forms are visible: the left has a rounded top and split "
        "lower legs, while the right is a compact framed mark with a small upper "
        "projection.",
        "图像中有两个相邻形体：左侧顶部弧形、下部笔画分开，右侧为紧凑围框痕迹，"
        "上部带小型外伸。",
    ),
    "obs-unk-000463": (
        "A rounded central enclosure has several forked upper projections and two "
        "diagonal lower strokes extending outward.",
        "弧形中央围合带有数个分叉上伸，下方有两条斜笔向外延伸。",
    ),
    "obs-unk-000464": (
        "A tall branching form has two curved outer legs and a narrower central "
        "stroke descending between them.",
        "高直分支形体有两条弧形外侧笔，中间夹一条较窄下行笔。",
    ),
    "obs-unk-000465": (
        "A dense upper crossing cluster sits above a rounded rectangular lower "
        "enclosure with a short central extension.",
        "密集上部交叉笔组位于弧角矩形下部围合之上，围合下方有短中央外伸。",
    ),
    "obs-unk-000466": (
        "Two tall upper strokes frame a small central rounded opening; several "
        "short pointed strokes project from the lower cluster.",
        "两条高直上部笔围住小型中央弧形空隙，下部笔组有数条短尖角外伸。",
    ),
    "obs-unk-000467": (
        "Several dense wavy vertical strokes form a narrow cluster with a small "
        "central loop and a slanting side projection.",
        "数条密集弯曲竖笔形成窄长笔组，中部有小型环状笔，侧面有斜向外伸。",
    ),
    "obs-unk-000468": (
        "A thick left upright is crossed by a central horizontal stroke; a small "
        "upper diamond-like mark and short lower projections stand to the right.",
        "粗重左侧直笔被中央横笔穿过；右侧有小型菱角状上部痕迹和短下伸。",
    ),
    "obs-unk-000469": (
        "A broad two-legged curved form stands beside a separate narrow right mark "
        "with a small rounded lower end.",
        "宽幅双足弧形形体旁边有分离的窄长右侧痕迹，末端带小型弧形笔。",
    ),
    "obs-unk-000470": (
        "A rounded rectangular upper frame contains a central loop; several "
        "pointed lower strokes descend beneath it.",
        "弧角矩形上框内有中央环状笔组，下方有数条尖角下行笔。",
    ),
    "obs-unk-000471": (
        "A small curved central cluster is surrounded by several detached short "
        "diagonal marks; the image limits resolution of individual breaks.",
        "小型弧形中央笔组周围有数个分离短斜痕；图像分辨率限制了"
        "单条笔画断续的判断。",
    ),
    "obs-unk-000472": (
        "A tall central stem has a small rounded upper enclosure, curved side "
        "strokes, and a pointed lower extension.",
        "高直中央笔干上部有小型弧形围合，两侧有弯曲笔画，下方有尖角外伸。",
    ),
    "obs-unk-000473": (
        "A tall central stem has a small rounded upper enclosure, curved side "
        "strokes, and a pointed lower extension; it is visually similar to "
        "obs-unk-000472 only.",
        "高直中央笔干上部有小型弧形围合，两侧有弯曲笔画，下方有尖角外伸；"
        "仅作与 obs-unk-000472 的视觉比较。",
    ),
    "obs-unk-000474": (
        "A tall central stem has a small rounded upper enclosure, curved side "
        "strokes, and a pointed lower extension; it is visually similar to "
        "obs-unk-000472 and obs-unk-000473 only.",
        "高直中央笔干上部有小型弧形围合，两侧有弯曲笔画，下方有尖角外伸；"
        "仅作与 obs-unk-000472、obs-unk-000473 的视觉比较。",
    ),
    "obs-unk-000475": (
        "A sparse rectangular frame has a curved left side and a long angled "
        "stroke descending from the right.",
        "稀疏矩形框左侧为弧形笔，右侧有长斜笔向下延伸。",
    ),
    "obs-unk-000476": (
        "A rounded left mark connects to a curved right stem ending below a small "
        "detached upper block.",
        "左侧弧形痕迹连接右侧弯曲笔干，笔干上方有分离的小型笔块。",
    ),
    "obs-unk-000477": (
        "A compact upper rectangular cluster sits above a central stem that splits "
        "into two long lower strokes.",
        "紧凑上部矩形笔组位于中央笔干之上，中央笔干下方分成两条长笔。",
    ),
    "obs-unk-000478": (
        "A diagonal composite has stacked diamond-like upper enclosures and lower "
        "angular strokes extending toward the left.",
        "斜向组合体上部有叠置菱角状围合，下部折角笔画向左外伸。",
    ),
    "obs-unk-000479": (
        "A broad pointed upper enclosure contains several descending interior "
        "strokes that end at different heights.",
        "宽幅尖角上部围合内有数条下行内部笔画，末端高度不一。",
    ),
    "obs-unk-000480": (
        "A rounded left mark connects to a curved right stem ending below a small "
        "detached upper block; it is visually similar to obs-unk-000476 only.",
        "左侧弧形痕迹连接右侧弯曲笔干，笔干上方有分离的小型笔块；"
        "仅作与 obs-unk-000476 的视觉比较。",
    ),
    "obs-unk-000481": (
        "A tall upper enclosure contains a small rounded central mark and side "
        "curves; three short descending strokes project below it.",
        "高直上部围合内有小型中央弧形痕迹和侧弧笔，下方有三条短下伸。",
    ),
    "obs-unk-000482": (
        "A broad upper horizontal stroke crosses a central stem; a small detached "
        "mark sits left of it and a rounded lower loop extends beneath.",
        "宽幅上横笔穿过中央笔干；左侧有小型分离痕迹，下方连接弧形环状笔组。",
    ),
    "obs-unk-000483": (
        "A broad rounded enclosure contains repeated narrow interior loops and "
        "short lower extensions.",
        "宽幅弧形围合内有重复的窄长内部环状笔组，并有短下部外伸。",
    ),
    "obs-unk-000484": (
        "A broad rounded enclosure contains repeated narrow interior loops and "
        "short lower extensions; it is visually similar to obs-unk-000483 only.",
        "宽幅弧形围合内有重复的窄长内部环状笔组，并有短下部外伸；"
        "仅作与 obs-unk-000483 的视觉比较。",
    ),
    "obs-unk-000485": (
        "A compact cross-like arrangement has a long upper horizontal stroke, a "
        "central vertical, and short lateral lower projections.",
        "紧凑交叉排列有长上横笔、中央竖笔和短侧向下部外伸。",
    ),
    "obs-unk-000486": (
        "A tall narrow framed form has a pointed upper contour, an interior cross "
        "stroke, and two lower legs; a separate curved stroke stands on the right.",
        "高直窄围框形体上部尖角，中部有交叉笔，下方分成两条笔；"
        "右侧另有弧形直笔。",
    ),
    "obs-unk-000487": (
        "A dense left cluster contains a small rounded center; a separate narrow "
        "crossing upright form stands on the right.",
        "左侧密集笔组内有小型弧形中央痕迹，右侧另有窄长交叉直立形体。",
    ),
    "obs-unk-000488": (
        "A broad upper horizontal stroke crosses a central descending form; lower "
        "curved strokes create a small enclosed loop.",
        "宽幅上横笔穿过中央下行形体；下部弧笔形成小型围合环状笔组。",
    ),
    "obs-unk-000489": (
        "A tall central upright has short side branches; a curved lower branch "
        "extends left and a small detached mark sits to the right.",
        "高直中央笔带短侧分支；下方有弧形左伸，右侧有小型分离痕迹。",
    ),
    "obs-unk-000490": (
        "A double-lobed upper bar sits above several descending strokes; a separate "
        "rounded triangular mark stands on the right.",
        "双瓣状上横笔位于数条下行笔之上；右侧另有弧角三角痕迹。",
    ),
    "obs-unk-000491": (
        "A forked upper contour crosses a horizontal stroke; a long central stem "
        "descends with a shorter side stroke on the left.",
        "分叉上部轮廓穿过横笔；长中央笔干向下延伸，左侧有较短侧笔。",
    ),
    "obs-unk-000492": (
        "A branching form has a small upper oval, curved side projections, and a "
        "pointed lower contour ending above a short horizontal bar.",
        "分支形体上部有小型椭圆，两侧有弧形外伸；下部为尖角轮廓，"
        "末端上方另有短横笔。",
    ),
    "obs-unk-000493": (
        "A compact upper rectangular frame sits above a central stem that divides "
        "into two lower diverging strokes.",
        "紧凑上部矩形框位于中央笔干之上，中央笔干下方分成两条外张笔。",
    ),
    "obs-unk-000494": (
        "A large open curved enclosure surrounds a central crossing stroke and a "
        "short lower branching mark.",
        "大型开放弧形围合包住中央交叉笔和短下部分支痕迹。",
    ),
    "obs-unk-000495": (
        "Two separated forms are visible: a sparse branching left cluster with "
        "detached small marks and a taller looped upright on the right.",
        "图像中有两个分离形体：左侧为稀疏分支笔组并带小型分离痕迹，"
        "右侧为更高的环状直立形体。",
    ),
    "obs-unk-000496": (
        "A small upper oval sits above a broad horizontal bar and a descending "
        "central stroke; a short curved projection extends on the lower right.",
        "小型上部椭圆位于宽横笔之上，并连接中央下行笔；下右有短弧形外伸。",
    ),
    "obs-unk-000497": (
        "A dense diagonal composite has a small lower enclosure and many short "
        "strokes projecting around its upper and right edges.",
        "密集斜向组合体下部有小型围合，周围上缘和右缘有多条短外伸笔。",
    ),
    "obs-unk-000498": (
        "Two tall side strokes frame a small upper rectangular block and a central "
        "pointed lower enclosure.",
        "两条高直侧笔围住小型上部矩形笔块和中央尖角下部围合。",
    ),
    "obs-unk-000499": (
        "Two separated compact forms are visible: a small upright rectangular mark "
        "on the left and a lower rounded rectangular form with an upper cross stroke "
        "on the right.",
        "图像中有两个分离的紧凑形体：左侧为小型直立矩形痕迹，右侧为"
        "带上部横笔的下部弧角矩形形体。",
    ),
    "obs-unk-000500": (
        "A rounded central enclosure has forked upper projections and two diagonal "
        "lower strokes; it is visually similar to obs-unk-000463 only.",
        "弧形中央围合带分叉上伸和两条斜向下伸；仅作与 obs-unk-000463 的视觉比较。",
    ),
    "obs-unk-000501": (
        "A rounded central enclosure has forked upper projections and a compact "
        "lower rectangular base; it is visually similar to obs-unk-000500 only.",
        "弧形中央围合带分叉上伸和紧凑下部矩形基部；仅作与 obs-unk-000500 的视觉比较。",
    ),
    "obs-unk-000502": (
        "A broad horizontal central stroke has short upper side marks and a lower "
        "pointed enclosure with a small interior opening.",
        "宽幅中央横笔带短上部侧痕，下方有尖角围合并含小型内部空隙。",
    ),
    "obs-unk-000503": (
        "Two tall side strokes frame a small upper rectangular block and a central "
        "pointed lower enclosure.",
        "两条高直侧笔围住小型上部矩形笔块和中央尖角下部围合；"
        "仅作与 obs-unk-000498 的视觉比较。",
    ),
    "obs-unk-000504": (
        "A diagonal left enclosure contains a rounded central mark; separate curved "
        "and forked strokes stand to the right.",
        "斜向左侧围合内有中央弧形痕迹；右侧另有弯曲和分叉笔画。",
    ),
    "obs-unk-000505": (
        "Two small upper rectangular marks sit above a central crossing and a dense "
        "lower branching cluster.",
        "两个小型上部矩形痕迹位于中央交叉和密集下部分支笔组之上。",
    ),
    "obs-unk-000506": (
        "A rounded central enclosure is flanked by branching side strokes and a "
        "narrow wavy form on the right; short lower points project below.",
        "弧形中央围合两侧有分支笔，右侧另有窄长弯曲形体；下方有短尖角外伸。",
    ),
    "obs-unk-000507": (
        "A rectangular frame contains several horizontal interior strokes and has "
        "short projections above and below; two vertical side marks flank it.",
        "矩形框内有数条横向内部笔，两侧由竖笔夹持，上下有短外伸。",
    ),
    "obs-unk-000508": (
        "Two separated forms are visible: a small branching cluster on the left and "
        "a taller looped upright on the right.",
        "图像中有两个分离形体：左侧为小型分支笔组，右侧为更高的环状直立形体。",
    ),
    "obs-unk-000509": (
        "A dense diagonal left cluster stands beside a narrow right upright with "
        "several short branching projections.",
        "密集斜向左侧笔组旁有窄直立右侧形体，并带数个短分支外伸。",
    ),
    "obs-unk-000510": (
        "A narrow forked upright form stands beside a dense right cluster and a "
        "pointed lower extension; it is visually similar to obs-unk-000401 only.",
        "窄直立分叉形体旁有密集右侧笔组和尖角下伸；仅作与 obs-unk-000401 的视觉比较。",
    ),
    "obs-unk-000511": (
        "A central rounded mark is crossed by a left curved stroke and right side "
        "projections; a small rectangular base sits below.",
        "中央弧形痕迹被左侧弯曲笔穿过，右侧有外伸，下方有小型矩形基部。",
    ),
    "obs-unk-000512": (
        "A rounded central enclosure is crossed by a long horizontal stroke with "
        "short side projections; a stem and small lower block extend below.",
        "弧形中央围合被长横笔穿过并带短侧伸；下方接笔干和小型下部笔块。",
    ),
    "obs-unk-000513": (
        "Only a very small U-shaped mark is visible in the low-resolution image; "
        "individual stroke details require a higher-resolution source check.",
        "低分辨率图像中仅清楚可见极小 U 形痕迹；单条笔画细节需用更高分辨率来源复核。",
    ),
    "obs-unk-000514": (
        "Two separated compact rectangular forms are visible, each with a short "
        "upright or horizontal projection.",
        "图像中有两个分离的紧凑矩形形体，各自带短直立或横向外伸。",
    ),
    "obs-unk-000515": (
        "A dense diagonal left cluster stands beside a narrow right upright with "
        "several short branching projections; it is visually similar to "
        "obs-unk-000509 only.",
        "密集斜向左侧笔组旁有窄直立右侧形体并带短分支外伸；"
        "仅作与 obs-unk-000509 的视觉比较。",
    ),
    "obs-unk-000516": (
        "A rectangular frame contains several horizontal interior strokes and has "
        "short projections above and below; it is visually similar to obs-unk-000507 "
        "only.",
        "矩形框内有数条横向内部笔，上下有短外伸；仅作与 obs-unk-000507 的视觉比较。",
    ),
    "obs-unk-000517": (
        "A central rounded mark is crossed by a left curved stroke and right side "
        "projections; a small rectangular base sits below; it is visually similar "
        "to obs-unk-000511 only.",
        "中央弧形痕迹被左侧弯曲笔穿过，右侧有外伸，下方有小型矩形基部；"
        "仅作与 obs-unk-000511 的视觉比较。",
    ),
    "obs-unk-000518": (
        "Two separated rectangular forms have narrow central stems and short upper "
        "or lower projections.",
        "两个分离的矩形形体各有窄中央笔干和短上部或下部外伸。",
    ),
    "obs-unk-000519": (
        "A dense upright branching cluster has a small horizontal left projection "
        "and several curved strokes descending on the right.",
        "密集直立分支笔组带小型左横向外伸，右侧有数条弯曲下行笔。",
    ),
    "obs-unk-000520": (
        "A dense diagonal composite has crossing central strokes, a pointed lower "
        "contour, and short side projections.",
        "密集斜向组合体有中央交叉笔、尖角下部轮廓和短侧向外伸。",
    ),
    "obs-unk-000521": ("A compact central cluster has a rounded upper mark, side strokes, and a small rectangular lower base.", "紧凑中央笔组带弧形上部痕迹、侧笔和小型矩形下部基座。"),
    "obs-unk-000522": ("Two separated rectangular forms have narrow stems and short side projections.", "两个分离矩形形体各有窄笔干和短侧向外伸。"),
    "obs-unk-000523": ("A dense upright branching cluster has a small left horizontal mark and several right-side strokes.", "密集直立分支笔组带小型左横痕，右侧有数条笔画。"),
    "obs-unk-000524": ("A dense diagonal composite has crossing strokes and pointed side and lower extensions.", "密集斜向组合体有交叉笔画及尖角侧部、下部外伸。"),
    "obs-unk-000525": ("A rounded central cluster has side curves and a compact rectangular lower base; it is visually similar to obs-unk-000521 only.", "弧形中央笔组带侧弧笔和紧凑矩形下部基座；仅作与 obs-unk-000521 的视觉比较。"),
    "obs-unk-000526": ("A tall narrow form has a crossing middle and a rounded lower opening.", "高直窄形体中部有交叉，下部有弧形空隙。"),
    "obs-unk-000527": ("A small upper rectangular frame sits above a curved lower loop and short side strokes.", "小型上部矩形框位于弧形下部环状笔组之上，并带短侧笔。"),
    "obs-unk-000528": ("A compact diagonal form has a small upper projection, crossing middle, and pointed lower end.", "紧凑斜向形体带小型上伸、中央交叉和尖角下端。"),
    "obs-unk-000529": ("A rounded upper cap sits above a narrow stem with several short lower projections.", "弧形上部笔帽位于窄笔干之上，下方有数个短外伸。"),
    "obs-unk-000530": ("A small rounded upper mark sits above a crossed narrow stem and a short lower stroke.", "小型弧形上部痕迹位于交叉窄笔干之上，下方有短笔。"),
    "obs-unk-000531": ("A tall rounded segmented form has a long descending central stem.", "高直弧形分格形体带长中央下行笔干。"),
    "obs-unk-000532": ("A rounded upper loop sits above a broad lower block with side projections.", "弧形上部环状笔组位于宽幅下部笔块之上，并带侧向外伸。"),
    "obs-unk-000533": ("A compact rounded central form has a horizontal crossing and a pointed lower stem.", "紧凑弧形中央形体有横向交叉和尖角下行笔干。"),
    "obs-unk-000534": ("A narrow rectangular frame has a curved left stroke and a short lower extension.", "窄矩形框带弧形左笔和短下部外伸。"),
    "obs-unk-000535": ("A broad rounded lower enclosure has a serrated upper edge with several pointed projections.", "宽幅弧形下部围合上缘呈连续尖角外伸。"),
    "obs-unk-000536": ("A detached dark upper mark sits above a broad lower curved enclosure crossed by horizontal strokes.", "分离深色上部痕迹位于宽幅弧形下部围合之上，围合内有横笔。"),
    "obs-unk-000537": ("A pointed upper mark sits above a small rectangular lower block and a short central stem.", "尖角上部痕迹位于小型矩形下部笔块之上，并连接短中央笔干。"),
    "obs-unk-000538": ("A dense diagonal form has a pointed upper projection and a compact lower crossing.", "密集斜向形体带尖角上伸和紧凑下部交叉。"),
    "obs-unk-000539": ("A dense diagonal form has a broad left block and several pointed right projections.", "密集斜向形体左侧宽厚，右侧有数个尖角外伸。"),
    "obs-unk-000540": ("A rounded enclosure has a segmented left interior and a pointed right projection.", "弧形围合内左侧有分格，右侧带尖角外伸。"),
    "obs-unk-000541": (
        "Two small enclosed marks sit above an open angular lower frame with two descending side strokes.",
        "两个小型围合痕迹位于开放的下部折角框架之上，框架两侧有下行笔。",
    ),
    "obs-unk-000542": (
        "A tall central stem has a pointed upper wedge, two detached side marks, and a U-shaped lower base.",
        "高直中央笔干带尖角上部，两侧有分离小痕迹，下部为 U 形基座。",
    ),
    "obs-unk-000543": (
        "The compact form repeats a tall central stem, pointed upper wedge, detached side marks, and U-shaped base.",
        "紧凑形体重复高直中央笔干、尖角上部、两侧分离痕迹和 U 形基座。",
    ),
    "obs-unk-000544": (
        "A broad conical cap sits above two horizontal bands, a narrow stem, and forked lower strokes.",
        "宽幅锥形上部位于两道横向带痕、窄笔干和分叉下部笔画之上。",
    ),
    "obs-unk-000545": (
        "A tall arch-like outer contour encloses a rectangular grid of horizontal and vertical strokes.",
        "高直拱形外轮廓围合横、竖笔画组成的矩形格状内部。",
    ),
    "obs-unk-000546": (
        "A tall arch-like contour encloses a smaller rounded rectangular cluster with several crossing strokes.",
        "高直拱形轮廓围合较小的弧边矩形笔组，内部有数条交叉笔。",
    ),
    "obs-unk-000547": (
        "A small pointed cap and horizontal bar sit above a rectangular enclosure containing crossing strokes.",
        "小型尖角上部和横向笔位于矩形围合之上，围合内有交叉笔画。",
    ),
    "obs-unk-000548": (
        "A small rounded upper mark sits on a narrow stem above a broad shallow enclosure with side projections.",
        "小型弧形上部痕迹位于窄笔干之上，下方是带侧向外伸的宽浅围合。",
    ),
    "obs-unk-000549": (
        "A crossed upper cluster sits left of a rectangular lower block with an interior horizontal line and two stems.",
        "交叉上部笔组位于矩形下部笔块左侧，笔块内有横线并向下伸出两笔。",
    ),
    "obs-unk-000550": (
        "A diagonal composite has a rounded upper loop, a crossing middle, and a pointed lower triangular end.",
        "斜向组合体带弧形上部环、中央交叉和尖角三角形下端。",
    ),
    "obs-unk-000551": (
        "A dense upright cluster has a long descending left stroke, compact central marks, and rounded right strokes.",
        "密集直立笔组带长下行左笔，中央笔画紧凑，右侧有弧形笔。",
    ),
    "obs-unk-000552": (
        "The form repeats a small rounded upper mark, narrow stem, and broad shallow lower enclosure with projections.",
        "该形体重复小型弧形上部痕迹、窄笔干和带外伸的宽浅下部围合。",
    ),
    "obs-unk-000553": (
        "A dense composite has a dark upper cap, a central horizontal crossing, and a large curved right descent.",
        "密集组合体带深色上部笔帽、中央横向交叉和宽大的右侧弧形下行笔。",
    ),
    "obs-unk-000554": (
        "An arched outer contour encloses a central curved stroke and small detached rectangular side marks.",
        "拱形外轮廓围合中央弧形笔，左右有小型分离矩形痕迹。",
    ),
    "obs-unk-000555": (
        "The arched enclosure and central curved stroke resemble obs-unk-000554, with no identity claim made.",
        "拱形围合和中央弧形笔与 obs-unk-000554 视觉相近；不作身份判断。",
    ),
    "obs-unk-000556": (
        "A pointed arch-like enclosure has an open triangular interior and a long curved stroke on the right.",
        "尖角拱形围合内有开放三角形笔组，右侧带长弧形笔。",
    ),
    "obs-unk-000557": (
        "A compact crossed cluster has a rounded upper loop, a horizontal bar, and diverging lower strokes.",
        "紧凑交叉笔组带弧形上部环、横向笔和向两侧分开的下部笔。",
    ),
    "obs-unk-000558": (
        "A narrow framed block on the left is paired with two tall pointed strokes on the right.",
        "左侧为窄框状笔块，右侧并列两条高直尖角笔。",
    ),
    "obs-unk-000559": (
        "A long horizontal top stroke with short ends sits above a rounded pointed lower enclosure.",
        "长横上笔两端有短下伸，位于弧形尖底下部围合之上。",
    ),
    "obs-unk-000560": (
        "A tall rectangular lower enclosure has an interior horizontal division and a long left side stroke.",
        "高直矩形下部围合内有横向分隔，左侧带长竖向笔。",
    ),
    "obs-unk-000561": (
        "A rounded upper loop and two diagonal side strokes sit above a broad curved lower enclosure.",
        "弧形上部环和两条斜向侧笔位于宽幅弧形下部围合之上。",
    ),
    "obs-unk-000562": (
        "A dense connected form combines a left rectangular frame, central crossings, a rounded right cluster, and a long descending stroke.",
        "密集相连形体组合左侧矩形框、中央交叉、右侧弧形笔组和长下行笔。",
    ),
    "obs-unk-000563": (
        "A long curved left stroke stands beside a gridded upper block and a branching lower cluster.",
        "长弧形左笔旁有格状上部笔块和分支状下部笔组。",
    ),
    "obs-unk-000564": (
        "Two long curved left strokes flank a dense gridded right cluster with short detached side marks.",
        "两条长弧形左笔围绕右侧密集格状笔组，旁有短分离痕迹。",
    ),
    "obs-unk-000565": (
        "A rounded upper loop flows into a broad curved lower contour with three pointed lower projections.",
        "弧形上部环连接宽幅弧形下部轮廓，下缘有三个尖角外伸。",
    ),
    "obs-unk-000566": (
        "A compact crossed cluster has a rounded upper loop, a horizontal crossing, and diverging lower strokes.",
        "紧凑交叉笔组带弧形上部环、横向交叉和分开的下部笔。",
    ),
    "obs-unk-000567": (
        "A tall diagonal cluster contains a chain of small enclosed crossings and long outer strokes.",
        "高直斜向笔组内有连续小型围合交叉，外侧带长笔。",
    ),
    "obs-unk-000568": (
        "A rectangular gridded block with forked upper strokes has a long central descent and curved side strokes.",
        "矩形格状笔块上方有分叉笔，下方有长中央下行笔和弧形侧笔。",
    ),
    "obs-unk-000569": (
        "A dense angular cluster has pointed upper strokes, a central crossing, and rounded lower openings.",
        "密集折角笔组带尖角上部笔、中央交叉和弧形下部空隙。",
    ),
    "obs-unk-000570": (
        "A gridded central block has forked upper strokes, a long lower stem, and two curved side marks.",
        "格状中央笔块带分叉上部笔、长下行笔干和两侧弧形痕迹。",
    ),
    "obs-unk-000571": (
        "A tall diagonal chain of enclosed crossings ends in long strokes spreading at the lower sides.",
        "高直斜向连续围合交叉下端向两侧伸出长笔。",
    ),
    "obs-unk-000572": (
        "A broad left framed wedge is joined to a dense right cluster with branching strokes.",
        "宽幅左侧框状折角笔块连接右侧密集笔组，右侧有分支笔。",
    ),
    "obs-unk-000573": (
        "A dense diagonal form has pointed left strokes, a narrow central descent, and rounded right marks.",
        "密集斜向形体带尖角左笔、窄中央下行笔和弧形右侧痕迹。",
    ),
    "obs-unk-000574": (
        "Several tall diagonal strokes surround a rounded central opening and a compact lower cluster.",
        "数条高直斜向笔围绕弧形中央空隙，下部有紧凑笔组。",
    ),
    "obs-unk-000575": (
        "A small gridded upper block sits above a narrow central stem ending in two pointed lower loops.",
        "小型格状上部笔块位于窄中央笔干之上，笔干末端有两个尖角下部环。",
    ),
    "obs-unk-000576": (
        "A crossed central cluster has a rounded upper loop, a horizontal bar, and two long lower strokes.",
        "交叉中央笔组带弧形上部环、横向笔和两条长下部笔。",
    ),
    "obs-unk-000577": (
        "A compact symmetric cluster has a central rounded opening and multiple short lateral and lower strokes.",
        "紧凑近对称笔组有中央弧形空隙，并带多条短侧笔和下部笔。",
    ),
    "obs-unk-000578": (
        "A vertical oval grid on the left is paired with branching right strokes and a long slanting descent.",
        "左侧竖向椭圆格状笔组连接右侧分支笔和长斜向下行笔。",
    ),
    "obs-unk-000579": (
        "A smaller oval grid on the left is paired with branching right strokes and a long curved descent.",
        "较小椭圆格状笔组位于左侧，右侧有分支笔和长弧形下行笔。",
    ),
    "obs-unk-000580": (
        "An elongated pointed upper enclosure sits above a lower row of three rounded marks and side strokes.",
        "细长尖角上部围合位于下部三个弧形痕迹和侧笔之上。",
    ),
    "obs-unk-000581": (
        "A gridded central block is flanked by long curved strokes, lower pointed marks, and two detached side forms.",
        "格状中央笔块两侧有长弧形笔，下部有尖角痕迹，旁有两个分离形体。",
    ),
    "obs-unk-000582": (
        "A branching central form has an elongated upper loop, short side loops, and a triangular lower frame.",
        "分支状中央形体带细长上部环、短侧环和三角形下部框架。",
    ),
    "obs-unk-000583": (
        "A rounded gridded upper block sits above a large central oval and two angled lower side blocks.",
        "弧形格状上部笔块位于大型中央椭圆和两个斜向下部侧块之上。",
    ),
    "obs-unk-000584": (
        "A tall crossed cluster has an upper pointed loop, short left projections, and a long curved right stroke.",
        "高直交叉笔组带尖角上部环、短左侧外伸和长弧形右笔。",
    ),
    "obs-unk-000585": (
        "A dense triangular cluster has gridded central strokes, long curved sides, and two pointed lower marks.",
        "密集三角形笔组有中央格状笔、长弧形侧笔和两个尖角下部痕迹。",
    ),
    "obs-unk-000586": (
        "A small branching cluster on the left is paired with a tall oval gridded loop and a long lower descent.",
        "左侧小型分支笔组连接高直椭圆格状环和长下行笔。",
    ),
    "obs-unk-000587": (
        "A dense diagonal composite has a rounded upper loop, a central crossing, and curved lower side strokes.",
        "密集斜向组合体带弧形上部环、中央交叉和弧形下部侧笔。",
    ),
    "obs-unk-000588": (
        "A small upper cap sits over a rectangular banded block, with a detached rounded mark below.",
        "小型上部笔帽位于带横带的矩形笔块之上，下方有分离弧形痕迹。",
    ),
    "obs-unk-000589": (
        "A dense diagonal chain has a rounded upper loop and several curved strokes descending on both sides.",
        "密集斜向连续笔组带弧形上部环，两侧有数条弧形下行笔。",
    ),
    "obs-unk-000590": (
        "Two separated gridded blocks are linked by long vertical and curved strokes with short top bars.",
        "两个分离格状笔块由长竖向和弧形笔连接，上部各有短横笔。",
    ),
    "obs-unk-000591": (
        "A rounded gridded upper cap sits above two large angular lower branches and a central descent.",
        "弧形格状上部笔帽位于两个大型折角下部分支和中央下行笔之上。",
    ),
    "obs-unk-000592": (
        "A dense diagonal cluster has branching left strokes, a tall right block, and a long lower descent.",
        "密集斜向笔组带分支左笔、高直右侧笔块和长下行笔。",
    ),
    "obs-unk-000593": (
        "Four angular lobes meet at a central crossing, with short interior strokes in each lobe.",
        "四个折角笔瓣在中央交叉汇合，每个笔瓣内有短笔。",
    ),
    "obs-unk-000594": (
        "A compact angular cluster has a pointed upper stroke and broad lower left and right projections.",
        "紧凑折角笔组带尖角上笔，下部向左右宽幅外伸。",
    ),
    "obs-unk-000595": (
        "A small rounded upper mark and left horizontal stroke sit above a narrow rectangular enclosure.",
        "小型弧形上部痕迹和左横笔位于窄矩形围合之上。",
    ),
    "obs-unk-000596": (
        "A dense diagonal chain contains two elongated rounded openings and a narrow central crossing.",
        "密集斜向连续笔组内有两个细长弧形空隙和窄中央交叉。",
    ),
    "obs-unk-000597": (
        "A compact near-symmetric form has two rounded upper projections, a central enclosure, and lower side strokes.",
        "紧凑近对称形体带两个弧形上伸、中央围合和下部侧笔。",
    ),
    "obs-unk-000598": (
        "A gridded central enclosure has two rounded upper projections and two diverging lower legs; it resembles obs-unk-000597 visually only.",
        "格状中央围合带两个弧形上伸和两条分开的下部笔；仅作与 obs-unk-000597 的视觉比较。",
    ),
    "obs-unk-000599": (
        "A bow-like symmetric form has two upper hooks, a central crossing, and curved lower side strokes.",
        "近对称弓形笔组带两个上部钩状笔、中央交叉和弧形下部侧笔。",
    ),
    "obs-unk-000600": (
        "A tall rectangular arch has an interior horizontal division and two long descending side strokes.",
        "高直矩形拱形围合内有横向分隔，两侧有长下行笔。",
    ),
    "obs-unk-000601": (
        "A rounded upper enclosure with a pointed interior sits above a shallow lower curve and a long right descent.",
        "弧形上部围合内有尖角笔，位于浅弧形下部笔和长右侧下行笔之上。",
    ),
    "obs-unk-000602": (
        "Two zigzag upper rows sit above a central stem with three horizontal bars and a short lower base.",
        "两排折线状上部笔位于中央笔干之上，笔干带三道横笔和短下部基座。",
    ),
    "obs-unk-000603": (
        "A pointed upper frame with crossing interior strokes sits above a lower angular enclosure and central stem.",
        "带交叉内部笔画的尖角上部框架位于折角下部围合和中央笔干之上。",
    ),
    "obs-unk-000604": (
        "A tall central form is enclosed by curved side strokes, with a pointed upper mark and triangular lower base.",
        "高直中央形体由弧形侧笔围合，上部有尖角痕迹，下部有三角形基座。",
    ),
    "obs-unk-000605": (
        "A rectangular upper band contains repeated pointed strokes above a curved lower enclosure and horizontal base.",
        "矩形上部横带内有重复尖角笔，下方连接弧形围合和横向基座。",
    ),
    "obs-unk-000606": (
        "A tall triangular left frame is paired with a branching right cluster and a small upper cap.",
        "高直三角形左框连接分支状右侧笔组，上方带小型笔帽。",
    ),
    "obs-unk-000607": (
        "Two separate arch-like frames are stacked vertically, each with a short interior diagonal stroke.",
        "两个分离拱形框上下排列，每个框内都有短斜向笔。",
    ),
    "obs-unk-000608": (
        "A small rectangular frame on the left is paired with a dense branching diagonal cluster on the right.",
        "左侧小型矩形框连接右侧密集分支斜向笔组。",
    ),
    "obs-unk-000609": (
        "A small rounded mark and long central descent stand beside a broad rounded enclosure with an inner block.",
        "小型弧形痕迹和长中央下行笔旁有宽幅弧形围合，围合内有笔块。",
    ),
    "obs-unk-000610": (
        "A small rounded left mark and wavy descent stand beside a tall pointed enclosure on a short base.",
        "小型弧形左侧痕迹和波状下行笔旁有高直尖角围合及短基座。",
    ),
    "obs-unk-000611": (
        "A long curved left stroke stands beside a narrow upper frame and a broad rounded lower enclosure.",
        "长弧形左笔旁有窄上部框架和宽幅弧形下部围合。",
    ),
    "obs-unk-000612": (
        "A broad left wedge with horizontal divisions is paired with a dense curved branching cluster on the right.",
        "带横向分隔的宽幅左侧折角笔块连接右侧密集弧形分支笔组。",
    ),
    "obs-unk-000613": (
        "A small wavy rounded cluster on the left is paired with a tall pointed right panel containing interior marks.",
        "左侧小型波状弧形笔组连接高直尖角右侧笔板，笔板内有内部痕迹。",
    ),
    "obs-unk-000614": (
        "Two rounded separated lobes sit beside a tall rectangular panel with several horizontal interior bands.",
        "两个分离弧形笔瓣位于高直矩形笔板旁，笔板内有数道横带。",
    ),
    "obs-unk-000615": (
        "A broad curved upper stroke arches over a pointed central form ending in two long lower strokes.",
        "宽幅弧形上笔覆盖尖角中央形体，中央形体下端伸出两条长笔。",
    ),
    "obs-unk-000616": (
        "A tall arch-like frame encloses a central horizontal and vertical cluster with short outer side strokes.",
        "高直拱形框围合中央横竖笔组，外侧带短侧笔。",
    ),
    "obs-unk-000617": (
        "A rounded left cluster with an interior loop is paired with a tall pointed right panel.",
        "带内部环的弧形左侧笔组连接高直尖角右侧笔板。",
    ),
    "obs-unk-000618": (
        "Detached short upper strokes sit above a small rounded central cluster and curved lower descents.",
        "分离短上部笔位于小型弧形中央笔组和弧形下行笔之上。",
    ),
    "obs-unk-000619": (
        "Detached curved upper marks surround a compact central cluster with long horizontal side strokes.",
        "分离弧形上部痕迹围绕紧凑中央笔组，中央两侧有长横笔。",
    ),
    "obs-unk-000620": (
        "A curved outer enclosure surrounds a central rectangular and curved cluster with long descending sides.",
        "弧形外部围合包住中央矩形和弧形笔组，两侧有长下行笔。",
    ),
    "obs-unk-000621": (
        "Two detached curved marks sit above a compact branching cluster with a long right descent.",
        "两个分离弧形痕迹位于紧凑分支笔组之上，右侧有长下行笔。",
    ),
    "obs-unk-000622": (
        "Two detached upper marks sit above a broad horizontal stroke, a central oval, and a curved lower descent.",
        "两个分离上部痕迹位于宽横笔、中央椭圆和弧形下行笔之上。",
    ),
    "obs-unk-000623": (
        "Two detached dark marks sit above a dense crossed lower cluster with a long left diagonal stroke.",
        "两个分离深色痕迹位于密集交叉下部笔组之上，左侧有长斜笔。",
    ),
    "obs-unk-000624": (
        "Two long outer strokes frame a central rounded cluster with a pointed upper mark and lower projections.",
        "两条长外侧笔围合中央弧形笔组，上部有尖角痕迹，下部有外伸。",
    ),
    "obs-unk-000625": (
        "A dense angular central cluster has several detached short side marks and a long lower stroke.",
        "密集折角中央笔组带数个分离短侧痕迹和长下部笔。",
    ),
    "obs-unk-000626": (
        "A tall triangular upper frame sits above a rounded enclosure with pointed interior strokes and detached sides.",
        "高直三角形上部框架位于弧形围合之上，围合内有尖角笔，侧有分离痕迹。",
    ),
    "obs-unk-000627": (
        "Four triangular lobes meet around a central crossing to form a compact four-sided cluster.",
        "四个三角形笔瓣围绕中央交叉汇合，形成紧凑四向笔组。",
    ),
    "obs-unk-000628": (
        "A small pointed cap and horizontal bar sit above a rectangular enclosure containing crossing strokes.",
        "小型尖角笔帽和横笔位于矩形围合之上，围合内有交叉笔。",
    ),
    "obs-unk-000629": (
        "A crossed upper cluster sits above horizontal bands and two long descending side strokes.",
        "交叉上部笔组位于横向带痕之上，两侧有长下行笔。",
    ),
    "obs-unk-000630": (
        "A small upper cap and branching mark sit above a rectangular banded block with a short lower base.",
        "小型上部笔帽和分支痕迹位于带横带矩形笔块之上，下方有短基座。",
    ),
    "obs-unk-000631": (
        "An hourglass-like upper crossing sits above a broad rounded lower block with two long descending strokes.",
        "沙漏状上部交叉位于宽幅弧形下部笔块之上，下方伸出两条长笔。",
    ),
    "obs-unk-000632": (
        "A dense upper cap joins stacked left side loops and a broad curved stroke descending on the right.",
        "密集上部笔帽连接左侧叠置弧形环，右侧有宽幅弧形下行笔。",
    ),
    "obs-unk-000633": (
        "A dense rounded cluster on the left is paired with a tall right panel containing horizontal bands.",
        "左侧密集弧形笔组连接高直右侧笔板，笔板内有横向带痕。",
    ),
    "obs-unk-000634": (
        "A narrow wavy central cluster is paired with a pointed right panel and short side strokes.",
        "窄幅波状中央笔组连接尖角右侧笔板，并带短侧笔。",
    ),
    "obs-unk-000635": (
        "A small wavy left cluster stands beside a tall pointed right stroke with a narrow interior opening.",
        "小型波状左侧笔组旁有高直尖角右笔，右笔内有窄空隙。",
    ),
    "obs-unk-000636": (
        "A tall rectangular panel has two interior sections and long curved strokes descending on both sides.",
        "高直矩形笔板内分为两段，两侧有长弧形下行笔。",
    ),
    "obs-unk-000637": (
        "A small gridded block on the left is paired with a dense branching diagonal cluster and long descent.",
        "左侧小型格状笔块连接密集分支斜向笔组和长下行笔。",
    ),
    "obs-unk-000638": (
        "A broad rounded enclosure contains central horizontal and vertical strokes with branching right projections.",
        "宽幅弧形围合内有中央横竖笔，右侧带分支外伸。",
    ),
    "obs-unk-000639": (
        "A pointed upper arch encloses a central rounded mark above a dense lower branching cluster.",
        "尖角上部拱形围合中央弧形痕迹，下方连接密集分支笔组。",
    ),
    "obs-unk-000640": (
        "A tall open angular enclosure on the left is separated from a rounded horizontal-banded cluster on the right.",
        "左侧高直开放折角围合与右侧弧形横带笔组分离。",
    ),

}

MATERIAL_VISUAL_OBSERVATIONS.update(
    {
        "obs-unk-000641": (
            "A curved upper stroke descends into a narrow central stem, with detached short marks on the left and crossed lower projections.",
            "上部弧形笔画向下连接窄中轴；左侧有分离短痕，底部有交叉外伸。",
        ),
        "obs-unk-000642": (
            "A compact lower triangular enclosure contains two horizontal bars, with detached marks above and a separate curved descent on the right.",
            "紧凑下部三角围合内有两道横痕；上方有分离痕迹，右侧另有弧形下行笔画。",
        ),
        "obs-unk-000643": (
            "Two rectangular side panels with horizontal interior bars flank a central crossing and upright strokes.",
            "两侧矩形笔组各有横向内痕，中部可见交叉和竖向笔画。",
        ),
        "obs-unk-000644": (
            "A detached short vertical mark stands left of a tall composite with a pointed upper crossing and a long curved lower descent.",
            "高窄笔组左侧有分离短竖痕；上部有尖角交叉，底部有长弧形下行。",
        ),
        "obs-unk-000645": (
            "A broad rounded enclosure has two short upper prongs, two inner horizontal bars, and a lower stem splitting into two feet.",
            "宽弧形围合上方有两处短竖出头，内部有两道横痕，底部中轴分成两处外伸。",
        ),
        "obs-unk-000646": (
            "Stacked crossing and rounded marks form a narrow center above a broad lower oval with a short base.",
            "交叉和弧形痕迹叠置形成窄中部，下方接宽圆形笔组和短底座。",
        ),
        "obs-unk-000647": (
            "A separated long curved stroke stands beside a compact looped cluster, with a small detached diagonal mark below.",
            "分离的长弧形笔画位于紧凑环状笔组一侧，下方另有小型分离斜痕。",
        ),
        "obs-unk-000648": (
            "A left rectangular loop and a taller right panel are linked by a central diagonal stroke and a long lower descent.",
            "左侧矩形环状笔组与右侧高直笔板由中部斜笔连接，底部有长下行笔画。",
        ),
        "obs-unk-000649": (
            "Two rounded diamond-like loops are stacked around a central stem, with a detached curved stroke at the left.",
            "两个带圆弧的棱形环圈围绕中轴叠置，左侧有分离弧形笔画。",
        ),
        "obs-unk-000650": (
            "A tall left stroke with a short branch stands beside a rounded right enclosure containing a horizontal bar and upright stroke.",
            "左侧高直笔画带短分支，右侧弧形围合内可见横痕和竖向笔画。",
        ),
        "obs-unk-000651": (
            "A dense crossed upper cluster is paired with a detached vertical mark and an open lower loop with two rounded projections.",
            "上部密集交叉笔组旁有分离竖痕，下部为开放回环并有两处圆形外伸。",
        ),
        "obs-unk-000652": (
            "A wavy left stem with small loops stands beside a tall angular right enclosure with a broad inner opening and base.",
            "波曲左侧竖干带小型回环，旁有高直折角围合，内部可见宽开口和底部。",
        ),
        "obs-unk-000653": (
            "Two rectangular side panels with horizontal interior bars flank a central crossing and upright strokes.",
            "两侧矩形笔组各有横向内痕，中部可见交叉和竖向笔画。",
        ),
        "obs-unk-000654": (
            "A tall curved left form is paired with a narrow central stem, a small rounded mark, and a detached short right stroke.",
            "高直弧形左侧笔组连接窄中轴，中部附近有小圆弧痕，右侧有分离短笔。",
        ),
        "obs-unk-000655": (
            "Short crossed marks form a compact left cluster beside a tall zigzagging curved stroke on the right.",
            "短小交叉笔画形成紧凑左侧笔组，右侧有高直且曲折的长笔。",
        ),
        "obs-unk-000656": (
            "A broad curved enclosure surrounds a small interior opening and descends to an open lower base; a detached dot sits above right.",
            "宽弧形围合内有小型空隙，底部收于开放底部；右上方有分离小点痕。",
        ),
        "obs-unk-000657": (
            "A long curved upper stroke extends toward a short central stem, with a separate upright stroke and lower branch at the right.",
            "长弧形上部笔画向短中轴延伸，右侧另有竖向笔画和下部外伸分支。",
        ),
        "obs-unk-000658": (
            "A large arched outer contour contains a small upper opening and central stroke, with two pointed lower projections.",
            "大型拱形外轮廓内有小型上部空隙和中部笔画，下方有两处尖角外伸。",
        ),
        "obs-unk-000659": (
            "A stacked double-loop mark sits above a horizontal crossing and a broad lower cluster with side projections.",
            "叠置双环痕迹位于横向交叉笔画之上，下方为宽笔组并有两侧外伸。",
        ),
        "obs-unk-000660": (
            "A tall angular enclosure frames a central pointed upright form, with a detached wavy stroke at the left.",
            "高直折角围合框住中部尖角竖向笔组，左侧有分离波曲笔画。",
        ),
    }
)

MATERIAL_VISUAL_OBSERVATIONS.update(
    {
        "obs-unk-000661": (
            "Two adjacent dense forms are visible: the left has a long descending stem, while the right has a rounded upper loop and lower diagonal projection.",
            "可见两个相邻密集笔组：左侧有长下行中轴，右侧有上部弧形环和下部斜向外伸。",
        ),
        "obs-unk-000662": (
            "Two tall neighboring forms each have a rounded upper cap, an open lower interior, and paired descending projections.",
            "两个相邻高直笔组各有弧形上部、开放下部空隙和成对下行外伸。",
        ),
        "obs-unk-000663": (
            "An open left loop, a central crossing stem, and a tall right enclosure with a long descending edge stand together.",
            "左侧开放环、中部交叉中轴和右侧高直围合并列，右侧边缘有长下行笔画。",
        ),
        "obs-unk-000664": (
            "A narrow left stroke and a curved right stroke flank a tall central crossing with a small opening and broad lower enclosure.",
            "窄左笔和弧形右笔夹住高直中部交叉；中部有小空隙，下方接宽围合。",
        ),
        "obs-unk-000665": (
            "A broad upper banded enclosure has two interior openings, with detached short strokes at the left and a lower mark at the right.",
            "宽上部横带围合内有两处空隙；左侧有分离短笔，右侧下方有外伸痕迹。",
        ),
        "obs-unk-000666": (
            "Two pointed upper strokes rise from a dense central cluster above a rounded lower enclosure with a small opening.",
            "两个尖角上行笔画从密集中部向上伸出，下方接带小空隙的弧形围合。",
        ),
        "obs-unk-000667": (
            "Two long curved upright strokes stand in parallel, with a separate pointed and curved mark descending at the right.",
            "两条长弧形竖向笔画近于平行，右侧另有尖角并弯曲下行的分离笔。",
        ),
        "obs-unk-000668": (
            "Short hooked strokes sit above a central loop and descending stem, with a detached small rounded mark at the upper right.",
            "短钩状笔画位于中央环状痕和下行中轴之上，右上方有分离小圆痕。",
        ),
        "obs-unk-000669": (
            "A compact looped left form, a tall central stem with side projections, and a detached curved right mark meet above a broad base.",
            "紧凑环状左部、高直中轴及两侧外伸和分离弧形右痕共同位于宽底部之上。",
        ),
        "obs-unk-000670": (
            "A forked upper form joins a broad lower loop with two long descending projections and a short side stroke.",
            "上部叉状笔组连接宽下部环状围合，下方有两条长下行外伸和一处短侧笔。",
        ),
        "obs-unk-000671": (
            "Dense branching strokes surround a small central opening, with long lower descents on both sides.",
            "密集分支笔画围绕小型中部空隙，两侧都有长下行笔画。",
        ),
        "obs-unk-000672": (
            "A detached long vertical stroke stands left of a tall angular panel with an inner horizontal band and curved lower edge.",
            "分离长竖笔位于高直折角笔板左侧，笔板内有横带，底部边缘弯曲下行。",
        ),
        "obs-unk-000673": (
            "Small upper strokes sit over two horizontal bands, flanked by detached vertical marks and an open lower frame.",
            "小型上部笔画位于两道横带之上，两侧有分离竖痕，下方为开放框形。",
        ),
        "obs-unk-000674": (
            "A rounded upper loop and central stem lead to a lower triangular enclosure, with long detached side strokes.",
            "弧形上部环和中轴连接下部三角围合，两侧有长而分离的侧向笔画。",
        ),
        "obs-unk-000675": (
            "A compact wavy left form stands beside a tall diagonal cluster with several descending projections.",
            "紧凑波曲左部位于高直斜向笔组一侧，右部有多处向下外伸。",
        ),
        "obs-unk-000676": (
            "A left looped form and a tall slanting right stroke meet above a lower triangular enclosure and short separated marks.",
            "左侧环状笔组和右侧高直斜笔相接，下方有三角围合及短分离痕迹。",
        ),
        "obs-unk-000677": (
            "A stacked double-loop mark sits above a horizontal crossing and a broad lower cluster with lateral projections.",
            "叠置双环痕迹位于横向交叉之上，下方为宽笔组并有两侧外伸。",
        ),
        "obs-unk-000678": (
            "Two rounded loops are stacked above a lower horizontal loop, with a detached curved stroke at the left.",
            "两个弧形环圈叠置于下部横向环状笔组之上，左侧有分离弧形笔画。",
        ),
        "obs-unk-000679": (
            "A tall narrow wavy composite has pointed upper strokes, an open central channel, and a long curved descent at the left.",
            "高窄波曲笔组上部有尖角笔画，中部留开放通道，左侧有长弧形下行。",
        ),
        "obs-unk-000680": (
            "A broad angular enclosure frames a central rounded mark crossed by horizontal strokes and a heavy lower base.",
            "宽折角围合框住中部弧形痕迹，中部有横向交叉笔画，下方接较重底部。",
        ),
    }
)

MATERIAL_VISUAL_OBSERVATIONS.update(
    {
        "obs-unk-000681": (
            "A left rectangular panel and a right looped form are linked by a central stem, with a long descent below the right form.",
            "左侧矩形笔板与右侧环状笔组由中轴连接，右侧下方有长下行笔画。",
        ),
        "obs-unk-000682": (
            "A detached curved stroke stands left of a dense upper cluster with an inner band and a long descent to a lower rectangle.",
            "分离弧形笔位于密集上部笔组左侧，笔组内有横带，长笔下行至下部矩形。",
        ),
        "obs-unk-000683": (
            "A looped left form with a long lower descent stands beside a pointed upper mark and a separate tall stem.",
            "带长下行笔的环状左部旁有尖角上部痕迹和分离高直中轴。",
        ),
        "obs-unk-000684": (
            "A dense diagonal cluster has a small central opening, parallel lower strokes, and pointed outer projections.",
            "密集斜向笔组中有小型中部空隙，下方有平行笔画和尖角外伸。",
        ),
        "obs-unk-000685": (
            "A broad angular enclosure contains an upper horizontal bar and central stem, bounded by two curved side strokes.",
            "宽折角围合内有上部横痕和中轴，两侧由弧形笔画围住。",
        ),
        "obs-unk-000686": (
            "Two rectangular looped panels flank a central crossing and upright stroke, with pointed projections below.",
            "两个矩形环状笔板夹住中部交叉和竖向笔画，下方有尖角外伸。",
        ),
        "obs-unk-000687": (
            "A tall wavy looped form stands left of a separate pointed cap and an open lower loop with pointed projections.",
            "高直波曲环状笔组位于分离尖角笔帽和开放下部环组左侧，下部有尖角外伸。",
        ),
        "obs-unk-000688": (
            "Two rectangular panels each contain horizontal interior bars, with a short lower base on the left and a curved descent on the right.",
            "两个矩形笔板各有横向内痕，左下方有短底部，右侧有弧形下行。",
        ),
        "obs-unk-000689": (
            "A horizontal crossing surrounds a small central oval, with a curved stem and side projections extending below.",
            "横向交叉围绕小型中部椭圆痕迹，下方有弧形中轴和侧向外伸。",
        ),
        "obs-unk-000690": (
            "A tall pointed central mass stands between curved side strokes above a broad lower enclosure with a small opening.",
            "高直尖角中部位于两侧弧形笔之间，下方接带小空隙的宽围合。",
        ),
        "obs-unk-000691": (
            "A tall rectangular panel with a lower curved projection stands beside a separate short curved vertical stroke.",
            "高直矩形笔板下方有弧形外伸，旁边另有分离短弧形竖笔。",
        ),
        "obs-unk-000692": (
            "A broad upper arch and horizontal band sit above a central oval and dense lower branching projections.",
            "宽上部拱形和横带位于中部椭圆痕迹之上，下方有密集分支外伸。",
        ),
        "obs-unk-000693": (
            "A tall central branching form has an inner opening and curled side marks, ending in a lower triangular base.",
            "高直中部分支笔组有内侧空隙和两侧卷曲痕迹，底部收于三角底座。",
        ),
        "obs-unk-000694": (
            "A peaked dense cluster has a rounded central opening, parallel lower strokes, and a pointed right edge.",
            "密集尖顶笔组中有圆形中部空隙，下方有平行笔画，右侧边缘尖出。",
        ),
        "obs-unk-000695": (
            "A stacked looped left form stands beside a tall narrow right stem with a small lower loop and point.",
            "叠置环状左部位于高窄右侧中轴旁，右侧下方有小环和尖角外伸。",
        ),
        "obs-unk-000696": (
            "A tall rectangular left panel with an inner opening stands beside a smaller right looped panel and lower curved strokes.",
            "高直左侧矩形笔板内有空隙，旁边是较小右侧环状笔板和下部弧形笔画。",
        ),
        "obs-unk-000697": (
            "A stacked double-loop form descends to a pointed lower mark, beside a separate tall stem with a pointed cap.",
            "叠置双环笔组向下连接尖角痕迹，旁边有带尖角笔帽的分离高直中轴。",
        ),
        "obs-unk-000698": (
            "Two rectangular panels stand above a lower central crossing with branching downward projections.",
            "两个矩形笔板位于下部中部交叉之上，下方有分支下行外伸。",
        ),
        "obs-unk-000699": (
            "A broad rounded left loop is paired with a tall curved right form containing a small opening and lower hook.",
            "宽弧形左环与高直弧形右部并列，右部内有小空隙和下部钩状笔画。",
        ),
        "obs-unk-000700": (
            "Two dense neighboring forms are visible: the left is wavy and looped, while the right has pointed upper and lower projections.",
            "可见两个相邻密集笔组：左侧波曲并带环状痕迹，右侧上下都有尖角外伸。",
        ),
    }
)

@dataclass(frozen=True)
class Candidate:
    project_id: str
    object_dir: Path
    packet_path: Path
    primary_external_ref_id: str
    source_id: str
    source_package_id: str
    download_id: str
    source_group: str
    source_group_label: str
    source_class_id: str
    source_class_path: str
    source_image_path: str
    source_image_count: str
    rights_status: str
    risk_note: str
    caution: str
    review_status: str


def filesystem_path(path: Path) -> str:
    resolved = path.resolve()
    if os.name == "nt":
        return "\\\\?\\" + str(resolved)
    return str(resolved)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(filesystem_path(path), "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_size(path: Path) -> int:
    return os.stat(filesystem_path(path)).st_size


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        if not rows:
            raise ValueError(f"cannot infer fieldnames for empty CSV: {path}")
        fieldnames = list(rows[0])
    with open(filesystem_path(path), "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fieldnames} for row in rows])


def wrapped_bullet(text: str) -> str:
    return textwrap.fill(
        f"- {text}",
        width=MAX_HUMAN_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=True,
        break_on_hyphens=False,
    )


def wrapped_check(text: str) -> str:
    return textwrap.fill(
        f"- [ ] {text}",
        width=MAX_HUMAN_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )


def wrapped_paragraph(text: str) -> str:
    return textwrap.fill(
        text,
        width=MAX_HUMAN_LINE_LENGTH,
        break_long_words=True,
        break_on_hyphens=False,
    )


def upsert_rows(path: Path, key: str, new_rows: list[dict[str, str]]) -> None:
    rows = read_csv(path)
    fields = list(rows[0]) if rows else list(new_rows[0])
    by_key = {row[key]: row for row in rows}
    for row in new_rows:
        by_key[row[key]] = row
    write_csv(path, [by_key[row_key] for row_key in sorted(by_key)], fields)


def sanitize_token(value: str) -> str:
    return "".join(ch if ch.isascii() and (ch.isalnum() or ch in "-_") else "-" for ch in value).strip("-")


def find_zip_member(zip_file: zipfile.ZipFile, source_path: str) -> str:
    normalized = source_path.replace("\\", "/")
    names = zip_file.namelist()
    if normalized in names:
        return normalized
    matches = [name for name in names if name.replace("\\", "/").endswith(normalized)]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise FileNotFoundError(f"zip member not found: {source_path}")
    raise ValueError(f"ambiguous zip member for {source_path}: {matches[:3]}")


def next_asset_number(asset_rows: list[dict[str, str]]) -> int:
    numbers = [
        int(row["asset_id"].rsplit("-", 1)[1])
        for row in asset_rows
        if row.get("asset_id", "").startswith("asset-") and row["asset_id"].rsplit("-", 1)[1].isdigit()
    ]
    return max(numbers, default=0) + 1


def existing_asset_by_project(asset_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        row["related_project_ids"]: row
        for row in asset_rows
        if row.get("asset_type") == "glyph_candidate_image"
        and row.get("related_project_ids", "").startswith("obs-unk-")
    }


def load_candidates(root: Path) -> list[Candidate]:
    candidates: list[Candidate] = []
    for row in read_csv(root / UNDECIPHERED_INDEX):
        packet_path = root / row["materialized_candidate_packet_path"]
        object_dir = packet_path.parent
        candidates.append(
            Candidate(
                project_id=row["unknown_candidate_id"],
                object_dir=object_dir,
                packet_path=packet_path,
                primary_external_ref_id=row["primary_external_ref_id"],
                source_id=row["source_id"],
                source_package_id=row["source_package_id"],
                download_id=row["evidence_download_id"],
                source_group=row["source_group"],
                source_group_label=row["source_group_label"],
                source_class_id=row["source_class_id"],
                source_class_path=row["source_class_path"],
                source_image_path=row["first_source_image_path"],
                source_image_count=row["source_image_count"],
                rights_status=row["rights_status"],
                risk_note=row["risk_note"],
                caution=row["caution"],
                review_status=row["review_status"],
            )
        )
    return candidates


def image_info(path: Path) -> dict[str, str]:
    with Image.open(filesystem_path(path)) as image:
        dpi = image.info.get("dpi", ("", ""))
        icc = image.info.get("icc_profile", b"")
        return {
            "image_format": image.format or "",
            "pixel_width": str(image.width),
            "pixel_height": str(image.height),
            "color_mode": image.mode,
            "dpi_x": str(dpi[0]) if dpi and dpi[0] else "",
            "dpi_y": str(dpi[1]) if dpi and len(dpi) > 1 and dpi[1] else "",
            "icc_profile_bytes": str(len(icc) if icc else 0),
        }


def visual_profile(path: Path) -> dict[str, str]:
    with Image.open(filesystem_path(path)) as image:
        gray = image.convert("L")
        width, height = gray.size
        pixels = list(gray.getdata())
        foreground = [(index % width, index // width) for index, value in enumerate(pixels) if value < LUMA_THRESHOLD]
        mean_luma = ImageStat.Stat(gray).mean[0]
    if foreground:
        xs = [point[0] for point in foreground]
        ys = [point[1] for point in foreground]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        bbox_width = x_max - x_min + 1
        bbox_height = y_max - y_min + 1
    else:
        x_min = y_min = x_max = y_max = bbox_width = bbox_height = 0
    pixel_count = width * height
    foreground_count = len(foreground)
    return {
        "pixel_width": str(width),
        "pixel_height": str(height),
        "foreground_bbox_x_min": str(x_min),
        "foreground_bbox_y_min": str(y_min),
        "foreground_bbox_x_max": str(x_max),
        "foreground_bbox_y_max": str(y_max),
        "foreground_bbox_width": str(bbox_width),
        "foreground_bbox_height": str(bbox_height),
        "foreground_pixel_count": str(foreground_count),
        "foreground_pixel_ratio": f"{foreground_count / pixel_count:.8f}" if pixel_count else "0.00000000",
        "mean_luma": f"{mean_luma:.4f}",
    }


def metadata_yaml(
    candidate: Candidate,
    asset_id: str,
    relative_asset_path: Path,
    raw_bytes: bytes,
    output_path: Path,
) -> str:
    info = image_info(output_path)
    return f"""asset_id: {asset_id}
asset_type: glyph_candidate_image
local_file: {relative_asset_path.name}
canonical_path: {relative_asset_path.as_posix()}
file_size_bytes: {file_size(output_path)}
checksum_sha256: {sha256_file(output_path)}
image_format: {info["image_format"]}
pixel_width: {info["pixel_width"]}
pixel_height: {info["pixel_height"]}
color_mode: {info["color_mode"]}
related_project_ids:
  - {candidate.project_id}
related_external_ref_ids:
  - {candidate.primary_external_ref_id}
source_id: {candidate.source_id}
source_package_id: {candidate.source_package_id}
download_id: {candidate.download_id}
source_image_path: {candidate.source_image_path}
source_image_count_expected: {candidate.source_image_count}
raw_source_image_checksum_sha256: {sha256_bytes(raw_bytes)}
rights_status: {candidate.rights_status}
analysis_scope: local_review_image_derivative_only
risk_note: {RISK_NOTE}
review_status: needs_human_visual_review
research_boundary: candidate_image_not_scholarship
caution: {BOUNDARY_CAUTION}
updated_at: {UPDATED_AT}
"""


def visual_source_index(candidate: Candidate, asset_id: str, relative_asset_path: Path) -> list[dict[str, str]]:
    return [
        {
            "visual_source_index_id": f"{candidate.project_id}-visual-source-001",
            "project_id": candidate.project_id,
            "primary_external_ref_id": candidate.primary_external_ref_id,
            "source_id": candidate.source_id,
            "source_package_id": candidate.source_package_id,
            "download_id": candidate.download_id,
            "asset_id": asset_id,
            "visual_material_status": "committed_review_image_derivative",
            "committed_image_path": relative_asset_path.as_posix(),
            "source_image_reference_path": candidate.source_image_path,
            "source_image_sequence_in_candidate": "001",
            "source_image_count_expected": candidate.source_image_count,
            "registered_storage_hint": RAW_ZIP.as_posix(),
            "resolved_local_archive_path": RAW_ZIP.as_posix(),
            "local_archive_status": "registered_external_archive_available_outside_git",
            "rights_status": candidate.rights_status,
            "risk_note": RISK_NOTE,
            "review_status": "needs_human_visual_review",
            "research_boundary": "co_located_visual_source_index_not_scholarship",
            "caution": BOUNDARY_CAUTION,
            "updated_at": UPDATED_AT,
        }
    ]


def build_visual_source_rows(
    candidate: Candidate,
    asset_id: str,
    relative_asset_path: Path,
    visual_index_path: Path,
) -> list[dict[str, str]]:
    if visual_index_path.exists():
        rows = read_csv(visual_index_path)
        if rows and len(rows) > 1:
            for index, row in enumerate(rows, start=1):
                row["project_id"] = candidate.project_id
                row["primary_external_ref_id"] = candidate.primary_external_ref_id
                row["source_id"] = candidate.source_id
                row["source_package_id"] = row.get("source_package_id") or candidate.source_package_id
                row["download_id"] = row.get("download_id") or candidate.download_id
                row["asset_id"] = asset_id if index == 1 else row.get("asset_id", "")
                row["visual_material_status"] = (
                    "committed_review_image_derivative"
                    if index == 1
                    else row.get("visual_material_status", "source_image_reference_only_no_committed_glyph_image")
                )
                row["committed_image_path"] = relative_asset_path.as_posix() if index == 1 else ""
                row["source_image_sequence_in_candidate"] = (
                    row.get("source_image_sequence_in_candidate") or f"{index:03d}"
                )
                row["source_image_count_expected"] = row.get("source_image_count_expected") or candidate.source_image_count
                row["registered_storage_hint"] = row.get("registered_storage_hint") or RAW_ZIP.as_posix()
                row["resolved_local_archive_path"] = row.get("resolved_local_archive_path") or RAW_ZIP.as_posix()
                row["local_archive_status"] = "registered_external_archive_available_outside_git"
                row["rights_status"] = candidate.rights_status
                row["risk_note"] = row.get("risk_note") or RISK_NOTE
                row["review_status"] = "needs_human_visual_review"
                row["research_boundary"] = row.get("research_boundary") or "co_located_visual_source_index_not_scholarship"
                existing_caution = row.get("caution", "")
                row["caution"] = (
                    BOUNDARY_CAUTION
                    if "local derivative is not present" in existing_caution
                    else existing_caution or BOUNDARY_CAUTION
                )
                row["updated_at"] = UPDATED_AT
            return rows
    return visual_source_index(candidate, asset_id, relative_asset_path)


def readme_text(candidate: Candidate, asset_id: str, asset_name: str) -> str:
    return f"""# {candidate.project_id} Local Object Materials / {candidate.project_id} 本地对象资料

English:
This directory is the object-local human research entrance for one HUST-OBC undeciphered oracle-character candidate. Start with the human review sheet, visual gallery, source route, local image, and concrete questions; use structured support files only to trace and verify the human-readable evidence.

简体中文：
本目录是一个 HUST-OBC 未释甲骨字候选的同目录工作资料夹。人类可读说明、图像图库、复核表、来源路线、本地图像和 AI 可读候选包都放在同一具体对象目录内。

## Local Files / 本地文件

- Structured support packet / 结构化辅助候选包: `01_undeciphered-candidate-packet.json`
- Structured support visual/source index / 结构化辅助图像来源索引: `02_visual-source-index.csv`
- Human-readable visual gallery / 人类可读图像图库: `04_visual-gallery.md`
- Human review sheet / 人工复核表: `05_human-review-sheet.md`
- Local review image / 本地复核图像: `03_visual-assets/{asset_name}`

## Human Oracle Character Review Slots / 甲骨单字人工复核槽位

Structured support files only serve the human oracle-character dossier.

结构化辅助文件只服务本对象内的人类甲骨单字档案。

- Open the visual gallery and record visible strokes or damage.
- Check HUST-OBC source image, package, rights, and risk note.
- Name variant, near-form, component, and later-script routes as pending.
- Keep readings, identities, disputes, and bibliography as review tasks.
- Check inscription, plate, collection, findspot, and period gaps.
- Write every missing item as a concrete question before research.
- 先打开图像图库，记录可见笔画、残缺或疑点。
- 核对 HUST-OBC 来源图像、来源包、权利和风险提示。
- 将异体、近形、构件和后世字形路线标为待复核。
- 释读、身份、争议和文献关系只记为待查任务。
- 核对卜辞、图版、馆藏、出土地和时期缺口。
- 正式研究前，所有缺失项都写成具体问题。

## Object Summary / 对象摘要

- Project ID / 项目 ID: `{candidate.project_id}`
- Primary external reference / 首选外部参考: `{candidate.primary_external_ref_id}`
- Source group / 来源分组: `{candidate.source_group}` ({candidate.source_group_label})
- Source class path / 来源分类路径: `{candidate.source_class_path}`
- Source image path / 来源图像路径: `{candidate.source_image_path}`
- Asset ID / 资产 ID: `{asset_id}`

## Boundary / 边界

English:
This is a preparation-stage candidate packet and image entrance. It is not an accepted character record, not an accepted reading, not a component conclusion, and not a decipherment conclusion.

简体中文：
这是准备阶段的候选资料包和图像入口。它不是正式甲骨单字记录，不是已确认释读，不是构件结论，也不是破译结论。
"""


def gallery_text(candidate: Candidate, asset_id: str, asset_name: str, metadata_name: str) -> str:
    return f"""# {candidate.project_id} Visual Gallery / {candidate.project_id} 图像资料页

English:
This human-readable gallery stays inside the same concrete candidate directory as the structured support packet and visual/source index.

简体中文：
本图像资料页与 AI 可读候选包、图像与来源索引放在同一个具体候选目录内。

- Visual/source index / 图像与来源索引: `02_visual-source-index.csv`

## Review Image / 复核图像

![{candidate.project_id} glyph candidate](03_visual-assets/{asset_name})

- Asset ID / 资产 ID: `{asset_id}`
- Local image / 本地图像: `03_visual-assets/{asset_name}`
- Local metadata / 本地 metadata: `03_visual-assets/{metadata_name}`
- Source image path / 来源图像路径: `{candidate.source_image_path}`
- Source package / 来源包: `{candidate.source_package_id}`
- Download ID / 下载 ID: `{candidate.download_id}`
- Rights status / 权利状态: `{candidate.rights_status}`
- Risk note / 风险提示: {RISK_NOTE}

## Research Boundary / 研究边界

English:
The image shown here is source-marked preparation material for human visual review. It is not an accepted glyph identity, not an accepted reading, not a component conclusion, and not a decipherment conclusion.

简体中文：
本页图像是带来源标记的准备阶段材料，用于人工视觉复核。它不是已确认字形身份，不是已确认释读，不是构件结论，也不是破译结论。
"""


def review_sheet_text(candidate: Candidate, asset_id: str) -> str:
    english_scope = wrapped_paragraph(
        "Review only whether the local image, packet, and source-route "
        "metadata match the registered HUST-OBC source package. Do not record "
        "a reading, identity confirmation, component conclusion, or "
        "decipherment conclusion here."
    )
    chinese_scope = "\n".join(
        [
            "这里只复核本地图像、候选包和来源路线 metadata 是否对应已登记的",
            "HUST-OBC 来源包。不要在此记录释读、身份确认、构件结论或破译结论。",
        ]
    )
    checklist = "\n".join(
        [
            wrapped_check("Source image path checked against `02_visual-source-index.csv`"),
            wrapped_check("Local review image opens and is readable"),
            wrapped_check(f"Asset registry row checked: `{asset_id}`"),
            wrapped_check("Rights and risk note reviewed"),
            wrapped_check("No formal reading or identity claim added"),
        ]
    )
    concrete_questions = "\n".join(
        [
            wrapped_bullet("Which HUST-OBC source image should be checked first?"),
            wrapped_bullet(
                "Which glyph, codepoint, or later-script route is only a "
                "candidate clue?"
            ),
            wrapped_bullet(
                "Which inscription, plate, collection, findspot, or period "
                "context is still missing?"
            ),
            wrapped_bullet(
                "Which rights status or source-package risk must be rechecked "
                "before reuse?"
            ),
            wrapped_bullet(
                "What evidence is still missing before any formal reading or "
                "identity judgment?"
            ),
            "",
            "- 应先核对哪一张 HUST-OBC 来源图像？",
            "- 哪些字形、codepoint 或后世字形路线只是候选线索？",
            "- 还缺哪些卜辞、图版、馆藏、出土地或时期上下文？",
            "- 复用前还要复核哪些权利状态或来源包风险？",
            "- 正式释读或身份判断前还缺哪些证据？",
        ]
    )
    return f"""# {candidate.project_id} Human Review Sheet / {candidate.project_id} 人工复核表

## Review Scope / 复核范围

English:
{english_scope}

简体中文：
{chinese_scope}

## Checklist / 清单

{checklist}

## Concrete Questions To Check / 具体待查问题

{concrete_questions}

## Status / 状态

- Review status / 复核状态: `needs_human_visual_review`
- Promotion status / 提升状态: `not_promoted`
- Identity claim status / 身份结论状态: `no_identity_claim`
- Decipherment claim status / 释读结论状态: `no_claim`
"""


def readme_text(candidate: Candidate, asset_id: str, asset_name: str) -> str:
    lines = [
        f"# {candidate.project_id} Local Object Materials / "
        f"{candidate.project_id} 本地对象资料",
        "",
        "English:",
        wrapped_paragraph(
            "This directory is the object-local human research entrance for "
            "one HUST-OBC undeciphered oracle-character candidate. Start with "
            "the human review sheet, visual gallery, source route, local "
            "image, and concrete questions; use structured support files only "
            "to trace and verify the human-readable evidence."
        ),
        "",
        "简体中文:",
        wrapped_paragraph(
            "本目录是一个 HUST-OBC 未释甲骨字候选的同目录工作资料夹。"
            "人类可读说明、图像图廊、复核表、来源路线、本地图像和 AI "
            "可读候选包都放在同一个具体对象目录内。"
        ),
        "",
        "## Local Files / 本地文件",
        "",
        wrapped_bullet(
            "Structured support packet / 结构化辅助候选包: "
            "`01_undeciphered-candidate-packet.json`"
        ),
        wrapped_bullet(
            "Structured support visual/source index / 结构化辅助图像来源索引: "
            "`02_visual-source-index.csv`"
        ),
        wrapped_bullet(
            "Human-readable visual gallery / 人类可读图像图廊: "
            "`04_visual-gallery.md`"
        ),
        wrapped_bullet(
            "Human research dossier / 人类研究档案: "
            "`05_human-research-dossier.md`"
        ),
        wrapped_bullet(
            "Human review sheet / 人工复核表: `05_human-review-sheet.md`"
        ),
        wrapped_bullet(
            "Context evidence dossier / 上下文证据档案: "
            "`08_character-context-evidence-dossier.md`"
        ),
        wrapped_bullet(
            "Archaeology and paleography review / 考古文字学复核: "
            "`10_archaeology-paleography-review.md`"
        ),
        wrapped_bullet(
            "Human research readiness / 人类研究准备度: "
            "`12_human-research-readiness-review.md`"
        ),
        wrapped_bullet(
            "Readiness index / 准备度索引: "
            "`13_human-research-readiness-index.json`"
        ),
        wrapped_bullet(
            "Local review image / 本地复核图像: "
            f"`03_visual-assets/{asset_name}`"
        ),
        *(
            [
                wrapped_bullet(
                    "Human visual observation / 人类图像观察: "
                    "`14_material-visual-observation.md`"
                )
            ]
            if candidate.project_id in MATERIAL_VISUAL_OBSERVATIONS
            else []
        ),
        "",
        "## Human Oracle Character Review Slots / 甲骨单字人工复核槽位",
        "",
        "Structured support files only serve the human oracle-character dossier.",
        "",
        "结构化辅助文件只服务本对象内的人类甲骨单字档案。",
        "",
        wrapped_bullet("Open the visual gallery and record visible strokes or damage."),
        wrapped_bullet("Check HUST-OBC source image, package, rights, and risk note."),
        wrapped_bullet(
            "Name variant, near-form, component, and later-script routes as pending."
        ),
        wrapped_bullet(
            "Keep readings, identities, disputes, and bibliography as review tasks."
        ),
        wrapped_bullet("Check inscription, plate, collection, findspot, and period gaps."),
        wrapped_bullet("Write every missing item as a concrete question before research."),
        wrapped_bullet("先打开图像图库，记录可见笔画、残缺或疑点。"),
        wrapped_bullet("核对 HUST-OBC 来源图像、来源包、权利和风险提示。"),
        wrapped_bullet("将异体、近形、构件和后世字形路线标为待复核。"),
        wrapped_bullet("释读、身份、争议和文献关系只记为待查任务。"),
        wrapped_bullet("核对卜辞、图版、馆藏、出土地和时期缺口。"),
        wrapped_bullet("正式研究前，所有缺失项都写成具体问题。"),
        "",
        "## Object Summary / 对象摘要",
        "",
        wrapped_bullet(f"Project ID / 项目 ID: `{candidate.project_id}`"),
        wrapped_bullet(
            "Primary external reference / 首选外部参考: "
            f"`{candidate.primary_external_ref_id}`"
        ),
        wrapped_bullet(
            "Source group / 来源分组: "
            f"`{candidate.source_group}` ({candidate.source_group_label})"
        ),
        wrapped_bullet(
            f"Source class path / 来源分类路径: `{candidate.source_class_path}`"
        ),
        wrapped_bullet(
            f"Source image path / 来源图像路径: `{candidate.source_image_path}`"
        ),
        wrapped_bullet(f"Asset ID / 资产 ID: `{asset_id}`"),
        "",
        "## Boundary / 边界",
        "",
        "English:",
        wrapped_paragraph(
            "This is a preparation-stage candidate packet and image entrance. "
            "It is not an accepted character record, not an accepted reading, "
            "not a component conclusion, and not a decipherment conclusion."
        ),
        "",
        "简体中文:",
        wrapped_paragraph(
            "这是准备阶段的候选资料包和图像入口。它不是正式甲骨单字"
            "记录，不是已确认释读，不是构件结论，也不是破译结论。"
        ),
    ]
    return "\n".join(lines) + "\n"


def ensure_material_observation_link(readme_path: Path) -> None:
    """Add the human observation route without replacing curated README text."""
    if not readme_path.exists():
        return
    text = readme_path.read_text(encoding="utf-8")
    if "14_material-visual-observation.md" in text:
        return
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if (
            "Local review image" in line
            or "本地复核图像" in line
            or "Committed glyph image" in line
            or "已提交字形图像" in line
        ):
            lines.insert(
                index + 1,
                "- Human visual observation / 人类图像观察: "
                "`14_material-visual-observation.md`",
            )
            readme_path.write_text(
                "\n".join(lines).rstrip() + "\n",
                encoding="utf-8",
                newline="\n",
            )
            return
    raise ValueError(f"README has no local-image route: {readme_path}")


def gallery_text(candidate: Candidate, asset_id: str, asset_name: str, metadata_name: str) -> str:
    lines = [
        f"# {candidate.project_id} Visual Gallery / {candidate.project_id} 图像资料页",
        "",
        "English:",
        wrapped_paragraph(
            "This human-readable gallery stays inside the same concrete "
            "candidate directory as the structured support packet and "
            "visual/source index."
        ),
        "",
        "简体中文:",
        wrapped_paragraph(
            "本图像资料页与 AI 可读候选包、图像与来源索引放在同一个"
            "具体候选目录内。"
        ),
        wrapped_bullet(
            "Visual/source index / 图像与来源索引: `02_visual-source-index.csv`"
        ),
        "",
        "## Review Image / 复核图像",
        "",
        f"![{candidate.project_id} glyph candidate](03_visual-assets/{asset_name})",
        "",
        wrapped_bullet(f"Asset ID / 资产 ID: `{asset_id}`"),
        wrapped_bullet(f"Local image / 本地图像: `03_visual-assets/{asset_name}`"),
        wrapped_bullet(
            f"Local metadata / 本地 metadata: `03_visual-assets/{metadata_name}`"
        ),
        wrapped_bullet(
            f"Source image path / 来源图像路径: `{candidate.source_image_path}`"
        ),
        wrapped_bullet(f"Source package / 来源包: `{candidate.source_package_id}`"),
        wrapped_bullet(f"Download ID / 下载 ID: `{candidate.download_id}`"),
        wrapped_bullet(f"Rights status / 权利状态: `{candidate.rights_status}`"),
        wrapped_bullet(f"Risk note / 风险提示: {RISK_NOTE}"),
        "",
        "## Research Boundary / 研究边界",
        "",
        "English:",
        wrapped_paragraph(
            "The image shown here is source-marked preparation material for "
            "human visual review. It is not an accepted glyph identity, not "
            "an accepted reading, not a component conclusion, and not a "
            "decipherment conclusion."
        ),
        "",
        "简体中文:",
        wrapped_paragraph(
            "本页图像是带来源标记的准备阶段材料，用于人工视觉复核。"
            "它不是已确认字形身份，不是已确认释读，不是构件结论，"
            "也不是破译结论。"
        ),
    ]
    return "\n".join(lines) + "\n"


def review_sheet_text(candidate: Candidate, asset_id: str) -> str:
    english_scope = wrapped_paragraph(
        "Review only whether the local image, packet, and source-route "
        "metadata match the registered HUST-OBC source package. Do not record "
        "a reading, identity confirmation, component conclusion, or "
        "decipherment conclusion here."
    )
    chinese_scope = wrapped_paragraph(
        "这里只复核本地图像、候选包和来源路线 metadata 是否对应已登记的 "
        "HUST-OBC 来源包。不要在此记录释读、身份确认、构件结论或破译结论。"
    )
    checklist = "\n".join(
        [
            wrapped_check("Source image path checked against `02_visual-source-index.csv`"),
            wrapped_check("Local review image opens and is readable"),
            wrapped_check(f"Asset registry row checked: `{asset_id}`"),
            wrapped_check("Rights and risk note reviewed"),
            wrapped_check("No formal reading or identity claim added"),
        ]
    )
    concrete_questions = "\n".join(
        [
            wrapped_bullet("Which HUST-OBC source image should be checked first?"),
            wrapped_bullet(
                "Which glyph, codepoint, or later-script route is only a "
                "candidate clue?"
            ),
            wrapped_bullet(
                "Which inscription, plate, collection, findspot, or period "
                "context is still missing?"
            ),
            wrapped_bullet(
                "Which rights status or source-package risk must be rechecked "
                "before reuse?"
            ),
            wrapped_bullet(
                "What evidence is still missing before any formal reading or "
                "identity judgment?"
            ),
            "",
            wrapped_bullet("应先核对哪一张 HUST-OBC 来源图像？"),
            wrapped_bullet(
                "哪些字形、codepoint 或后世字形路线只是候选线索？"
            ),
            wrapped_bullet(
                "还缺哪些卜辞、图版、馆藏、出土地或时期上下文？"
            ),
            wrapped_bullet(
                "复用前还要复核哪些权利状态或来源包风险？"
            ),
            wrapped_bullet(
                "正式释读或身份判断前还缺哪些证据？"
            ),
        ]
    )
    return "\n".join(
        [
            f"# {candidate.project_id} Human Review Sheet / "
            f"{candidate.project_id} 人工复核表",
            "",
            "## Review Scope / 复核范围",
            "",
            "English:",
            english_scope,
            "",
            "简体中文:",
            chinese_scope,
            "",
            "## Checklist / 清单",
            "",
            checklist,
            "",
            "## Concrete Questions To Check / 具体待查问题",
            "",
            concrete_questions,
            "",
            "## Status / 状态",
            wrapped_bullet("Review status / 复核状态: `needs_human_visual_review`"),
            wrapped_bullet("Promotion status / 提升状态: `not_promoted`"),
            wrapped_bullet("Identity claim status / 身份结论状态: `no_identity_claim`"),
            wrapped_bullet("Decipherment claim status / 释读结论状态: `no_claim`"),
            "",
        ]
    )


def material_visual_observation_text(
    candidate: Candidate,
    asset_id: str,
    asset_name: str,
) -> str:
    english_observation, chinese_observation = MATERIAL_VISUAL_OBSERVATIONS[
        candidate.project_id
    ]
    lines = [
        f"# Material Visual Observation / {candidate.project_id} 实物图像观察",
        "",
        "English:",
        wrapped_paragraph(
            "This note records only visible marks in one local, source-linked "
            "review image. It is a preparation-stage observation for a human "
            "researcher, not a reading or component assignment."
        ),
        "",
        "简体中文：",
        wrapped_paragraph(
            "本记录只描述一张有来源链接的本地复核图像中直接可见的痕迹，"
            "供人类研究者在预处理阶段查阅，不是释读或构件归属判断。"
        ),
        "",
        "## Evidence Opened / 已打开证据",
        "",
        wrapped_bullet(f"Project ID / 项目 ID: `{candidate.project_id}`"),
        wrapped_bullet(
            f"External reference / 外部参照: `{candidate.primary_external_ref_id}`"
        ),
        wrapped_bullet(
            "Local image / 本地图像: "
            f"`03_visual-assets/{asset_name}`"
        ),
        wrapped_bullet(
            "Source image route / 来源图像路线: "
            "open `02_visual-source-index.csv`"
        ),
        wrapped_bullet(f"Source / 来源: `{candidate.source_id}`"),
        wrapped_bullet(
            f"Source package / 来源包: `{candidate.source_package_id}`"
        ),
        wrapped_bullet(f"Download route / 下载路线: `{candidate.download_id}`"),
        wrapped_bullet(
            "Rights and risk / 权利与风险: "
            f"`{candidate.rights_status}`; see the visual index risk note."
        ),
        "",
        "## Direct Visual Record / 直接可见记录",
        "",
        wrapped_bullet(f"English observation: {english_observation}"),
        wrapped_bullet(f"中文观察: {chinese_observation}"),
        "",
        "## Next Checks / 下一步核查",
        "",
        wrapped_bullet(
            "Open the image metadata and source row before comparing another form."
        ),
        wrapped_bullet(
            "Check whether a second view, rubbing, plate, or inscription "
            "context exists."
        ),
        wrapped_bullet(
            "Record variants, near forms, components, readings, and disputes "
            "only after source review."
        ),
        wrapped_bullet("打开图像 metadata 和来源行，再与其他字形进行比较。"),
        wrapped_bullet("查找是否存在第二视角、拓片、图版或卜辞上下文。"),
        wrapped_bullet("完成来源复核后，再记录异体、近形、构件、释读和争议。"),
        "",
        "## Boundary / 边界",
        "",
        wrapped_paragraph(
            "This is a visual observation record, not a reading or component "
            "assignment, not an inscription identity claim, and not a "
            "decipherment conclusion."
        ),
        wrapped_paragraph(
            "本记录是图像观察记录，不是释读、构件归属、卜辞身份或破译结论。"
        ),
        "",
    ]
    return "\n".join(lines)


def asset_source_row(candidate: Candidate, asset_id: str, relative_asset_path: Path, output_path: Path) -> dict[str, str]:
    return {
        "asset_id": asset_id,
        "asset_type": "glyph_candidate_image",
        "canonical_path": relative_asset_path.as_posix(),
        "file_size_bytes": str(file_size(output_path)),
        "related_project_ids": candidate.project_id,
        "primary_external_ref_id": candidate.primary_external_ref_id,
        "source_ids": candidate.source_id,
        "source_url": FIGSHARE_SOURCE_URL,
        "rights_status": candidate.rights_status,
        "risk_note": RISK_NOTE,
        "review_status": "needs_human_visual_review",
        "updated_at": UPDATED_AT,
    }


def rights_row(asset_id: str) -> dict[str, str]:
    number = asset_id.rsplit("-", 1)[1]
    return {
        "review_id": f"asset-rights-review-{number}",
        "asset_id": asset_id,
        "reviewer": "codex-agent",
        "rights_status_before": "unreviewed",
        "rights_status_after": "source_marked_risk_noted",
        "evidence": (
            "HUST-OBC raw package is registered as large-src-000001; Figshare package "
            "metadata reports CC BY 4.0 while the Scientific Data article page uses "
            "CC BY-NC-ND 4.0."
        ),
        "reviewed_at": UPDATED_AT,
        "notes": "Preparation-stage local review image only; not decipherment evidence.",
    }


def asset_map_row(candidate: Candidate, asset_id: str, relative_asset_path: Path) -> dict[str, str]:
    return {
        "project_id": asset_id,
        "record_type": "glyph_candidate_image",
        "canonical_path": relative_asset_path.as_posix(),
        "primary_external_ref_id": candidate.primary_external_ref_id,
        "all_external_ref_ids": f"{candidate.primary_external_ref_id};large-src-000001;{candidate.download_id}",
        "source_ids": candidate.source_id,
        "rights_status": candidate.rights_status,
        "review_status": "needs_human_visual_review",
        "updated_at": UPDATED_AT,
    }


def technical_profile_row(asset_id: str, relative_asset_path: Path, output_path: Path) -> dict[str, str]:
    info = image_info(output_path)
    number = asset_id.rsplit("-", 1)[1]
    return {
        "profile_id": f"asset-image-profile-{number}",
        "asset_id": asset_id,
        "asset_path": relative_asset_path.as_posix(),
        "image_format": info["image_format"],
        "pixel_width": info["pixel_width"],
        "pixel_height": info["pixel_height"],
        "color_mode": info["color_mode"],
        "dpi_x": info["dpi_x"],
        "dpi_y": info["dpi_y"],
        "icc_profile_bytes": info["icc_profile_bytes"],
        "file_size_bytes": str(file_size(output_path)),
        "checksum_sha256": sha256_file(output_path),
        "analysis_tool": "Pillow",
        "analysis_scope": "image_technical_metadata_only",
        "caution": "Technical profile records file properties only; it is not glyph segmentation or paleographic interpretation.",
        "review_status": "needs_human_visual_review",
        "updated_at": UPDATED_AT,
    }


def visual_profile_row(asset_id: str, relative_asset_path: Path, output_path: Path) -> dict[str, str]:
    profile = visual_profile(output_path)
    number = asset_id.rsplit("-", 1)[1]
    return {
        "visual_profile_id": f"asset-visual-profile-{number}",
        "asset_id": asset_id,
        "asset_path": relative_asset_path.as_posix(),
        "analysis_tool": "Pillow",
        "analysis_method": "pillow_luma_threshold_bbox_v1",
        "luma_threshold": str(LUMA_THRESHOLD),
        **profile,
        "analysis_scope": "visual_preprocessing_metadata_only",
        "caution": "Algorithmic foreground candidate only; not glyph segmentation, component analysis, or paleographic interpretation.",
        "review_status": "needs_human_visual_review",
        "updated_at": UPDATED_AT,
    }


def build_materials(
    root: Path,
    project_ids: set[str] | None = None,
) -> dict[str, int]:
    root = root.resolve()
    raw_zip = root / RAW_ZIP
    if sha256_file(raw_zip) != EXPECTED_RAW_SHA256:
        raise ValueError(f"HUST-OBC raw zip checksum mismatch: {raw_zip}")

    candidates = load_candidates(root)
    if project_ids:
        candidates = [
            candidate
            for candidate in candidates
            if candidate.project_id in project_ids
        ]
    asset_rows = read_csv(root / ASSET_SOURCE_INDEX)
    existing_assets = existing_asset_by_project(asset_rows)
    next_number = next_asset_number(asset_rows)

    new_asset_rows: list[dict[str, str]] = []
    new_rights_rows: list[dict[str, str]] = []
    new_map_rows: list[dict[str, str]] = []
    new_technical_rows: list[dict[str, str]] = []
    new_visual_rows: list[dict[str, str]] = []
    reused_asset_count = 0

    with zipfile.ZipFile(raw_zip) as zip_file:
        for candidate in candidates:
            existing = existing_assets.get(candidate.project_id)
            if existing:
                asset_id = existing["asset_id"]
                relative_asset_path = Path(existing["canonical_path"])
                output_path = root / relative_asset_path
                reused_asset_count += 1
            else:
                asset_id = f"asset-{next_number:06d}"
                next_number += 1
                safe_ref = sanitize_token(candidate.primary_external_ref_id)
                asset_dir = candidate.object_dir / "03_visual-assets"
                asset_dir.mkdir(parents=True, exist_ok=True)
                relative_asset_path = (asset_dir / f"001_{asset_id}_{safe_ref}_glyph.jpg").relative_to(root)
                output_path = root / relative_asset_path
                raw_bytes = zip_file.read(find_zip_member(zip_file, candidate.source_image_path))
                with open(filesystem_path(output_path), "wb") as file:
                    file.write(raw_bytes)
                new_asset_rows.append(asset_source_row(candidate, asset_id, relative_asset_path, output_path))
                new_rights_rows.append(rights_row(asset_id))
                new_map_rows.append(asset_map_row(candidate, asset_id, relative_asset_path))
                new_technical_rows.append(technical_profile_row(asset_id, relative_asset_path, output_path))
                new_visual_rows.append(visual_profile_row(asset_id, relative_asset_path, output_path))

            with open(filesystem_path(output_path), "rb") as file:
                output_bytes = file.read()
            metadata_path = output_path.with_suffix(".yaml")
            with open(filesystem_path(metadata_path), "w", encoding="utf-8", newline="\n") as file:
                file.write(metadata_yaml(candidate, asset_id, relative_asset_path, output_bytes, output_path))
            visual_index_path = candidate.object_dir / "02_visual-source-index.csv"
            write_csv(
                visual_index_path,
                build_visual_source_rows(candidate, asset_id, relative_asset_path, visual_index_path),
            )
            asset_name = relative_asset_path.name
            metadata_name = metadata_path.name
            # Existing human-facing files may contain curated provenance and
            # review notes.  Never replace them during a derived-material run;
            # only create a missing file from the current template.
            for filename, content in [
                ("README.md", readme_text(candidate, asset_id, asset_name)),
                (
                    "04_visual-gallery.md",
                    gallery_text(candidate, asset_id, asset_name, metadata_name),
                ),
                ("05_human-review-sheet.md", review_sheet_text(candidate, asset_id)),
            ]:
                output_file = candidate.object_dir / filename
                if not output_file.exists():
                    output_file.write_text(content, encoding="utf-8", newline="\n")
            if candidate.project_id in MATERIAL_VISUAL_OBSERVATIONS:
                ensure_material_observation_link(candidate.object_dir / "README.md")
                with open(
                    filesystem_path(
                        candidate.object_dir / "14_material-visual-observation.md"
                    ),
                    "w",
                    encoding="utf-8",
                    newline="\n",
                ) as file:
                    file.write(
                        material_visual_observation_text(
                            candidate,
                            asset_id,
                            asset_name,
                        )
                    )

    if new_asset_rows:
        upsert_rows(root / ASSET_SOURCE_INDEX, "asset_id", new_asset_rows)
        upsert_rows(root / ASSET_RIGHTS_REVIEW_LOG, "asset_id", new_rights_rows)
        upsert_rows(root / ASSET_ID_SOURCE_MAP, "project_id", new_map_rows)
        upsert_rows(root / ASSET_IMAGE_TECHNICAL_PROFILE, "asset_id", new_technical_rows)
        upsert_rows(root / ASSET_IMAGE_VISUAL_PROFILE, "asset_id", new_visual_rows)

    return {
        "candidate_count": len(candidates),
        "new_asset_count": len(new_asset_rows),
        "reused_asset_count": reused_asset_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    parser.add_argument(
        "--project-id",
        action="append",
        dest="project_ids",
        help="Process only the selected candidate project ID; repeat as needed.",
    )
    args = parser.parse_args()
    result = build_materials(args.root, set(args.project_ids or []))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
