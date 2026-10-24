# Operation Shadow — Explainable Account-Recovery Risk Detector

## What it does
A small, dependency-free Python detector for the supplied synthetic workshop CSV. It scores each event using four signals: device familiarity, location change, MFA outcome, and account-recovery changes. It explains the score and recommends safe defensive follow-up.

## Run
```bash
python detector.py operation-shadow-round-1-variant-b-account-recovery.csv
```

Optional structured outputs:
```bash
python detector.py operation-shadow-round-1-variant-b-account-recovery.csv --json results.json --csv results.csv
```

Requires Python 3. No third-party packages, network calls, credentials, or live-system access.

## Scoring rules
- Unknown device: +15
- Location change: +15
- Failed MFA: +20
- MFA passed in an unusual context: +5
- Recovery page opened: +15
- Recovery email change requested: +25
- Score capped at 100
- Low: 0–34; Medium: 35–59; High: 60–100

These weights are illustrative and not calibrated probabilities. A score prioritizes review; it does not prove compromise. In particular, a requested recovery change is not evidence that it completed.

## Safety and limitations
This tool is designed for synthetic evidence only. It does not contact accounts or services, open links, or perform scans. Production use would require validation against labelled data, calibration, additional context, and false-positive/false-negative testing.
