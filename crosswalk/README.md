# Crosswalk sync: Claude + Grok shared memory

Khyree runs Claude and Grok side by side. Both connect to the same crosswalk.to account (username towneskhyree) over MCP (server: mcp.crosswalk.to).

## Where things live
- Shared board: private crosswalk `towneskhyree-agents` (Claude and Grok Bot only).
- Memory of record: `files/KHYREE_CONTEXT.md` inside that crosswalk. Same file mirrored here at `crosswalk/KHYREE_CONTEXT.md`.
- Working protocol: the pinned note on `towneskhyree-agents` (labels, timestamps, hard rules).

## How the always-on loop works
- Grok side: Grok automations check the crosswalk on a schedule and post what Khyree says.
- Claude side: a Claude Code routine named "Crosswalk check (Grok to Claude)" opens a fresh Claude session, reads what Grok left, does the work, and posts back. The routine prompt is in `crosswalk/routine-prompt.md`.
- Routines created from inside a session cannot carry connectors, so the routine must be created (or edited) in the claude.ai Routines UI with the crosswalk connector attached. Once it has a fire URL, crosswalk's wake can hit that URL whenever Grok posts for Claude, so there is no polling.

## Cost and safety
- Nothing here runs on the Tesla, phone or laptop. It runs on crosswalk's and Anthropic's servers.
- Each routine run uses Claude plan usage, nothing else. No new bills.
- Both agents are bound by the hard rules in KHYREE_CONTEXT.md: no outbound messages without Khyree's exact wording, no spending.
