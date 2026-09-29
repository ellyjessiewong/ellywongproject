---
name: green-edge-review
description: Find commonalities across Green/winning trades from confluences and notes to reinforce edge. Use after screenshots are renamed.
disable-model-invocation: true
icon: beaker
color: green
---

# Green edge review

Analyze winning trades to reinforce what is working.

## Source of files

1. Prefer renamed Green trades in `renamed/` (filenames containing `_Green`)
2. Fall back to user-selected files if provided
3. Read confluences and notes from the screenshot content and any sidecar notes

## Process

1. Collect Green trades only.
2. Extract confluences, playbook, direction, and freeform notes from each.
3. Find recurring patterns across winners.
4. Compare lightly to Red trades only if useful for contrast; keep the focus on Green edge.
5. Write the review to `reviews/` with dated filename, e.g. `reviews/YYYY-MM-DD-green-edge.md`.

## Output format

```markdown
# Green edge review — [date range]

## Dataset
- Trades included:
- Playbooks seen:

## Top recurring confluences
1. ... (example filenames)

## Notes / process patterns on winners
1. ...

## Strongest playbooks (from this sample)
| Playbook | Green count | Common confluences |
| --- | --- | --- |

## Edge checklist (before entry)
- [ ] ...

## Facts vs inferences
- Facts:
- Inferences:

## Limits
- What this sample cannot prove yet
```

## Hard rules

- Not financial advice.
- Do not invent confluences that are not visible in the notes/screenshots.
- Cite example filenames for each major pattern.
