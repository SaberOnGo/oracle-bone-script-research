# Source Access Boundary Review / 来源访问边界复核

## Human Result / 人类阅读结果

- Affected source count: 0
- Grouped failure-condition task count: 0
- Preserved access-attempt count: 0
- Older source-engineering access/checksum gap rows: 9

原始访问记录逐条保留，但人工任务按来源和故障条件归并。无来源
payload 时没有 checksum 是同一访问边界的结果，不再另算一次任务。
重试次数不会增加人类任务数；只有新的故障条件才新增任务。

Access attempts remain separate provenance records. Human tasks are
grouped by source and failure condition. A missing checksum for an
unsaved payload is evidence of the same access boundary, not a second
independent review task.

## Grouped Tasks / 归并后任务

## Opening Order / 复核顺序

1. Open the source's human-readable dossier or source note.
2. Open the exact download IDs in the source download log.
3. Compare a historical success or browser capture when listed.
4. Retry only after the route, network, or access condition changes.
5. Record a concrete metadata-only or retry decision.

人工复核时，先读来源档案，再核对本表列出的 download ID。若已有
历史成功记录或浏览器 metadata，应同时比较。只有路线、网络或访问
条件变化时才重试，并记录具体的 metadata-only 或重试决定。

## Boundary / 边界

This is a preprocessing access review. It does not prove source
availability, preserve a source payload, clear rights, promote a
source, import corpus records, or make a decipherment conclusion.

本表只用于预处理访问复核。它不证明来源当前可用，不代表已保存
来源 payload，不裁定权利，不提升来源，不导入语料，也不形成释读
结论。
