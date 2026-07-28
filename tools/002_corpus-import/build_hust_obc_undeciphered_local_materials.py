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
