# Corpus Validation Tools / 语料校验工具

English:
This tool area records how repository and corpus checks protect the
human-readable research archive. Validators should confirm that object-local
dossiers, source provenance, graph edge routes, statistics, and generated
support files remain reviewable before formal oracle-bone research begins.

简体中文：
本工具区说明仓库和语料校验如何保护人类可读研究档案。validator 应确认
对象内 dossier、source provenance、graph edge 路线、statistics 和生成的
辅助文件在正式甲骨文研究开始前仍可供人工复核。

## Human Review Entry Order / 人工复核入口顺序

English:

1. Open the concrete object-local dossier or source note first.
2. Check source provenance, rights status, risk note, and review status.
3. Check generated route files only after the human entry is readable.
4. Use graph edge and statistics files to find missing review routes.
5. Run validators after editing docs, schemas, scripts, or generated outputs.
6. Record failures as concrete next checks, not as empty placeholders.

简体中文：

1. 先打开具体对象内 dossier 或来源说明。
2. 核查 source provenance、rights status、risk note 和复核状态。
3. 人类入口可读后，再核查生成的路线文件。
4. 使用 graph edge 和 statistics 文件寻找缺失复核路线。
5. 修改文档、schema、脚本或生成结果后运行 validator。
6. 失败项要写成具体下一步待查问题，不能留成空模板。

## Concrete Questions To Check / 具体待查问题

English:

- Which object-local dossier failed, and which evidence route is missing?
- Which source provenance row lacks checksum, manifest, or field map?
- Which graph edge is only a route and must not be treated as scholarship?
- Which statistics row points to a missing human-readable file?
- Which generated file changed without a matching validator or test?
- Which remaining issue blocks a human reviewer from checking the object?

简体中文：

- 哪个 object-local dossier 未通过，缺哪条证据路线？
- 哪条 source provenance 记录缺 checksum、manifest 或字段映射？
- 哪条 graph edge 只是路线，不能当成学术结论？
- 哪条 statistics 行指向缺失的人类可读文件？
- 哪个生成文件改变了，却没有匹配 validator 或测试？
- 哪个剩余问题会阻止人工复核者检查该对象？

## Current Validator / 当前校验器

English:
The skeleton validator lives at
`tools/validation/check_repository_skeleton.py`. Python tests import it through
that stable package path. Keep new checks close to the human archive rule they
protect, and add focused unit tests when the rule changes.

简体中文：
骨架校验器位于 `tools/validation/check_repository_skeleton.py`。Python 测试
通过这个稳定包路径导入它。新增检查应靠近它保护的人类档案规则，并在规则
变化时补充聚焦单元测试。

## Research Boundary / 研究边界

English:
Passing validation proves that required files and review routes are present.
It does not prove a reading, component assignment, inscription identity,
correspondence, rights clearance, or decipherment conclusion. It is not a
decipherment conclusion.
This is not a decipherment conclusion.

简体中文：
通过校验只能证明必需文件和复核路线存在。它不证明释读、构件归属、卜辞
身份、字形对应、权利清理或破译结论。它不是释读结论。
