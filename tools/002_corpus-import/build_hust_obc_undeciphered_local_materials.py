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
}


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
