# Count Reconciliation / 数量对账

## Three Evidence Layers / 三层证据

1. The official classified table states grand total `609`.
2. The repository parser retained `612` row records, delta `+3`.
3. The row audit assigns `612` rows to `71` parsed sections and records each
   section's declared and observed counts.

1. 官方分类表声明总数为 `609`。
2. 仓库解析保留 `612` 条行记录，差值为 `+3`。
3. 逐行审计把这些行分配到 `71` 个解析分节，并同时记录声明数与观察数。

These are different measurements. The delta does not prove missing or
duplicate inscriptions. It may involve page layout, parser behavior,
multi-line references, repeated identifiers, or genuine list inconsistency.

三者不是同一种测量。差值不能证明存在缺失或重复卜辞，也可能来自页面
排版、解析规则、多行参照、重复号码或来源页面本身的不一致。

## Four Parsed Section Mismatches / 四处分节差异

| Section key | Page declaration | Rows observed | Difference |
| --- | ---: | ---: | ---: |
| `period-i-group-19` | `13` | `22` | `+9` |
| `period-ii-group-1` | `29` | `28` | `-1` |
| `period-ii-group-19` | `22` | `21` | `-1` |
| `period-ii-group-4` | `16` | `21` | `+5` |

These four discrepancies come from the checked local reconciliation index,
not from a claim that one side is correct. Their differences do not sum to
the grand-total delta because other headings and unclassified rows enter the
page structure differently.

这四项取自已检查的本地对账索引，不表示任何一边已经被认定为正确。它们
的分节差值不能直接相加来解释总数差，因为其他标题和未分类行在页面结构
中采用了不同的计数方式。

## Period V Group 8 / 第 V 期第 8 组

This section exposes three non-equivalent signals:

- the classified table displays no Period V value for thematic Group 8;
- the current official search-rendered page shows `Group 8 [10]`;
- the local reconciliation records no parsed declaration and `21` rows.

这一分节出现三种不能互换的信号：分类总表第 V 期第 8 组为空，当前官方
页面的搜索呈现显示 `Group 8 [10]`，本地对账则记录“未解析到声明数”和
`21` 行。可能是页面修订、HTML 结构或解析器行为造成，当前为
`unresolved`。

## Unclassified / 未分类

The page ends with `Unclassified`. The local audit has no declared section
count and preserves four retained rows: `ybu01` through `ybu04`. They remain
routes for checking, not four automatically accepted inscription objects.

页面末尾有 `Unclassified`。本地审计未记录其声明数，但保留四条行记录，
即 `ybu01` 至 `ybu04`。它们只是待核查路线，不会自动成为四个正式卜辞
对象。

## Non-Negotiable Rule / 不可省略的规则

Do not average, delete, add, or silently choose among `609`, `612`, `[10]`,
or `21`. 在逐条打开页面和著录证据前，不得静默修正这些数值，也不得以
某个“看起来合理”的数字覆盖原始证据层。

