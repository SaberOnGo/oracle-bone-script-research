# H2 Identifier Crosswalk Investigation
# H2 编号互证调查

Access dates / 访问日期: 2026-08-12, 2026-08-13

## English

### Result and boundary

OBIMD `H2`, Yinqi Wenyuan record `合2`, and National Library oracle bone
14427 now form a high-confidence Heji 2 cross-source candidate. This is not
a formal `obi-*` identity. The National Library page supplies a readable
source-reported partial transcription; no project reading is proposed.

No opened source states the literal expansion of the OBIMD code `H2`.
Instead, the candidate rests on two object-level visual routes and an
institutional catalog statement. The effective rights status remains
`metadata_only_until_verified`.

### Direct source evidence

1. The version-of-record article is available at
   `https://doi.org/10.1038/s41597-026-06967-0` and
   `https://pmc.ncbi.nlm.nih.gov/articles/PMC13128845/`.
2. Its final Table 2 defines `RubbingName` as “Catalog abbreviation of the
   rubbing image” and gives `H2` as an example. It does not expand `H`.
3. The article reports 9,913 specimens from *Jiaguwen Heji* and 164 from
   Huayuanzhuang East. The pinned dataset has 9,913 `H` and 164 `HD`
   identifiers. This is aggregate corpus-family evidence, not a row mapping.
4. The pinned dataset revision is
   `c8b1f31bb61c6d1cafb6e55ca377b1df4c9951b8`.
5. On 2026-08-12, `https://jgw.aynu.edu.cn/AynuBone/BookList` returned
   collection `甲骨文合集--合`, code `010001H`. A collection-limited request to
   `https://jgw.aynu.edu.cn/AynuBone/Search` returned visible row `合2`, system
   ID `108548`, source `甲骨文合集`, form `拓片`.
6. On that access date and request configuration, a direct query for `H2`
   returned zero visible piece-number rows. This is only a query observation;
   it does not prove that no mapping exists.
7. The detail endpoint for `108548` returned `Code=406` and
   `登录失效，请先登录`. Object-level fields were therefore not acquired.
8. On 2026-08-28, a National Library article identified its oracle bone
   14427 as Heji 2 and printed a photograph and rubbing matching OBIMD `H2`.
9. The same page printed a partial transcription, retained here as
   source-reported text rather than a project reading.

### Replayed visual comparison

On 2026-08-13, the exact official thumbnail URL was fetched into memory:

`https://jgw.aynu.edu.cn/File/GetFirstSmallPic?dbId=34&recordId=108548&key=`
`4EgKVaG1cYado6vj7L8iYg%3d%3d`

The response was a 4,571-byte, 129 by 150 RGB JPEG with SHA-256
`5321d3b9adf0a1bde32e4092715741a04461908c9c6e911c57e1f7544ab32437`.
No thumbnail bytes were saved or committed.

The read-only replay compared it with 10,077 package members: the target plus
10,076 alternative candidates. `rubbing/h00002.jpg` ranked first at explicit
dHash distance 0; the next distance was 12. Direct MAD was 8.7851 and inverted
MAD was 196.3636. Sorting is by distance, then case-sensitive member path.

The full top-k, all hashes, Pillow version, dHash bit order, resize method,
tie rule, and MAD definition are in `92_visual-crosswalk-replay-manifest.json`.
The runnable method is documented in
`tools/007_obimd-h2-crosswalk/README.md`.

The earlier replay and the National Library page now support a
high-confidence catalog-identity candidate. They do not confirm the exact
Heji page, archaeological fields, or character-to-box alignment.

### Unresolved questions

- Which exact *Jiaguwen Heji* volume, plate, and page contain `合2`?
- Which transcription edition and page did OBIMD annotators use?
- What are the independently sourced institution, object number, findspot,
  period, and group?
- Does a rights-permitted transcription align with all seven OBIMD boxes?

## 简体中文

### 结果与边界

OBIMD `H2`、殷契文渊 `合2` 与国图甲骨 14427 现共同构成《合集》2 的
高置信跨来源候选，但不是正式 `obi-*` 身份。国家图书馆页面提供可读的
来源报告残辞，本项目不据此提出释读。

已打开来源没有逐字展开 OBIMD 代码 `H2`，候选依据是两条对象级视觉路线
和一条机构著录陈述。有效权利状态仍为
`metadata_only_until_verified`。

### 直接来源证据

1. 正式版论文 DOI、开放 PMC 页面见英文部分。最终表 2 把 `RubbingName`
   定义为“拓片图像的著录缩写”，以 `H2` 为例，但没有展开字母 `H`。
2. 论文报告 9,913 项来自《甲骨文合集》，164 项来自花园庄东地；固定版本数据
   恰有 9,913 个 `H` 和 164 个 `HD` 标识。这是来源族总体证据，不是逐条映射。
3. 2026-08-12，官方 `BookList` 返回“甲骨文合集--合”和代码 `010001H`；
   限定该资料集的官方 `Search` 请求返回 `合2`、系统 ID `108548`、来源
   《甲骨文合集》、形式“拓片”。
4. 同一访问日和请求配置下，直接查询 `H2` 得到零条可见片号记录。这只是一项
   具体查询观察，不能证明映射不存在。
5. `108548` 详情接口返回 `Code=406` 和“登录失效，请先登录”，所以没有取得
   对象级释文、时期、馆藏或互证字段。
6. 2026-08-28，国家图书馆文章把国图甲骨 14427 对应为《合集》2，并刊出
   与 OBIMD `H2` 相符的照片、拓片和来源报告残辞。

### 已复跑视觉比较

2026-08-13，工具只在内存读取官方精确缩略图 URL。响应为 4,571 字节、
129×150 的 RGB JPEG；SHA-256 见英文部分。仓库没有保存或提交缩略图字节。

只读工具比较包内 10,077 个成员，即目标与 10,076 个替代候选。
`rubbing/h00002.jpg` 以明确 dHash 距离 0 排第 1，下一距离为 12；直接 MAD
为 8.7851，反色 MAD 为 196.3636。排序先按距离，再按区分大小写的成员路径。

完整 top-k、全部哈希、Pillow 版本、dHash 位顺序、缩放方法、平手规则和 MAD
定义见 `92_visual-crosswalk-replay-manifest.json`；复跑命令见
`tools/007_obimd-h2-crosswalk/README.md`。

早期复跑与国家图书馆页面共同支持高置信著录身份候选，但不确认《合集》
确切页码、考古字段或字框与释文逐字对应。

### 具体待查问题

- `合2` 在《甲骨文合集》中的确切卷、图版和页码是什么？
- OBIMD 标注者采用了哪一释文版本及页码？
- 馆藏机构、对象号、出土地、时期和组类有哪些独立来源？
- 权利允许的释文能否与 OBIMD 的七个框逐一对应？

## Evidence grades / 证据等级

- A: peer-reviewed version-of-record article and final Table 2.
- A：同行评议正式版论文及最终表 2。
- B: pinned official dataset packages and checksums.
- B：固定版本官方数据包及校验和。
- B: institutional search metadata observed on the stated access date.
- B：所述访问日观察到的机构平台检索元数据。
- A: National Library authorship, catalog crosswalk, and figure 3.
- A：国家图书馆作者、著录对应关系及图 3。
- C: replayed algorithmic comparison against 10,076 alternative candidates.
- C：对 10,076 个替代候选完成复跑的算法视觉比较。
- D: public aggregator route, retained only as a documented image mismatch.
- D：公开聚合路线，仅作为已记录图文错配保留。
