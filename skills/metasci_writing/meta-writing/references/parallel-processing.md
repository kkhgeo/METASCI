# Parallel Processing (Subagent)

Read this when Loop 1 counts enough sources to make parallel reading worthwhile.
For one or two sources, run sequentially — dispatch overhead exceeds the saving.

## Dispatch thresholds

| Condition | Action |
|---|---|
| 3 or more Knowledge files | Dispatch one subagent per file |
| 2 or more PDFs | Dispatch one subagent per file |
| Figures and tables both present | Dispatch one subagent per data type |
| 2 or more web queries | Dispatch one subagent per query |
| 1-2 sources total | Run sequentially |

## What parallelises, and what does not

| Task | Parallel | Reason |
|---|---|---|
| Reading several Knowledge files | Yes | Independent inputs |
| Reading several PDFs | Yes | Independent inputs |
| Analysing My Data (figures + tables) | Yes | Independent inputs |
| Web search across several queries | Yes | Independent inputs |
| Writing (Loop 5) | No | Requires the merged source set |
| Verification (Phase 4) | No | Depends on the finished draft |

Loops 2, 3, and 4 hold the parallelisable work. Loop 5 and Phase 4 are sequential.

## Subagent prompt — Knowledge file reading

```
You are analysing an academic Knowledge markdown file.

Extract every Claim + Citation pair relevant to the topic "[topic]".

Assign each pair one category:
- Theoretical Foundations
- Empirical Precedents
- Methodological Heritage
- Contextual Knowledge
- Critical Discourse

File:
[file contents]

Return a table and nothing else:
| Claim | Citation | Category | Source |
|-------|----------|----------|--------|

Copy each Claim as the source states it. These are notes for the writer,
not draft prose — the writer restates them. Preserve the original's hedging
level and scope so the restatement can too.
```

## Subagent prompt — PDF reading

Use the same shape, substituting the PDF path for the file contents and adding:

```
Record the page or section each Claim came from, so the writer can verify it
against the original during Phase 4 Step 3.
```

## Merging returns

Collect every subagent's table into one list before Loop 5 begins. Where two
subagents returned the same Claim from different sources, keep both rows —
independent support for one claim is worth recording, and Loop 5 decides
whether to cite one or both.
