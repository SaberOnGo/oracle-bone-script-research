# Xiaoxuetang OBM Access Boundary Review Log Draft / 小學堂 OBM 访问边界复核日志草稿

## Status / 状态

- Review log draft ID / 复核日志草稿 ID: `xxt-obm-access-review-log-draft-0001`
- Follow-up review task ID / 后续复核任务 ID: `xxt-obm-followup-review-0001`
- Draft status / 草稿状态: `draft_not_collected`
- Evidence collection status / 证据收集状态: `not_collected`
- Human review status / 人工复核状态: `not_started`
- Formal schema compatibility / 正式 schema 兼容状态: `not_formal_inscription_or_obs_char_schema`
- Research boundary / 研究边界: `xxt_obm_access_boundary_review_log_draft_not_scholarship`
- Updated at / 更新时间: `2026-06-11`

## Route / 路由

- Source ID / 来源 ID: `src-xiaoxuetang-obm`
- Targeted download ID / 目标下载 ID: `dl-xxt-obm-appendix01`
- Targeted URL / 目标 URL: `https://xiaoxue.iis.sinica.edu.tw/obm/Home/Appendix01`
- Artifact kind / 资料类型: `old_catalog_abbreviation_appendix`

## Route Files To Open / 待打开路由文件

- `corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv`
- `corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv`
- `project_registry/006_large-source-register/002_source-download-log.csv`
- `corpus/006_research-sources-and-bibliography/000_source-registers/011_core-institutional-access-profile.csv`
- `corpus/006_research-sources-and-bibliography/000_source-registers/012_obm-abbreviation-staging.csv`

## Review Sections / 复核章节

English: Existing queue-074 metadata is materialized below for review.
It is access-boundary evidence only, not row-level import proof,
not an old-catalog confirmation, not a holding match, and not a
decipherment conclusion.

简体中文：以下只把 074 队列已有 metadata 实体化为复核快照。
这只是访问边界证据，不是行级导入证据、旧著录确认、
馆藏匹配或释读结论。

### Existing Access Boundary Snapshot / 已有访问边界快照

- commit_policy: `download_to_tmp_log_checksum_only`
- download_status: `downloaded_access_restricted_page`
- http_status: `200`
- logged_file_size_bytes: `36917`
- logged_checksum_sha256:
-   - `6465bc25b5527f4605db42effef880065e97ee6553bcfc5a68674480f7215781`
- profile_match_count: `1`
- profile_ids: `source-access-000016`
- profile_areas: `appendix_staging_boundary`
- profile_review_statuses: `source-access-000016=reviewed_metadata_only`
- profile_normalized_values:
-   - `source-access-000016=old_catalog_book_abbrev_rows_staged=90`
- staging_row_count: `90`
- staging_row_kind_counts: `old_catalog_book_abbreviation=90`
- staging_review_statuses:
-   - `obm-oldcat-abbrev-0001=reviewed_metadata_only`
-   - `obm-oldcat-abbrev-0002=reviewed_metadata_only`
-   - `obm-oldcat-abbrev-0003=reviewed_metadata_only`
-   - `obm-oldcat-abbrev-0004=reviewed_metadata_only`
-   - `obm-oldcat-abbrev-0005=reviewed_metadata_only`
- route_file_count: `5`
- missing_route_file_count: `0`
- route_file_review_status: `reviewed_route_files_exist`

### Source Register Row / 来源登记行

- Status / 状态: `metadata_captured_from_074_queue`
- Evidence items / 证据条目:
  - source_id: `src-xiaoxuetang-obm`
  - rights_status: `metadata_only_until_verified`
  - risk_note:
  -   - `Site returned an access-restricted HTML page`
  -   - ` treat as access evidence only.`
- Notes / 备注:
  - English: Verify source ID, download ID, rights status, and risk note.
  - 简体中文：打开来源行；核对来源 ID、下载 ID、权利状态和风险说明。

### Source Download Manifest Row / 来源下载 manifest 行

- Status / 状态: `metadata_captured_from_074_queue`
- Evidence items / 证据条目:
  - targeted_download_id: `dl-xxt-obm-appendix01`
  - targeted_url: `https://xiaoxue.iis.sinica.edu.tw/obm/Home/Appendix01`
  - artifact_kind: `old_catalog_abbreviation_appendix`
  - download_status: `downloaded_access_restricted_page`
- Notes / 备注:
  - English: Confirm URL, artifact kind, status, and route files.
  - 简体中文：打开下载 manifest 行；确认 URL、资料类型、状态和路由文件。

### Download Log Row / 下载日志行

- Status / 状态: `metadata_captured_from_074_queue`
- Evidence items / 证据条目:
  - http_status: `200`
  - logged_file_size_bytes: `36917`
  - logged_checksum_sha256:
  -   - `6465bc25b5527f4605db42effef880065e97ee6553bcfc5a68674480f7215781`
- Notes / 备注:
  - English: Verify access result, size, checksum, and timestamp.
  - 简体中文：打开下载日志行；核对访问结果、大小、checksum 和时间戳。

### Access Profile Rows / 访问画像行

- Status / 状态: `metadata_captured_from_074_queue`
- Evidence items / 证据条目:
  - profile_match_count: `1`
  - profile_ids: `source-access-000016`
  - profile_areas: `appendix_staging_boundary`
  - profile_review_statuses: `source-access-000016=reviewed_metadata_only`
  - profile_normalized_values:
  -   - `source-access-000016=old_catalog_book_abbrev_rows_staged=90`
- Notes / 备注:
  - English: Verify access result, restriction status, and permitted route.
  - 简体中文：打开访问画像行；核对访问结果、受限状态和允许路线。

### Staging Rows When Available / 已存在的 staging 行

- Status / 状态: `metadata_captured_from_074_queue`
- Evidence items / 证据条目:
  - staging_row_count: `90`
  - staging_row_kind_counts: `old_catalog_book_abbreviation=90`
  - staging_review_statuses:
  -   - `obm-oldcat-abbrev-0001=reviewed_metadata_only`
  -   - `obm-oldcat-abbrev-0002=reviewed_metadata_only`
  -   - `obm-oldcat-abbrev-0003=reviewed_metadata_only`
  -   - `obm-oldcat-abbrev-0004=reviewed_metadata_only`
  -   - `obm-oldcat-abbrev-0005=reviewed_metadata_only`
- Notes / 备注:
  - English: Open staging rows before old-catalog, holding, or row claims.
  - 简体中文：提出旧著录、馆藏或行级主张前，先打开 staging 行。

### Official Access Boundary / 官方访问边界

- Status / 状态: `metadata_captured_from_074_queue`
- Evidence items / 证据条目:
  - download_status: `downloaded_access_restricted_page`
  - risk_note:
  -   - `Site returned an access-restricted HTML page`
  -   - ` treat as access evidence only.`
  - commit_policy: `download_to_tmp_log_checksum_only`
- Notes / 备注:
  - English: Check official boundary before public derivative decisions.
  - 简体中文：记录公开派生决定前，先核查官方页面访问边界。

### Review Log / 复核日志

- Status / 状态: `metadata_captured_from_074_queue`
- Evidence items / 证据条目:
  - route_file_count: `5`
  - missing_route_file_count: `0`
  - route_file_review_status: `reviewed_route_files_exist`
- Notes / 备注:
  - English: Record source-marked access observations; keep import claims empty.
  - 简体中文：只记录带来源标记的访问观察；保持导入和身份主张为空。

## Required Next Checks / 必需下一步检查

- `open_registered_source_and_download_rows`
  - English: Open registered source, manifest, and download-log rows.
  - 简体中文：打开已登记的来源行、下载 manifest 行和下载日志行。
- `open_access_profile_rows`
  - English: Open the cited OBM access-profile rows.
  - 简体中文：打开被引用的 OBM 访问画像行。
- `open_staging_rows_before_old_catalog_or_holding_claims`
  - English: Open staging rows before old-catalog or holding claims.
  - 简体中文：在提出旧著录或拓藏/馆藏主张前先打开已分期的简称行。
- `use_manual_browser_or_institutional_export_before_any_row_level_claim`
  - English: Use browser or institutional export before row-level claims.
  - 简体中文：在提出任何行级主张前，先使用人工浏览或机构导出路径。
- `record_no_identity_assignment_or_decipherment_claim`
  - English: Record no identity, assignment, or decipherment claim.
  - 简体中文：记录本后续复核不提出身份、分配或释读结论。

## Rights And Risk / 权利与风险

- Rights status / 权利状态: `metadata_only_until_verified`
- Risk note / 风险说明: Site returned an access-restricted HTML page; treat as access evidence only.

## Review Log / 复核日志

- Status / 状态: `created_from_074_followup_review_queue`
- Evidence collection / 证据收集: `not_collected`
- Decision / 决定: no row-level import, no old-catalog confirmation, no holding match, no inscription assignment, and no decipherment conclusion.

## Caution / 警示

English: This draft is a routing scaffold only for Xiaoxuetang OBM access-boundary follow-up. It is not source evidence, not a Heji row import, not an old-catalog confirmation, not a holding or collection match, not a formal inscription assignment, and not a decipherment conclusion.

简体中文：本草稿只是小學堂 OBM 访问边界后续复核的路由脚手架；不是来源证据，不是《合集》行导入，不是旧著录确认，不是馆藏/拓藏匹配，不是正式卜辞分配，也不是释读结论。
