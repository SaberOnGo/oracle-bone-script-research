# Text And OCR Quality Review / 文本与 OCR 质量复核

## English

The OBIMD row remains `source_uid_sequence_only`. It supplies seven UIDs,
bounding boxes, one group label, and order numbers, but no human-readable
transcription, OCR, punctuation, or edition locator.

The National Library page now supplies a source-reported partial
transcription for NLC 14427 / Heji 2. This is a separate text layer. It is
not the OBIMD row text or a project transcription. The OBIMD hierarchy files
supply six modern lookup routes. The seventh route has glyph codepoint PUA
`U+FFB45` and platform reference `十一月`. Those fields serve different roles,
so they are not contradictory. The multi-character reference is instead a
granularity warning: one main UID cannot be treated as one accepted reading.

Therefore the OBIMD row has no readable full transcription or OCR. The UIDs
must never be rendered as if they were an ancient sentence or modern Chinese
translation. `InscriptionSentence1` is a dataset group-category value, not a
claim that this dossier has established the full linguistic boundaries of an
ancient divination charge.

The seven source boxes were directly checked in the registered rubbing and
facsimile. This confirms visible occurrences, not text completeness. The
latter remains `not_assessable` until the printed plate and a page-located,
edition-specific transcription are compared with those images.

## 简体中文

OBIMD 来源行仍是 `source_uid_sequence_only`。它提供七个 UID、字框、
一个组标签和次序号，但没有人类可读释文、OCR、标点或版本定位。

国家图书馆页面现为国图 14427 /《合集》2 提供来源报告残辞。这是独立
文本层，不是 OBIMD 行内文字或项目释文。OBIMD 层级文件为六框提供今字
检索路线；第七框字形码位为 PUA `U+FFB45`，平台参考今字值为 `十一月`。
两字段用途不同，并不互相矛盾；但多字参考值构成粒度警告，不能把一个
主字 UID 当成一个已接受释读。

因此，OBIMD 行内仍没有可读的卜辞全文或 OCR。不得把有序 UID 渲染成古代
句子或
现代汉语译文。`InscriptionSentence1` 是数据集的组类字段，不表示本档案
已经确定一条古代卜问的完整语言边界。

七个来源字框已经在登记拓片和摹本中直接核对。这只确认可见出现位置，
不确认文本完整性。只有把印刷图版和可定位页码的版本释文与两图比较后，
才能评估文本完整性；目前状态应保持 `not_assessable`。

## Next Text Check / 下一项文本核查

Open the printed Heji volume 1 plate 2 and locate the edition-specific
transcription used during annotation. Test every box against it and preserve
disagreement. Do not silently convert a platform label into OCR.

须打开《合集》第 1 册图版 2，并查明 OBIMD 标注所据版本级释文。逐框核对
并保留分歧；不得把平台标签静默转换成 OCR。
