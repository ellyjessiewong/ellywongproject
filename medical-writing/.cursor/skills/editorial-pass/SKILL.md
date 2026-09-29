---
name: editorial-pass
description: Editorial polish for medical writing while preserving approved claim language. Use for style, clarity, consistency, and length edits.
disable-model-invocation: true
icon: book-open
color: green
---

# Editorial pass

Polish draft copy for clarity and house style without changing approved medical claim meaning.

## Inputs

Ask for any missing item:

1. Draft to edit
2. Style guide (`style/style-guide.md`)
3. Optional constraints: character limits, channel, US/UK spelling, trademark rules
4. Optional: claim bank, if claim strings must be preserved exactly

## Process

1. Identify spans that are approved claim language (exact bank strings or user-marked claims).
2. Edit freely around those spans for clarity, grammar, consistency, and length.
3. Treat approved claim strings as locked:
   - Do not strengthen, weaken, or rephrase them.
   - If a claim must change to fit a limit, propose an alternative in the change log and mark `Needs MLR review`.
4. Apply style-guide rules: product names, abbreviations, capitalization, lists, numerals, trademarks, footnote style.
5. Check consistency of drug name, indication phrasing, and repeated boilerplate.
6. Return the edited draft plus a change log.

## Output format

```markdown
# Editorial pass: [piece name]

## Edited draft
...

## Change log
| Location | Before | After | Type | Claim impact |
| --- | --- | --- | --- | --- |
| ... | ... | ... | style / clarity / length / consistency | none / claim preserved / needs MLR review |

## Preserved claim strings
| Claim ID or label | Exact text preserved |
| --- | --- |

## Still needs human review
- ...
```

## Hard rules for this skill

- Never invent new clinical or promotional claims while editing.
- Never alter fair-balance / ISI / mandatory language unless the user supplies replacement approved text.
- Prefer smaller edits over rewrites.
- If shortening would change claim meaning, say so and stop rather than forcing a fit.
