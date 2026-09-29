---
name: copy-deck
description: Build a pharmaceutical marketing copy deck from a brief and approved claims. Use when creating slide, section, or channel copy decks.
disable-model-invocation: true
icon: book-open
color: blue
---

# Copy deck

Create a structured copy deck using only approved claim language from this workspace.

## Inputs

Ask for any missing item before drafting:

1. Brief or creative request (`drafts/` or `@` file)
2. Product / brand / audience / channel (if not in the brief)
3. Approved claim bank (`claims/claim-bank.md` unless the user points elsewhere)
4. Style guide (`style/style-guide.md`)
5. Any mandatory / fair-balance / ISI constraints the user provides

## Process

1. Read the brief and extract: objective, audience, channel, required sections, length limits, must-include topics.
2. Pull candidate claims **only** from the claim bank. Prefer claims whose audience/channel/status fit the brief.
3. Map claims to deck sections before writing full copy.
4. Draft copy using exact approved claim wording whenever possible.
5. If a needed message is not in the bank, add a `GAP` row — do **not** invent claim language.
6. Apply house style from `style/style-guide.md` for non-claim connective tissue only (transitions, section labels, UI chrome).
7. End with a claim usage index and open questions for medical/legal review.

## Output format

Use this structure:

```markdown
# Copy deck: [piece name]

## Meta
- Channel:
- Audience:
- Brief:
- Claim bank used:
- Status: Draft for MLR / internal review

## Deck

### Section 1 — [name]
- **Headline:** ...
- **Body:** ...
- **Claim IDs:** CLAIM-001, CLAIM-002
- **Reference IDs:** REF-001
- **Notes:** exact approved wording | adapted for length (needs review) | layout only

### Section 2 — ...

## Claim usage index
| Claim ID | Where used | Exact / Adapted | Refs |
| --- | --- | --- | --- |

## Gaps / unsupported needs
| Needed message | Why needed | Suggested next step |
| --- | --- | --- |

## Review flags
- ...
```

## Hard rules for this skill

- Never invent efficacy, safety, comparative, or indication language.
- Never invent references.
- Mark adapted claim wording clearly so it can be reviewed.
- Keep promotional vs mandatory/fair-balance content visually separate when the user provides mandatory language.
