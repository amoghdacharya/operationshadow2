# Operation Shadow — Round 2 Timeline Correlator

A small, dependency-free Python workflow that orders the supplied synthetic evidence, separates observed facts from an unconfirmed hypothesis, highlights investigation priorities, and lists evidence needed before claiming data exfiltration.

## Run
```bash
python3 trace_attack.py
```
Optional exports:
```bash
python3 trace_attack.py --json timeline.json --csv timeline.csv
```

## Key conclusion
The observed sequence is: known-device sign-in → permission settings viewed → bulk export requested/queued → export job cancelled. It warrants investigation, but the evidence does not prove a permission change, completed export, or data exfiltration.

## Evidence needed
Completed-job and execution records; output/object creation records; file/report access and download logs; storage logs; network egress telemetry; session/user correlation and byte counts.

## Limitations
This is a deterministic rule-and-evidence summary, not a trained RNN, LSTM, or Transformer. The timestamps are reproduced as supplied; no timezone was provided. Uses fictional workshop evidence only and does not access live systems.
