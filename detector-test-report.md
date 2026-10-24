# Operation Shadow — Test Results

Input file: `operation-shadow-round-1-variant-b-account-recovery.csv`

Events processed: **4**

| Event | Time | Score | Risk | Evidence |
|---|---:|---:|---|---|
| B-211 | 11:02 | 0 | LOW | No configured indicators |
| B-212 | 11:06 | 65 | HIGH | Unrecognized device (+15); Location differs from normal activity (+15); MFA authentication failed (+20); Account recovery page accessed (+15) |
| B-213 | 11:08 | 60 | HIGH | Unrecognized device (+15); Location differs from normal activity (+15); MFA passed despite an unusual context (+5); Recovery email change requested; completion unconfirmed (+25) |
| B-214 | 11:16 | 0 | LOW | No configured indicators |

## Interpretation

High-risk events should be escalated for human review. Scores are illustrative rule-based priorities, not probabilities or proof of compromise. A recovery-change request is not confirmation that the change completed.

## Safety

Only the provided synthetic workshop CSV was analyzed. No links were opened and no live systems or accounts were accessed.