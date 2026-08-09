# OBIMD Rights Conflict Review / OBIMD 权利冲突复核

## Purpose / 用途

English:
This note records an active rights conflict for OBIMD. It is a source and
repository-use decision, not a copyright opinion and not scholarship. Until
the copyright holders reconcile the statements, the repository must treat
OBIMD files and derivatives as metadata-only or local-private material.

简体中文：
本页记录 OBIMD 当前存在的权利表述冲突。它是来源和仓库使用决定，
不是法律意见，也不是学术结论。在权利人统一说明前，仓库必须把
OBIMD 文件和派生件按仅 metadata 或本地私有资料处理。

## Evidence Read In The Same Session / 同次核查的证据

1. Hugging Face dataset card:
   `https://huggingface.co/datasets/KLOBIP/OBIMD`
   The live page labels the dataset `cc-by-4.0` and says it is licensed under
   CC-BY 4.0. The recorded route is `dl-obimd-hf-readme`; its captured
   payload was 3,871 bytes with SHA-256
   `2ad91fb999e3ea176a2f7dd39cf67b5e8cfb327d9f22f6713aa1d196a61932de`.

2. Official code README:
   `https://raw.githubusercontent.com/libang1991/OBIMD/main/README.md`
   The README says the dataset is released for academic research only and
   that commercial use requires special permission from the authors. The
   recorded route is `dl-obimd-github-readme`; its payload was 5,543 bytes
   with SHA-256
   `3361eb37c65a01de05d73b57525500eeed6db7c35dcc16c303794a467c4bbd3e`.

3. Scientific Data article and licence notice:
   `https://doi.org/10.1038/s41597-026-06967-0`
   The article notice identifies CC BY-NC-ND 4.0 and warns that third-party
   material may have separate credit-line terms. The repository currently
   records this as a live web observation without a local page checksum;
   it must not be treated as a downloaded licence file.

These statements are not interchangeable. A dataset-card label cannot by
itself override the repository README, article licence notice, or a
third-party credit line. The conflict is therefore unresolved.

## Effective Repository Decision / 当前仓库生效决定

The machine-readable override is
`006_obimd-rights-status-override.csv`. It supersedes the historical
`licensed_for_repository` value for repository-use decisions while retaining
that value as a traceable legacy declaration. The effective status is
`metadata_only_until_verified` for the OBIMD source, packages, assets, and
component-candidate derivatives. Fifty rights-log rows without a matching
asset are `local_private_only` until their asset identity is restored.

The override does not delete or rewrite historical rows. It prevents a
legacy value from silently authorizing public redistribution. A future
rights-holder statement may close the override only after a new evidence row,
checksum or live-access record, scope decision, and independent review.

## Human Review Questions / 人工复核问题

- Which file or credit line is covered by each licence statement?
- Does CC BY-NC-ND cover dataset files, article text, or only credited media?
- Does the academic-only README apply to code, data, images, or all three?
- Which authors or rights holders can reconcile the statements in writing?
- Which existing derivative needs removal, replacement, or private storage?
- 哪条许可说明对应哪些文件或 credit line？
- CC BY-NC-ND 覆盖数据文件、论文正文，还是仅覆盖署名媒体？
- academic-only README 针对代码、数据、图像，还是三者全部？
- 哪些作者或权利人可以用书面说明统一这些表述？
- 哪些现有派生件需要删除、替换或移入私有存储？

## Boundary / 边界

This review does not grant permission, decide ownership, validate a glyph,
assign a component, identify an inscription, or make a decipherment claim.

本复核不授予许可，不决定所有权，不确认字形，不作构件归属、卜辞
身份或释读结论。
