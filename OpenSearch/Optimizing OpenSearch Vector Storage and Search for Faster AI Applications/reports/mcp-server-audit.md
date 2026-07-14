# ML Commons MCP Server Audit: bg-opensearch-test

**Date:** 2026-07-13
**Auditor:** Automated test run (curl against the cluster REST and MCP endpoints)

## Environment

```
Cluster:    bg-opensearch-test (Instaclustr managed)
Version:    OpenSearch 3.5.0
Topology:   7 nodes (3 data nodes with roles data/ingest/ml,
            3 dedicated cluster managers, 1 coordinator-only node)
Endpoint:   https://load-balancer.40134c8195b149f2bd4024f0dd1392cf.cnodes.io:9200
Auth:       Basic auth, user icopensearch (password redacted)
Transport:  HTTPS through the Instaclustr load balancer
MCP server: OpenSearch-MCP-Stateless-Server, version 0.1.0 (ML Commons plugin)
```

## Executive summary

The built-in ML Commons MCP server on OpenSearch 3.5.0 works end to end on this Instaclustr managed cluster: enable, tool registration, tool listing, tool update, tool removal, the Streamable HTTP JSON-RPC handshake, and live tool calls (list indexes, read a mapping, run a search) all succeeded, and authentication is correctly enforced with 401 on both the MCP endpoint and the management APIs. Median round-trip for an MCP call through the load balancer was about 194 ms. Two rough edges matter for users: registering a tool without an explicit `name` field fails with a cryptic 400, and a tool call against a nonexistent index can return an internal transport-action string that leaks a node IP instead of a plain "no such index" message. The legacy SSE transport endpoint does not exist on 3.5, so Streamable HTTP is the only transport. Of 23 recorded checks, 21 passed, 1 were partial, and 1 failed (SSE, which is absent by design on this version).

## Results table

| Test # | Area | Test | Expected | Actual | Result |
|---|---|---|---|---|---|
| 0 | Pre-audit | Capture starting state | Factory baseline | Setting already true and 3 tools already registered from an earlier probe; removed and reset before starting | PASS |
| 1 | Lifecycle | Baseline of `plugins.ml_commons.mcp_server_enabled` with `include_defaults` | Default false, no explicit value | `defaults.plugins.ml_commons.mcp_server_enabled: "false"`, no persistent or transient value after cleanup | PASS |
| 2 | Lifecycle | Tool list while server disabled | "Not enabled" error | Clear message: "The MCP server is not enabled. To enable, please update the setting plugins.ml_commons.mcp_server_enabled". Returned as HTTP 500 rather than a 4xx | PASS |
| 3 | Lifecycle | Enable via persistent cluster setting | acknowledged true | `{"acknowledged":true}` with the setting echoed back as "true" | PASS |
| 4 | Tool mgmt | Register ListIndexTool, IndexMappingTool, SearchIndexTool in one call | created true per node | First attempt without `name` fields failed with 400 "[match] requires query value". With explicit `name` per tool: `created:true` from all 7 nodes | PASS |
| 5 | Tool mgmt | GET tools/_list shows all three | 3 tools with create_time | All 3 returned with type, name, description, create_time | PASS |
| 6 | Tool mgmt | Register a duplicate tool name | Clear error | HTTP 400: "Unable to register tool: a tool with the same name already exists." | PASS |
| 7 | Tool mgmt | POST tools/_update to change a description | Endpoint works or clean error | Endpoint exists on 3.5. `updated:true` from all 7 nodes; _list shows the new description plus a `last_update_time` field | PASS |
| 8 | Tool mgmt | Remove one tool, verify 2 remain, re-register | removed true, list of 2, created true | `removed:true` on all 7 nodes, _list showed exactly 2, re-register returned `created:true` on all 7 nodes | PASS |
| 9 | MCP protocol | initialize handshake (protocolVersion 2025-03-26) | serverInfo returned | serverInfo: name "OpenSearch-MCP-Stateless-Server", version "0.1.0"; capabilities include tools.listChanged true; instructions state the server is stateless with no sessions | PASS |
| 10 | MCP protocol | tools/list | All tools with JSON schemas | All 3 tools returned with full inputSchema objects including required fields and additionalProperties false | PASS |
| 11 | MCP protocol | tools/call ListIndexTool with `{"indices": []}` | Cluster index listing | CSV-style listing of 13 indexes with health, doc counts, and store sizes; isError false | PASS |
| 12 | MCP protocol | tools/call IndexMappingTool on mcp-audit-temp | Mapping returned | Calls against fresh index mcp-audit-temp returned the full mapping and settings | PASS |
| 13 | MCP protocol | tools/call SearchIndexTool, match title "martian" on mcp-audit-temp | One hit (The Martian) | Against mcp-audit-temp seeded with a "The Martian" document, the tool returned the hit with _source and _score; isError false | PASS |
| 14 | Error handling | Nonexistent index, unknown tool, malformed JSON-RPC | Helpful errors | Mixed. ListIndexTool on a nonexistent index: cryptic "[ip-10-2-158-33][10.2.158.33:9300][indices:monitor/settings/get]" (leaks node IP, no mention of the index). Unknown tool: proper -32602 with data "Tool not found: NoSuchToolXYZ", though the message field reads "Unknown tool: invalid_tool_name". Malformed body: proper -32700 Parse error | PARTIAL |
| 15 | End to end | Fresh index mcp-audit-temp: create, doc, search and mapping via MCP, delete | All succeed | Index created, doc indexed with refresh, both tool calls succeeded (see 12 and 13), index deleted afterward | PASS |
| 16 | Transport | SSE endpoint /_plugins/_ml/mcp/sse | Stream opens | Endpoint does not exist on 3.5: "no handler found" for both GET and POST, also with append_to_base_url=true. GET on /_plugins/_ml/mcp returns 405, which is spec-compliant for a stateless Streamable HTTP server. Streamable HTTP is the only transport on this version | FAIL |
| 17 | Security | initialize with wrong credentials | 401 | HTTP 401 Unauthorized, no JSON-RPC processing | PASS |
| 18 | Security | tools/_list with wrong credentials | 401 | HTTP 401 Unauthorized | PASS |
| 19 | Performance | 5 initialize calls, wall time | Reasonable latency | min 0.183 s, median 0.194 s, max 0.215 s through the load balancer, all HTTP 200 | PASS |
| 20 | Restoration | Remove all three tools | removed true, empty list | `removed:true` on all 7 nodes; tools/_list returned `{"tools":[]}` | PASS |
| 21 | Restoration | Reset mcp_server_enabled to null | Setting gone, endpoints disabled | `{"acknowledged":true,"persistent":{},"transient":{}}`. tools/_list returns the "not enabled" error again. Persistent settings block contains no mcp keys (pre-existing course-related ml_commons settings were left untouched) | PASS |
| 22 | Restoration | No mcp-audit-* index remains | Empty result | `_cat/indices/mcp-audit-*` returned zero rows | PASS |
| 23 | Restoration | Overall restoration verified as found | Cluster back to baseline | MCP setting unset (default false), tool registry empty, no audit indexes, no course or platform index touched. Note the "as found" state was itself dirty (see Test 0); the cluster was restored to the correct factory baseline rather than the dirty state | PASS |

Totals: 21 PASS, 1 PARTIAL, 1 FAIL.

## Capability checklist

- [x] Server enable via persistent cluster setting
- [x] Tool register (requires explicit `name` per tool, see Finding 2)
- [x] Tool list (REST management API)
- [x] Tool update (tools/_update exists and works on 3.5)
- [x] Tool remove
- [x] Streamable HTTP handshake (initialize)
- [x] tools/list over MCP protocol
- [x] tools/call ListIndexTool
- [x] tools/call IndexMappingTool
- [x] tools/call SearchIndexTool
- [ ] SSE transport (endpoint absent on 3.5, Streamable HTTP only)
- [x] Auth enforcement (401 on MCP endpoint and on management APIs)
- [x] Clean disable and full restoration

## Findings and caveats

- **Tool registration silently depends on the `name` field.** Registering with only `type` and `description` fails with HTTP 400 "[match] requires query value", which is an internal query-validation error surfacing instead of a proper "name is required" message. With `name` set explicitly on each tool, registration works first try. Course material must always include `name`.
- **Error-message quality is inconsistent, with a minor information leak.** A ListIndexTool call against a nonexistent index returned `[ip-10-2-158-33][10.2.158.33:9300][indices:monitor/settings/get]` as the entire error message. That is unhelpful to a user and it exposes an internal node IP and transport action name to any MCP client. By contrast, IndexMappingTool and SearchIndexTool return a clean "no such index [x]" for the same situation, and malformed JSON-RPC gets a proper -32700 Parse error.
- **Unknown-tool error contains placeholder text.** Calling a tool that does not exist returns code -32602 with message "Unknown tool: invalid_tool_name". The useful detail is in the `data` field ("Tool not found: NoSuchToolXYZ"), but the message field looks like an unfilled template.
- **Disabled-state errors use HTTP 500.** When the server is disabled, management endpoints return a clear, actionable message, but with status 500 rather than a 4xx. Monitoring that alerts on 5xx codes could misread a deliberately disabled feature as a server fault.
- **No SSE transport on 3.5.** The `/_plugins/_ml/mcp/sse` endpoint returns "no handler found" for every method tried. Streamable HTTP at `/_plugins/_ml/mcp` is the only transport, and it identifies itself as a stateless server (no sessions, GET returns 405). Course text and client configs should not reference SSE.
- **Tool registration fans out to all 7 nodes.** Register, update, and remove calls each return per-node acknowledgments from all seven nodes, including the three dedicated cluster managers and the coordinator-only node, not just the ml-role data nodes.
- **Latency is fine.** About 190 ms per MCP round trip through the load balancer (min 0.183 s, median 0.194 s, max 0.215 s over 5 initialize calls). No timeouts or hangs were observed in any test.
- **Support status.** The MCP server is an experimental ML Commons feature (server self-reports version 0.1.0) and is not an officially supported feature of the Instaclustr managed platform.

