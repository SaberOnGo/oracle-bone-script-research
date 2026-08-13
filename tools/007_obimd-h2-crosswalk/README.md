# OBIMD H2 Visual Crosswalk Replay
# OBIMD H2 视觉互证复跑工具

This read-only command compares one official thumbnail with every raster member
of the ignored local OBIMD rubbing package. It writes JSON to standard output
and never saves image bytes. Pillow is the only non-stdlib dependency.

本只读命令把一张官方缩略图与忽略区内 OBIMD 拓片包的全部图像成员比较。
命令只向标准输出写 JSON，绝不保存图像字节。除标准库外仅依赖 Pillow。

## Online replay / 在线复跑

Run from the repository root. The URL response stays in memory.

在仓库根目录运行。URL 响应只留在内存中。

```powershell
$thumbUrl = 'https://jgw.aynu.edu.cn/File/GetFirstSmallPic?' + `
  'dbId=34&recordId=108548&key=' + `
  '4EgKVaG1cYado6vj7L8iYg%3d%3d'
$manifest = 'corpus/002_oracle-bone-inscriptions/' + `
  '008_source-record-candidates/' + `
  '001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate/' + `
  '92_visual-crosswalk-replay-manifest.json'
python tools/007_obimd-h2-crosswalk/replay_h2_crosswalk.py `
  --run-date 2026-08-13 `
  --thumbnail-url $thumbUrl `
  --rubbing-zip external_local_archive/source_packages/obimd/rubbing.zip `
  --expected-thumbnail-sha256 `
  5321d3b9adf0a1bde32e4092715741a04461908c9c6e911c57e1f7544ab32437 `
  --expected-rubbing-zip-sha256 `
  4d07dca94e94c2d17edd7fa25be72b5673161c0c2d03dac4d2c094e5341b7747 `
  --target-member rubbing/h00002.jpg `
  --expected-target-member-sha256 `
  1ae9e411f0356cb9dc232d629d4620b0e5f66f42c83300ce95775950a75b01e5 `
  --verify-manifest $manifest
```

## Offline replay / 离线复跑

If a reviewer has lawfully acquired the exact response, use
`--thumbnail-file PATH` and add `--thumbnail-source-url URL`. The expected
response hash remains mandatory. The reviewer is responsible for keeping that
temporary input outside Git and deleting it according to local rights policy.

如复核者已依法取得同一响应，可改用 `--thumbnail-file PATH`，并增加
`--thumbnail-source-url URL`。响应预期哈希仍为必填。复核者须按本地权利政策
把临时输入留在 Git 之外并妥善删除。

`--verify-manifest` recomputes the complete record and fails if any field
differs from the committed manifest.

`--verify-manifest` 会重新计算完整记录；任何字段与已提交 manifest 不同，
命令都会失败。

The command verifies all three hashes before reporting a rank. Its dHash,
resize, bit order, sorting, tie rule, direct MAD, and inverted MAD are recorded
in every JSON result. A visual match is candidate evidence only; it does not
confirm a catalog identity, transcription, or reading.

命令在报告排名前核对三项哈希。每份 JSON 都记录 dHash、缩放、位顺序、排序、
平手规则、直接 MAD 和反色 MAD。视觉匹配只构成候选证据，不能确认著录身份、
释文或释读。
