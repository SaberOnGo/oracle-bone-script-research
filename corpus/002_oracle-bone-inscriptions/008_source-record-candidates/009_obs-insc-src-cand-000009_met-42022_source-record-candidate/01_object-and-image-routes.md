# Object and image routes / 对象和图像路线

## Object identity / 对象身份

| field | source-reported value |
| --- | --- |
| provider | The Metropolitan Museum of Art |
| object ID | `42022` |
| accession | `18.56.71` |
| title | `Oracle Bone Fragment` |
| object name | `Oracle bone fragment` |
| culture | `China` |
| period | `Shang dynasty (ca. 1600–1046 BCE)` |
| medium | `Bone` |
| credit line | `Rogers Fund, 1918` |

The object and API routes are:

- [Met object page][object-page]
- [Met API record][api-route]
- [primary image][primary-route]
- [additional image][additional-route]

These are museum routes. The accession is not a project ID or an inscription
identity.

## Image files / 图像文件

- `03_visual-assets/001_asset-021414_met-42022-image-002.jpg`
  is `primaryImage`, 2508142 bytes, SHA-256
  `61510f04c8d599e4e5f9bf50ebcb1cb2163ebd7243e4a125ce08e73fdadad8cd`,
  4000 x 2667 pixels.
- `03_visual-assets/002_asset-021415_met-42022-image-001.jpg`
  is `additionalImages[0]`, 2643473 bytes, SHA-256
  `c58ede9b6aa3fe82128ecf0522abb4969d25afd1c8fba17217b3208cd690122e`,
  4000 x 2667 pixels.

The files are unchanged downloads from the two API image URLs. No crop,
rotation, enhancement, or OCR derivative is committed.

## Access and source record / 访问和来源记录

- Existing API download ID: `dl-metmuseum-object-42022`.
- Registry snapshot: 1504 bytes, SHA-256
  `6476cda2ef3e03fefb80be4c9b725e78b460131f7246d0faff101066297545c`.
- Registry access record: 2026-06-05, HTTP 200.
- Image fetch used for this object page: 2026-08-21 UTC.
- Source object dossier: `src-metmuseum-oracle-bone`.

The registry route proves the API snapshot and the image URLs as source
routes. The object page does not supply a plate, Heji entry, or full text.

Exact paths are recorded as host plus path here and as full URLs in the
source record and central registry:

- API path: `/public/collection/v1/objects/42022`.
- Primary image path: `/CRDImages/as/original/LC-18_56_71_002.jpg`.
- Additional image path: `/CRDImages/as/original/LC-18_56_71_001.jpg`.

[object-page]: https://www.metmuseum.org/art/collection/search/42022
[api-route]: https://collectionapi.metmuseum.org
[primary-route]: https://images.metmuseum.org
[additional-route]: https://images.metmuseum.org
