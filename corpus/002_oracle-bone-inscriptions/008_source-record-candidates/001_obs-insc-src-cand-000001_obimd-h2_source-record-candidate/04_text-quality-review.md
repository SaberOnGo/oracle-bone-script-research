# Text And OCR Quality Review / 文本与 OCR 质量复核

## English

The OBIMD row remains `source_uid_sequence_only`. It supplies seven UIDs,
bounding boxes, one group label, and order numbers, but no human-readable
transcription, OCR, punctuation, or edition locator.

The National Library page now supplies a source-reported partial
transcription for NLC 14427 / Heji 2. This is a separate text layer. It is
not the OBIMD row text, not a project transcription, and not yet aligned to
the seven boxes.

Therefore the OBIMD row has no readable full transcription or OCR. The UIDs
must never be rendered as if they were an ancient sentence or modern Chinese
translation. `InscriptionSentence1` is a dataset group-category value, not a
claim that this dossier has established the full linguistic boundaries of an
ancient divination charge.

The seven source boxes all carry ordinary dataset markers, but this only
describes the current encoding. Text completeness remains `not_assessable`
until the rubbing, facsimile, a cited transcription page, and an independent
catalog record are compared together.

## 简体中文

OBIMD 来源行仍是 `source_uid_sequence_only`。它提供七个 UID、字框、
一个组标签和次序号，但没有人类可读释文、OCR、标点或版本定位。

国家图书馆页面现为国图 14427 /《合集》2 提供来源报告残辞。这是独立
文本层，不是 OBIMD 行内文字，不是项目释文，也尚未与七个字框逐一对齐。

因此，OBIMD 行内仍没有可读的卜辞全文或 OCR。不得把有序 UID 渲染成古代
句子或
现代汉语译文。`InscriptionSentence1` 是数据集的组类字段，不表示本档案
已经确定一条古代卜问的完整语言边界。

七个来源字框都带普通数据集标记，但这只能描述当前编码。只有把拓片、
摹本、有引文的释文页和独立著录记录一并比较后，才能评估文本完整性；
目前状态应保持 `not_assessable`。

## Next Text Check / 下一项文本核查

Locate the exact source edition and page used during OBIMD annotation, then
record the transcription as a sourced transcription candidate with its own
quality note. Do not silently convert a platform reference label into OCR.

须查明 OBIMD 标注时使用的确切版本和页码，再把释文作为带来源的释文候选
记录，并另写质量说明。不得把平台参考标签静默转换成 OCR。
