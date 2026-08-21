# Catalog citation network / 著录引用网络

## Nodes / 节点

- **IHP item page**: official object label, short display, and metadata.
- **IHP collection page**: collection-level navigation to `Jia Bian 0959`.
- **Project source object**: `src-ihp-museum-oracle-bones`, its register row,
  overview download log, and rights warning.
- **Project object candidate**: `ihp-mus-obj-00002`, accession `R038861`,
  private image routes, and object-level claim gate.
- **Future catalog evidence**: the exact `Jia Bian` volume/page/plate and an
  independent record, not yet located.

## Relations / 关系

| From | Relation | To | Status |
| --- | --- | --- | --- |
| collection page | lists | item page | checked |
| item page | describes | `R038861` | source-reported |
| source object | routes | item page | registered source family |
| object candidate | records | item page and images | candidate route |
| item page | cites | no named publication | absent |
| item page | proposes | no named scholar | absent |

The collection page and item page are not independent scholarly arguments.
They are two pages in one institutional source family. Counting them twice
would inflate evidence independence.

馆藏总览页和对象页不是两份独立学术论证，而是同一机构来源族的两个页面。不能把它们
重复计数为独立证据。

No proposer, rejection, alternate reading, or citation relationship is
identified on the current item route. Absence on this page is not evidence of
scholarly agreement.

当前对象路线没有识别出提出者、驳回意见、异读或引用关系。页面未出现不等于学界一致。

## Network next checks / 网络下一步

1. Link the exact catalog edition and page once opened.
2. Search published studies for `Jia Bian 0959` and `R038861` together.
3. Record each cited reading separately, with proposer, date, locator, and
   contrary evidence.
