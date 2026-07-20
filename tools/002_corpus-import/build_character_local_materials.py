#!/usr/bin/env python3
"""Build co-located human and AI material indexes for character directories."""

from __future__ import annotations

import argparse
import csv
import json
import re
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
    "obs-char-000141": (
        "The image has an angled upper cap above a compact grid-like middle form, "
        "with several short uprights extending below the lower edge.",
        "图像上方有折角盖状形，中部为紧凑的网格状形体，下缘向下伸出数道短竖笔。",
    ),
    "obs-char-000142": (
        "The broad image combines a heavy left vertical with two horizontal bands "
        "and a separate tall curved form on the right.",
        "宽大图像左侧有粗重竖笔和两道横向带状笔，右侧另有一处高而弯曲的形体。",
    ),
    "obs-char-000143": (
        "The narrow image has a small forked upper stem, a rounded loop on the "
        "left, and a long curved stroke descending on the right.",
        "狭长图像上方有小分叉主笔，左侧有圆弧环状笔，右侧有长弯曲下行笔。",
    ),
    "obs-char-000144": (
        "The image has a pointed upper mark, a banded diagonal form opening toward "
        "the lower left, and a thin curved stroke descending on the right.",
        "图像上方有尖状痕迹，左下方有带平行横痕的斜向开放形，右侧有细弯曲下行笔。",
    ),
    "obs-char-000145": (
        "The image has a broad angular upper chevron, a rounded open lower-left "
        "frame, and a central descending stroke with a short branch.",
        "图像上方有宽折角形，下方左侧有圆弧开放框，中部有下行主笔并带短分支。",
    ),
    "obs-char-000146": (
        "The narrow image has a short upper horizontal mark, two long descending "
        "curved strokes, and a small forked mark near the bottom.",
        "狭长图像上方有短横笔，两道长弯曲笔向下延伸，底部附近有小型分叉痕迹。",
    ),
    "obs-char-000147": (
        "The very narrow image has several short side marks on the left, a long "
        "descending stroke, and a compact branching knot near the lower end.",
        "极狭长图像左侧有数道短侧痕，中央有长下行笔，下端附近有紧凑分叉交结。",
    ),
    "obs-char-000148": (
        "The image has a central crossing, a long pointed descending stroke, and "
        "short outward projections on both sides near the upper half.",
        "图像中部有交叉点，向下延伸长而尖的主笔，上半部两侧有短向外伸笔。",
    ),
    "obs-char-000149": (
        "The image combines a long curved stroke on the left with a compact upper "
        "enclosure and a narrow descending stroke on the right.",
        "图像左侧有长弯曲笔，右侧上方有紧凑围合形，并有窄下行笔向下延伸。",
    ),
    "obs-char-000150": (
        "The image has two curved upper side strokes around a small rectangular "
        "middle enclosure, with a central vertical stroke below it.",
        "图像上方两侧有弯曲笔围绕小型长方形中部围合，下方接一条中央竖笔。",
    ),
    "obs-char-000151": (
        "The image has a pointed upper descending stroke, a compact angular loop "
        "on the left, and a short lower projection.",
        "图像上方有尖状下行笔，左侧有紧凑折角环状形，下方有短伸出笔。",
    ),
    "obs-char-000152": (
        "The image combines a narrow banded form on the left with a broad pointed "
        "arch on the right and a small enclosed loop inside it.",
        "图像左侧有窄而带横痕的形体，右侧有宽大的尖顶拱形，内部另有小型围合环。",
    ),
    "obs-char-000153": (
        "The image has a small curved upper mark, a compact stacked middle form, "
        "and a rounded open stroke curving along the lower edge.",
        "图像上方有小弯曲痕迹，中部为紧凑叠置形体，下缘有沿边弯曲的开放笔画。",
    ),
    "obs-char-000154": (
        "The image has a pointed upper stem, a broad horizontal lower-left form, "
        "and a compact rectangular mark on the lower right.",
        "图像上方有尖状主笔，下方左侧有宽横向形体，右下方有紧凑长方形痕迹。",
    ),
    "obs-char-000155": (
        "The narrow image has an angled upper stroke, a small triangular enclosure "
        "near the middle, and several fine strokes extending below it.",
        "狭长图像上方有折斜笔，中部附近有小型三角围合，下方延伸出数道细笔。",
    ),
    "obs-char-000156": (
        "The low-resolution gray image has a curved left stroke beside a compact "
        "dark form with a short internal crossing mark.",
        "低分辨率灰度图像左侧有弯曲笔，右侧为紧凑深色形体，内部带短交叉痕迹。",
    ),
    "obs-char-000157": (
        "The image has a rounded outer descending form, a pointed branching mark "
        "inside the lower left, and a thin stroke continuing downward.",
        "图像有圆弧外轮廓向下延伸，左下内部有尖状分叉痕迹，并有细笔继续下行。",
    ),
    "obs-char-000158": (
        "The image combines a long curved stroke on the left with stacked angular "
        "bands above a rounded lower loop on the right.",
        "图像左侧有长弯曲笔，右侧上方为叠置折角横带，下方接圆弧环状形。",
    ),
    "obs-char-000159": (
        "The image has a rough square enclosure containing crossing strokes, with "
        "a separate long vertical stroke along the right side.",
        "图像有粗略方形围合，内部含交叉笔，右侧另有一条分离的长竖笔。",
    ),
    "obs-char-000160": (
        "The image is a dense central knot of crossing and looping strokes, with "
        "longer side strokes extending above and below it.",
        "图像中部是交叉、环绕笔组成的密集结状形体，两侧有较长笔画向上下伸出。",
    ),
    "obs-char-000161": (
        "The narrow image has a dense branched upper cluster, a long central "
        "descending stroke, and short irregular marks along the right side.",
        "狭长图像上方有密集分叉笔群，中部有长下行主笔，右侧有不规则短痕。",
    ),
    "obs-char-000162": (
        "The broad image contains a separate curved stroke on the left and a deep "
        "V-shaped form on the right ending in a compact rectangular block.",
        "宽大图像左侧有分离的弯曲笔，右侧为深 V 形结构，下端接紧凑长方形块。",
    ),
    "obs-char-000163": (
        "The narrow image has a small angular upper cap, a long curved outer stroke, "
        "and a short inner branch descending beside it.",
        "狭长图像上方有小型折角盖状笔，外侧有长弯曲笔，旁边有短内部分支下行。",
    ),
    "obs-char-000164": (
        "The image is formed by two long narrow strokes crossing near the middle, "
        "with both ends tapering unevenly.",
        "图像由两道长而窄的笔画在中部附近交叉构成，两端收笔长短和粗细不齐。",
    ),
    "obs-char-000165": (
        "The low-resolution gray image has a dense upper horizontal cluster and a "
        "thin curved stroke descending below it.",
        "低分辨率灰度图像上方有密集横向笔群，下方有细弯曲笔向下延伸。",
    ),
    "obs-char-000166": (
        "The image has two short upper horizontal bars, a narrow descending stroke, "
        "and a hooked projection near the lower end.",
        "图像上方有两道短横笔，中部有窄下行笔，下端附近有钩状伸出笔。",
    ),
    "obs-char-000167": (
        "The broad image shows two separated tall forms: a long curved stroke on "
        "the left and a branched angular form on the right with a small terminal mark.",
        "宽大图像可见左右分离的两处高形：左侧为长弯曲笔，右侧为分叉折角形，并带小末端痕迹。",
    ),
    "obs-char-000168": (
        "The low-resolution gray image has a small triangular upper frame above a "
        "short rectangular lower enclosure.",
        "低分辨率灰度图像上方有小型三角框，下方接短小长方形围合。",
    ),
    "obs-char-000169": (
        "The narrow image has a long central descending stroke with short horizontal "
        "and diagonal branches extending to the left near the upper half.",
        "狭长图像中部有长下行主笔，上半部左侧伸出短横笔和短斜向分支。",
    ),
    "obs-char-000170": (
        "The low-resolution gray image has a thin central vertical stroke, a small "
        "upper branch, and short side strokes crossing near the middle.",
        "低分辨率灰度图像有细中央竖笔，上方有小分支，中部附近有短侧笔交叉。",
    ),
    "obs-char-000171": (
        "The image has a three-pronged upper form, a long curved descending stroke, "
        "and a short angular projection near the lower left.",
        "图像上部呈三叉形，下方有长弯曲下行笔，左下附近有短折角伸出笔。",
    ),
    "obs-char-000172": (
        "The narrow image has a long central descending stroke, short upper side "
        "marks, and a branching projection toward the right at mid-height.",
        "狭长图像中部有长下行主笔，上方有短侧痕，中部高度向右伸出分支。",
    ),
    "obs-char-000173": (
        "The tall image has a central vertical stroke with short irregular branches "
        "extending to both sides.",
        "高形图像中部有竖直主笔，两侧伸出长短不齐的短分支。",
    ),
    "obs-char-000174": (
        "The image has a rounded angular upper loop connected to a long curved stroke "
        "that descends and hooks toward the lower right.",
        "图像上方有圆弧折角环状形，连接长弯曲笔向下延伸并在右下方收成钩状。",
    ),
    "obs-char-000175": (
        "The image has a broad forked upper form, a narrow central descending stroke, "
        "and a small curved lower continuation.",
        "图像上方有宽分叉形，中部有窄下行主笔，下方接小段弯曲延续笔。",
    ),
    "obs-char-000176": (
        "The image has a leaf-like upper cluster with several internal curved strokes "
        "and a thin pointed continuation below.",
        "图像上方有叶状笔群，内部含数道弯曲笔，下方接细而尖的延续笔。",
    ),
    "obs-char-000177": (
        "The image is a single broad inverted V-shaped form with two long tapering "
        "strokes meeting at the top.",
        "图像由单一宽大的倒 V 形构成，两道长而渐细的笔在上方相接。",
    ),
    "obs-char-000178": (
        "The image has a rectangular outer frame with a central angled opening and "
        "two short vertical strokes descending below the lower edge.",
        "图像有长方形外框，中部为折角开口，下缘向下伸出两道短竖笔。",
    ),
    "obs-char-000179": (
        "The large dark image has a heavy upper horizontal bar, two long side "
        "strokes, a central angular crossing form, and a small detached dot.",
        "大幅深色图像上方有粗重横梁，两侧有长竖笔，中部有折角交叉形，并有小分离点痕。",
    ),
    "obs-char-000180": (
        "The image contains two separate short curved vertical strokes with uneven "
        "thickness and tapering ends.",
        "图像含两道分离的短弯曲竖笔，粗细不均，末端呈渐细收笔。",
    ),
    "obs-char-000181": (
        "The image has two long curved descending strokes and a small rounded loop "
        "near the lower center.",
        "图像有两道长弯曲下行笔，中部下方附近有小型圆弧环。",
    ),
    "obs-char-000182": (
        "The image has a pointed upper junction, two long outer strokes descending "
        "on both sides, and a short central lower stroke.",
        "图像上方有尖状交接点，两侧有长外笔向下延伸，中部下方有短笔。",
    ),
    "obs-char-000183": (
        "The low-resolution image shows a small horizontal crossing, a short left "
        "projection, and a thin diagonal stroke descending toward the lower right.",
        "低分辨率图像可见小型横向交叉、左侧短伸笔，以及向右下延伸的细斜笔。",
    ),
    "obs-char-000184": (
        "The dark image has a rounded upper enclosure, two long side strokes, and a "
        "curved lower-right projection crossing the interior.",
        "深色图像上方有圆弧围合，两侧有长竖笔，右下方有弯曲伸笔穿过内部。",
    ),
    "obs-char-000185": (
        "The image has a narrow forked upper stem and several curved overlapping "
        "strokes gathered in the lower half.",
        "图像上方有窄分叉主笔，下半部聚集数道相互重叠的弯曲笔。",
    ),
    "obs-char-000186": (
        "The image forms a deep U-shaped lower frame with two upright side strokes, "
        "short upper caps, and crossing strokes inside the lower opening.",
        "图像下部形成深 U 形框，两侧有竖笔，上端有短盖笔，框内有交叉笔。",
    ),
    "obs-char-000187": (
        "The image has a compact banded upper cluster, a central descending group of "
        "strokes, and irregular side projections.",
        "图像上方有紧凑带状笔群，中部有分组下行笔，两侧有不规则伸出笔。",
    ),
    "obs-char-000188": (
        "The broad image has several upright strokes crossing a horizontal banded "
        "form, with diagonal projections extending below both sides.",
        "宽大图像有数道竖笔穿过横向带状形体，两侧向下伸出斜向笔。",
    ),
    "obs-char-000189": (
        "The low-resolution gray image has two rounded upper lobes above a short "
        "horizontal base and a thin central descending stroke.",
        "低分辨率灰度图像上方有两个圆弧上部，下面接短横底部和细中央下行笔。",
    ),
    "obs-char-000190": (
        "The image has a pointed upper enclosure with long strokes descending on both "
        "sides and a shorter diagonal projection toward the right.",
        "图像上方有尖顶围合，两侧有长笔向下延伸，右侧另有较短斜向伸笔。",
    ),
    "obs-char-000191": (
        "The broad image has a long horizontal band crossed by several short upright "
        "strokes, with uneven projections extending below it.",
        "宽大图像有长横向带状笔，数道短竖笔穿过其间，下方伸出长短不齐的笔画。",
    ),
    "obs-char-000192": (
        "The image has a pointed upper cap, two long curved inner strokes, and broad "
        "outer strokes descending toward the lower sides.",
        "图像上方有尖顶盖状形，内部有两道长弯曲笔，外侧笔向下延伸至两边下方。",
    ),
    "obs-char-000193": (
        "The image has a central angular crossing with a short upper stroke, a long "
        "diagonal stroke toward the lower left, and a separate lower-right mark.",
        "图像中部有折角交叉，上方有短笔，左下方有长斜笔，右下另有分离痕迹。",
    ),
    "obs-char-000194": (
        "The narrow image has a small rounded upper mark, two horizontal bands, and "
        "a thin central stroke descending below them.",
        "狭长图像上方有小圆弧痕迹，中部有两道横带，下方接细中央下行笔。",
    ),
    "obs-char-000195": (
        "The large image has a rounded outer frame, an inner loop and horizontal band, "
        "and long side strokes continuing below the lower edge.",
        "大幅图像有圆弧外框，内部含环状形和横带，下缘两侧有长笔继续向下。",
    ),
    "obs-char-000196": (
        "The image is a dense chain of crossing and looping strokes with short side "
        "projections extending at several levels.",
        "图像是交叉、环绕笔组成的密集链状形体，多个高度有短侧向伸笔。",
    ),
    "obs-char-000197": (
        "The image has a rounded angular upper loop connected to a long curved stroke "
        "that descends and hooks near the lower right.",
        "图像上方有圆弧折角环状形，连接长弯曲笔向下延伸，并在右下附近收成钩状。",
    ),
    "obs-char-000198": (
        "The image has a pointed outer frame, a dark inner elongated form, and a long "
        "thin stroke descending below the lower opening.",
        "图像有尖顶外框，内部为深色长形痕迹，下方开口处向下延伸长细笔。",
    ),
    "obs-char-000199": (
        "The image has a short upper horizontal bar, a rounded middle enclosure, a "
        "small lower loop, and upright side strokes.",
        "图像上方有短横笔，中部有圆弧围合，下方有小环状形，两侧有竖向笔画。",
    ),
    "obs-char-000200": (
        "The image has a small upper cap above a rectangular enclosure on the left, "
        "with a long descending stroke and a short branch on the right.",
        "图像上方有小盖状笔，左侧为长方形围合，右侧有长下行笔并带短分支。",
    ),
    "obs-char-000201": (
        "The image has a broad angular upper form, a long descending stroke on the "
        "right, and a pointed lower-left projection.",
        "图像上方有宽折角形，右侧有长下行笔，左下方有尖状伸出笔。",
    ),
    "obs-char-000202": (
        "The image has a dense upper branching cluster, a rounded lower-left loop, "
        "and a thin descending stroke on the right.",
        "图像上方有密集分叉笔群，左下方有圆弧环状形，右侧有细下行笔。",
    ),
    "obs-char-000203": (
        "The image has a deep rounded lower bowl, two short upright strokes inside, "
        "and a narrow central opening at the top.",
        "图像下部有深圆弧碗状框，内部有两道短竖笔，上方中央有窄开口。",
    ),
    "obs-char-000204": (
        "The very narrow image has a thin vertical stroke with a short curved branch "
        "projecting toward the lower right.",
        "极狭长图像有细竖笔，并在下方右侧伸出短弯曲分支。",
    ),
    "obs-char-000205": (
        "The narrow image has a long descending stroke with a branching diagonal "
        "form opening toward the lower left.",
        "狭长图像有长下行主笔，向左下方展开折斜分支形。",
    ),
    "obs-char-000206": (
        "The image has a short separate stroke on the left, a branching central form, "
        "and a long curved stroke descending toward the lower right.",
        "图像左侧有分离短笔，中部有分叉形，右下方有长弯曲笔向下延伸。",
    ),
    "obs-char-000207": (
        "The image has two short forked marks on the left and a pointed upper-right "
        "form connected to a long curved descending stroke.",
        "图像左侧有两道短分叉痕，右上方有尖状形，连接长弯曲下行笔。",
    ),
    "obs-char-000208": (
        "The image has a long central vertical stroke, short branching marks on the "
        "left, and several small cross strokes along the right.",
        "图像中部有长竖主笔，左侧有短分支，右侧沿线分布数道小交叉笔。",
    ),
    "obs-char-000209": (
        "The image combines a compact grid of crossing strokes on the left with a "
        "separate long curved stroke on the right.",
        "图像左侧为紧凑交叉笔组成的网格，右侧另有一条分离的长弯曲笔。",
    ),
    "obs-char-000210": (
        "The image has a pointed upper V-shaped mark, a curved branching lower-left "
        "form, and a separate long stroke on the right.",
        "图像上方有尖顶 V 形痕迹，左下方有弯曲分支形，右侧另有分离长笔。",
    ),
    "obs-char-000211": (
        "The image has a triangular upper frame with a horizontal internal bar, a "
        "broad lower stroke, and a separate angular form on the right.",
        "图像上方有三角框，内部有横笔，下方有宽笔，右侧另有分离的折角形。",
    ),
    "obs-char-000212": (
        "The narrow image has a branching upper stem, several fine strokes gathered "
        "in the middle, and a curved lower-right continuation.",
        "狭长图像上方有分叉主笔，中部聚集数道细笔，下方右侧有弯曲延续笔。",
    ),
    "obs-char-000213": (
        "The broad image combines a dense horizontal grid on the left with a separate "
        "tall curved stroke on the right and a diagonal crossing near the base.",
        "宽大图像左侧为密集横向网格，右侧有分离高弯曲笔，底部附近有斜向交叉笔。",
    ),
    "obs-char-000214": (
        "The image has a large rounded loop on the left connected through a central "
        "crossing to a long curved stroke on the right.",
        "图像左侧有大型圆弧环，经过中部交叉连接右侧长弯曲笔。",
    ),
    "obs-char-000215": (
        "The image has two long descending side strokes, a short fork near the upper "
        "middle, and several pointed projections along the lower edge.",
        "图像两侧有长下行笔，中上部有短分叉，下缘有数道尖状伸出笔。",
    ),
    "obs-char-000216": (
        "The image has a three-peaked upper cluster, horizontal internal bands, a "
        "compact lower block, and a separate curved stroke on the right.",
        "图像上方有三尖峰笔群，内部有横向带，下方有紧凑块状形，右侧另有分离弯曲笔。",
    ),
    "obs-char-000217": (
        "The image combines a small upper fork with a compact lower grid-like form "
        "and a separate long curve along the right side.",
        "图像上方有小分叉，下方为紧凑网格状形，右侧另有分离长弯曲笔。",
    ),
    "obs-char-000218": (
        "The image has a long curved stroke on the left and an elongated right frame "
        "containing crossing diagonal and horizontal strokes.",
        "图像左侧有长弯曲笔，右侧为长形框，内部含斜向和横向交叉笔。",
    ),
    "obs-char-000219": (
        "The image has a broad upper curved cap, a hanging central loop, and a "
        "separate thin curved stroke on the right.",
        "图像上方有宽弯曲盖状笔，中部有悬垂环状形，右侧另有分离细弯曲笔。",
    ),
    "obs-char-000220": (
        "The large image contains two separated angular forms with long descending "
        "strokes, branching lower ends, and a curved opening on the right.",
        "大幅图像含左右分离的两处折角形，带长下行笔、下部分支和右侧弯曲开口。",
    ),
    "obs-char-000221": (
        "The image contains several separated forms: a forked upper mark, a short "
        "upright oval on the left, a long curved stroke on the right, and lower hooks.",
        "图像含数处分离形体：上方有分叉痕，左侧有短直椭圆形，右侧有长弯曲笔，下方有钩状笔。",
    ),
    "obs-char-000222": (
        "The narrow image has a branching upper cluster, a rounded central opening, "
        "and a thin curved stroke continuing down the right side.",
        "狭长图像上方有分叉笔群，中部有圆弧开口，右侧有细弯曲笔继续下行。",
    ),
    "obs-char-000223": (
        "The very narrow image has a long descending stroke with a short diagonal "
        "branch projecting toward the lower right.",
        "极狭长图像有长下行笔，并向右下伸出短斜向分支。",
    ),
    "obs-char-000224": (
        "The image has three parallel curved descending strokes with short pointed "
        "projections near their lower ends.",
        "图像有三道相互平行的弯曲下行笔，下端附近带短尖状伸出笔。",
    ),
    "obs-char-000225": (
        "The large dark image has a dense circular outer frame filled with crossing "
        "diagonal strokes and a central vertical line.",
        "大幅深色图像有密集圆形外框，内部充满交叉斜笔，并有中央竖线。",
    ),
    "obs-char-000226": (
        "The image has a rounded lower frame, several short forked upper strokes, and "
        "small interior marks around a central vertical axis.",
        "图像下部有圆弧框，上方有数道短分叉笔，中央竖轴周围有小内部痕迹。",
    ),
    "obs-char-000227": (
        "The image is a simple thin curved upper stroke that turns into a long "
        "descending line on the right.",
        "图像由上方简单细弯曲笔构成，并在右侧转为长下行线。",
    ),
    "obs-char-000228": (
        "The low-resolution gray image shows two short separated strokes, one more "
        "upright and one curving outward toward the lower right.",
        "低分辨率灰度图像可见两道分离短笔，一道较直立，另一道向右下弯曲外展。",
    ),
    "obs-char-000229": (
        "The large image has a deep rounded outer frame, a pointed inner crossing "
        "form, two stacked lower enclosures, and a separate right upright.",
        "大幅图像有深圆弧外框，内部有尖状交叉形，下方有两层叠置围合，右侧另有竖笔。",
    ),
    "obs-char-000230": (
        "The narrow image has a long central descending stroke with several short "
        "curved side strokes opening toward the left.",
        "狭长图像有长中央下行笔，左侧展开数道短弯曲侧笔。",
    ),
    "obs-char-000231": (
        "The narrow upright image has a curved outer stroke, a short crossing "
        "stroke near the upper middle, and a hooked descending stroke on the right.",
        "狭长直立图像有弯曲外笔，上部中段有短交叉笔，右侧有钩状下行笔。",
    ),
    "obs-char-000232": (
        "The small image shows a single long curved stroke with a short horizontal "
        "branch near the upper middle; the lower end is partly faint.",
        "小幅图像可见一条长弯曲笔画，上部中段有短横向分支；下端部分较浅。",
    ),
    "obs-char-000233": (
        "The thin upright image has a long central stroke, a pointed upper branch, "
        "and two separated diagonal marks toward the lower left.",
        "纤细直立图像有长中央笔，上方有尖状分支，下方偏左有两道分离斜痕。",
    ),
    "obs-char-000234": (
        "Two tall tapered strokes rise side by side, with a small angled connection "
        "near the top; the lower ends remain separate.",
        "两道高而渐尖的笔画并列上行，顶部附近有小型折角连接，下端仍彼此分离。",
    ),
    "obs-char-000235": (
        "The image has a block-like angular outer contour and an inner open angular "
        "stroke; the right side is straighter than the left.",
        "图像有块状折角外轮廓和内部开放折角笔画；右侧比左侧更直。",
    ),
    "obs-char-000236": (
        "The large image has a thick bent outer frame, a smaller inner enclosure, "
        "and several branching strokes inside the enclosure.",
        "大幅图像有粗重折弯外框，内部另有较小围合，并含数道分叉笔画。",
    ),
    "obs-char-000237": (
        "The compact image is divided by diagonal crossings and short angular marks, "
        "with a small branching form visible near the lower left.",
        "紧凑图像中可见斜向交叉和短折角痕迹，左下附近有小型分叉形体。",
    ),
    "obs-char-000238": (
        "The low-contrast gray image shows a curved outer stroke around a thin "
        "central vertical form with short diagonal branches.",
        "低对比度灰度图像有环抱中央的弯曲外笔，中部细竖形带有短斜向分支。",
    ),
    "obs-char-000239": (
        "The image has a rounded lower contour, an upright left-side stroke, several "
        "short branching marks above, and a detached diagonal mark at lower right.",
        "图像有圆弧下部轮廓，左侧有直立笔，上方有数道短分叉痕，右下另有分离斜痕。",
    ),
    "obs-char-000240": (
        "A slanting upper stroke runs above two small angular enclosed marks; the "
        "lower marks are separated and partly irregular.",
        "一道斜向上部笔画位于两个小型折角围合痕迹之上；下部痕迹分离且部分不规则。",
    ),
    "obs-char-000241": (
        "The narrow image has a long upright stroke, a short horizontal branch near "
        "the middle, and a longer stroke extending toward the lower right.",
        "狭长图像有长直立笔，中部附近有短横向分支，并有较长笔画向右下伸展。",
    ),
    "obs-char-000242": (
        "The thin upright image has a pointed upper turn, a short cross stroke, and "
        "a narrow descending tail below the crossing.",
        "纤细直立图像上方有尖转笔，中部有短交叉笔，交叉处下方有窄长下行尾笔。",
    ),
    "obs-char-000243": (
        "Three tall strokes stand within an open rounded lower contour; the center "
        "stroke reaches higher than the curved base.",
        "三道高直笔画位于开放的圆弧下部轮廓内；中央笔高出弯曲底部。",
    ),
    "obs-char-000244": (
        "The narrow image has a curved left-side stem, a pointed upper turn, and two "
        "short diagonal strokes opening toward the right.",
        "狭长图像有弯曲左侧主干、尖状上转笔，并向右展开两道短斜笔。",
    ),
    "obs-char-000245": (
        "The small dark image is a thin irregular upright stroke with a visibly "
        "thickened, rounded terminal at the bottom.",
        "小幅深色图像呈纤细而不规则的直立笔画，下端有明显加粗的圆钝末端。",
    ),
    "obs-char-000246": (
        "Three tall interior strokes rise from an open rounded lower contour, forming "
        "a compact upward cluster without a closed upper frame.",
        "三道高直内部笔画从开放圆弧下部轮廓中上行，形成紧凑上聚形，顶部没有闭合外框。",
    ),
    "obs-char-000247": (
        "A small rectangular grid-like form appears at the top, followed by a curved "
        "descending stroke with short side branches below it.",
        "顶部有小型矩形网格状形体，下方接弯曲下行笔，并带有短侧向分支。",
    ),
    "obs-char-000248": (
        "The low-contrast gray image is a compact cluster of crossing angular strokes; "
        "fine terminals are difficult to separate at this size.",
        "低对比度灰度图像呈交叉折角笔画的紧凑聚集；受尺寸影响，细小末端难以分开。",
    ),
    "obs-char-000249": (
        "The image has crossing strokes at the top, an angular enclosed middle area, "
        "and a long diagonal stroke descending along the right side.",
        "图像顶部有交叉笔，中部有折角围合区域，右侧有长斜笔向下伸展。",
    ),
    "obs-char-000250": (
        "Two separated dark clusters are visible: the left is a thin upright form with "
        "a short top branch, while the right is denser and more heavily branched.",
        "图像可见两个分离的深色聚集：左侧为带短顶部笔的纤细直立形，右侧更密集且分叉更多。",
    ),
    "obs-char-000251": (
        "The image is a broad tapered horizontal stroke with a short curved branch "
        "dropping from its lower edge near the center.",
        "图像为宽而渐尖的横向笔画，中部附近从下缘垂下一道短弯曲分支。",
    ),
    "obs-char-000252": (
        "The image has a rounded rectangular outer contour, a short upper bar, and "
        "several irregular strokes inside the lower enclosed area.",
        "图像有圆弧矩形外轮廓、短上横笔，内部下方围合区域中有数道不规则笔画。",
    ),
    "obs-char-000253": (
        "A thick curved loop forms the main body, with an open interior and a short "
        "separate stroke on the right.",
        "粗重弯曲环状笔形成主体，内部开放，右侧另有一道短分离笔。",
    ),
    "obs-char-000254": (
        "The narrow image has a pointed leaf-like outer contour, a thin interior line, "
        "and a detached diagonal stroke below.",
        "狭长图像有尖状叶形外轮廓、细内部笔，下方另有一道分离斜笔。",
    ),
    "obs-char-000255": (
        "A long central vertical stroke separates two rounded side forms; the left and "
        "right forms are similar in size but not identical in contour.",
        "长中央竖笔将两个圆弧侧形分开；左右形体大小相近，但轮廓并不完全相同。",
    ),
    "obs-char-000256": (
        "The thin upright image contains a long central stroke with several short "
        "angled branches clustered along its right side.",
        "纤细直立图像有长中央笔，右侧沿线聚集数道短折角分支。",
    ),
    "obs-char-000257": (
        "Two long angled strokes open upward from a small lower junction; a short "
        "branch projects toward the right side.",
        "两道长斜笔从下部小连接处向上张开，右侧有一道短分支外伸。",
    ),
    "obs-char-000258": (
        "The compact dark image has a dense rounded stroke cluster on the left and a "
        "taller angular open form on the right.",
        "紧凑深色图像左侧有密集圆弧笔画聚集，右侧有较高的开放折角形体。",
    ),
    "obs-char-000259": (
        "Two separated forms are visible: a small stack of rounded marks on the left "
        "and a long curved form with a pointed lower tail on the right.",
        "图像可见两个分离形体：左侧是小型叠置圆弧痕，右侧是带尖状下尾的长弯曲形。",
    ),
    "obs-char-000260": (
        "The large dark image has a thick upper block, two long descending strokes, and "
        "a heavy irregular terminal at the lower right.",
        "大幅深色图像有粗重上部块状形体、两道长下行笔，右下有厚重不规则末端。",
    ),
    "obs-char-000261": (
        "The small image shows a thin curved stroke descending from the upper left, "
        "with a short branch extending near the lower junction.",
        "小型图像有一道从左上向下弯曲的细笔画，靠近下部连接处另有短分支。",
    ),
    "obs-char-000262": (
        "The tall image has two long upright strokes, three short horizontal bars "
        "near the top, and a central forked form beneath them.",
        "高形图像有两道长竖向笔画，上部附近有三道短横画，下方为中央分叉形体。",
    ),
    "obs-char-000263": (
        "The narrow image shows a tall outer stroke with a small stacked enclosed "
        "form near the center; the lower end remains partly open.",
        "狭长图像有高而外侧的笔画，中部附近有小型叠置闭合形体，下端仍部分开放。",
    ),
    "obs-char-000264": (
        "The low-contrast image shows a small arched upper outline and several "
        "separated angular marks below it; surface detail needs recheck.",
        "低对比度图像上方有小型拱形轮廓，下方有数处分离折角痕迹；表面细节仍需复核。",
    ),
    "obs-char-000265": (
        "The image has two slender upper branches, a rounded enclosed mark below, "
        "and a short detached stroke at the left.",
        "图像上部有两道纤细分支，下方有圆弧闭合痕迹，左侧另有短分离笔画。",
    ),
    "obs-char-000266": (
        "The upright image has a pointed upper junction, two curved outer strokes, "
        "and a small enclosed mark along the central axis.",
        "直立图像上方有尖状连接处，两道弯曲外侧笔画，中轴线上有小型闭合痕迹。",
    ),
    "obs-char-000267": (
        "The dark image contains several rounded upper lobes, a dense central knot, "
        "and a long irregular stroke descending toward the lower right.",
        "深色图像含数个圆弧上部形体、密集中央结点，并向右下延出长而不规则笔画。",
    ),
    "obs-char-000268": (
        "The small image shows a narrow curved upright stroke with a short forked "
        "branch near its upper end and a separate lower curve.",
        "小型图像有窄而弯曲的直立笔画，上端附近有短分叉，下面另有弧形痕迹。",
    ),
    "obs-char-000269": (
        "The image has three short parallel curved marks on the left and a long "
        "descending stroke on the right with a slight angular turn.",
        "图像左侧有三道短而平行的弯曲痕迹，右侧有长下行笔画并带轻微折转。",
    ),
    "obs-char-000270": (
        "The narrow image shows a long upright stroke, a short side branch near the "
        "top, and a small curved terminal at the lower end.",
        "狭长图像有长竖向笔画，上部附近有短侧分支，下端有小型弯曲收笔。",
    ),
    "obs-char-000271": (
        "The narrow image shows a thin descending stroke with an angular upper bend "
        "and two short curved marks near the middle; the lower stem continues apart.",
        "狭长图像有一道带上部折转的细下行笔画，中部附近有两处短弯曲痕迹；下部笔干继续向下。",
    ),
    "obs-char-000272": (
        "The image shows two separated upright forms; each has a curved upper end, "
        "a short diagonal branch, and a tapering lower stroke.",
        "图像有两个分离的直立形体；各自上端弯曲，并有短斜向分支和渐细下行笔画。",
    ),
    "obs-char-000273": (
        "The compact image has an angular outer outline, a diagonal internal stroke, "
        "and a long thin stroke descending on the right.",
        "小型图像有折角外轮廓，内部有一道斜向笔画，右侧另有长而纤细的下行笔画。",
    ),
    "obs-char-000274": (
        "The tall dark image has a narrow irregular upper cluster, a long central "
        "stem, a rectangular middle block, and a flaring lower terminal.",
        "高而深色的图像有狭长不规则上部簇，中部有长笔干和矩形块状形体，下部向外展开收笔。",
    ),
    "obs-char-000275": (
        "The small image shows a compact dark upper cluster with short angled marks "
        "and a long slender stroke descending along the right.",
        "小型图像上部有紧密深色簇和短折角痕迹，右侧有一道长而纤细的下行笔画。",
    ),
    "obs-char-000276": (
        "The narrow image contains several short angular branches around a thin "
        "descending stroke; the lower tip tapers and remains irregular.",
        "狭长图像有数处分布在细下行笔画周围的短折角分支，下端渐细且轮廓不规则。",
    ),
    "obs-char-000277": (
        "The image shows a rounded upper outline with interior marks, followed by a "
        "long narrow lower stem crossed by short diagonal strokes.",
        "图像上部有带内部痕迹的圆弧轮廓，下方接长而狭窄的笔干，并有短斜向交叉笔画。",
    ),
    "obs-char-000278": (
        "The image has two upright sides joined by a low U-shaped base and a short "
        "horizontal bar; the right upper end is rounded and dark.",
        "图像有两道直立侧笔连接低位 U 形底部，并有短横画；右上端呈圆钝深色。",
    ),
    "obs-char-000279": (
        "The image shows a low outlined base with two upright supports, a small "
        "enclosed middle block, and a central upper stem with a rounded terminal.",
        "图像有低位外框底部和两道直立支撑，中部有小型闭合块状形体，中央向上伸出带圆钝末端的笔干。",
    ),
    "obs-char-000280": (
        "The image has an angular curved outline on the left with a small internal "
        "opening, plus a separate descending stroke on the right.",
        "图像左侧有带小型内部开口的折角弧形轮廓，右侧另有分离的下行笔画。",
    ),
    "obs-char-000281": (
        "The image has a large slanted rounded contour on the right, crossed by a "
        "descending stroke, with small separated marks at the left and lower right.",
        "图像右侧有大型倾斜弧形轮廓，中部有下行笔画穿过，左侧和右下方另有分离的小痕迹。",
    ),
    "obs-char-000282": (
        "The compact image shows a small curved enclosure with a dark lower base, "
        "a short branching mark above, and an open extension toward the right.",
        "紧凑图像有小型弧形闭合轮廓和较深的下部底线，上方有短分支痕迹，右侧留有开放延伸。",
    ),
    "obs-char-000283": (
        "The narrow image has a long upper horizontal stroke, a small lower-left "
        "enclosure with an inner bar, and a long descending stroke at the right.",
        "狭长图像上方有长横画，下方左侧有带内横画的小型闭合轮廓，右侧有长下行笔画。",
    ),
    "obs-char-000284": (
        "The image combines a small rounded bowl-like mark on the left with a "
        "larger angular upright form on the right and a long diagonal lower stroke.",
        "图像左侧有小型圆弧碗状痕迹，右侧有较大的折角直立形体，下方延伸长斜向笔画。",
    ),
    "obs-char-000285": (
        "The narrow dark image contains adjoining upright and branching strokes, "
        "with short cross marks near the upper middle and split strokes below.",
        "狭窄深色图像含相邻的直立和分支笔画，中上部有短横向痕迹，下方有分开的笔画。",
    ),
    "obs-char-000286": (
        "The image shows a rounded U-like enclosure with upright side strokes, a "
        "low horizontal base, and a short horizontal mark inside.",
        "图像有圆弧 U 形轮廓和直立侧笔，底部为低位横画，内部另有短横向痕迹。",
    ),
    "obs-char-000287": (
        "The thin image has a long upright stroke at the left, a small angular mark "
        "near its upper end, and a separate rounded enclosure on the right.",
        "纤细图像左侧有长直立笔画，上端附近有小型折角痕迹，右侧另有分离的圆弧轮廓。",
    ),
    "obs-char-000288": (
        "The image has a broad rounded outer contour with a pointed upper tip and "
        "a short diagonal interior mark; a small side stroke is also visible.",
        "图像有宽大的圆弧外轮廓和尖状上端，内部有短斜向痕迹，侧边还可见一处小笔画。",
    ),
    "obs-char-000289": (
        "The image shows two adjoining dark block-like enclosures, each with a "
        "narrow vertical interior strip and a slightly irregular lower edge.",
        "图像显示两个相邻的深色块状闭合轮廓，各自带有狭窄的内部竖向条痕，下缘略不规则。",
    ),
    "obs-char-000290": (
        "The compact image has an upper rounded arch and a lower rounded enclosure "
        "with a short horizontal interior mark, separated by a narrow gap.",
        "紧凑图像上部为圆弧拱形，下部为带短内横画的圆弧闭合轮廓，中间有狭窄间隔。",
    ),
    "obs-char-000291": (
        "The image has a rounded lower enclosure, an interior upright mark rising "
        "to a pointed top, and a curved outer stroke around the upper area.",
        "图像下部有圆弧闭合轮廓，内部竖向痕迹向上延伸至尖端，上部外围有弧形笔画。",
    ),
    "obs-char-000292": (
        "The tall image contains a narrow rectangular framework with horizontal "
        "cross strokes and a small rounded enclosure at the lower end.",
        "高而狭的图像含窄长框架和数道横向交叉笔画，下端有小型圆弧闭合轮廓。",
    ),
    "obs-char-000293": (
        "The image has a large curved enclosing stroke on the left and a separate "
        "rounded lower form on the right, joined by a short horizontal mark.",
        "图像左侧有大型弧形包围笔画，右侧有分离的圆弧下部形体，两者由短横向痕迹相接。",
    ),
    "obs-char-000294": (
        "The narrow image shows a long angled upper stroke, a descending side line, "
        "and a small lower enclosure containing a short horizontal mark.",
        "狭长图像有长斜向上部笔画和下行侧线，下部有带短内横画的小型闭合轮廓。",
    ),
    "obs-char-000295": (
        "The dark image contains a slim central vertical cluster, short side bars, "
        "and several forked or crossing strokes toward the lower end.",
        "深色图像含纤细的中央竖向簇、短侧向横痕，以及下端附近数处分叉或交叉笔画。",
    ),
    "obs-char-000296": (
        "The image has a broad peaked outer contour with sloping side strokes and "
        "a small rounded enclosure with an inner horizontal mark.",
        "图像有宽大的尖顶外轮廓和倾斜侧笔，内部有带内横画的小型圆弧闭合轮廓。",
    ),
    "obs-char-000297": (
        "The image consists of two vertically stacked rounded rectangular outlines "
        "with a narrow gap and no clearly visible interior mark.",
        "图像由上下叠置的两个圆角长方形轮廓组成，中间有狭窄间隔，未见清楚的内部痕迹。",
    ),
    "obs-char-000298": (
        "The narrow image contains several branching upright strokes and a lower "
        "rounded enclosure with a short horizontal interior mark.",
        "狭长图像含数道分支直立笔画，下部有带短内横画的圆弧闭合轮廓。",
    ),
    "obs-char-000299": (
        "The image has a large peaked outer angle, nested sloping strokes, and a "
        "small lower rounded enclosure with a short inner bar.",
        "图像有大型尖顶折角外轮廓和嵌套的斜向笔画，下部有带短内横画的小型圆弧闭合轮廓。",
    ),
    "obs-char-000300": (
        "The low-contrast gray image shows several short slanting marks at the left "
        "and a small rounded enclosure at the right; contrast needs recheck.",
        "低对比度灰色图像左侧有数道短斜向痕迹，右侧有小型圆弧闭合轮廓；对比度仍需复核。",
    ),
    "obs-char-000301": (
        "The image shows paired pointed upper strokes, curved enclosing sides, "
        "and a separate broad curved base with interior crossing marks.",
        "图像上方有成对尖状笔画，两侧呈弧形围合，下方另有宽弧形底部，内部可见交叉痕迹。",
    ),
    "obs-char-000302": (
        "The image has a tall right-side stem, a small upper rectangular enclosure, "
        "and a separate rounded lower enclosure.",
        "图像右侧有高直主干，上方有小型方形闭合轮廓，下方另有圆弧闭合轮廓。",
    ),
    "obs-char-000303": (
        "A long descending central stroke is joined to a rounded right enclosure; "
        "a curved lower tail extends to the left.",
        "图像中部有长下行笔画并连接右侧圆弧闭合轮廓，下方有向左弯曲的尾部。",
    ),
    "obs-char-000304": (
        "The image combines a small left enclosure with a taller branching upright "
        "form and a pointed descending lower stroke.",
        "图像左侧有小型闭合轮廓，右侧为较高的分叉直立形体，下方有尖状下行笔画。",
    ),
    "obs-char-000305": (
        "The image has paired upper horizontal strokes, a narrow crossed middle, "
        "and a broad rounded lower enclosure.",
        "图像上方有成对横向笔画，中部狭窄且相交，下方有宽大的圆弧闭合轮廓。",
    ),
    "obs-char-000306": (
        "The dark image shows a compact angular upper cluster, a descending diagonal "
        "stroke, and curved lower strokes extending to both sides.",
        "深色图像上部为紧凑折角笔画群，中部有下行斜笔画，下方弧形笔画向两侧伸展。",
    ),
    "obs-char-000307": (
        "The image has an open tall frame with two uprights, branching central marks, "
        "and a curved lower base.",
        "图像有开放的高框架和两侧直笔画，中部有分叉痕迹，下方有弧形底部。",
    ),
    "obs-char-000308": (
        "A broad rectangular framework contains two horizontal internal bars, with "
        "long side strokes descending below its lower edge.",
        "图像呈宽方形框架，内部有两道横向笔画，两侧长笔画从下缘向下延伸。",
    ),
    "obs-char-000309": (
        "The small light image shows a thin descending curved stroke, a short upper "
        "mark, and a detached curved mark at the right.",
        "浅色小图像有纤细下行弧笔画、上方短痕迹，右侧另有分离的弧形痕迹。",
    ),
    "obs-char-000310": (
        "The image shows a large U-like curved stroke and a detached small angular "
        "mark near the upper right.",
        "图像有大型 U 形弧曲笔画，右上方另有分离的小型折角痕迹。",
    ),
    "obs-char-000311": (
        "A tall central vertical stroke has an upper branching cross form, a small "
        "left lower enclosure, and a short horizontal foot.",
        "图像有高直中轴，上方为分叉交叉形，左下方有小型闭合轮廓，底部有短横笔画。",
    ),
    "obs-char-000312": (
        "The image contains three small rounded enclosure-like forms arranged across "
        "the upper and lower portions.",
        "图像含三个小型圆弧闭合形体，分布在上部和下部不同位置。",
    ),
    "obs-char-000313": (
        "A broad arched enclosure spans the middle, with a small upper enclosure and "
        "several pointed strokes descending from the lower edge.",
        "图像中部为宽拱形闭合轮廓，上方有小型闭合轮廓，下缘向下伸出数道尖状笔画。",
    ),
    "obs-char-000314": (
        "The image has a tall central stem with branching upper strokes, small side "
        "enclosures, and a pointed lower extension.",
        "图像有高直中干和上部分叉笔画，两侧有小型闭合轮廓，下方有尖状延伸。",
    ),
    "obs-char-000315": (
        "The rounded outer form contains horizontal and vertical interior marks, "
        "with a branching top and a small lower enclosure.",
        "图像外部呈圆弧形，内部有横竖痕迹，上方分叉，下方有小型闭合轮廓。",
    ),
    "obs-char-000316": (
        "The image combines a small left rounded form with a tall angular right form, "
        "crossing central strokes, and a hooked lower curve.",
        "图像左侧有小型圆弧形体，右侧为高直折角形体，中部笔画相交，下方有钩状弧笔画。",
    ),
    "obs-char-000317": (
        "A curved upper stroke and small left enclosure accompany a long branching "
        "stroke descending along the right side.",
        "图像上方有弧形笔画和左侧小型闭合轮廓，右侧有长分叉笔画向下延伸。",
    ),
    "obs-char-000318": (
        "The image has a long upper horizontal stroke, a central inverted-angle form, "
        "and pointed strokes descending at both sides.",
        "图像上方有长横笔画，中部为倒折角形体，两侧向下伸出尖状笔画。",
    ),
    "obs-char-000319": (
        "Two tall side frameworks flank a small rounded lower enclosure, with short "
        "horizontal and vertical interior marks.",
        "图像两侧有高直框架，中部下方为小型圆弧闭合轮廓，内部有短横竖痕迹。",
    ),
    "obs-char-000320": (
        "The image has a peaked outer contour, a central descending stroke, and a "
        "rounded lower enclosure; the small image needs detail recheck.",
        "图像有尖顶外轮廓、中部下行笔画和下方圆弧闭合轮廓；图像较小，细节仍需复核。",
    ),
    "obs-char-000321": (
        "The tall image has left branching strokes, a right rectangular enclosure, "
        "and a separate rounded lower enclosure.",
        "高直图像左侧有分叉笔画，右侧有方形闭合轮廓，下方另有圆弧闭合轮廓。",
    ),
    "obs-char-000322": (
        "A large dark rounded upper cluster sits on a long vertical stroke; smaller "
        "rounded marks flank it, with a crossbar and lower descending stroke.",
        "大型深色圆弧上部形体位于长直笔画之上，两侧有较小圆弧痕迹，下面有横笔画和下行笔画。",
    ),
    "obs-char-000323": (
        "The image has a central branching vertical stroke, a small oval enclosure, "
        "and a broad curved base with an irregular lower edge.",
        "图像中部有分叉直笔画和小型椭圆闭合轮廓，下方有宽弧形底部，底缘不规则。",
    ),
    "obs-char-000324": (
        "A central upright form is flanked by a small left detached enclosure and "
        "curved branching strokes on the right.",
        "图像中部为直立形体，左侧有分离的小型闭合轮廓，右侧有弧形分叉笔画。",
    ),
    "obs-char-000325": (
        "The image has central crossed and branching strokes, several small detached "
        "rounded marks, and a long descending central line.",
        "图像中部笔画交叉并分叉，周围有数个分离的圆弧痕迹，中部有长下行线条。",
    ),
    "obs-char-000326": (
        "Two rounded terminal forms are joined by an upper horizontal stroke, with a "
        "single central vertical stroke descending below.",
        "上方两个圆弧末端形体由横笔画连接，中部有一条直笔画向下延伸。",
    ),
    "obs-char-000327": (
        "The image shows upper branching strokes, two rounded lower loops, and a "
        "central vertical stem.",
        "图像上部有分叉笔画，下方有两个圆弧环状形体，中部为直立主干。",
    ),
    "obs-char-000328": (
        "A small upper left enclosure and a tall upper right angular stroke sit above "
        "a dense lower cluster of horizontal and vertical marks.",
        "上方左侧有小型闭合轮廓，右侧有高直折角笔画，下方是密集的横竖痕迹群。",
    ),
    "obs-char-000329": (
        "The dark image has a thick central rounded enclosure, a pointed left upper "
        "stroke, and a long curved stroke descending on the right.",
        "深色图像中部有厚重圆弧闭合轮廓，左上有尖状笔画，右侧有长弧形下行笔画。",
    ),
    "obs-char-000330": (
        "The large dark composite form contains an upper angular mass, a central "
        "rectangular enclosure, and several curved lower strokes.",
        "大型深色复合形体含上部折角形体、中部方形闭合轮廓和数道下部弧形笔画。",
    ),
    "obs-char-000331": (
        "A central tall form with a pointed top is surrounded by four small detached "
        "rounded marks and a middle enclosure.",
        "中部高直形体顶部尖突，周围有四个分离的小型圆弧痕迹，中部另有闭合轮廓。",
    ),
    "obs-char-000332": (
        "The image has a small upper triangular enclosure, a long curved descending "
        "stroke, and a rounded lower enclosure.",
        "图像上方有小型三角闭合轮廓，右侧有长弧形下行笔画，下方有圆弧闭合轮廓。",
    ),
    "obs-char-000333": (
        "The tall rectangular enclosure contains one long interior vertical stroke "
        "with a slight diagonal change.",
        "高直方形闭合轮廓内部有一条长直笔画，并在中部略有斜向变化。",
    ),
    "obs-char-000334": (
        "The image consists of four separated parallel horizontal strokes of "
        "different lengths.",
        "图像由四道分离的平行横笔画组成，四道笔画长短不同。",
    ),
    "obs-char-000335": (
        "A pointed diamond-like outer enclosure contains a central horizontal and "
        "vertical crossing structure.",
        "尖顶菱状外部闭合轮廓内部有横竖交叉结构。",
    ),
    "obs-char-000336": (
        "A thin central vertical stroke is flanked by two outward curved forms and a "
        "small rounded mark at the top.",
        "纤细中部直笔画两侧有向外弯曲的形体，顶部另有小型圆弧痕迹。",
    ),
    "obs-char-000337": (
        "The broad rounded outer contour contains several dark internal rounded marks "
        "and an irregular lower crossing area.",
        "宽大的圆弧外轮廓内部有数个深色圆弧痕迹，下部有不规则交叉区域。",
    ),
    "obs-char-000338": (
        "The rectangular outer frame contains branching central strokes and a short "
        "lower diagonal mark.",
        "方形外框内部有中部的分叉笔画和下方短斜向痕迹。",
    ),
    "obs-char-000339": (
        "The low-contrast gray image shows a compact dark rounded cluster at the left "
        "and a detached curved stroke at the right; contrast needs recheck.",
        "低对比度灰色图像左侧有紧凑深色圆弧笔画群，右侧有分离的弧形笔画；对比度仍需复核。",
    ),
    "obs-char-000340": (
        "The large rectangular grid contains multiple internal horizontal and vertical "
        "divisions with irregular lower marks.",
        "大型方形格状轮廓内部有多道横竖分隔笔画，下部痕迹不规则。",
    ),
    "obs-char-000341": (
        "The rectangular outer enclosure contains central diagonal and vertical "
        "strokes with small upper and lower extensions.",
        "方形外部闭合轮廓内部有中部斜竖笔画，并带有上下方的小型延伸。",
    ),
    "obs-char-000342": (
        "The tall narrow enclosure contains a central oval-like form and a short "
        "right-side projection.",
        "高直狭长闭合轮廓内部有中部椭圆状形体，右侧有短向外伸出。",
    ),
    "obs-char-000343": (
        "The tall rectangular frame contains a central diamond-like enclosure and "
        "short horizontal divisions.",
        "高直方形框架内部有中部菱状闭合轮廓和数道短横分隔笔画。",
    ),
    "obs-char-000344": (
        "A broad rounded upper enclosure sits above three branching lower strokes "
        "with short side projections.",
        "宽大的圆弧上部闭合轮廓下方有三道分叉笔画，并带有短侧向伸出。",
    ),
    "obs-char-000345": (
        "The pointed diamond-like enclosure stands on a long horizontal base stroke "
        "with a slightly uneven edge.",
        "尖顶菱状闭合轮廓立于长横底部笔画之上，底缘略有不平。",
    ),
    "obs-char-000346": (
        "A narrow pointed central form has a short horizontal cross stroke and a "
        "flared lower point.",
        "狭长尖状中部形体有短横交叉笔画，下方形成展开的尖状末端。",
    ),
    "obs-char-000347": (
        "The image has a tall pointed upper outline, a small rounded lower enclosure, "
        "and a short base stroke.",
        "图像上方为高直尖顶轮廓，下方有小型圆弧闭合轮廓和短底部笔画。",
    ),
    "obs-char-000348": (
        "The large rounded outer contour contains a tall branching central stroke and "
        "several detached short marks; the dark image needs recheck.",
        "大型圆弧外轮廓内部有高直分叉中轴和数个分离短痕迹；深色图像仍需复核。",
    ),
    "obs-char-000349": (
        "A slim curved upper stroke descends into two adjoining angular lower forms "
        "with a small pointed top.",
        "纤细弧形上部笔画向下连接两个相邻折角形体，顶部有小型尖状部分。",
    ),
    "obs-char-000350": (
        "A tall central stem branches widely to both sides and ends in a rounded lower "
        "enclosure, with many short side strokes.",
        "高直中轴向两侧大幅分叉，下端为圆弧闭合轮廓，周围有许多短侧向笔画。",
    ),
    "obs-char-000351": (
        "The dense image contains overlapping angular enclosures, crossing strokes, "
        "and a pointed lower-left extension.",
        "密集图像含相互重叠的折角闭合轮廓、交叉笔画和左下方尖状延伸。",
    ),
    "obs-char-000352": (
        "Three separated upright forms are visible, with short horizontal or branching "
        "marks near their upper and lower sections.",
        "图像可见三个分离的直立形体，上下部附近有短横或分叉痕迹。",
    ),
    "obs-char-000353": (
        "The narrow image has a slanting branched upper stroke, a curved lower stroke, "
        "and a short left-side projection.",
        "狭长图像上方有斜向分叉笔画，下方有弧形笔画，左侧有短向外伸出。",
    ),
    "obs-char-000354": (
        "A central pointed enclosure is crossed by a short horizontal stroke and joined "
        "to a thin lower stem.",
        "中部尖状闭合轮廓被短横笔画穿过，并连接下方纤细主干。",
    ),
    "obs-char-000355": (
        "The image has a broad rounded lower enclosure, a central descending stroke, "
        "and short side strokes beneath a small upper bar.",
        "图像下部有宽圆弧闭合轮廓，中部有下行笔画，上方小横笔画下有短侧向痕迹。",
    ),
    "obs-char-000356": (
        "The low-contrast gray image shows a slim branching stroke and a separate long "
        "right-side mark; contrast needs recheck.",
        "低对比度灰色图像有纤细分叉笔画，右侧另有长痕迹；对比度仍需复核。",
    ),
    "obs-char-000357": (
        "The dark image has a broad upper horizontal stroke, a central rounded mark, "
        "and long branching strokes descending below.",
        "深色图像上方有宽横笔画，中部有圆弧痕迹，下方有长分叉笔画向下延伸。",
    ),
    "obs-char-000358": (
        "A thin central stem is flanked by two small pointed upper forms and a long "
        "curved lower extension.",
        "纤细中部主干两侧有两个小型尖状上部形体，下方有长弧形延伸。",
    ),
    "obs-char-000359": (
        "The roof-like outer contour contains several short interior strokes and a "
        "small rounded lower mark.",
        "屋顶状外部轮廓内部有数道短笔画，下方有小型圆弧痕迹。",
    ),
    "obs-char-000360": (
        "A central rounded enclosure is crossed by horizontal and vertical strokes, "
        "with pointed forms extending in four directions.",
        "中部圆弧闭合轮廓被横竖笔画交叉，四个方向均有尖状形体延伸。",
    ),
    "obs-char-000361": (
        "A bold angular upper form is connected to a long vertical stroke and a "
        "small pointed lower enclosure.",
        "粗重的上部折角形体连接长竖笔画，下方接有小型尖状闭合轮廓。",
    ),
    "obs-char-000362": (
        "A short upper horizontal stroke sits above a compact central mark and a "
        "broad lower horizontal base.",
        "短上横笔画位于紧凑中部痕迹和宽下横底笔画之上。",
    ),
    "obs-char-000363": (
        "Two forked upper strokes rise over a small rectangular enclosure with two "
        "descending legs.",
        "两个分叉上行笔画位于小型矩形闭合轮廓之上，轮廓下有两条下行支脚。",
    ),
    "obs-char-000364": (
        "A compact rounded upper outline surrounds a central rectangular area, with "
        "side loops and a lower stem.",
        "紧凑的圆弧上部轮廓围出中央矩形区域，两侧有环状痕迹并连接下部主干。",
    ),
    "obs-char-000365": (
        "The small dark image shows a thin vertical trace with a pointed upper hook "
        "and an irregular lower cluster; recheck is needed.",
        "小幅深色图像显示纤细竖向痕迹、尖状上钩和不规则下部痕迹；需要复核。",
    ),
    "obs-char-000366": (
        "An angular pointed upper form is joined to a long slanting lower stroke and "
        "a short left branch.",
        "尖状折角上部形体连接长斜向下行笔画，左侧另有短分支。",
    ),
    "obs-char-000367": (
        "A thin central stem has several short diagonal branches and a forked upper "
        "end.",
        "纤细中央主干带有数个短斜向分支，上端呈分叉形。",
    ),
    "obs-char-000368": (
        "A narrow central stem carries a small enclosed upper mark, horizontal side "
        "strokes, and a curved lower extension.",
        "狭长中央主干上方有小型闭合痕迹，两侧有横向笔画，下方有弧形延伸。",
    ),
    "obs-char-000369": (
        "A curved leaf-like upper contour is joined to a thin stem with short side "
        "strokes and a pointed lower extension.",
        "弧形叶状上部轮廓连接纤细主干，两侧有短笔画，下方有尖状延伸。",
    ),
    "obs-char-000370": (
        "A large sweeping angular contour crosses a central vertical stroke and "
        "continues into several long curved descenders.",
        "大型弧折轮廓横跨中央竖笔画，并向下延伸出数条长弧形笔画。",
    ),
    "obs-char-000371": (
        "A thin vertical form has a hooked upper contour, short cross-strokes, and a "
        "forked lower extension.",
        "纤细竖向形体有钩状上部轮廓、短横笔画和分叉下部延伸。",
    ),
    "obs-char-000372": (
        "A broad lower enclosure is topped by a short horizontal stroke and a "
        "separate long upper mark.",
        "宽大的下部闭合轮廓上方有短横笔画，另有一条较长上部痕迹。",
    ),
    "obs-char-000373": (
        "A vertical upper stroke branches into a left pointed enclosure and several "
        "long lower strokes.",
        "上部竖笔画分出左侧尖状闭合轮廓，并向下连接数条长笔画。",
    ),
    "obs-char-000374": (
        "Several close vertical strokes are crossed by short side branches and a "
        "pointed upper form.",
        "数条相近竖笔画被短侧向分支和尖状上部形体交叉。",
    ),
    "obs-char-000375": (
        "A pointed upper fork opens into two long descending strokes with a narrow "
        "central line.",
        "尖状上部分叉向下展开为两条长下行笔画，中间有一条狭长笔画。",
    ),
    "obs-char-000376": (
        "A thin central stem branches into a pointed upper fork and two long side "
        "strokes.",
        "纤细中央主干分出尖状上部分叉和两条长侧向笔画。",
    ),
    "obs-char-000377": (
        "A short upper horizontal bar sits above a central stem, side branches, and "
        "an open angular lower form.",
        "短上横笔画位于中央主干、侧向分支和开放折角下部形体之上。",
    ),
    "obs-char-000378": (
        "A bold central vertical stroke branches into two sweeping upper arms and a "
        "large open lower curve; a separate short lower mark is visible.",
        "粗重中央竖笔画分出两条弧形上臂和大型开放下部曲线；下方另见短痕迹。",
    ),
    "obs-char-000379": (
        "A small upper crossbar and central stem lead to side branches and two narrow "
        "lower strokes.",
        "小型上部横笔画和中央主干连接侧向分支及两条狭长下部笔画。",
    ),
    "obs-char-000380": (
        "A curved hook-like upper contour continues into a thin vertical lower stroke.",
        "弧形钩状上部轮廓继续连接纤细竖向下行笔画。",
    ),
    "obs-char-000381": (
        "A central vertical stroke meets a short cross-stroke, a long right branch, "
        "and two diverging lower strokes beneath paired upper tips.",
        "中央竖笔画与短横笔画和长右向分支相接，上方有成对尖端，下方有两条分行笔画。",
    ),
    "obs-char-000382": (
        "An open rectangular upper outline sits above a central junction with three "
        "thin descending strokes.",
        "开放矩形上部轮廓位于中央交接点之上，下方有三条纤细下行笔画。",
    ),
    "obs-char-000383": (
        "A bold central loop twists between two upper branches and a long lower "
        "vertical extension.",
        "粗重中央环状笔画在两个上部分支与长竖向下部延伸之间扭转交接。",
    ),
    "obs-char-000384": (
        "A long central vertical stroke passes through two overlapping rectangular "
        "outlines and ends in a short lower zigzag.",
        "长中央竖笔画穿过两个重叠矩形轮廓，下端接短折线。",
    ),
    "obs-char-000385": (
        "A forked upper stem sits above a peaked open outline and a short crooked "
        "central mark.",
        "分叉上部主干位于尖顶开放轮廓之上，轮廓内有短曲折中央痕迹。",
    ),
    "obs-char-000386": (
        "A central pointed enclosure is flanked by long descending strokes and "
        "topped by a narrow fork.",
        "中央尖状闭合轮廓两侧有长下行笔画，上方接狭窄分叉。",
    ),
    "obs-char-000387": (
        "The image contains two separated dark forms: a branching angular form at "
        "left and a U-shaped upper contour with a long stem at right.",
        "图像含两个分离的深色形体：左侧为分支折角形，右侧为带长主干的 U 状上部轮廓。",
    ),
    "obs-char-000388": (
        "A thin central stem is crossed by several short angled branches, with "
        "multiple narrow descenders.",
        "纤细中央主干被数个短斜向分支交叉，并有多条狭窄下行笔画。",
    ),
    "obs-char-000389": (
        "Two separated forms are visible: an upper forked stem with side branches "
        "and a detached lower V-shaped loop.",
        "可见两个分离形体：上方为带侧向分支的分叉主干，下方为独立 V 状环形轮廓。",
    ),
    "obs-char-000390": (
        "A thin looping central trace has a small hooked top and two long diverging "
        "lower strokes.",
        "纤细环曲中央痕迹上端有小钩，下方有两条长分行笔画。",
    ),
    "obs-char-000391": (
        "A broad top bar caps a tapering enclosure with short internal cross-strokes, "
        "ending at a pointed base line.",
        "宽上横笔画覆盖逐渐收窄的闭合轮廓，内部有短横笔画，下端接尖点状底线。",
    ),
    "obs-char-000392": (
        "A tall branching form contains a rounded rectangular middle enclosure, a "
        "long central stem, and two levels of lower forks.",
        "高长分支形体中部有圆角矩形闭合轮廓，并有长中央主干和两层下部分叉。",
    ),
    "obs-char-000393": (
        "A central roof-like outline and vertical stem are flanked by two small "
        "detached curled marks.",
        "中央屋顶状轮廓和竖向主干两侧各有一个分离的小型卷曲痕迹。",
    ),
    "obs-char-000394": (
        "A thin curved outline contains a pointed side enclosure, with a separate "
        "narrow right-side trace; contrast needs recheck.",
        "纤细弧形轮廓含尖状侧部闭合形，右侧另有狭窄痕迹；对比度需要复核。",
    ),
    "obs-char-000395": (
        "Several dark curved and diagonal strokes cross around a narrow central loop.",
        "数条深色弧形和斜向笔画围绕狭窄中央环形痕迹交叉。",
    ),
    "obs-char-000396": (
        "Two similar separated forms each show an upper crossing, a small rectangular "
        "loop, and an angular lower descender.",
        "两个相似的分离形体各有上部交叉、小矩形环形轮廓和折角下行笔画。",
    ),
    "obs-char-000397": (
        "A narrow vertical trace passes through a small upper loop and continues into "
        "a long angular lower stroke.",
        "狭窄竖向痕迹穿过小型上部环形轮廓，并继续连接长折角下部笔画。",
    ),
    "obs-char-000398": (
        "Two small upper enclosed marks connect to a long curved lower stroke and a "
        "short side branch.",
        "两个小型上部闭合痕迹连接长弧形下部笔画和短侧向分支。",
    ),
    "obs-char-000399": (
        "A thin central crossing is joined to an open pointed upper mark, a long "
        "right-side stroke, and irregular lower curves.",
        "纤细中央交叉连接开放尖状上部痕迹、长右侧笔画和不规则下部曲线。",
    ),
    "obs-char-000400": (
        "The image contains a compact hooked and looped form at left and a detached "
        "capped vertical stroke at right.",
        "图像左侧有紧凑钩曲环形形体，右侧有分离的带横帽竖笔画。",
    ),
    "obs-char-000401": (
        "Two adjacent clusters are visible: a crossed grid-like group at left and a "
        "looping vertical group with a zigzag lower end at right.",
        "可见两个相邻笔画群：左侧为交叉网格状笔画，右侧为下端折曲的环状竖向笔画群。",
    ),
    "obs-char-000402": (
        "A bold vertical trace crosses an upper rectangular arrangement, a middle "
        "oval enclosure, and a large angular lower loop.",
        "粗重竖向痕迹穿过上部矩形组合、中部椭圆闭合轮廓和大型折角下部环形轮廓。",
    ),
    "obs-char-000403": (
        "A thin left cluster of curved and angled strokes stands beside a tall right "
        "stem crossed by two short bars.",
        "左侧纤细弧折笔画群与右侧高长主干并列，右侧主干被两条短横笔画穿过。",
    ),
    "obs-char-000404": (
        "Two separated tall forms are visible: a crossed loop-and-angle form at left "
        "and a vertical form with two angular side bends at right.",
        "可见两个分离的高长形体：左侧为交叉环折形，右侧为带两个侧向折角的竖向形体。",
    ),
    "obs-char-000405": (
        "A small detached circular enclosure with a central mark sits left of a "
        "separate looping and zigzag form.",
        "带中央痕迹的小型分离圆形轮廓位于左侧，右侧另有独立的环曲折线形体。",
    ),
    "obs-char-000406": (
        "A thin curved vertical trace passes through a small central loop and "
        "continues into a lower zigzag.",
        "纤细弧形竖向痕迹穿过小型中央环形轮廓，并继续连接下部折线。",
    ),
    "obs-char-000407": (
        "Two separated forms are visible: a compact looped angular form at left and "
        "a forked vertical stem with short branches at right.",
        "可见两个分离形体：左侧为紧凑环折形，右侧为带短分支的分叉竖向主干。",
    ),
    "obs-char-000408": (
        "The image contains a narrow capped loop at left and a larger crossed "
        "enclosure with a long angular lower extension at right.",
        "图像左侧有狭窄带横帽环形轮廓，右侧有较大交叉闭合形和长折角下部延伸。",
    ),
    "obs-char-000409": (
        "Two dark separated forms are visible: a divided oval with a hooked lower "
        "stroke at left and a forked branching stem at right.",
        "可见两个深色分离形体：左侧为带下钩的分隔椭圆，右侧为分叉分支主干。",
    ),
    "obs-char-000410": (
        "A thin vertical trace crosses a small upper rectangular loop and continues "
        "through several sharp lower bends; contrast needs recheck.",
        "纤细竖向痕迹穿过小型上部矩形环形轮廓，并连接数个尖折下部笔画；对比度需要复核。",
    ),
    "obs-char-000411": (
        "Several thin branching, looping, and diagonal strokes overlap around two "
        "close vertical stems.",
        "数条纤细分支、环曲和斜向笔画围绕两条相近竖向主干重叠。",
    ),
    "obs-char-000412": (
        "A thin left stem with short branches stands beside a looping right form with "
        "upper prongs and angular lower strokes.",
        "带短分支的纤细左侧主干与右侧环曲形体并列，右侧有上部分叉和折角下部笔画。",
    ),
    "obs-char-000413": (
        "A broad open triangular top narrows into small central loops and a long "
        "angular lower extension.",
        "宽大开放三角形上部向下收窄为小型中央环形笔画，并连接长折角下部延伸。",
    ),
    "obs-char-000414": (
        "Two separated forms are visible: a crossed rectangular cluster at left and "
        "a tall curved form with an upper enclosure at right.",
        "可见两个分离形体：左侧为交叉矩形笔画群，右侧为带上部闭合轮廓的高长弧形形体。",
    ),
    "obs-char-000415": (
        "The small low-contrast image contains several separated marks, including an "
        "upper open rectangle, a crossed loop, and lower angled traces; contrast "
        "needs recheck.",
        "小幅低对比度图像含数个分离痕迹，包括上部开放矩形、交叉环形和下部折角痕迹；"
        "对比度需要复核。",
    ),
    "obs-char-000416": (
        "A detached small square and forked mark at left stand beside a larger looped, "
        "crossed, and angular form at right.",
        "左侧分离的小方形和分叉痕迹与右侧较大的环曲、交叉、折角形体并列。",
    ),
    "obs-char-000417": (
        "A narrow central diagonal form combines a small upper loop, a right forked "
        "stem, and several lower angular strokes.",
        "狭窄中央斜向形体连接小型上部环形、右侧分叉主干和数条下部折角笔画。",
    ),
    "obs-char-000418": (
        "A broad curved outer stroke surrounds a compact central enclosure and "
        "several thin upper marks.",
        "宽大弧形外部笔画围绕紧凑中央闭合轮廓和数条纤细上部痕迹。",
    ),
    "obs-char-000419": (
        "Two separated bold forms are visible: a capped rectangular cross at left "
        "and a large crossed upper loop with an angular lower extension at right.",
        "可见两个粗重分离形体：左侧为带横帽矩形交叉，右侧为大型交叉上部环形及折角下部延伸。",
    ),
    "obs-char-000420": (
        "Several stacked zigzag strokes form a narrow vertical cluster with pointed "
        "upper tips and short internal crossings.",
        "数条层叠折线组成狭窄竖向笔画群，上端有尖状笔画，内部有短交叉。",
    ),
    "obs-char-000421": (
        "Two bold forms appear side by side: the left has a rectangular lower frame, "
        "while the right has crossed central strokes and an angular lower extension.",
        "两个粗重形体左右并列：左侧下部为矩形框架，右侧中央笔画交叉并向下折角延伸。",
    ),
    "obs-char-000422": (
        "The small image shows two narrow upright forms and a detached short horizontal "
        "stroke near the lower left; fine strokes are difficult to resolve.",
        "小图中可见两个狭长直立形体，左下另有一短横；细笔画因分辨率较低而难以辨清。",
    ),
    "obs-char-000423": (
        "Two compact upright forms are separated by white space; each combines angular "
        "outer strokes with small enclosed or crossing areas.",
        "两个紧凑直立形体以空白分隔，均由折角外轮廓和小型闭合或交叉区域组成。",
    ),
    "obs-char-000424": (
        "Two small stacked box-like marks at left stand apart from a taller narrow form "
        "at right with crossing and angled strokes.",
        "左侧两个小型层叠框状痕迹与右侧较高狭长形体分离，右侧可见交叉和斜折笔画。",
    ),
    "obs-char-000425": (
        "Two bold separated forms are visible: a sinuous crossed form at left and a "
        "tall pointed outline on a short base at right.",
        "可见两个粗重分离形体：左侧为曲折交叉形，右侧为立于短底线上的高尖轮廓。",
    ),
    "obs-char-000426": (
        "Two bold forms are separated: the left is a four-armed crossed figure with "
        "outlined ends, and the right has crossed upper strokes and an angular lower loop.",
        "两个粗重形体彼此分离：左侧为四向交叉且末端带轮廓，右侧上部交叉、下部呈折角环曲。",
    ),
    "obs-char-000427": (
        "The small image contains two narrow upright forms; the left is tightly twisted, "
        "and the right has a central crossing and forked lower strokes.",
        "小图包含两个狭长直立形体：左侧紧密扭曲，右侧中央交叉且下部笔画分叉。",
    ),
    "obs-char-000428": (
        "A detached left cluster has two long upper strokes above a short bar, while a "
        "taller right cluster combines a central crossing with angled lower strokes.",
        "分离的左侧笔画群由短横及其上两条长笔画组成，右侧较高笔画群中央交叉、下部斜折。",
    ),
    "obs-char-000429": (
        "Several closely spaced narrow forms overlap visually; crossed upper strokes and "
        "multiple descending angled lines are visible, but boundaries are unclear.",
        "数个狭长形体间距很近并在视觉上重叠；可见上部交叉和多条下行斜线，边界不清。",
    ),
    "obs-char-000430": (
        "A single narrow vertical cluster contains several short transverse strokes, "
        "small internal crossings, and one thin descending tail.",
        "单个狭长竖向笔画群包含数条短横、若干内部交叉和一条纤细下垂尾笔。",
    ),
    "obs-char-000431": (
        "A large outer enclosure surrounds a smaller inner rectangle, with two separated "
        "forked or angled extensions descending from the lower sides.",
        "大型外部围框包围较小内矩形，下部两侧各有分离的分叉或折角延伸。",
    ),
    "obs-char-000432": (
        "A broad curved stroke crosses a central angular cluster; a separate hooked or "
        "bent extension descends toward the lower left.",
        "宽弧笔画穿过中央折角笔画群，另有钩曲或弯折延伸向左下方下垂。",
    ),
    "obs-char-000433": (
        "The very small image shows a narrow vertical form with short branching strokes "
        "near the top and a compact crossed cluster in the middle.",
        "极小图像显示狭长竖向形体，上部有短分支笔画，中部为紧凑交叉笔画群。",
    ),
    "obs-char-000434": (
        "Two adjacent upright forms are visible: the left has an upper crossing and curved "
        "lower stroke, while the right has a small boxed top and long descending lines.",
        "两个直立形体相邻：左侧上部交叉、下部弯曲，右侧顶部有小框并带长下行笔画。",
    ),
    "obs-char-000435": (
        "A gridded rectangular form at left is separated from a taller angular form at "
        "right with an upper crossing and a bent lower stroke.",
        "左侧网格状矩形与右侧较高折角形体分离，右侧上部交叉并有弯折下部笔画。",
    ),
    "obs-char-000436": (
        "The low-contrast narrow image shows a long curved vertical stroke with several "
        "short side branches and an angular bend near the lower middle.",
        "低对比度狭窄图像中可见一条长弯曲竖笔，带数条短侧枝，中下部有折角。",
    ),
    "obs-char-000437": (
        "Two irregular side clusters flank a central enclosed or crossed area; a broad "
        "curved stroke extends downward and bends to the right.",
        "两个不规则侧部笔画群夹着中央闭合或交叉区域，一条宽弧笔向下并折向右侧。",
    ),
    "obs-char-000438": (
        "A compact slanting cluster combines several small upper angular marks, a central "
        "crossing, and multiple narrow strokes descending from the lower edge.",
        "紧凑斜向笔画群由数个上部小折角、中央交叉和多条自下缘下垂的狭长笔画组成。",
    ),
    "obs-char-000439": (
        "A compact angular cluster at left connects or closely approaches a thin branching "
        "form at upper right; two long angled strokes descend below.",
        "左侧紧凑折角笔画群与右上纤细分支形体相接或紧邻，下方有两条长斜笔。",
    ),
    "obs-char-000440": (
        "The very small low-resolution image shows a dense irregular cluster with several "
        "short crossings and two longer slanting strokes along the right side.",
        "极小低分辨率图像显示密集不规则笔画群，内部有数处短交叉，右侧有两条较长斜笔。",
    ),
    "obs-char-000441": (
        "Two bold forms are separated by white space: the left combines an upper triangular "
        "area with a lower frame, while the right has crossed upper and angular lower strokes.",
        "两个粗重形体以空白分隔：左侧结合上部三角区域和下部框架，右侧上部交叉、下部折角。",
    ),
    "obs-char-000442": (
        "Two vertically separated clusters are visible: an upper crossed looping form with "
        "a bent tail, and a lower broad curve flanked by two branching strokes.",
        "可见两个上下分离的笔画群：上部为交叉环曲形及弯折尾笔，下部宽弧两侧各有分支笔画。",
    ),
    "obs-char-000443": (
        "The very small image shows a narrow vertical form with two stacked enclosed marks "
        "near the top, a curved middle stroke, and a thin angular tail.",
        "极小图像显示狭长竖向形体，顶部附近有两个层叠闭合痕迹，中部弯曲并带纤细折角尾笔。",
    ),
    "obs-char-000444": (
        "A dense branching cluster at left is separated from a smaller narrow zigzag form "
        "at right; several fine stroke boundaries are difficult to resolve.",
        "左侧密集分支笔画群与右侧较小狭长折线形分离，若干纤细笔画边界难以辨清。",
    ),
    "obs-char-000445": (
        "Two compact forms stand apart: the left has a long top bar and descending central "
        "stroke, while the right has a small upper enclosure and a bent lower extension.",
        "两个紧凑形体彼此分离：左侧有长顶横和中央下行笔画，右侧有小型上部围框及弯折下部延伸。",
    ),
    "obs-char-000446": (
        "Two narrow upright forms are separated; the left stacks a forked top, small box, "
        "and curved lower outline, while the right is crossed and sinuous.",
        "两个狭长直立形体彼此分离；左侧层叠分叉顶部、小框和弯曲下轮廓，右侧交叉且曲折。",
    ),
    "obs-char-000447": (
        "The low-contrast image contains two separated narrow forms: a crossed and curved "
        "form at left and a pointed outlined form at right.",
        "低对比度图像包含两个分离的狭长形体：左侧交叉弯曲，右侧为尖顶轮廓形。",
    ),
    "obs-char-000448": (
        "Three parallel vertical strokes stand above a rectangular enclosure crossed by "
        "two diagonals, with two short legs descending from its lower corners.",
        "三条平行竖笔位于矩形围框上方，框内有两条对角交叉，下方两角各伸出一条短腿。",
    ),
    "obs-char-000449": (
        "A single narrow form has a pointed outer loop enclosing crossed angular strokes, "
        "with a long curved line descending from the lower end.",
        "单个狭长形体外部为尖状环形，内部有交叉折角笔画，下端延伸出一条长弯曲线。",
    ),
    "obs-char-000450": (
        "The very small low-contrast image shows two similar separated forms, each with a "
        "small outlined top and two thin strokes descending at angles.",
        "极小低对比度图像显示两个相似分离形体，各有小型轮廓顶部和两条斜向下垂的细笔。",
    ),
    "obs-char-000451": (
        "An angled upper stroke connects to a small rectangular enclosure, with one short "
        "side branch and a narrow vertical extension below.",
        "上部斜向笔画连接小型矩形围框，侧面有一条短分支，下方为狭长竖向延伸。",
    ),
    "obs-char-000452": (
        "A central vertical stroke carries several alternating short branches, a small "
        "enclosed oval near the middle, and a pointed lower fork.",
        "中央竖笔两侧分布数条交替短枝，中部附近有小型椭圆围框，下端呈尖状分叉。",
    ),
    "obs-char-000453": (
        "A bold broad form has a leaf-shaped upper enclosure, crossed diagonal arms, a wide "
        "curved middle, a lower outlined area, and long outer descending strokes.",
        "粗重大型形体上部有叶状围框，中部斜臂交叉并呈宽弧，下方有轮廓区域及两条外侧长下行笔。",
    ),
    "obs-char-000454": (
        "A narrow upright form combines an angular open top, a small central enclosure, a "
        "short crossbar, and one long descending vertical stroke.",
        "狭长直立形体结合折角开口顶部、小型中央围框、短横和一条长下行竖笔。",
    ),
    "obs-char-000455": (
        "Two separated forms are visible: an oval-topped form on a forked curved stem at "
        "left, and a vertical looped form with a detached small diamond at right.",
        "可见两个分离形体：左侧椭圆顶部连接分叉弯曲主干，右侧竖向环曲并有分离的小菱形。",
    ),
    "obs-char-000456": (
        "A triangular upper outline sits above a rectangular lower enclosure at left; a "
        "separate long curved vertical stroke descends along the right side.",
        "左侧三角形上轮廓位于矩形下部围框之上，右侧另有一条分离的长弯曲竖笔下垂。",
    ),
    "obs-char-000457": (
        "The very narrow image shows three stacked marks: an upper crossing, a small central "
        "chevron, and a lower pointed arch with two long descending sides.",
        "极狭窄图像显示三个层叠痕迹：上部交叉、中央小折角，以及下部带两条长侧笔的尖拱形。",
    ),
    "obs-char-000458": (
        "A compact boxed and crossed cluster occupies the top of a narrow upright form, "
        "above two long parallel curved strokes and a shorter inner line.",
        "紧凑框状交叉笔画群位于狭长直立形体顶部，下方有两条长平行弯笔和一条较短内线。",
    ),
    "obs-char-000459": (
        "A broad arched stroke has a short central stem rising from its top and two long "
        "slightly curved strokes descending from the left and right ends.",
        "宽拱形笔画顶部中央伸出一条短竖，两端各有一条略弯的长笔向下延伸。",
    ),
    "obs-char-000460": (
        "Several long parallel vertical strokes form a narrow cluster, with two short "
        "horizontal bars crossing the central strokes at different heights.",
        "数条长平行竖笔组成狭窄笔画群，两条短横在不同高度穿过中央竖笔。",
    ),
    "obs-char-000461": (
        "A narrow pointed outer loop encloses several stacked angular and curved strokes, "
        "including a small upper division and a hooked lower cluster.",
        "狭长尖顶外环包围数条层叠折角和弯曲笔画，其中上部有小型分隔，下部为钩曲笔画群。",
    ),
    "obs-char-000462": (
        "The small low-contrast image shows an arched outer outline with several thin "
        "descending inner strokes; their lower boundaries are difficult to resolve.",
        "小型低对比度图像显示拱形外轮廓和数条纤细下行内笔，其下端边界难以辨清。",
    ),
    "obs-char-000463": (
        "A pointed arch formed by two long side strokes encloses a central crossing with "
        "one vertical and one transverse stroke.",
        "两条长侧笔组成尖拱形外轮廓，内部中央由一条竖笔和一条横向笔画交叉。",
    ),
    "obs-char-000464": (
        "An angular outer outline surrounds a compact curled inner cluster, with two long "
        "slightly curved strokes descending below the center.",
        "折角外轮廓围绕紧凑卷曲内笔画群，中央下方有两条略弯的长笔下垂。",
    ),
    "obs-char-000465": (
        "A pointed outer outline contains a compact crossed rectangular area and a curved "
        "lower extension; one short thin stroke projects from the lower left.",
        "尖顶外轮廓内有紧凑交叉矩形区域和弯曲下部延伸，左下另伸出一条短细笔。",
    ),
    "obs-char-000466": (
        "A leaf-shaped outer loop is divided by a central vertical stroke with short side "
        "branches, ending in a bold crossing below the loop.",
        "叶状外环由带短侧枝的中央竖笔分隔，竖笔在外环下方以粗重交叉收束。",
    ),
    "obs-char-000467": (
        "A broad angular arch with long vertical sides encloses a short bent stroke near "
        "the upper center and a detached short base below it.",
        "宽折角拱形带两条长竖侧笔，内部上中部有一条短弯笔，其下另有分离短底线。",
    ),
    "obs-char-000468": (
        "A pointed outer enclosure contains an upper transverse bar and several descending "
        "inner strokes, including a small open loop near the lower left.",
        "尖顶外围框内有上部横笔和数条下行内笔，左下附近另有小型开口环形。",
    ),
    "obs-char-000469": (
        "A pointed outline open along the bottom surrounds a central top bar and one long "
        "vertical stroke, with a shorter parallel stroke beside it.",
        "底部开口的尖顶轮廓包围中央顶横和一条长竖笔，其旁另有一条较短平行笔画。",
    ),
    "obs-char-000470": (
        "Separated pointed outer strokes surround a central elongated loop crossed by a "
        "diagonal line; a thin detached vertical stroke stands at left.",
        "分离的尖顶外部笔画围绕中央细长环形，环内有斜线交叉，左侧另立一条纤细分离竖笔。",
    ),
    "obs-char-000471": (
        "A narrow pointed outer outline encloses a small upper rectangle and several curved "
        "or branching lower strokes that meet near the bottom.",
        "狭长尖顶外轮廓内有小型上部矩形，数条弯曲或分支下部笔画在底部附近相接。",
    ),
    "obs-char-000472": (
        "A broad arched outer outline encloses an irregular inner form with an upper curve, "
        "a left angular branch, and two narrow descending strokes.",
        "宽拱形外轮廓包围不规则内形，其中有上部弧线、左侧折角分支和两条狭长下行笔画。",
    ),
    "obs-char-000473": (
        "A thin detached curved stroke at left stands beside a pointed outlined form at "
        "right that contains a small central enclosure and a long lower base.",
        "左侧纤细分离弯笔与右侧尖顶轮廓形并列，右形内部有小型中央围框和较长下底线。",
    ),
    "obs-char-000474": (
        "A broad polygonal arch surrounds a compact inner enclosure with a short upper bar "
        "and a squared lower outline.",
        "宽多折拱形围绕紧凑内围框，内形带一条短上横和方折下部轮廓。",
    ),
    "obs-char-000475": (
        "The low-contrast image shows a pointed outer outline, an upper internal crossing, "
        "a sinuous central vertical stroke, and a detached horizontal base below.",
        "低对比度图像显示尖顶外轮廓、上部内部交叉、曲折中央竖笔和下方分离横底线。",
    ),
    "obs-char-000476": (
        "A small low-resolution polygonal enclosure contains a divided rectangular area "
        "near the upper left; the outer lower edge is broad and nearly horizontal.",
        "小型低分辨率多边外围框在左上附近包围分隔矩形区域，外框下缘宽且近似水平。",
    ),
    "obs-char-000477": (
        "A large bold pointed arch encloses a long central horizontal bar, three short marks "
        "above it, and three separated vertical marks below.",
        "大型粗重尖拱形包围一条中央长横，其上有三处短痕，下方有三条分离竖向痕迹。",
    ),
    "obs-char-000478": (
        "A narrow pointed outer outline surrounds a branching inner cluster; one long thin "
        "stroke descends separately below the left side of the cluster.",
        "狭长尖顶外轮廓围绕分支内笔画群，一条长细笔从笔画群左下方分离下垂。",
    ),
    "obs-char-000479": (
        "Several separated long strokes suggest a broad pointed outer outline around a "
        "central crossed angular form, with additional curved strokes descending below.",
        "数条分离长笔构成宽尖顶外轮廓的可见片段，围绕中央交叉折角形，下方另有弯曲下行笔画。",
    ),
    "obs-char-000480": (
        "A pointed polygonal outer enclosure contains two separated inner outlines: a "
        "small rounded rectangular form above and a larger rectangular form below.",
        "尖顶多边外围框内有两个分离内轮廓：上部为小型圆角矩形，下部为较大矩形。",
    ),
    "obs-char-000481": (
        "A broad pointed upper outline surrounds a central vertical stroke crossed by "
        "several short horizontal or slanting bars; the outer sides remain partly separated.",
        "宽尖顶上部轮廓围绕中央竖笔，竖笔被数条短横或斜笔穿过，外侧笔画部分断离。",
    ),
    "obs-char-000482": (
        "A long horizontal stroke is crossed by two upward diagonals, while a central lower "
        "stem passes through an elongated loop and ends in a deep curved hook.",
        "长横被两条上行斜笔穿过，中央下部主干贯穿细长环形，并以深弯钩收尾。",
    ),
    "obs-char-000483": (
        "An irregular polygonal outer frame encloses several closely spaced parallel curved "
        "strokes descending from a shared upper area.",
        "不规则多边外框包围数条间距很近的平行弯曲笔画，这些笔画从共同上部区域向下延伸。",
    ),
    "obs-char-000484": (
        "A pointed outer outline encloses a central vertical stroke with two upper diagonal "
        "branches and shorter transverse strokes near the middle.",
        "尖顶外轮廓包围中央竖笔，竖笔上部有两条斜向分支，中部附近另有较短横向笔画。",
    ),
    "obs-char-000485": (
        "A detached pointed top and two long side strokes surround a central rectangular "
        "loop divided by one vertical inner line.",
        "分离尖顶和两条长侧笔围绕中央矩形环形，环内由一条竖线分隔。",
    ),
    "obs-char-000486": (
        "A narrow vertical form stacks a pointed upper loop with internal branches, a small "
        "lower diamond-shaped loop, and a forked crossing at the bottom.",
        "狭长竖向形体层叠尖顶上环及其内部分支、小型下部菱形环和底部叉状交叉。",
    ),
    "obs-char-000487": (
        "A pointed upper outline contains several detached short vertical marks and a curved "
        "inner stroke, with one long diagonal line descending from the lower right.",
        "尖顶上部轮廓内有数条分离短竖和一条弯曲内笔，右下伸出一条长斜线。",
    ),
    "obs-char-000488": (
        "A bold broad arch surrounds a smaller inner arch and several long parallel curved "
        "strokes that descend from its upper area.",
        "粗重宽拱形围绕较小内拱和数条长平行弯笔，这些弯笔从上部区域向下延伸。",
    ),
    "obs-char-000489": (
        "A thick outlined form has a rounded pointed top, two long outer sides, and a broad "
        "horizontal base, leaving a tall open central area.",
        "粗线轮廓形顶部圆钝而尖，两侧为长外笔，下部有宽横底线，中央留出高长空白。",
    ),
    "obs-char-000490": (
        "A large pointed arch encloses three separated inner groups: a small lower-left box, "
        "a curved central stem, and a long right vertical crossed by short bars.",
        "大型尖拱形包围三组分离内形：左下小框、中央弯曲主干，以及被短横穿过的右侧长竖。",
    ),
    "obs-char-000491": (
        "A bold pointed outer outline surrounds a central branching vertical stroke and "
        "several detached short marks, above a broad curved lower base.",
        "粗重尖顶外轮廓围绕中央分支竖笔和数条分离短痕，下方为宽弯曲底部笔画。",
    ),
    "obs-char-000492": (
        "A long top bar and left vertical form an open frame around detached inner dashes, "
        "a branching central stem, and a crossed cluster extending toward the lower right.",
        "长顶横和左侧竖笔构成开口框架，内有分离短线、分支中央主干和伸向右下的交叉笔画群。",
    ),
    "obs-char-000493": (
        "A broad pointed arch encloses one central upright stroke with several short branches "
        "on its upper left and two diverging lower extensions.",
        "宽尖拱形包围一条中央直立笔画，其左上有数条短分支，下部延伸分向两侧。",
    ),
    "obs-char-000494": (
        "A vertical dotted column at left stands beside a tall angular form at right with a "
        "segmented diagonal band, bent stem, lower crossing, and horizontal base.",
        "左侧竖向点列与右侧高长折角形并列；右形含分段斜带、弯折主干、下部交叉和横底线。",
    ),
    "obs-char-000495": (
        "The very small image shows a pointed outer outline, a compact crossed triangular "
        "cluster in the center, and a detached short horizontal mark below.",
        "极小图像显示尖顶外轮廓、中央紧凑交叉三角笔画群和下方分离短横。",
    ),
    "obs-char-000496": (
        "A pointed polygonal outer frame encloses an upper oval loop with crossed branches; "
        "below it are two stacked groups of horizontal and vertical strokes.",
        "尖顶多边外框包围带交叉分支的上部椭圆环，其下有两组层叠横竖笔画。",
    ),
    "obs-char-000497": (
        "A bold central vertical trunk divides into several long upward branches on both "
        "sides and narrows into a rounded descending end.",
        "粗重中央竖向主干向两侧分出数条长上行枝笔，下部收窄为圆钝下垂端。",
    ),
    "obs-char-000498": (
        "A long horizontal stroke has a forked left-pointing end and crosses a central "
        "vertical line and a large curved loop opening toward the left.",
        "长横左端呈叉状指向左侧，并穿过中央竖线和一个向左开口的大型弯曲环形。",
    ),
    "obs-char-000499": (
        "The small narrow image shows an upper angular outlined cluster and a lower crossed "
        "branching cluster, with a long thin stroke descending along the right side.",
        "小型狭窄图像显示上部折角轮廓笔画群和下部交叉分支笔画群，右侧有一条长细笔下垂。",
    ),
    "obs-char-000500": (
        "A narrow upright form combines a forked upper crossing, a central enclosed diamond "
        "divided by short strokes, and two long diverging lower extensions.",
        "狭长直立形体结合叉状上部交叉、由短笔分隔的中央菱形围框和两条长分向下部延伸。",
    ),
    "obs-char-000501": (
        "Two short horizontal bars and a small vertical mark sit above a long central curved "
        "stroke that ends in several crossed and branching lower lines.",
        "两条短横和一条小竖位于长中央弯笔上方，中央笔下端以数条交叉分支线收束。",
    ),
    "obs-char-000502": (
        "An irregular outlined form at left contains several crossing divisions and connects "
        "toward a long right vertical stroke with a short transverse branch.",
        "左侧不规则轮廓形内有数处分隔交叉，并向带短横分支的右侧长竖笔连接。",
    ),
    "obs-char-000503": (
        "Two bold forms stand apart: a branching vertical trunk with a lower loop on a base "
        "at left, and a curved upper arch with a long descending side at right.",
        "两个粗重形体彼此分离：左侧为带下环和底线的分支竖干，右侧为上部弯拱及长下行侧笔。",
    ),
    "obs-char-000504": (
        "The very small low-contrast image shows two separated clusters: short marks above "
        "a forked form at left and a narrow branching vertical form at right.",
        "极小低对比度图像显示两个分离笔画群：左侧叉形上方有短痕，右侧为狭长分支竖形。",
    ),
    "obs-char-000505": (
        "Three detached tapered vertical strokes are arranged side by side, with the central "
        "stroke longer and straighter than the two curved outer strokes.",
        "三条分离渐尖竖笔并列，中央笔较长且较直，两侧外笔较短并弯曲。",
    ),
    "obs-char-000506": (
        "Four small detached tapered marks form a loose vertical diamond arrangement, with "
        "one mark above, two at the sides, and one below.",
        "四个小型分离渐尖痕迹组成疏松竖向菱形排列，上方一处、两侧各一处、下方一处。",
    ),
    "obs-char-000507": (
        "A bold central loop is crossed by a horizontal bar and rises into a bent upper stem; "
        "two detached vertical marks stand near its lower left and right sides.",
        "粗重中央环形被横笔穿过并向上形成弯折主干，下部左右附近各有一条分离竖痕。",
    ),
    "obs-char-000508": (
        "Two short detached top bars stand above a broad angular outline open at the bottom, "
        "which encloses a small rounded loop and short central stroke.",
        "两条分离短顶横位于底部开口的宽折角轮廓上方，轮廓内有小圆环和短中央笔。",
    ),
    "obs-char-000509": (
        "A very narrow form has a small upper crossing and a long diagonal-to-curved stroke "
        "descending below it; fine boundaries are difficult to resolve.",
        "极狭长形体上部有小型交叉，下方延伸一条由斜转弯的长笔，细部边界难以辨清。",
    ),
    "obs-char-000510": (
        "A thin curved vertical stem has an upper forked crossing, several short parallel "
        "branches spreading to the lower left, and a hooked lower end.",
        "纤细弯曲竖干上部呈叉状交叉，下部左侧展开数条短平行分支，末端钩曲。",
    ),
    "obs-char-000511": (
        "A vertical stack combines a small upper triangle, a central rectangle, a wider lower "
        "triangle, and four thin parallel strokes descending from the base.",
        "竖向层叠形由小型上三角、中央矩形、较宽下三角和从底部下垂的四条细平行笔组成。",
    ),
    "obs-char-000512": (
        "A single sinuous form curves into a broad open loop, with one short upper branch, "
        "a left-pointing stroke, and a thin descending tail.",
        "单个曲折形体弯成宽开口环，带一条短上分支、一条左向笔和一条纤细下垂尾笔。",
    ),
    "obs-char-000513": (
        "Two long upright strokes frame a central diagonal crossing and a short right-pointing "
        "branch, leaving the lower ends open and separate.",
        "两条长直立笔夹着中央斜向交叉和一条短右向分支，下端开口并彼此分离。",
    ),
    "obs-char-000514": (
        "A narrow zigzag vertical form contains a small central loop, with a long upper "
        "diagonal and a short bent lower extension.",
        "狭长折线竖形中部有小环，上方为长斜笔，下方为短弯折延伸。",
    ),
    "obs-char-000515": (
        "The very faint image shows a thin central stem dividing into two long lower branches "
        "with several finer side offshoots; the upper tip is slightly curved.",
        "极淡图像显示纤细中央干分成两条长下枝，并带数条更细侧枝，上端略弯。",
    ),
    "obs-char-000516": (
        "A curved central stem has one long upper-left branch and two long diverging lower "
        "strokes, with two detached short marks inside the right side.",
        "弯曲中央干带一条长左上分支和两条分向下部的长笔，右侧内部另有两处分离短痕。",
    ),
    "obs-char-000517": (
        "A narrow angular upper loop continues into a long curved outer stroke, enclosing "
        "three detached short vertical marks at different heights.",
        "狭窄折角上环延续为长弯曲外笔，内部在不同高度有三条分离短竖痕。",
    ),
    "obs-char-000518": (
        "A tiny divided box-like cluster with protruding upper strokes sits above a long bent "
        "stem that ends in a crossed angular lower form.",
        "带上部伸出笔画的小型分隔框状群位于长弯折主干上方，主干下端形成交叉折角形。",
    ),
    "obs-char-000519": (
        "A bold central trunk divides upward into several long branches, with the widest fork "
        "near the middle and a single tapered lower stem.",
        "粗重中央干向上分出数条长枝，中部附近分叉最宽，下方为单条渐尖主干。",
    ),
    "obs-char-000520": (
        "A long tapered vertical stroke contains a small open loop on its lower left and is "
        "crossed near the bottom by a short horizontal line extending to the right.",
        "长渐尖竖笔左下含小型开口环，并在近底部被一条向右伸出的短横穿过。",
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
    "asset_id",
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
    object_root = root / "corpus/001_oracle-characters"
    targets: dict[str, dict[str, Path | str]] = {}
    packet_paths = [
        *object_root.glob("*/*/01_candidate-character-packet.json"),
        *object_root.glob("*/*/01_undeciphered-candidate-packet.json"),
    ]
    for packet_path in sorted(packet_paths):
        object_dir = packet_path.parent
        project_id = project_id_from_object_dir(object_dir)
        targets[project_id] = {
            "object_dir": object_dir,
            "packet": packet_path.name,
        }
    if not targets:
        raise FileNotFoundError("No character packet directories were found")
    return dict(sorted(targets.items()))


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
        rows = list(csv.DictReader(file))
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        if row.get("visual_source_index_id"):
            indexed[row["visual_source_index_id"]] = row
        if row.get("source_image_reference_path"):
            indexed[row["source_image_reference_path"]] = row
    return indexed


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
                    "asset_id": existing_row.get("asset_id", ""),
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
        unique_rows = {
            row.get("visual_source_index_id", str(index)): row
            for index, row in enumerate(existing_visual_rows.values())
        }
        return sorted(unique_rows.values(), key=lambda row: row.get("visual_source_index_id", ""))

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


def local_asset_exists(root: Path, path: str) -> bool:
    if not path:
        return False
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = (root / candidate).resolve()
    if candidate.is_file():
        return True
    if candidate.is_absolute() and candidate.drive:
        return Path("\\\\?\\" + str(candidate)).is_file()
    return False


def normalize_visual_rows(root: Path, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    for row in rows:
        path = row.get("committed_image_path", "")
        if not path:
            continue
        if not row.get("asset_id"):
            match = re.search(r"(asset-\d+)", path)
            if match:
                row["asset_id"] = match.group(1)
        if local_asset_exists(root, path):
            row["visual_material_status"] = "committed_review_image_derivative"
        else:
            row["visual_material_status"] = (
                "source_image_reference_only_no_committed_glyph_image"
            )
            row["caution"] = (
                "The image path is a registered route, but the local derivative "
                "is not present on the current disk; do not treat the route as "
                "an opened image."
            )
    return rows


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
    root: Path,
    packet_name: str,
    packet: dict,
    visual_rows: list[dict[str, str]],
    material_observation_available: bool = False,
) -> str:
    external_id = packet.get("primary_external_ref_id", "")
    source_id = packet.get("source_id", "")
    status_counts = sorted({row["visual_material_status"] for row in visual_rows})
    image_ref_count = sum(1 for row in visual_rows if row["source_image_reference_path"])
    image_routes = [row["committed_image_path"] for row in visual_rows if row.get("committed_image_path")]
    committed_images = [path for path in image_routes if local_asset_exists(root, path)]
    packet_record_type = packet.get("record_type", "")
    caution = packet.get("caution", "")
    local_path = object_dir.as_posix()
    status_text = ", ".join(status_counts)
    committed_image_text = relative_committed_images(object_dir, committed_images)
    if not committed_images and image_routes:
        committed_image_text = "registered image route only; local file missing"
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
    append_wrapped_bullet(
        lines,
        "Registered image routes / 已登记图像路线",
        f"`{len(image_routes)}`",
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


def build_gallery_text(
    project_id: str,
    packet_name: str,
    packet: dict,
    visual_rows: list[dict[str, str]],
    root: Path,
) -> str:
    external_id = packet.get("primary_external_ref_id", "")
    source_id = packet.get("source_id", "")
    committed_rows = [
        row
        for row in visual_rows
        if local_asset_exists(root, row.get("committed_image_path", ""))
    ]
    image_route_count = sum(1 for row in visual_rows if row.get("committed_image_path"))
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


def build_gallery_text(
    project_id: str,
    packet_name: str,
    packet: dict,
    visual_rows: list[dict[str, str]],
    root: Path,
) -> str:
    external_id = packet.get("primary_external_ref_id", "")
    source_id = packet.get("source_id", "")
    committed_rows = [
        row
        for row in visual_rows
        if local_asset_exists(root, row.get("committed_image_path", ""))
    ]
    image_route_count = sum(1 for row in visual_rows if row.get("committed_image_path"))
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
    append_wrapped_bullet(
        lines,
        "Registered image routes / 已登记图像路线数",
        f"`{image_route_count}`",
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
    root: Path,
) -> str:
    observation = MATERIAL_VISUAL_OBSERVATIONS.get(project_id)
    committed = [
        row
        for row in visual_rows
        if local_asset_exists(root, row.get("committed_image_path", ""))
    ]
    if not observation or not committed:
        return ""
    row = committed[0]
    local_path = Path(row["committed_image_path"])
    if local_path.is_absolute():
        local_path_for_display = local_path
    else:
        local_path_for_display = root / local_path
    try:
        local_path_text = local_path_for_display.resolve().relative_to(
            object_dir.resolve()
        ).as_posix()
    except ValueError:
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
        visual_rows = normalize_visual_rows(root, visual_rows)
        outputs[project_id] = {
            "object_dir": object_dir,
            "readme_path": object_dir / "README.md",
            "visual_index_path": visual_index_path,
            "gallery_path": object_dir / "04_visual-gallery.md",
            "material_observation_path": object_dir / "14_material-visual-observation.md",
            "readme_text": build_readme_text(
                project_id,
                object_dir.relative_to(root),
                root,
                packet_name,
                packet,
                visual_rows,
                bool(MATERIAL_VISUAL_OBSERVATIONS.get(project_id))
                and any(
                    local_asset_exists(root, row.get("committed_image_path", ""))
                    for row in visual_rows
                ),
            ),
            "gallery_text": build_gallery_text(
                project_id, packet_name, packet, visual_rows, root
            ),
            "visual_rows": visual_rows,
            "material_observation_text": build_material_observation_text(
                project_id, object_dir, packet, visual_rows, root
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
