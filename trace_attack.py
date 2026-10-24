#!/usr/bin/env python3
"""Operation Shadow Round 2: evidence timeline and cautious incident triage.
Uses only fictional workshop evidence; performs no network or live-system actions.
"""
import argparse
import csv
import json
from pathlib import Path

EVENTS = [
    {"event_id":"TB-311","time":"13:01","event":"Successful sign-in from known device","source":"identity_log","status":"observed","evidence_gap":"User confirmation not collected"},
    {"event_id":"TB-312","time":"13:04","event":"Permission settings opened","source":"admin_audit","status":"observed","evidence_gap":"No permission change recorded"},
    {"event_id":"TB-313","time":"13:09","event":"Bulk report export requested","source":"report_service","status":"observed","evidence_gap":"Request status is queued"},
    {"event_id":"TB-314","time":"13:11","event":"Export job cancelled","source":"report_service","status":"observed","evidence_gap":"No output file record"},
    {"event_id":"TB-315","time":"13:20","event":"Possible data access abuse","source":"analyst_hypothesis","status":"unconfirmed","evidence_gap":"Need completed-job and access logs"},
]

def assess(e):
    event_id = e["event_id"]
    if event_id == "TB-311":
        interpretation = "Authentication succeeded on a known device; user intent is not verified."
        priority = "MEDIUM"
        next_step = "Confirm sign-in with the user and correlate IP, session, and authentication context."
    elif event_id == "TB-312":
        interpretation = "Permission settings were viewed; no permission change is recorded."
        priority = "MEDIUM"
        next_step = "Review surrounding admin audit events and determine which settings were accessed."
    elif event_id == "TB-313":
        interpretation = "A bulk export was requested and queued; this does not establish that data was exported."
        priority = "HIGH"
        next_step = "Inspect job state, queue history, scope, requester, and downstream execution logs."
    elif event_id == "TB-314":
        interpretation = "The export job was cancelled and no output file record is listed in this evidence set."
        priority = "HIGH"
        next_step = "Verify cancellation completion and check storage, service, and audit logs for any partial output."
    else:
        interpretation = "Analyst hypothesis only; the supplied evidence does not establish data access abuse."
        priority = "INVESTIGATE"
        next_step = "Test the hypothesis against completed-job records, file access logs, object/storage logs, and network egress telemetry."
    return {**e, "priority": priority, "interpretation": interpretation, "next_step": next_step}

def main():
    parser = argparse.ArgumentParser(description="Correlate the supplied synthetic Round 2 evidence.")
    parser.add_argument("--json", dest="json_path", help="Optional JSON output file")
    parser.add_argument("--csv", dest="csv_path", help="Optional CSV output file")
    args = parser.parse_args()
    results = [assess(e) for e in sorted(EVENTS, key=lambda x: x["time"])]
    print("OPERATION SHADOW — ROUND 2: TRACE THE ATTACK")
    print("=" * 54)
    print("Reconstructed timeline (all times as supplied; timezone not specified):")
    for r in results:
        print(f'\n{r["time"]} | {r["event_id"]} | {r["priority"]} | {r["status"].upper()}')
        print(f'  Event: {r["event"]} [{r["source"]}]')
        print(f'  Assessment: {r["interpretation"]}')
        print(f'  Evidence gap: {r["evidence_gap"]}')
        print(f'  Next step: {r["next_step"]}')
    print("\nLIKELY PATH (hypothesis, not a confirmed attack):")
    print("Known-device sign-in -> permission settings viewed -> bulk export requested -> job cancelled.")
    print("The sequence warrants review, but it does not prove unauthorized access or data exfiltration.")
    print("\nPRIORITIZED RESPONSE:")
    print("1. Preserve identity, admin-audit, report-service, storage, and network logs.")
    print("2. Verify the sign-in and export request with the account owner through a trusted channel.")
    print("3. Confirm whether the export job actually executed, partially ran, or produced artifacts.")
    print("4. Review permissions and revert only changes confirmed unauthorized (none recorded in supplied evidence).")
    print("5. Escalate if corroborating evidence establishes unauthorized access or transfer.")
    print("\nEXFILTRATION EVIDENCE NEEDED:")
    print("- Completed job status and job execution history")
    print("- Export output/object creation records and file sizes")
    print("- File/report access and download audit logs")
    print("- Storage access logs and network egress/transfer telemetry")
    print("- Correlation to user/session, destination, byte counts, and timestamps")
    print("\nLimitations: this is a deterministic evidence-summary workflow, not an RNN/LSTM/Transformer model.")
    print("It uses only the fictional events supplied in the workshop.")
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"\nJSON saved: {args.json_path}")
    if args.csv_path:
        fields = ["event_id","time","event","source","status","priority","interpretation","evidence_gap","next_step"]
        with open(args.csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(results)
        print(f"CSV saved: {args.csv_path}")

if __name__ == "__main__":
    main()
