# Published Opposite-Face Plate Review
# 出版物异面图版复核

Review date / 复核日期: `2026-08-28`

Status / 状态:
`published_plate_source_reported_object_match_side_unresolved`

## Research question / 研究问题

Can a published plate independently place the committed CC0 image in an
object-level publication context, without turning the plate into a project
transcription or accepting the `Heji` and `Yingcang` hints?

出版图版能否独立把已提交的 CC0 图像放入逐件出版语境，同时不把图版
误写成项目释文，也不直接接受《合集》和《英藏》的著录线索？

## Opened evidence / 已打开证据

A public 13-page PDF sample opens Andrew Robinson's chapter, `The Origins
of Writing`. PDF page 1 is the printed spread 20--21. The right page displays
one oracle-bone face. PDF page 2 contains printed page 22; its caption names
the previous-page object as British Library `Or.7694/1535`.

公开的 13 页 PDF 样张打开 Andrew Robinson 的章节 `The Origins of
Writing`。PDF 第 1 页对应印刷页 20--21，右页显示甲骨一面。PDF 第 2 页
含印刷页 22；图注把前页对象标为大英图书馆 `Or.7694/1535`。

The caption also source-reports an inscribed animal bone from China, dated
to the Late Shang and approximately 1300--1050 BC. These are publication
fields, not independently adjudicated archaeological facts.

图注还把它描述为中国出土的有刻辞动物骨，年代为晚商，约公元前
1300--1050 年。这些是出版物字段，不是项目独立裁定的考古事实。

## Capture receipt / 捕获回执

Ignored capture root:

`.working/bl-1535-publication-route-20260828/`

PDF route components:

- Host: `cache.nebula.phx3.secureserver.net`.
- Path: `/17a4d5b7cb3074f62a350296a4a591f3`.
- Query key: `AccessKeyId=A43E21C9CA4E33A77D3E`.
- Other query fields: `alloworigin=1`; `disposition=0`.

Capture:

- File: `writing-catalogue-public-sample.pdf`.
- Size: `1093393` bytes.
- SHA-256:
  `ebc0d151823ff672d86fc86e7800cb7f40eb718fbab02a8810f62a153a0a7446`.
- Pages: `13`.
- PDF creator: `Adobe InDesign CC 14.0 (Macintosh)`.
- PDF creation timestamp: `2019-01-17T11:05:41Z`.
- Review render: pages 1--2 at `180 dpi`.

The public route is a cache domain, not a British Library domain. Public
availability does not establish redistribution rights or an authoritative
master-file relationship.

公开路线位于缓存域名，不属于大英图书馆域名。能够公开访问不等于获得
再分发权，也不能证明该文件就是馆方主文件。

## Bibliographic chain / 书目链

Andrew Robinson's author page identifies `The Origins of Writing` as a
chapter in the British Library exhibition catalogue `Writing: Making Your
Mark`, published in 2019.

Andrew Robinson 本人网页把 `The Origins of Writing` 列为大英图书馆
2019 年展览图录 `Writing: Making Your Mark` 中的章节。

The author page could be read through the web index, but a local capture was
not made because its TLS certificate produced a hostname-mismatch error.
The project did not bypass that certificate check.

作者网页可通过网络索引读取，但本地下载遇到 TLS 证书域名不匹配，故没有
绕过证书检查，也没有把失败访问伪装成已保存快照。

The University of Sunderland repository records Ewan Clayton, British
Library Publishing, London, 2019, and ISBN `9780712352482`. It describes the
work as the catalogue for the 26 April--27 August 2019 British Library
exhibition.

桑德兰大学仓储记录 Ewan Clayton、British Library Publishing、London、
2019 和 ISBN `9780712352482`，并说明它配套大英图书馆 2019 年
4 月 26 日至 8 月 27 日展览。

Repository capture:

- File: `sunderland-writing-record.html`.
- Size: `49304` bytes.
- SHA-256:
  `53227e1cbc296cc5fd00e96e1d41953a204f4e2bdc29a590b3d163d14189dc93`.
- Route: `https://sure.sunderland.ac.uk/id/eprint/11980/`.

Book trade records also expose hardcover ISBN `9780712352536`. Because the
opened PDF contains no title or copyright page, neither ISBN is assigned to
the captured sample itself. The two edition routes remain separate.

书商记录另有精装 ISBN `9780712352536`。由于已打开 PDF 不含扉页或
版权页，本项目不把任一 ISBN 直接绑定到该样张，并继续分开保留两个版本
路线。

## Image-first observation / 图像优先观察

The published face has a dark background. It shows a broad composite bone
with narrow central fragments, a large lower opening, and several vertical
columns of incised signs. No scale bar is visible.

出版图使用黑色背景，显示一件宽大的合成骨片：中央有数条狭长残片，
下部有大缺口，并可见多列纵向刻辞。图中没有尺度条。

The committed CC0 image shows a light-background face with repeated pits,
grooves, cracks, and faint incisions. The outer silhouette is visually
compatible with the publication plate after horizontal mirroring: both have
the broad lateral pieces, narrow central strips, and lower central opening.

已提交 CC0 图像使用浅色背景，可见重复钻凿、槽痕、裂纹和浅刻痕。把轮廓
水平镜像后，外形与出版图相容：两者都有两侧宽片、中央狭条和下部中央
缺口。

This is an opposite-surface compatibility observation, not a measured image
registration. No OpenCV runtime was available in the current environment,
so the project records no invented match score. The publication caption,
not the outline comparison, is the source for the object label.

这只是异面轮廓相容观察，不是量化配准。本次环境没有可用 OpenCV，项目
因此不虚构匹配分数。对象标签来自出版图注，而不是轮廓比较。

## Evidence effect / 证据作用

This review upgrades the plate route from `not_independently_verified` to
`published_plate_source_reported_object_match_side_unresolved`.

本次把图版路线从 `not_independently_verified` 提升为
`published_plate_source_reported_object_match_side_unresolved`。

The upgrade means only that a 2019 publication plate and caption route are
open and checksum-bound. It does not establish which face is `r` or `v`,
and it does not verify `Heji 39498v` or `Yingcang 1117v`.

该提升只表示 2019 年出版图版和图注路线已打开并绑定校验和；它没有确定
哪一面是 `r` 或 `v`，也没有核实《合集》39498v 或《英藏》1117v。

## Rights and risk / 权利与风险

The committed Commons JPEG remains CC0 for that image file. The publication
sample has no checked reuse licence. Its PDF, rendered pages, and crops stay
in ignored storage. Git retains only bibliographic facts, checksums, and
visual observations.

已提交 Commons JPEG 的 CC0 状态只适用于该图像文件。出版样张尚无已核
再利用许可；PDF、渲染页和裁切图全部留在忽略区。Git 只保留书目事实、
校验和与视觉观察。

Risk status:
`metadata_and_visual_observation_only_until_reuse_terms_verified`.

## Withheld claims / 暂缓主张

- exact `r` or `v` assignment of the published face;
- `Heji 39498v` and `Yingcang 1117v` identity;
- line order, sign segmentation, transcription, OCR, or translation;
- findspot, diviner group, period subgroup, and archaeological batch;
- character identity, component analysis, or decipherment.

- 出版图面的准确 `r`／`v` 分配；
- 《合集》39498v 和《英藏》1117v 身份；
- 行序、单字切分、摹写、OCR 或翻译；
- 出土地、贞人组、时期小组和考古批次；
- 单字身份、构件分析或破译。

## Falsification / 证伪条件

The object-level route must be withdrawn or revised if a title or copyright
page binds the sample to another publication, if the printed caption is
shown to name another image, or if an official item record contradicts the
`Or.7694/1535` assignment.

若扉页或版权页证明样张属于另一出版物、印刷图注实际指向另一图像，或官方
逐项记录否定 `Or.7694/1535` 分配，则必须撤回或修订该对象级路线。

The opposite-face observation must also be withdrawn if a scale-bearing
official image shows a non-matching outer outline or fragment arrangement.

若带尺度的官方图像显示外轮廓或残片排列不符，也必须撤回异面观察。

## Concrete next checks / 具体下一步待查

1. Open the title and copyright pages for the exact sample edition.
2. Resolve the missing item-level British Library catalogue record.
3. Obtain a source-labelled face pair that explicitly assigns `r` and `v`.
4. Open page-addressable `Heji 39498` and `Yingcang 1117` plates.
5. Obtain a rights-cleared, line-addressable text before sign mapping.

1. 打开该样张对应版本的扉页和版权页。
2. 解析缺失的大英图书馆逐项馆藏记录。
3. 取得明确标注 `r` 与 `v` 的同源双面图。
4. 打开可定位页码的《合集》39498 和《英藏》1117 图版。
5. 在字形映射前取得权利清楚、可逐行定位的文本。

This remains a source-record candidate. No reading or decipherment is
promoted.

本对象仍是来源记录候选；没有释读或破译获得晋级。
