---
name: red-trade-reflection
description: Find commonalities across Red/losing trades from confluences and notes for reflection. Use after screenshots are renamed.
disable-model-invocation: true
icon: bug
color: red
---

# Red trade reflection

Analyze losing trades to support honest process reflection.

## Source of files

1. Prefer renamed Red trades in `renamed/` (filenames containing `_Red`)
2. Fall back to user-selected files if provided
3. Read confluences and notes from the screenshot content and any sidecar notes

## Process

1. Collect Red trades only.
2. Extract confluences, playbook, direction, and freeform notes from each.
3. Find recurring failure patterns and missing pieces versus typical Green trades when renamed Green files are available.
4. Focus on process, confluence gaps, and repeated emotional/notes language — not shame.
5. Write the review to `reviews/` with dated filename, e.g. `reviews/YYYY-MM-DD-red-reflection.md`.

## Output format

```markdown
# Red trade reflection — [date range]

## Dataset
- Trades included:
- Playbooks seen:

## Top recurring failure patterns
1. ... (example filenames)

## Missing confluences vs Green trades
1. ...

## Repeating process / emotion notes
1. ...

## Avoid checklist
- [ ] ...

## Reflection questions
1. ...
2. ...
3. ...

## Facts vs inferences
- Facts:
- Inferences:

## Limits
- What this sample cannot prove yet
```

## Hard rules

- Not financial advice.
- Do not invent mistakes or notes that are not supported by the screenshots.
- Cite example filenames for each major pattern.
- Be direct and constructive; no moralizing.
