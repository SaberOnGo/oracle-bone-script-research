# Large Source Register / 大型来源登记表

English:
Use this registry for important source packages that are too large, too generated, or too risky to commit directly. The raw package may live in an ignored local archive, institutional storage, object storage, Git LFS, or a GitHub Release after project approval, but its provenance trail must be recorded here.

简体中文：
本登记表用于记录重要但过大、生成性太强或不适合直接提交的来源包。原始包经项目批准后可以放在已忽略的本地归档、机构存储、对象存储、Git LFS 或 GitHub Release 中，但来源链必须记录在这里。

This register links large raw sources to smaller reviewed derivatives in `corpus/`, `research/`, `project_registry/`, or `doc/public/user_research/`.

本登记表把大型原始来源与 `corpus/`、`research/`、`project_registry/` 或 `doc/public/user_research/` 中较小、已复核的派生记录连接起来。

## Files / 文件

- `001_large-source-register.csv`: large source package registry.
- `001_large-source-register.csv`：大型来源包登记表。
- `002_source-download-log.csv`: download/access log with status, size, checksum, and storage hints.
- `002_source-download-log.csv`：下载/访问日志，记录状态、大小、checksum 和存放线索。

## Required Fields / 必需信息

English:
Each large-source row should preserve source ID, source name, access route, local or external storage hint, expected size, checksum when available, rights status, risk note, derived record paths, and review status.

简体中文：
每条大型来源记录应保留来源 ID、来源名称、访问路径、本地或外部存放线索、预期大小、可用时的 checksum、权利状态、风险提示、派生记录路径和复核状态。

## Boundary / 边界

English:
Large-source registration is not permission to commit oversized raw files to regular Git. It is also not evidence that any derived reading, component assignment, inscription identity, or correspondence is confirmed.

简体中文：
大型来源登记不等于允许把超大原始文件提交到普通 Git，也不证明任何派生释读、构件归属、卜辞身份或字形对应已经确认。
