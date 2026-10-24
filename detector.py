#!/usr/bin/env python3
"""
Operation Shadow — Explainable Account-Recovery Risk Detector
Uses synthetic workshop data only. No network or live-system access.
Usage:
  python detector.py input.csv
  python detector.py input.csv --json results.json --csv results.csv
"""
import argparse
import csv
import json
from pathlib import Path

def truthy(value):
    return str(value).strip().lower() in {"yes", "true", "1", "y"}

def analyze(event):
    score = 0
    reasons = []
    def flag(points, reason):
        nonlocal score
        score += points
        reasons.append({"points": points, "reason": reason})

    if not truthy(event.get("device_known", "")):
        flag(15, "Unrecognized device")
    if truthy(event.get("location_change", "")):
        flag(15, "Location differs from normal activity")

    mfa = str(event.get("mfa_result", "")).strip().lower()
    if mfa == "failed":
        flag(20, "MFA authentication failed")
    elif mfa == "passed" and (
        not truthy(event.get("device_known", ""))
        or truthy(event.get("location_change", ""))
    ):
        flag(5, "MFA passed despite an unusual context")

    change = str(event.get("account_change", "")).strip().lower()
    if change == "recovery_page_opened":
        flag(15, "Account recovery page accessed")
    elif change == "recovery_email_change_requested":
        flag(25, "Recovery email change requested; completion unconfirmed")

    score = min(score, 100)
    level = "HIGH" if score >= 60 else "MEDIUM" if score >= 35 else "LOW"

    if level == "HIGH":
        actions = [
            "Escalate to the security/incident-response team.",
            "Verify the activity with the account owner using a trusted channel.",
            "Review active sessions and revoke suspicious sessions.",
            "Check recovery settings and reverse unauthorized changes if confirmed."
        ]
    elif level == "MEDIUM":
        actions = [
            "Verify the activity with the account owner using a trusted channel.",
            "Review authentication and account-change logs.",
            "Confirm whether any requested recovery change was completed."
        ]
    else:
        actions = [
            "Retain the event for correlation with other signals.",
            "Do not treat this event alone as proof of compromise."
        ]

    return {
        "event_id": event.get("event_id", "unknown"),
        "time": event.get("time", ""),
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons or [{"points": 0, "reason": "No configured risk indicators triggered"}],
        "recommended_actions": actions,
        "analyst_note": event.get("analyst_note", ""),
        "limitations": [
            "Illustrative rule weights; scores are not probabilities.",
            "A requested recovery change does not prove completion.",
            "Low risk under these rules does not prove an event is legitimate."
        ]
    }

def main():
    parser = argparse.ArgumentParser(description="Explainable synthetic sign-in/recovery detector")
    parser.add_argument("input_csv", type=Path, help="CSV containing synthetic events")
    parser.add_argument("--json", dest="json_out", type=Path, help="Optional JSON output path")
    parser.add_argument("--csv", dest="csv_out", type=Path, help="Optional summary CSV output path")
    args = parser.parse_args()

    with args.input_csv.open(newline="", encoding="utf-8-sig") as f:
        events = list(csv.DictReader(f))
    if not events:
        raise SystemExit("No events found in input CSV.")

    results = [analyze(event) for event in events]
    print("OPERATION SHADOW — SYNTHETIC SECURITY ANALYSIS")
    print("=" * 52)
    for result in results:
        print(f'{result["event_id"]} | {result["time"]} | {result["risk_level"]} | score {result["risk_score"]}')
        for reason in result["reasons"]:
            print(f'  +{reason["points"]:>2}  {reason["reason"]}')
        print("  Recommended actions:")
        for action in result["recommended_actions"]:
            print(f"   - {action}")
        print()

    if args.json_out:
        args.json_out.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"JSON results saved to: {args.json_out}")
    if args.csv_out:
        with args.csv_out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "event_id", "time", "risk_score", "risk_level", "reasons", "recommended_actions"
            ])
            writer.writeheader()
            for result in results:
                writer.writerow({
                    "event_id": result["event_id"],
                    "time": result["time"],
                    "risk_score": result["risk_score"],
                    "risk_level": result["risk_level"],
                    "reasons": "; ".join(
                        f'{r["reason"]} (+{r["points"]})' for r in result["reasons"]
                    ),
                    "recommended_actions": "; ".join(result["recommended_actions"])
                })
        print(f"CSV summary saved to: {args.csv_out}")

if __name__ == "__main__":
    main()
