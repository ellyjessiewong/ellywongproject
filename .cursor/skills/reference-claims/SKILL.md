---
name: reference-claims
description: Attach references from the approved claim bank and reference library to draft statements. Use when adding footnotes, citations, or a reference list.
disable-model-invocation: true
icon: book-open
color: cyan
---

# Reference claims

Map draft claims to approved claim IDs and their linked references. Insert citations in house format. Never invent sources.

## Inputs

Ask for any missing item:

1. Draft or copy deck to reference
2. Claim bank (`claims/claim-bank.md`)
3. Reference library (`references/reference-library.md`)
4. Style guide citation format (`style/style-guide.md`)

## Process

1. Identify each substantive claim in the draft that needs a citation.
2. Match it to a claim ID in the claim bank.
3. Pull linked reference IDs from that claim entry.
4. Resolve each reference ID in `references/reference-library.md`.
5. Insert in-text / footnote markers using the house citation style.
6. Build a deduplicated reference list in the order required by the style guide.
7. List unresolved items: claim with no refs, ref ID missing from library, draft text with no claim match.

## Output format

```markdown
# Referencing pass: [piece name]

## Annotated copy
[draft with citation markers inserted]

## Claim → reference map
| Location | Draft claim / text | Claim ID | Reference IDs | Citation markers |
| --- | --- | --- | --- | --- |

## Reference list
1. [formatted citation]
2. ...

## Unresolved
| Item | Problem | Needed action |
| --- | --- | --- |
```

## Hard rules for this skill

- Use only references linked through the approved claim bank / reference library.
- Do not fabricate authors, titles, journals, years, DOIs, or URLs.
- Do not “borrow” a nearby reference for an unsupported claim.
- If a claim has no linked reference, mark it unresolved instead of guessing.
- Preserve existing citation numbering when the user asks for a minimal-diff update.
