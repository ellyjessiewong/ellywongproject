---
name: fact-check
description: Verify draft copy against the approved claim data bank. Use for claim accuracy, wording drift, and unsupported-statement review.
disable-model-invocation: true
icon: shield
color: orange
---

# Fact check

Compare draft copy to the approved claim bank and report what is supported, drifted, or unsupported.

## Inputs

Ask for any missing item:

1. Draft to check (`drafts/`, `decks/`, or pasted text)
2. Claim bank (`claims/claim-bank.md` unless the user points elsewhere)
3. Optional: product, audience, or indication filter if the bank is large

## Process

1. Break the draft into checkable statements (headlines, body claims, footnotes that assert facts).
2. For each statement, search the claim bank for an exact or near match.
3. Classify each statement:
   - `PASS` — exact approved wording (or clearly non-claim UI/label text)
   - `ADAPTED` — same meaning as an approved claim, but wording changed; needs MLR review
   - `DRIFT` — stronger/weaker/different meaning than the nearest approved claim
   - `UNSUPPORTED` — no matching approved claim
   - `CONFLICT` — contradicts another used claim or bank entry
4. Flag absolute language, comparative claims, and indication/audience mismatches.
5. Do **not** silently rewrite claims to “fix” them. Report first; suggest fixes only as optional review text.

## Output format

```markdown
# Fact check: [piece name]

## Summary
- PASS:
- ADAPTED:
- DRIFT:
- UNSUPPORTED:
- CONFLICT:

## Line-by-line review
| Location | Draft text | Status | Matching claim ID | Bank wording | Issue |
| --- | --- | --- | --- | --- | --- |

## Highest-priority issues
1. ...

## Optional compliant replacements
Only suggest replacements that are exact bank wording, or clearly marked as needing review.

| Location | Suggested text | Claim ID | Notes |
| --- | --- | --- | --- |
```

## Hard rules for this skill

- Source of truth is the claim bank, not general medical knowledge.
- Never invent supporting claims or study results.
- If the bank is missing or inaccessible, stop and say so.
- Prefer quoting bank wording over paraphrasing it in the report.
