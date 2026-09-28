# Work assistant — medical writing

This workspace is a Cursor work assistant for pharmaceutical marketing medical writing.

## What this folder is for

- Copy deck creation from briefs + approved claims
- Fact checking against the approved claim data bank
- Referencing from the claim bank and linked references
- Editorial polish that does not change approved claim meaning

## Source of truth

| Path | Contents |
| --- | --- |
| `claims/claim-bank.md` | Approved claim language + claim IDs |
| `references/reference-library.md` | Approved references linked to claims |
| `style/style-guide.md` | House style and editorial conventions |
| `drafts/` | Briefs and in-progress copy |
| `decks/` | Finished or in-progress copy decks |

## How to work here

1. Put or update approved materials in `claims/`, `references/`, and `style/`.
2. Put the brief or draft in `drafts/`.
3. In Agent chat, run a skill with `/`:
   - `/copy-deck`
   - `/fact-check`
   - `/reference-claims`
   - `/editorial-pass`
4. `@` the relevant files (brief, draft, claim bank) when you invoke the skill.

## Hard constraints

- Use only approved claims and references from this workspace.
- Never invent medical claims, study results, or citations.
- Prefer exact approved claim wording; flag any rewrite for medical/legal review.
- Every substantive claim in output must include claim ID and linked reference IDs when available.
