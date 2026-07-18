#!/usr/bin/env python3
"""Build co-located human and AI material indexes for character directories."""

from __future__ import annotations

import argparse
import csv
import json
import textwrap
from pathlib import Path


MAX_HUMAN_MARKDOWN_LINE_LENGTH = 80
OBS_CHAR_LOCAL_MATERIAL_LIMIT = 1588
EXTRA_TARGET_PROJECT_IDS = ("obs-unk-005708", "obs-unk-006294")
TARGET_PROJECT_IDS = tuple(
    [f"obs-char-{index:06d}" for index in range(1, OBS_CHAR_LOCAL_MATERIAL_LIMIT + 1)]
    + list(EXTRA_TARGET_PROJECT_IDS)
)

MATERIAL_VISUAL_OBSERVATIONS = {
    "obs-char-000001": (
        "The narrow upright image shows a closed outer contour with diagonal "
        "and angular interior strokes.",
        "本图像呈狭长直立形，外侧有闭合轮廓，内部可见斜向和折角刻划。",
    ),
    "obs-char-000002": (
        "The image shows an open angular form, a long upper stroke, a curved "
        "right-side loop, and two short lower projections.",
        "图像呈开放的折角形，上方有长横向笔画，右侧有弯曲环状部分，下面有两处短伸出。",
    ),
    "obs-char-000003": (
        "The image is a tall curved form with separated short strokes on its "
        "left side; the marks do not form a confirmed label here.",
        "图像为高而弯曲的形体，左侧有分离的短笔画；本记录不把这些痕迹定为文字标签。",
    ),
    "obs-char-000004": (
        "The small, thin image has a central vertical stroke with several "
        "branching diagonal strokes.",
        "图像较小且线条纤细，中部有竖向笔画，并有数条分叉斜向笔画。",
    ),
    "obs-char-000005": (
        "The image shows paired curved outer strokes with shorter marks between "
        "them; the right edge is more strongly curved.",
        "图像可见成对弯曲外笔画，中间夹有短痕；右侧边缘的弯曲更明显。",
    ),
    "obs-char-000006": (
        "The compact image has a block-like upper outline and two rounded lower "
        "marks; the small size limits surface detail.",
        "图像上部呈块状轮廓，下部有两个圆弧状痕迹；图像尺寸限制了表面细节观察。",
    ),
    "obs-char-000007": (
        "The low-contrast gray image shows a compact central form and two small "
        "lower rounded marks; contrast needs human recheck.",
        "灰度较浅的图像呈紧凑中部形体，下方有两个小圆弧痕迹；对比度仍需人工复核。",
    ),
    "obs-char-000008": (
        "The image shows a rectangular enclosure, diagonal interior strokes, and "
        "a small central enclosed mark.",
        "图像呈长方形外框，内部有斜向笔画，中部另有小型闭合痕迹。",
    ),
    "obs-char-000009": (
        "The image contains two rows of small rounded forms, with paired marks "
        "visible in each row.",
        "图像含两行小型圆弧形体，每行都可见成对痕迹。",
    ),
    "obs-char-000010": (
        "The image shows a rectangular outer contour, an angular interior stroke, "
        "and a short downward tail.",
        "图像呈长方形外轮廓，内部有折角笔画，并向下伸出短尾。",
    ),
    "obs-char-000011": (
        "The narrow image has a pointed upper stroke, a horizontal cross stroke, "
        "a small central diamond-like area, and a split lower tail.",
        "狭长图像上方有尖状笔画，中部有横向交叉笔画和小型菱状区域，下方有分叉尾部。",
    ),
    "obs-char-000012": (
        "The image contains a broad left form and a separate right looped form, "
        "with detached marks near their upper and lower ends.",
        "图像含较宽的左侧形体和分离的右侧环状形体，上下端附近还可见分离痕迹。",
    ),
    "obs-char-000013": (
        "The thin upright image has branching strokes at the top, a narrow central "
        "stem, and a trailing diagonal mark below.",
        "纤细直立图像顶部有分叉笔画，中部为窄长主干，下方有拖出的斜向痕迹。",
    ),
    "obs-char-000014": (
        "Two separated forms are visible: the left has an angular crossing shape, "
        "while the right has a rounded loop and pointed top.",
        "图像可见两个分离形体：左侧为折角交叉形，右侧有圆弧环状部分和尖顶。",
    ),
    "obs-char-000015": (
        "The compact image has a horizontal and vertical framework, an open lower "
        "angle, and a separate long stroke at the right.",
        "紧凑图像含横竖框架、下方开放折角，右侧另有一条较长笔画。",
    ),
    "obs-char-000016": (
        "The low-contrast gray image shows two small neighboring forms with rounded "
        "outer edges and central crossing marks.",
        "灰度较浅的图像显示两个相邻小形体，外缘呈圆弧状，中部有交叉痕迹。",
    ),
    "obs-char-000017": (
        "The image has a tall arched outer contour, a curved interior mark, and "
        "two long lower strokes.",
        "图像有高拱形外轮廓，内部有弯曲痕迹，下方有两条较长笔画。",
    ),
    "obs-char-000018": (
        "A second tall arched form is visible, with crossing interior strokes and "
        "long lines descending from the lower edge.",
        "图像呈另一种高拱形体，内部笔画交叉，底部向下延伸出较长线条。",
    ),
    "obs-char-000019": (
        "The small gray image shows a rounded upper mark, a short horizontal stroke, "
        "and two diverging lower strokes; contrast needs recheck.",
        "小型灰度图像上部有圆弧痕迹，中部有短横画，下方有两条分开的笔画；对比度仍需复核。",
    ),
    "obs-char-000020": (
        "The dark image shows a rectangular lower frame containing two parallel "
        "upright strokes and a narrow base.",
        "深色图像呈长方形下框，内部有两条平行竖向笔画，并有窄小底部。",
    ),
    "obs-char-000021": (
        "The small image shows a curved upper stroke, a narrow central stem, "
        "and a rounded lower enclosure with an open side.",
        "小型图像上方有弯曲笔画，中部为窄竖主干，下方有一侧开放的圆弧形框。",
    ),
    "obs-char-000022": (
        "The compact image has two upright side strokes, a short upper cross "
        "stroke, and a rounded lower bowl crossed by a horizontal mark.",
        "紧凑图像含两条竖向侧笔画、上方短横画，以及被横痕穿过的下部圆弧框。",
    ),
    "obs-char-000023": (
        "The dark form combines a pointed upper outline, several horizontal "
        "cross strokes, and multiple short descending strokes.",
        "深色形体上方呈尖顶轮廓，中部有数条横向交叉笔画，下方有多条短向下笔画。",
    ),
    "obs-char-000024": (
        "The tall image has a large arched outer contour, a central branching "
        "mark, and a forked lower extension.",
        "高形图像有大型拱形外轮廓，中部有分叉痕迹，下方延伸出分叉尾部。",
    ),
    "obs-char-000025": (
        "The thin upright image has a central vertical stroke, two leftward "
        "branching marks, and a long diagonal stroke on the right.",
        "纤细直立图像有中央竖画、向左分出的两处痕迹，右侧有长斜向笔画。",
    ),
    "obs-char-000026": (
        "The low-contrast image shows a branching central form with short "
        "diagonal strokes extending to both sides.",
        "灰度较浅的图像呈分叉中部形体，并有短斜向笔画向两侧伸出。",
    ),
    "obs-char-000027": (
        "The small dark image shows paired upright strokes, several short "
        "interior marks, and a narrow rectangular lower base.",
        "小型深色图像可见成对竖向笔画、数处内部短痕和窄长方形底部。",
    ),
    "obs-char-000028": (
        "The image contains a broad lower enclosure, an upper looped mark, "
        "and two detached strokes to the right.",
        "图像含宽大的下部框形、上方环状痕迹，右侧另有两条分离笔画。",
    ),
    "obs-char-000029": (
        "The thin gray image has two tall wavy strokes crossed by short "
        "horizontal marks and a straight lower tail.",
        "纤细灰度图像有两条高而弯曲的笔画，被短横痕穿过，并向下延出直尾。",
    ),
    "obs-char-000030": (
        "The narrow image shows a slightly curved upright stroke with two "
        "short diagonal branches on its left side.",
        "狭长图像呈略弯直立笔画，左侧分出两条短斜向笔画。",
    ),
    "obs-char-000031": (
        "The tall narrow image has a branching upper tip, a central descending "
        "stroke, and crossed short marks near the lower end.",
        "高而狭长图像顶部有分叉尖端，中部有向下主笔画，下端附近有交叉短痕。",
    ),
    "obs-char-000032": (
        "The small gray image shows a short horizontal mark, a central upright "
        "stroke, and an angular lower hook.",
        "小型灰度图像有短横痕、中央竖向笔画和下部折角钩状痕迹。",
    ),
    "obs-char-000033": (
        "Two neighboring forms are visible, each with a central oval-like mark "
        "and short strokes extending to both sides.",
        "图像可见两个相邻形体，各自有中央椭圆状痕迹，并向两侧伸出短笔画。",
    ),
    "obs-char-000034": (
        "The large elongated outline contains an enclosed central mark, upper "
        "diverging strokes, and a long lower extension.",
        "大型长形外轮廓内部有闭合中部痕迹、上方分开的笔画和长向下延伸。",
    ),
    "obs-char-000035": (
        "The compact image contains a small branching form beside a rectangular "
        "framework with an upper diagonal stroke.",
        "紧凑图像含一处小型分叉形体，旁边是带上方斜笔画的长方形框架。",
    ),
    "obs-char-000036": (
        "The small thin image has a rounded upper mark, crossing interior strokes, "
        "and a curved lower tail.",
        "小型纤细图像上方有圆弧痕迹，内部笔画交叉，下方有弯曲尾部。",
    ),
    "obs-char-000037": (
        "Two stacked forms are visible, each with a horizontal upper stroke, a "
        "right-side hooked descent, and a slanted lower edge.",
        "图像可见上下叠置的两个形体，各有上方横画、右侧下钩和倾斜下缘。",
    ),
    "obs-char-000038": (
        "The thin image has short parallel marks at the upper left, a central "
        "upright stroke, and a hooked lower extension.",
        "纤细图像左上有短平行痕迹，中部有竖向主笔画，下方延出钩状痕迹。",
    ),
    "obs-char-000039": (
        "The dark form combines a small rounded upper mark, a central upright, "
        "and two adjoining rectangular lower enclosures.",
        "深色形体含小型圆弧上部痕迹、中央竖画和两个相连的下部长方形框。",
    ),
    "obs-char-000040": (
        "The small image shows an upper open angular cluster and a separate lower "
        "cluster of crossing strokes.",
        "小型图像上方有开放折角痕迹，下方另有交叉笔画组成的分离形体。",
    ),
    "obs-char-000041": (
        "The large image has two outer curving strokes, branching marks between "
        "them, and two small enclosed oval-like marks.",
        "大型图像有两条弯曲外笔画，中间有分叉痕迹，并可见两个小型闭合椭圆状痕迹。",
    ),
    "obs-char-000042": (
        "The small gray image shows two neighboring upright forms with short "
        "angular and vertical marks.",
        "小型灰度图像可见两个相邻直立形体，含短折角和竖向痕迹。",
    ),
    "obs-char-000043": (
        "The compact image has an angular upper outline, a central crossing "
        "stroke, and a small hooked lower mark.",
        "紧凑图像上方呈折角轮廓，中部有交叉笔画，下方有小型钩状痕迹。",
    ),
    "obs-char-000044": (
        "The image shows a branching central stroke with short side marks and "
        "a curved lower extension.",
        "图像呈分叉中央笔画，两侧有短痕，下方有弯曲延伸。",
    ),
    "obs-char-000045": (
        "Two separated forms are visible: a small divided square-like form on "
        "the left and a thin upright form with an upper loop on the right.",
        "图像可见两个分离形体：左侧为分格小方形，右侧为带上部环状痕迹的纤细直立形。",
    ),
    "obs-char-000046": (
        "The tiny gray image has two neighboring angular upper marks, a short "
        "connecting stroke, and two thin lower strokes.",
        "微小灰度图像上方有两个相邻折角痕迹，中间有短连接笔画，下方有两条细笔画。",
    ),
    "obs-char-000047": (
        "The image has a long upper horizontal stroke, a left descending edge, "
        "and a central branching form above a curved lower mark.",
        "图像有长上横画、左侧向下边缘，中部为分叉形体，下方有弯曲痕迹。",
    ),
    "obs-char-000048": (
        "Two dark forms are stacked vertically: the upper has a long top bar and "
        "curved side strokes, while the lower forms a rounded bowl.",
        "图像上下叠置两个深色形体：上方有长横画和弯曲侧笔画，下方呈圆弧框。",
    ),
    "obs-char-000049": (
        "Two adjacent forms are visible, with branching strokes on the left and "
        "a looped, crossing form with a lower diamond-like mark on the right.",
        "图像可见两个相邻形体，左侧有分叉笔画，右侧有环状交叉形和下部菱状痕迹。",
    ),
    "obs-char-000050": (
        "The tiny gray image has a short top bar, a central upright stroke, and "
        "a small angular projection to the side.",
        "微小灰度图像有短上横画、中央竖向笔画和侧面的折角伸出。",
    ),
    "obs-char-000051": (
        "The small gray image has three short upper bars, a compact middle frame, "
        "and a pointed lower mark.",
        "小型灰度图像上方有三条短横画，中部为紧凑框形，下方有尖状痕迹。",
    ),
    "obs-char-000052": (
        "The narrow image shows a curved upright stroke, a branching upper mark, "
        "and a small enclosed oval near the lower right.",
        "狭长图像有弯曲直立笔画、上方分叉痕迹，右下附近有小型闭合椭圆。",
    ),
    "obs-char-000053": (
        "The large dark form has an upper loop, a central crossing, several long "
        "descending strokes, and a lower right enclosure.",
        "大型深色形体上方有环状痕迹，中部交叉，下方有多条长笔画，右下有闭合框。",
    ),
    "obs-char-000054": (
        "The image combines a broad crossed upper framework with a separate lower "
        "arched form and a central descending stroke.",
        "图像上方为宽大的交叉框架，下方有分离拱形体，中部有向下主笔画。",
    ),
    "obs-char-000055": (
        "The tiny gray image shows an angular upper cluster and a separate small "
        "rounded mark below it.",
        "微小灰度图像上方有折角形痕迹，下方另有一个小型圆弧痕迹。",
    ),
    "obs-char-000056": (
        "Two neighboring dark forms are visible, each with an upright stroke, a "
        "curved lower turn, and a short upper projection.",
        "图像可见两个相邻深色形体，各有直立笔画、下部弯转和短上部伸出。",
    ),
    "obs-char-000057": (
        "The large enclosed form has a broad upper frame, side loop-like marks, a "
        "central horizontal stroke, and a rounded lower bowl.",
        "大型闭合形体有宽上框、两侧环状痕迹、中央横画和下部圆弧框。",
    ),
    "obs-char-000058": (
        "The image shows a tall rectangular enclosure with angular interior marks, "
        "a horizontal upper stroke, and a short lower bar.",
        "图像呈高长方形外框，内部有折角痕迹，上方有横画，下方有短横痕。",
    ),
    "obs-char-000059": (
        "The small gray image has a curved angular upper cluster and a detached "
        "forked mark below; contrast needs human recheck.",
        "小型灰度图像上方有弯曲折角痕迹，下方有分离的分叉痕；对比度需人工复核。",
    ),
    "obs-char-000060": (
        "The tiny gray image shows a narrow vertical chain of enclosed diamond-like "
        "marks with short cross strokes; detail needs recheck.",
        "微小灰度图像呈窄长竖向链状形体，含闭合菱状痕迹和短交叉笔画；细节需复核。",
    ),
    "obs-char-000061": (
        "The small image shows a tall angular form with a lower rectangular frame "
        "and a separate curved mark on the right.",
        "小型图像呈高而折角的形体，下方有长方形框，右侧另有弯曲痕迹。",
    ),
    "obs-char-000062": (
        "The thin image has a central upright stroke, a pointed upper loop-like "
        "mark, and a hooked lower extension.",
        "纤细图像有中央竖画、上方尖状环形痕迹和下方钩状延伸。",
    ),
    "obs-char-000063": (
        "The tall narrow image contains a vertical lattice of crossed diamond-like "
        "marks with short side strokes.",
        "高而狭长图像含竖向交叉格状痕迹，并有短侧向笔画。",
    ),
    "obs-char-000064": (
        "The large dark image combines many horizontal and branching strokes with "
        "a long lower-left stem and a curved lower-right descent.",
        "大型深色图像含多条横向和分叉笔画，左下有长主干，右下有弯曲下行笔画。",
    ),
    "obs-char-000065": (
        "The small gray image shows a thin upright cluster with an enclosed angular "
        "center and curved lower marks.",
        "小型灰度图像呈纤细直立形体，中部有闭合折角痕迹，下方有弯曲笔画。",
    ),
    "obs-char-000066": (
        "Two separated forms are visible: the left has stacked crossing marks and "
        "a lower fork, while the right is a curved bracket-like form.",
        "图像可见两个分离形体：左侧有叠置交叉痕和下部分叉，右侧呈弯曲括状形体。",
    ),
    "obs-char-000067": (
        "The large image contains a tall branching form on the left and a dense "
        "angular form on the right, with several detached lower strokes.",
        "大型图像左侧为高而分叉的形体，右侧为密集折角形体，下方有数条分离笔画。",
    ),
    "obs-char-000068": (
        "The small gray image has a tall rectangular outer frame, curved interior "
        "marks, and three short lower projections.",
        "小型灰度图像有高长方形外框、内部弯曲痕迹和三条短下伸笔画。",
    ),
    "obs-char-000069": (
        "The tiny gray image shows a curved left cluster with short inner marks and "
        "a separate angular mark on the right.",
        "微小灰度图像左侧为弯曲形体并含短内部痕迹，右侧另有折角痕迹。",
    ),
    "obs-char-000070": (
        "The tiny gray image contains a curved left form with a short top bar and a "
        "separate upright hooked stroke on the right.",
        "微小灰度图像左侧为带短上横画的弯曲形体，右侧另有直立钩状笔画。",
    ),
    "obs-char-000071": (
        "The tiny image contains one short, thick horizontal stroke with slightly "
        "uneven edges.",
        "微小图像只有一条短而粗的横向笔画，边缘略不均匀。",
    ),
    "obs-char-000072": (
        "The small image shows a rounded rectangular enclosure with a continuous "
        "dark outer stroke.",
        "小型图像呈圆角长方形闭合框，外缘为连续深色笔画。",
    ),
    "obs-char-000073": (
        "The narrow image has a slightly curved upper stroke and a thin descending "
        "line attached near its middle.",
        "狭长图像上方有略弯横画，中部附近连接一条细长下行线。",
    ),
    "obs-char-000074": (
        "The small image consists of a horizontal stroke crossed by a longer "
        "vertical stroke.",
        "小型图像由一条横画和一条较长竖画交叉组成。",
    ),
    "obs-char-000075": (
        "The thin image shows a short upper bar, a diagonal descending stroke, and "
        "a second short lower branch.",
        "纤细图像上方有短横画，下方有斜向下行笔画和第二条短分支。",
    ),
    "obs-char-000076": (
        "The image contains three separated, roughly parallel horizontal strokes "
        "with uneven thickness.",
        "图像含三条分离且大致平行的横向笔画，粗细并不均匀。",
    ),
    "obs-char-000077": (
        "The image shows several short parallel horizontal strokes grouped closely "
        "together.",
        "图像可见数条彼此接近的短平行横向笔画。",
    ),
    "obs-char-000078": (
        "The small image has two broad curved horizontal strokes, one above the "
        "other, with an open gap between them.",
        "小型图像有上下两条宽而弯曲的横向笔画，中间留有开放间隔。",
    ),
    "obs-char-000079": (
        "The narrow image shows a central descending stem that branches into two "
        "long curved side strokes.",
        "狭长图像有中央下行主干，并向两侧分出两条长弯曲笔画。",
    ),
    "obs-char-000080": (
        "The large image has a thick upper horizontal cap, a long irregular "
        "descending stroke, and a diagonal branch on the lower left.",
        "大型图像上方有粗横向顶笔，中部有长而不规则的下行笔画，左下有斜向分支。",
    ),
    "obs-char-000081": (
        "The narrow image has a rounded upper contour, a short central "
        "horizontal stroke, and several angular marks descending below it.",
        "狭长图像上方有弧形轮廓，中部有短横笔，下面有数道向下的折角刻划。",
    ),
    "obs-char-000082": (
        "The image shows an open angular frame with a tall left stroke, a "
        "long lower baseline, and a diagonal stroke descending from above.",
        "图像呈开放的折角框形，左侧有长直笔，下方有长横基线，并有一道自上向下的斜笔。",
    ),
    "obs-char-000083": (
        "The compact image has a rounded outer enclosure, a peaked upper "
        "interior junction, and a smaller rectangular enclosure inside.",
        "小型图像有弧曲外框，上部内部笔画在中央形成尖角，内部另有较小的方框。",
    ),
    "obs-char-000084": (
        "The image is roughly symmetrical, with several short upper strokes "
        "and a broad curved lower enclosure that narrows toward the bottom.",
        "图像大致左右对称，上方有数道短笔，下方有宽弧形围合，向底部逐渐收窄。",
    ),
    "obs-char-000085": (
        "The isolated narrow image consists mainly of one long curving stroke "
        "that turns inward near the upper part and ends in a lower hook.",
        "孤立的狭长图像主要由一条长弯曲笔画构成，上部向内回转，底部收成钩状。",
    ),
    "obs-char-000086": (
        "The image has a tall central stem, a small rectangular loop on the "
        "left, and short branching strokes extending toward the right.",
        "图像有一条高直主干，左侧有小方环，并向右伸出数道短分支笔画。",
    ),
    "obs-char-000087": (
        "The narrow image has a curved upright left stroke, two short rightward "
        "branches, and a separate diagonal stroke at the lower left.",
        "狭长图像左侧有弧曲直立笔，向右分出两道短笔，左下另有一道斜笔。",
    ),
    "obs-char-000088": (
        "The enlarged image shows a central descending stroke crossed by broad "
        "diagonal strokes, with a separate curved stroke on the right.",
        "放大的图像中部有下行主笔，被数道宽斜笔交叉，右侧另有弧曲笔画。",
    ),
    "obs-char-000089": (
        "The compact image has a central vertical stroke, short horizontal "
        "strokes at several levels, and small side projections.",
        "小型图像有中央竖笔，在不同高度分布短横笔，并有小幅向两侧伸出。",
    ),
    "obs-char-000090": (
        "The image has a broad open rectangular outline with two parallel "
        "interior horizontal strokes and short outer end strokes.",
        "图像呈宽阔的开放方框轮廓，内部有两道平行横笔，外侧端部有短出笔。",
    ),
    "obs-char-000091": (
        "The small image has one short horizontal stroke at the top and a "
        "single long vertical stroke descending from its center.",
        "小型图像顶部有一道短横笔，并从中央向下延伸一条长直笔。",
    ),
    "obs-char-000092": (
        "The image contains two rounded upper loops joined by crossing strokes "
        "and two curved lower hooks on opposite sides.",
        "图像上方有两个弧形环，彼此由交叉笔画连接，下方两侧各有弯曲钩状笔。",
    ),
    "obs-char-000093": (
        "The isolated image is a thick curved stroke that bends inward from the "
        "upper left and tapers toward the lower end.",
        "孤立图像是一道粗弯曲笔画，自左上向内弯转，并向下端逐渐变细。",
    ),
    "obs-char-000094": (
        "The image has a tall central stroke, a short upper horizontal crossing, "
        "and a compact angular branch on the lower right.",
        "图像有高直主笔，上部有短横交叉笔，下右方有紧凑的折角分支。",
    ),
    "obs-char-000095": (
        "The image shows a tall left stroke, a diagonal central branch, a right "
        "side stroke, and a short lower baseline.",
        "图像左侧有高直笔，中部有斜向分支，右侧有短笔，下方有短横基线。",
    ),
    "obs-char-000096": (
        "The narrow image has several short upper marks, a descending central "
        "stroke, and two angular lower strokes opening to the sides.",
        "狭长图像上方有数道短笔，中部有下行主笔，下方有两道向两侧张开的折角笔。",
    ),
    "obs-char-000097": (
        "The small image has three separated upper marks, a long middle stroke, "
        "and a thin descending stroke below the center.",
        "小型图像上方有三道分离短笔，中部有长横笔，中央下方有细长下行笔。",
    ),
    "obs-char-000098": (
        "The image is vertically organized, with a pointed upper junction, "
        "short side branches, and a narrow central descending stem.",
        "图像按纵向组织，上部中央形成尖点，两侧有短分支，中部有狭长下行主干。",
    ),
    "obs-char-000099": (
        "The isolated narrow image consists of one long irregular curved stroke "
        "with a slight inward turn near the upper section.",
        "孤立的狭长图像由一条长而不规则的弯曲笔画构成，上部略向内回转。",
    ),
    "obs-char-000100": (
        "The image has a broad angular left branch, a central crossing stroke, "
        "and a rounded hook-like curve extending to the right.",
        "图像左侧有宽大的折角分支，中部有交叉笔，右侧伸出弧形钩状笔画。",
    ),
    "obs-char-000101": (
        "The image has a tall central axis, rounded enclosed marks on both "
        "sides, and a short hooked stroke near the upper right.",
        "图像有高直中央主轴，两侧可见弧形围合笔画，右上方另有短钩状笔。",
    ),
    "obs-char-000102": (
        "The enlarged image is arranged on a diagonal, with three rounded "
        "enclosures linked in sequence and a long lower descending stroke.",
        "放大图像沿斜向排列，有三个依次相连的弧形围合，并有长下行笔画。",
    ),
    "obs-char-000103": (
        "The small image has a thin irregular upright stroke at the right and "
        "a long low stroke extending leftward from its base.",
        "小型图像右侧有细而不规则的直立笔，底部有一道向左伸出的长低位笔画。",
    ),
    "obs-char-000104": (
        "The image consists of two thick, nearly parallel horizontal strokes "
        "with a narrow open gap between them.",
        "图像由两道粗而近于平行的横笔构成，中间留有狭窄开放间隔。",
    ),
    "obs-char-000105": (
        "The compact image has a broad horizontal top stroke and a long narrow "
        "vertical stroke descending from near its center.",
        "小型图像上方有宽横顶笔，并从接近中央处向下伸出长而窄的直笔。",
    ),
    "obs-char-000106": (
        "The image has two short upper horizontal strokes, a curved lower loop, "
        "and a separate hooked stroke on the lower left.",
        "图像上方有两道短横笔，下方有弧形环状笔，左下另有分离的钩状笔。",
    ),
    "obs-char-000107": (
        "The narrow image is formed by two long diagonal strokes meeting near "
        "the top and opening apart toward the lower edge.",
        "狭长图像由两道长斜笔构成，两笔在上方附近相接，向下端分开。",
    ),
    "obs-char-000108": (
        "The compact image has a central vertical stroke crossed by a horizontal "
        "stroke, with short angled side projections.",
        "小型图像有中央竖笔与横笔交叉，两侧带有短而倾斜的伸出笔画。",
    ),
    "obs-char-000109": (
        "The image has two short upper horizontal strokes above an open angular "
        "enclosure with a small inner corner.",
        "图像上方有两道短横笔，下方是开放折角围合，内部可见小型转角。",
    ),
    "obs-char-000110": (
        "The rounded image has a central vertical-and-horizontal junction and "
        "four short curved projections extending around it.",
        "弧形图像中部有横竖交接点，周围向四方伸出四道短弯曲笔画。",
    ),
    "obs-char-000111": (
        "The narrow image has a small angular upper mark, a long descending "
        "central stroke, and a short horizontal cross stroke near the lower end.",
        "狭长图像上方有小型折角痕迹，中部向下贯穿一条长笔画，靠近下端有短横笔。",
    ),
    "obs-char-000112": (
        "The image shows two upright side strokes with an open curved diagonal "
        "connection running from the upper left toward the lower right.",
        "图像可见两道直立侧笔画，并有开放的弧斜连接笔画从左上向右下延伸。",
    ),
    "obs-char-000113": (
        "The compact image has a pointed upper junction, sloping outer strokes, "
        "and an enclosed inner arch above two narrow lower extensions.",
        "紧凑图像上方有尖状交接点，两侧向外斜伸，内部有闭合弧形，下面延出两道窄笔。",
    ),
    "obs-char-000114": (
        "The light image has a small diamond-like central enclosure, short upper "
        "strokes, and two curved lower extensions that remain open at the sides.",
        "浅色图像中部有小型菱状围合，上方有短笔，下方伸出两道侧面开放的弯曲笔画。",
    ),
    "obs-char-000115": (
        "The tall image has a broad upper horizontal stroke, a descending central "
        "stroke, and a long curved stroke running down the right side.",
        "高形图像上方有宽横笔，中部向下有主笔，右侧沿下方延伸一条长弯曲笔。",
    ),
    "obs-char-000116": (
        "The image has a branching upper junction, a long central descending "
        "stroke, and several short detached curved marks on both sides.",
        "图像上方有分叉交接点，中部向下有长主笔，两侧另有数道分离的短弯曲痕迹。",
    ),
    "obs-char-000117": (
        "The image combines a small triangular upper form with two inner upright "
        "strokes and a broad open lower frame beneath a horizontal bar.",
        "图像由小型三角上部、内部两道竖笔和横笔下方宽大的开放下框组成。",
    ),
    "obs-char-000118": (
        "The image has a pointed triangular upper form, a horizontal cross stroke, "
        "two short uprights, and a rounded closed lower bowl.",
        "图像上部呈尖三角形，有横向交叉笔和两道短竖笔，下部为圆弧闭合框。",
    ),
    "obs-char-000119": (
        "The tall dark image has a broad top bar, diagonal strokes converging at "
        "the center, a long lower vertical, and crossing lower projections.",
        "高而深色的图像上方有宽横笔，斜向笔画在中部汇合，下方有长竖笔和交叉伸出笔。",
    ),
    "obs-char-000120": (
        "The small image has a pointed upper enclosure above a rectangular lower "
        "form, with a narrow central descending stroke and a split lower mark.",
        "小型图像上方有尖顶围合，下方为长方形形体，中部向下有窄笔，底部有分叉痕迹。",
    ),
    "obs-char-000121": (
        "The very narrow image forms a pointed upper tip with two curved outer "
        "strokes narrowing into a long tapering lower line.",
        "极狭长图像上端呈尖点，两侧弯曲外笔向下收拢为长而渐细的下行笔画。",
    ),
    "obs-char-000122": (
        "The low-resolution gray image shows a short angular upper block and a "
        "thicker curved stroke descending toward the lower right.",
        "低分辨率灰度图像上方有短折角块状痕迹，并有较粗弯曲笔向右下延伸。",
    ),
    "obs-char-000123": (
        "The broad image has two sloping strokes meeting at a high point, with a "
        "short horizontal stroke detached inside the lower opening.",
        "宽大图像由两道斜笔在高处相接构成，内部下方开口处有分离的短横笔。",
    ),
    "obs-char-000124": (
        "The image has a pointed central upper mark, a descending central stroke, "
        "and several short detached marks arranged on both sides.",
        "图像上方有尖状中央痕迹，中部向下有主笔，两侧排列着数道分离短痕。",
    ),
    "obs-char-000125": (
        "Two separated angular arch-like forms are visible, one broad above and a "
        "smaller one below, both open along their lower edges.",
        "图像可见上下分离的两处折角拱形痕迹，上方较宽，下方较小，底部都呈开放状态。",
    ),
    "obs-char-000126": (
        "The image contains four long upright curved strokes with pointed upper "
        "tips and uneven tapering lower ends.",
        "图像含四道长而直立的弯曲笔画，上端有尖点，下端收笔长短不齐。",
    ),
    "obs-char-000127": (
        "Two separated forms are visible: a small open triangular form above and a "
        "narrow angular hooked form below.",
        "图像可见上下分离的两种形体：上方为小型开放三角形，下方为窄长折角钩状形。",
    ),
    "obs-char-000128": (
        "The low-resolution gray image has a compact crossing mark on the left and "
        "a curved descending stroke on the right.",
        "低分辨率灰度图像左侧有紧凑交叉痕迹，右侧有弯曲向下的笔画。",
    ),
    "obs-char-000129": (
        "The image shows a tall straight form with a top cross stroke on the left, "
        "beside a separate curved descending form on the right.",
        "图像左侧为带顶部横笔的高直形体，右侧另有一处分离的弯曲下行形体。",
    ),
    "obs-char-000130": (
        "The narrow image has a long curved central stroke, a small upper branch, "
        "and a short horizontal crossing mark near the lower end.",
        "狭长图像有长弯曲主笔，上方有小分叉，下端附近有短横交叉痕迹。",
    ),
    "obs-char-000131": (
        "The narrow image has a small angular upper junction, a long descending "
        "stroke on the right, and a broken curved stroke along the left edge.",
        "狭长图像上方有小型折角交接处，右侧有长下行笔，左缘有断续弯曲笔。",
    ),
    "obs-char-000132": (
        "The dark image has a thick central descending stroke with several short "
        "curved branches extending unevenly to both sides.",
        "深色图像中部有粗长下行笔，两侧向外伸出数道长短不齐的弯曲分笔。",
    ),
    "obs-char-000133": (
        "The image has a tall central vertical stroke, a short horizontal cross "
        "near the top, and separate curved strokes on both sides.",
        "图像中部有高直主笔，上方附近有短横交叉笔，两侧另有分离的弯曲笔。",
    ),
    "obs-char-000134": (
        "Several narrow strokes meet near the center, with an upper fork, a long "
        "leftward curve, and short lower projections.",
        "数道窄笔在中部附近汇合，上方有分叉，左侧有长弯曲笔，下方有短伸出笔。",
    ),
    "obs-char-000135": (
        "The large image has a long upper stem that opens into a rounded right "
        "loop, while multiple curved strokes descend on the left and below.",
        "大幅图像上方有长直笔，向下分开形成右侧圆弧环状形，左侧和下方有多道弯曲下行笔。",
    ),
    "obs-char-000136": (
        "The image combines a small angular cluster at the top with a narrow "
        "curved stroke extending downward from its right side.",
        "图像上方有小型折角笔群，右侧连接一条向下延伸的窄弯曲笔。",
    ),
    "obs-char-000137": (
        "The image shows an open triangular upper frame, a crossbar inside it, "
        "and a narrow pointed stroke descending from the center.",
        "图像上部为开放三角形框，内部有横笔，中央向下延伸一条窄而尖的笔画。",
    ),
    "obs-char-000138": (
        "The tall image has a central descending stroke with two long curved side "
        "strokes and a short diagonal projection near the middle.",
        "高形图像中部有下行主笔，两侧有两道长弯曲笔，中部附近另有短斜向伸笔。",
    ),
    "obs-char-000139": (
        "The image has a central crossing point with four uneven strokes spreading "
        "upward and downward, including a curved lower-left stroke.",
        "图像中部有交叉点，四道长短不齐的笔画向上下展开，其中左下方有弯曲笔。",
    ),
    "obs-char-000140": (
        "The low-resolution gray image has a small horizontal upper enclosure and "
        "a thin central stroke descending below it with a short side mark.",
        "低分辨率灰度图像上方有小型横向围合痕迹，下方有细直主笔，并带短侧向痕迹。",
    ),
}
IMAGE_REFERENCE_RESULTS = (
    "corpus/009_statistics-and-derived-features/"
    "068_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-extraction-results.csv"
)
VISUAL_INDEX_FIELDS = [
    "visual_source_index_id",
    "project_id",
    "primary_external_ref_id",
    "source_id",
    "source_package_id",
    "download_id",
    "visual_material_status",
    "committed_image_path",
    "source_image_reference_path",
    "source_image_sequence_in_candidate",
    "source_image_count_expected",
    "registered_storage_hint",
    "resolved_local_archive_path",
    "local_archive_status",
    "rights_status",
    "risk_note",
    "review_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def project_id_from_object_dir(path: Path) -> str:
    for part in path.name.split("_"):
        if part.startswith("obs-char-") or part.startswith("obs-unk-"):
            return part
    raise ValueError(f"Cannot find project ID in object directory name: {path}")


def discover_target_dirs(root: Path) -> dict[str, dict[str, Path | str]]:
    target_ids = set(TARGET_PROJECT_IDS)
    object_root = root / "corpus/001_oracle-characters"
    targets: dict[str, dict[str, Path | str]] = {}
    packet_paths = [
        *object_root.glob("*/*/01_candidate-character-packet.json"),
        *object_root.glob("*/*/01_undeciphered-candidate-packet.json"),
    ]
    for packet_path in sorted(packet_paths):
        object_dir = packet_path.parent
        project_id = project_id_from_object_dir(object_dir)
        if project_id in target_ids:
            targets[project_id] = {
                "object_dir": object_dir,
                "packet": packet_path.name,
            }
    missing_ids = sorted(target_ids - set(targets))
    if missing_ids:
        raise FileNotFoundError(f"Missing target character packet directories: {', '.join(missing_ids)}")
    return {project_id: targets[project_id] for project_id in TARGET_PROJECT_IDS}


def read_image_reference_rows(root: Path) -> dict[str, list[dict[str, str]]]:
    path = root / IMAGE_REFERENCE_RESULTS
    rows_by_candidate: dict[str, list[dict[str, str]]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            rows_by_candidate.setdefault(row["unknown_candidate_id"], []).append(row)
    return rows_by_candidate


def read_existing_visual_rows(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return {
            row["source_image_reference_path"]: row
            for row in csv.DictReader(file)
            if row.get("source_image_reference_path")
        }


def archive_status(row: dict[str, str]) -> str:
    resolved = row.get("resolved_local_archive_path", "")
    if resolved and Path(resolved).exists():
        return "registered_external_archive_available_outside_git"
    if resolved:
        return "registered_external_archive_missing_on_current_disk"
    return "not_applicable_no_archive_path"


def build_visual_rows(
    project_id: str,
    packet: dict,
    image_reference_rows: list[dict[str, str]],
    existing_visual_rows: dict[str, dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    existing_visual_rows = existing_visual_rows or {}
    if image_reference_rows:
        rows = []
        for index, source_row in enumerate(image_reference_rows, start=1):
            existing_row = existing_visual_rows.get(source_row["source_image_path"], {})
            committed_image_path = existing_row.get("committed_image_path", "")
            visual_material_status = (
                "committed_review_image_derivative"
                if committed_image_path
                else "source_image_reference_only_no_committed_glyph_image"
            )
            rows.append(
                {
                    "visual_source_index_id": f"{project_id}-visual-source-{index:03d}",
                    "project_id": project_id,
                    "primary_external_ref_id": source_row["primary_external_ref_id"],
                    "source_id": source_row["source_id"],
                    "source_package_id": source_row["source_package_id"],
                    "download_id": source_row["download_id"],
                    "visual_material_status": visual_material_status,
                    "committed_image_path": committed_image_path,
                    "source_image_reference_path": source_row["source_image_path"],
                    "source_image_sequence_in_candidate": source_row["source_image_sequence_in_candidate"],
                    "source_image_count_expected": source_row["source_image_count_expected"],
                    "registered_storage_hint": source_row["registered_storage_hint"],
                    "resolved_local_archive_path": source_row["resolved_local_archive_path"],
                    "local_archive_status": existing_row.get("local_archive_status") or archive_status(source_row),
                    "rights_status": source_row["source_rights_status"],
                    "risk_note": source_row["risk_note"],
                    "review_status": "needs_human_visual_review",
                    "research_boundary": "co_located_visual_source_index_not_scholarship",
                    "caution": (
                        "Source image path metadata only; not a committed image, not an "
                        "accepted glyph identity, not an accepted reading, and not a "
                        "decipherment conclusion."
                    ),
                    "updated_at": "2026-06-20",
                }
            )
        return rows

    if existing_visual_rows:
        return sorted(existing_visual_rows.values(), key=lambda row: row.get("visual_source_index_id", ""))

    return [
        {
            "visual_source_index_id": f"{project_id}-visual-source-001",
            "project_id": project_id,
            "primary_external_ref_id": packet.get("primary_external_ref_id", ""),
            "source_id": packet.get("source_id", ""),
            "source_package_id": packet.get("source_package_id", ""),
            "download_id": ";".join(packet.get("evidence_download_ids", [])),
            "visual_material_status": "no_source_image_reference_extracted_yet",
            "committed_image_path": "",
            "source_image_reference_path": "",
            "source_image_sequence_in_candidate": "",
            "source_image_count_expected": "",
            "registered_storage_hint": "",
            "resolved_local_archive_path": "",
            "local_archive_status": "not_applicable_no_source_image_reference",
            "rights_status": packet.get("rights_status", ""),
            "risk_note": packet.get("risk_note", ""),
            "review_status": "needs_human_visual_review",
            "research_boundary": "co_located_visual_source_index_not_scholarship",
            "caution": (
                "This object has a local candidate packet but no extracted source-image "
                "reference in the current prepared records; not an accepted reading and "
                "not a decipherment conclusion."
            ),
            "updated_at": "2026-06-20",
        }
    ]


def relative_committed_images(object_dir: Path, committed_images: list[str]) -> str:
    if not committed_images:
        return "none in this directory yet"
    values = []
    for path in committed_images:
        asset_path = Path(path)
        values.append(
            asset_path.relative_to(object_dir).as_posix()
            if asset_path.is_relative_to(object_dir)
            else path
        )
    return "; ".join(values)


def wrap_markdown_text(text: str) -> list[str]:
    return textwrap.wrap(
        text,
        width=MAX_HUMAN_MARKDOWN_LINE_LENGTH,
        break_long_words=True,
        break_on_hyphens=False,
    ) or [""]


def append_wrapped_paragraph(lines: list[str], text: str) -> None:
    lines.extend(wrap_markdown_text(text))


def append_wrapped_bullet(lines: list[str], label: str, value: object) -> None:
    lines.extend(
        textwrap.wrap(
            f"- {label}: {value}",
            width=MAX_HUMAN_MARKDOWN_LINE_LENGTH,
            subsequent_indent="  ",
            break_long_words=True,
            break_on_hyphens=False,
        )
    )


def append_wrapped_plain_bullet(lines: list[str], text: str) -> None:
    lines.extend(
        textwrap.wrap(
            f"- {text}",
            width=MAX_HUMAN_MARKDOWN_LINE_LENGTH,
            subsequent_indent="  ",
            break_long_words=True,
            break_on_hyphens=False,
        )
    )


def build_readme_text(
    project_id: str,
    object_dir: Path,
    packet_name: str,
    packet: dict,
    visual_rows: list[dict[str, str]],
    material_observation_available: bool = False,
) -> str:
    external_id = packet.get("primary_external_ref_id", "")
    source_id = packet.get("source_id", "")
    status_counts = sorted({row["visual_material_status"] for row in visual_rows})
    image_ref_count = sum(1 for row in visual_rows if row["source_image_reference_path"])
    committed_images = [row["committed_image_path"] for row in visual_rows if row.get("committed_image_path")]
    packet_record_type = packet.get("record_type", "")
    caution = packet.get("caution", "")
    local_path = object_dir.as_posix()
    status_text = ", ".join(status_counts)
    committed_image_text = relative_committed_images(object_dir, committed_images)
    lines: list[str] = [
        f"# {project_id} Local Object Materials / {project_id} 本地对象资料",
        "",
        "English:",
    ]
    append_wrapped_paragraph(
        lines,
        "This directory is the object-local human research entrance for this "
        "concrete oracle-character object. Start with the human dossier, "
        "visual gallery, source route, and review questions; use structured "
        "support files only to trace and verify the human-readable evidence.",
    )
    lines.extend(["", "简体中文："])
    append_wrapped_paragraph(
        lines,
        "本目录是这个具体甲骨文字对象的同位工作目录。人类可读说明、图像和"
        "来源入口、AI 可读资料包和索引都放在同一具体对象目录中，不另建与 "
        "`corpus` 或对象目录并行的“人类看的目录”。",
    )
    lines.extend(["", "## Local Files / 本地文件", ""])
    append_wrapped_bullet(lines, "Human-readable page / 人类可读页面", "`README.md`")
    append_wrapped_bullet(
        lines,
        "Human-readable visual gallery / 人类可读图像页",
        "`04_visual-gallery.md`",
    )
    append_wrapped_bullet(
        lines,
        "Human-readable research dossier / 人类可读研究档案",
        "`05_human-research-dossier.md`",
    )
    append_wrapped_bullet(
        lines,
        "Human-readable context dossier / 人类可读语境档案",
        "`08_character-context-evidence-dossier.md`",
    )
    append_wrapped_bullet(
        lines,
        "Human-readable archaeology review / 人类可读考古文字复核",
        "`10_archaeology-paleography-review.md`",
    )
    if material_observation_available:
        append_wrapped_bullet(
            lines,
            "Human-readable material observation / 人类可读实物图像观察",
            "`14_material-visual-observation.md`",
        )
    append_wrapped_bullet(
        lines,
        "Human-readable readiness review / 人类可读研究准备度复核",
        "`12_human-research-readiness-review.md`",
    )
    append_wrapped_bullet(
        lines,
        "Structured support candidate packet / 结构化辅助候选包",
        f"`{packet_name}`",
    )
    append_wrapped_bullet(
        lines,
        "Structured support visual/source index / 结构化辅助图像来源索引",
        "`02_visual-source-index.csv`",
    )
    append_wrapped_bullet(
        lines,
        "Structured support readiness index / 结构化辅助准备度索引",
        "`13_human-research-readiness-index.json`",
    )
    lines.extend(
        [
            "",
            "## Human Oracle Character Review Slots / 甲骨单字人工复核槽位",
            "",
            "Structured support files only serve the human oracle-character dossier.",
            "",
            "结构化辅助文件只服务本对象内的人类甲骨单字档案。",
            "",
        ]
    )
    for question in [
        "Open the visual gallery and record visible strokes or damage.",
        "Check source image, catalog, plate, collection, and period routes.",
        "Name variant, near-form, component, and later-script routes as pending.",
        "Keep readings, identities, disputes, and bibliography as review tasks.",
        "Check rights, checksum, source package, manifest, and field map.",
        "Write every missing item as a concrete question before research.",
        "先打开图像图库，记录可见笔画、残缺或疑点。",
        "核对来源图像、著录、图版、馆藏和时期路线。",
        "将异体、近形、构件和后世字形路线标为待复核。",
        "释读、身份、争议和文献关系只记为待查任务。",
        "核对权利、checksum、来源包、manifest 和字段映射。",
        "正式研究前，所有缺失项都写成具体问题。",
    ]:
        append_wrapped_plain_bullet(lines, question)
    lines.extend(["", "## Object Summary / 对象摘要", ""])
    append_wrapped_bullet(lines, "Project ID / 项目 ID", f"`{project_id}`")
    append_wrapped_bullet(
        lines,
        "Primary external reference / 首选外部参考",
        f"`{external_id}`",
    )
    append_wrapped_bullet(lines, "Source / 来源", f"`{source_id}`")
    append_wrapped_bullet(
        lines,
        "Packet record type / 资料包类型",
        f"`{packet_record_type}`",
    )
    append_wrapped_bullet(lines, "Directory / 目录", f"`{local_path}`")
    lines.extend(["", "## Visual Material Status / 图像资料状态", ""])
    append_wrapped_bullet(lines, "Status / 状态", f"`{status_text}`")
    append_wrapped_bullet(
        lines,
        "Source image reference rows / 来源图像路径引用行数",
        f"`{image_ref_count}`",
    )
    append_wrapped_bullet(
        lines,
        "Committed glyph image / 已提交字形图像",
        committed_image_text,
    )
    lines.extend(["", "English:"])
    append_wrapped_paragraph(
        lines,
        "If `02_visual-source-index.csv` contains source image paths, those "
        "paths are source-package references only. The raw HUST-OBC package "
        "is registered as a large source and is not committed to normal Git. "
        "If the CSV has no source image path, the next preparation step is to "
        "restore or download the registered source package, extract a "
        "review-safe image derivative, and record rights/provenance before "
        "committing any image asset.",
    )
    lines.extend(["", "简体中文："])
    append_wrapped_paragraph(
        lines,
        "如果 `02_visual-source-index.csv` 中有来源图像路径，它们只是来源包"
        "内部路径引用。HUST-OBC 原始包已经按大型来源登记，不提交到普通 Git。"
        "如果 CSV 中还没有来源图像路径，下一步资料工程应先恢复或下载已登记"
        "来源包，抽取适合复核的图像派生件，并在提交任何图像资产前记录权利、"
        "出处和风险。",
    )
    lines.extend(["", "## Research Boundary / 研究边界", "", "English:"])
    append_wrapped_paragraph(
        lines,
        "This page is a preparation-stage object entrance. It is not an "
        "accepted character record, not an accepted reading, not a component "
        "conclusion, and not a decipherment conclusion.",
    )
    lines.append("This is not a decipherment conclusion.")
    lines.extend(["", "简体中文："])
    append_wrapped_paragraph(
        lines,
        "本页只是准备阶段的对象入口。它不是正式甲骨单字记录，不是已确认释读，"
        "不是构件结论，也不是破译结论。",
    )
    lines.extend(["", "## Review Notes / 复核说明", ""])
    append_wrapped_bullet(
        lines,
        "Review status / 复核状态",
        "`needs_human_visual_review`",
    )
    append_wrapped_bullet(
        lines,
        "Required next step / 下一步",
        "open the packet, visual gallery, and visual/source index in this same "
        "directory, then compare against source registers, source package "
        "manifests, and cross-source evidence.",
    )
    append_wrapped_bullet(lines, "Boundary caution / 边界提示", caution)
    return "\n".join(lines)


def build_gallery_text(project_id: str, packet_name: str, packet: dict, visual_rows: list[dict[str, str]]) -> str:
    external_id = packet.get("primary_external_ref_id", "")
    source_id = packet.get("source_id", "")
    committed_rows = [row for row in visual_rows if row.get("committed_image_path")]
    sections: list[str] = []
    for row in committed_rows:
        asset_path = Path(row["committed_image_path"])
        asset_name = asset_path.name
        metadata_name = asset_path.with_suffix(".yaml").name
        local_asset_path = f"03_visual-assets/{asset_name}"
        local_metadata_path = f"03_visual-assets/{metadata_name}"
        sections.append(
            f"""## {row["visual_source_index_id"]} / 图像条目

![{project_id} glyph candidate]({local_asset_path})

- Local image / 本地图像: `{local_asset_path}`
- Local metadata / 本地 metadata: `{local_metadata_path}`
- Source image path / 来源图像路径: `{row.get("source_image_reference_path", "")}`
- Source package / 来源包: `{row.get("source_package_id", "")}`
- Download ID / 下载 ID: `{row.get("download_id", "")}`
- Rights status / 权利状态: `{row.get("rights_status", "")}`
- Review status / 复核状态: `{row.get("review_status", "")}`
- Risk note / 风险提示: {row.get("risk_note", "")}
"""
        )
    if not sections:
        sections.append(
            """## No Committed Local Image Yet / 暂无已提交本地图像

English:
This object currently has no committed local glyph image derivative. Use `02_visual-source-index.csv` to inspect source-image references and source-package routing before extracting any review image into this same object directory.

简体中文：
本对象目前还没有已提交的本地字形图像派生件。请先查看 `02_visual-source-index.csv` 中的来源图像引用和来源包路线，再把可复核图像抽取到同一对象目录中。"""
        )
    return f"""# {project_id} Visual Gallery / {project_id} 图像资料页

English:
This human-readable gallery stays inside the same concrete oracle-character object directory as the structured support packet and visual/source index. It is a preparation-stage viewing surface for local review images, not a parallel human-only directory.

简体中文：
本图像资料页与 AI 可读资料包、图像和来源索引放在同一具体甲骨文字对象目录内。它只是准备阶段的人类查看入口，不是另建的并行“人类看的目录”。

## Object And Source / 对象与来源

- Project ID / 项目 ID: `{project_id}`
- Primary external reference / 首选外部参考: `{external_id}`
- Source / 来源: `{source_id}`
- Structured support packet / 结构化辅助包: `{packet_name}`
- Visual/source index / 图像与来源索引: `02_visual-source-index.csv`
- Committed local review images / 已提交本地复核图像数: `{len(committed_rows)}`

## Research Boundary / 研究边界

English:
Images shown here are source-marked preparation materials for human visual review. Each image is not an accepted glyph identity, not an accepted reading, not a component conclusion, and not a decipherment conclusion.

简体中文：
本页展示的图像只是带来源标记的准备阶段材料，用于人工视觉复核。它们不是已确认字形身份，不是已确认释读，不是构件结论，也不是破译结论。

{chr(10).join(sections)}
"""


def build_gallery_text(project_id: str, packet_name: str, packet: dict, visual_rows: list[dict[str, str]]) -> str:
    external_id = packet.get("primary_external_ref_id", "")
    source_id = packet.get("source_id", "")
    committed_rows = [row for row in visual_rows if row.get("committed_image_path")]
    lines: list[str] = [
        f"# {project_id} Visual Gallery / {project_id} 图像资料页",
        "",
        "English:",
    ]
    append_wrapped_paragraph(
        lines,
        "This human-readable gallery stays inside the same concrete "
        "oracle-character object directory as the structured support packet "
        "and visual/source index. It is a preparation-stage viewing surface "
        "for local review images, not a parallel human-only directory.",
    )
    lines.extend(["", "简体中文:"])
    append_wrapped_paragraph(
        lines,
        "本图像资料页与 AI 可读资料包、图像和来源索引放在同一具体甲骨"
        "文字对象目录内。它只是准备阶段的人类查看入口，不是另建的并行"
        "人类目录。",
    )
    lines.extend(["", "## Object And Source / 对象与来源", ""])
    append_wrapped_bullet(lines, "Project ID / 项目 ID", f"`{project_id}`")
    append_wrapped_bullet(
        lines,
        "Primary external reference / 首选外部参考",
        f"`{external_id}`",
    )
    append_wrapped_bullet(lines, "Source / 来源", f"`{source_id}`")
    append_wrapped_bullet(lines, "Structured support packet / 结构化辅助包", f"`{packet_name}`")
    append_wrapped_bullet(
        lines,
        "Visual/source index / 图像与来源索引",
        "`02_visual-source-index.csv`",
    )
    append_wrapped_bullet(
        lines,
        "Committed local review images / 已提交本地复核图像数",
        f"`{len(committed_rows)}`",
    )
    lines.extend(["", "## Research Boundary / 研究边界", "", "English:"])
    append_wrapped_paragraph(
        lines,
        "Images shown here are source-marked preparation materials for human "
        "visual review. Each image is not an accepted glyph identity, not an "
        "accepted reading, not a component conclusion, and not a decipherment "
        "conclusion.",
    )
    lines.extend(["", "简体中文:"])
    append_wrapped_paragraph(
        lines,
        "本页展示的图像只是带来源标记的准备阶段材料，用于人工视觉复核。"
        "它们不是已确认字形身份，不是已确认释读，不是构件结论，也不是"
        "破译结论。",
    )

    if committed_rows:
        for row in committed_rows:
            asset_path = Path(row["committed_image_path"])
            asset_name = asset_path.name
            metadata_name = asset_path.with_suffix(".yaml").name
            local_asset_path = f"03_visual-assets/{asset_name}"
            local_metadata_path = f"03_visual-assets/{metadata_name}"
            lines.extend(
                [
                    "",
                    f"## {row['visual_source_index_id']} / 图像条目",
                    "",
                    f"![{project_id} glyph candidate]({local_asset_path})",
                    "",
                ]
            )
            append_wrapped_bullet(lines, "Local image / 本地图像", f"`{local_asset_path}`")
            append_wrapped_bullet(
                lines,
                "Local metadata / 本地 metadata",
                f"`{local_metadata_path}`",
            )
            append_wrapped_bullet(
                lines,
                "Source image path / 来源图像路径",
                f"`{row.get('source_image_reference_path', '')}`",
            )
            append_wrapped_bullet(
                lines,
                "Source package / 来源包",
                f"`{row.get('source_package_id', '')}`",
            )
            append_wrapped_bullet(
                lines,
                "Download ID / 下载 ID",
                f"`{row.get('download_id', '')}`",
            )
            append_wrapped_bullet(
                lines,
                "Rights status / 权利状态",
                f"`{row.get('rights_status', '')}`",
            )
            append_wrapped_bullet(
                lines,
                "Review status / 复核状态",
                f"`{row.get('review_status', '')}`",
            )
            append_wrapped_bullet(
                lines,
                "Risk note / 风险提示",
                row.get("risk_note", ""),
            )
    else:
        lines.extend(
            [
                "",
                "## No Committed Local Image Yet / 暂无已提交本地图像",
                "",
                "English:",
            ]
        )
        append_wrapped_paragraph(
            lines,
            "This object currently has no committed local glyph image "
            "derivative. Use `02_visual-source-index.csv` to inspect "
            "source-image references and source-package routing before "
            "extracting any review image into this same object directory.",
        )
        lines.extend(["", "简体中文:"])
        append_wrapped_paragraph(
            lines,
            "本对象目前还没有已提交的本地字形图像派生件。请先查看 "
            "`02_visual-source-index.csv` 中的来源图像引用和来源包路线，"
            "再把可复核图像抽取到同一对象目录中。",
        )
    return "\n".join(lines) + "\n"


def build_material_observation_text(
    project_id: str,
    object_dir: Path,
    packet: dict,
    visual_rows: list[dict[str, str]],
) -> str:
    observation = MATERIAL_VISUAL_OBSERVATIONS.get(project_id)
    committed = [row for row in visual_rows if row.get("committed_image_path")]
    if not observation or not committed:
        return ""
    row = committed[0]
    local_path = Path(row["committed_image_path"])
    if local_path.is_relative_to(object_dir):
        local_path_text = local_path.relative_to(object_dir).as_posix()
    else:
        local_path_text = local_path.as_posix()
    lines: list[str] = [
        f"# Material Visual Observation / {project_id} 实物图像观察",
        "",
        "English:",
    ]
    append_wrapped_paragraph(
        lines,
        "This note records only the visible marks in one local, source-linked "
        "review image. It is a preparation-stage observation for a human "
        "researcher, not a reading or component assignment.",
    )
    lines.extend(["", "简体中文："])
    append_wrapped_paragraph(
        lines,
        "本记录只描述一张有来源链接的本地复核图像中直接可见的痕迹，供人类研究者在预处理阶段查阅，"
        "不是释读或构件归属判断。",
    )
    lines.extend(["", "## Evidence Opened / 已打开证据", ""])
    append_wrapped_bullet(lines, "Project ID / 项目 ID", f"`{project_id}`")
    append_wrapped_bullet(
        lines,
        "External reference / 外部参照",
        f"`{packet.get('primary_external_ref_id', '')}`",
    )
    append_wrapped_bullet(
        lines,
        "Local image / 本地图像",
        f"`{local_path_text}`",
    )
    append_wrapped_bullet(
        lines,
        "Source image route / 来源图像路线",
        "open 02_visual-source-index.csv",
    )
    append_wrapped_bullet(lines, "Source / 来源", f"`{row.get('source_id', '')}`")
    append_wrapped_bullet(
        lines,
        "Source package / 来源包",
        f"`{row.get('source_package_id', '')}`",
    )
    append_wrapped_bullet(
        lines,
        "Download route / 下载路线",
        f"`{row.get('download_id', '')}`",
    )
    append_wrapped_bullet(
        lines,
        "Rights and risk / 权利与风险",
        f"`{row.get('rights_status', '')}`; see the visual index risk note.",
    )
    lines.extend(["", "## Direct Visual Record / 直接可见记录", ""])
    append_wrapped_bullet(lines, "English observation", observation[0])
    append_wrapped_bullet(lines, "中文观察", observation[1])
    lines.extend(["", "## Next Checks / 下一步核查", ""])
    for question in [
        "Open the image metadata and source row before comparing another form.",
        "Check whether a second view, rubbing, plate, or inscription context exists.",
        "Record variants, near forms, components, readings, and disputes only after source review.",
        "打开图像 metadata 和来源行，再与其他字形进行比较。",
        "查找是否存在第二视角、拓片、图版或卜辞上下文。",
        "完成来源复核后，再记录异体、近形、构件、释读和争议。",
    ]:
        append_wrapped_plain_bullet(lines, question)
    lines.extend(["", "## Boundary / 边界", ""])
    append_wrapped_paragraph(
        lines,
        "This is a visual observation record, not a reading or component "
        "assignment, not an inscription identity claim, and not a decipherment conclusion.",
    )
    append_wrapped_paragraph(
        lines,
        "本记录是图像观察记录，不是释读、构件归属、卜辞身份或破译结论。",
    )
    return "\n".join(lines) + "\n"


def build_outputs(root: Path) -> dict[str, dict]:
    image_rows = read_image_reference_rows(root)
    outputs: dict[str, dict] = {}
    for project_id, target in discover_target_dirs(root).items():
        object_dir = target["object_dir"]
        packet_name = target["packet"]
        packet = read_json(object_dir / packet_name)
        visual_index_path = object_dir / "02_visual-source-index.csv"
        visual_rows = build_visual_rows(
            project_id,
            packet,
            image_rows.get(project_id, []),
            read_existing_visual_rows(visual_index_path),
        )
        outputs[project_id] = {
            "object_dir": object_dir,
            "readme_path": object_dir / "README.md",
            "visual_index_path": visual_index_path,
            "gallery_path": object_dir / "04_visual-gallery.md",
            "material_observation_path": object_dir / "14_material-visual-observation.md",
            "readme_text": build_readme_text(
                project_id,
                object_dir.relative_to(root),
                packet_name,
                packet,
                visual_rows,
                bool(MATERIAL_VISUAL_OBSERVATIONS.get(project_id))
                and any(row.get("committed_image_path") for row in visual_rows),
            ),
            "gallery_text": build_gallery_text(project_id, packet_name, packet, visual_rows),
            "visual_rows": visual_rows,
            "material_observation_text": build_material_observation_text(
                project_id, object_dir, packet, visual_rows
            ),
        }
    return outputs


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=VISUAL_INDEX_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(outputs: dict[str, dict]) -> None:
    for output in outputs.values():
        output["readme_path"].write_text(output["readme_text"].rstrip() + "\n", encoding="utf-8", newline="\n")
        output["gallery_path"].write_text(output["gallery_text"].rstrip() + "\n", encoding="utf-8", newline="\n")
        write_csv(output["visual_index_path"], output["visual_rows"])
        observation_text = output["material_observation_text"]
        observation_path = output["material_observation_path"]
        if observation_text:
            observation_path.write_text(
                observation_text.rstrip() + "\n",
                encoding="utf-8",
                newline="\n",
            )
        elif observation_path.exists():
            observation_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    outputs = build_outputs(args.root)
    write_outputs(outputs)
    print(f"Wrote local materials for {len(outputs)} character directories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
