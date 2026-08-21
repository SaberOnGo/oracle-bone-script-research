# Object and image routes / 对象与图像路线

## Object identity / 对象身份

| field | source-reported value |
| --- | --- |
| provider | The Metropolitan Museum of Art |
| object ID | `42045` |
| accession | `67.43.14` |
| title | `Oracle bone` |
| object name | `Oracle bone` |
| department | Asian Art |
| culture | China |
| period | Shang dynasty (ca. 1600–1046 BCE) |
| medium | Inscribed bone |
| dimensions | W. 3 cm; L. 22.5 cm |
| credit line | Gift of Paul E. Manheim, 1967 |

The API route is the official Open Access object endpoint:

`https://collectionapi.metmuseum.org/public/collection/v1/objects/42045`

The public object page is:

`https://www.metmuseum.org/art/collection/search/42045`

## Image routes / 图像路线

- API `primaryImage`:
  `https://images.metmuseum.org/CRDImages/as/original/LC-67_43_14_002.jpg`
  Local file: `03_visual-assets/001_asset-000001_met-42045-image-002.jpg`.
  Size 1780568 bytes; SHA-256
  `c605ae36f53ffdc5c1200e3bf23683aaaa6106a03e1c002ca5ab8f859e0333df`.
  Pixels: 2667 x 4000.
- API `additionalImages[0]`:
  `https://images.metmuseum.org/CRDImages/as/original/LC-67_43_14_001.jpg`
  Local file: `03_visual-assets/002_asset-000002_met-42045-image-001.jpg`.
  Size 1616877 bytes; SHA-256
  `c2c09d618ed7da7e38b845164186590f7fa416ec3487a319c7de75b84330a480`.
  Pixels: 2667 x 4000.

The API names the views but does not establish a recto-verso relationship.
The project therefore preserves the API labels and does not infer reading
order or object orientation.

API access and image retrieval were checked on 2026-08-21 UTC. The raw API
JSON remains in the ignored `.working/met-42045/` directory; this object
folder commits only the two public image bytes and source-derived records.

API 访问和图像获取于 2026-08-21 UTC 核对。原始 API JSON 仍在忽略区
`.working/met-42045/`；本对象目录只提交两张公开图像字节和来源派生记录。
