# Source Access Boundary Review / 来源访问边界复核

## Human Result / 人类阅读结果

- Affected source count: 7
- Grouped failure-condition task count: 8
- Preserved access-attempt count: 16
- Older source-engineering access/checksum gap rows: 9

原始访问记录逐条保留，但人工任务按来源和故障条件归并。无来源
payload 时没有 checksum 是同一访问边界的结果，不再另算一次任务。
重试次数不会增加人类任务数；只有新的故障条件才新增任务。

Access attempts remain separate provenance records. Human tasks are
grouped by source and failure condition. A missing checksum for an
unsaved payload is evidence of the same access boundary, not a second
independent review task.

## Grouped Tasks / 归并后任务

### `src-british-museum-oracle-bone`

- HTTP 403 boundary / HTTP 403 访问边界
- Attempts preserved: 2
- Download IDs / 下载记录：
  - `dl-british-museum-oa-165`
  - `dl-british-museum-oa-165-recheck-20260727`
- Status counts: http_error:2
- Latest attempt: 2026-07-26T22:18:08+00:00
- Reviewed browser metadata: browser-meta-000001
- Next checks: open_official_object_route_in_reviewed_browser;
  record_metadata_only_boundary_if_payload_remains_blocked

### `src-sinica-da-xiaoxuetang-site`

- TLS certificate validation failure / TLS 证书校验失败
- Attempts preserved: 2
- Download IDs / 下载记录：
  - `dl-sinica-da-xiaoxuetang-site`
  - `dl-sinica-da-xiaoxuetang-site-recheck-20260727`
- Status counts: download_error:2
- Latest attempt: 2026-07-26T22:18:09+00:00
- Next checks: verify_current_official_domain_and_certificate_state;
  do_not_disable_tls_validation_or claim_payload_access

### `src-sinica-yinshang-oracle-vocabulary`

- TLS certificate validation failure / TLS 证书校验失败
- Attempts preserved: 2
- Download IDs / 下载记录：
  - `dl-sinica-yinshang-oracle-vocabulary`
  - `dl-sinica-yinshang-oracle-vocabulary-recheck-20260727`
- Status counts: download_error:2
- Latest attempt: 2026-07-26T22:18:15+00:00
- Next checks: verify_current_official_domain_and_certificate_state;
  do_not_disable_tls_validation_or claim_payload_access

### `src-smithsonian-nmaa-oracle-bone`

- HTTP 403 boundary / HTTP 403 访问边界
- Attempts preserved: 1
- Download IDs / 下载记录：
  - `dl-smithsonian-nmaa-fsc-o-28`
- Status counts: http_error:1
- Latest attempt: 2026-06-05T06:55:31+00:00
- Historical successful context: dl-smithsonian-nmaa-fsc-o-26-archive
- Next checks: open_official_object_route_in_reviewed_browser;
  record_metadata_only_boundary_if_payload_remains_blocked

### `src-xiaoxuetang-jiaguwen`

- Access-restricted response / 受限访问响应
- Attempts preserved: 2
- Download IDs / 下载记录：
  - `dl-xxt-jgw-home`
  - `dl-xxt-jgw-about`
- Status counts: downloaded_access_restricted_page:2
- Latest attempt: 2026-06-04T09:28:31+00:00
- Next checks: open_saved_restricted_page_then_manually_verify_official_route;
  do_not_treat_restricted_html_as_source_content

### `src-xiaoxuetang-jiaguwen`

- TLS handshake failure / TLS 握手失败
- Attempts preserved: 2
- Download IDs / 下载记录：
  - `dl-xxt-jgw-kaiorder-0502`
  - `dl-xxt-jgw-kaiorder-1176`
- Status counts: download_error:2
- Latest attempt: 2026-06-11T11:06:09.7325982Z
- Next checks: verify_current_official_route_in_independent_browser;
  record_route_change_before_another automated retry

### `src-xiaoxuetang-obm`

- Access-restricted response / 受限访问响应
- Attempts preserved: 4
- Download IDs / 下载记录：
  - `dl-xxt-obm-example`
  - `dl-xxt-obm-guide`
  - `dl-xxt-obm-appendix01`
  - `dl-xxt-obm-appendix02`
- Status counts: downloaded_access_restricted_page:4
- Latest attempt: 2026-06-04T10:47:36+00:00
- Next checks: open_saved_restricted_page_then_manually_verify_official_route;
  do_not_treat_restricted_html_as_source_content

### `src-yinqi-wenyuan`

- Network timeout / 网络超时
- Attempts preserved: 1
- Download IDs / 下载记录：
  - `dl-yinqi-home-recheck-20260727`
- Status counts: download_error:1
- Latest attempt: 2026-07-26T20:41:47+00:00
- Historical successful context: dl-yinqi-home
- Next checks: compare_latest_timeout_with_historical_success;
  retry_only_when_network_condition_or_official_route_changes

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
