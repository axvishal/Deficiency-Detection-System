from datetime import datetime, timedelta

def analyze_discrepancies(results):
    summary = {
        "comparison_status": "consistent",
        "total_fields_compared": len(results),
        "matched_fields": 0,
        "discrepancies": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "details": []
    }

    for r in results:
        if r.get("match"):
            summary["matched_fields"] += 1
            continue

        summary["discrepancies"] += 1
        severity = classify_severity(r)

        summary[severity.lower()] += 1
        summary["details"].append({
            "field": r["field"],
            "form_value": r["form_value"],
            "proposal_value": r["proposal_value"],
            "variance": r.get("variance"),
            "severity": severity
        })

    if summary["discrepancies"] > 0:
        summary["comparison_status"] = "discrepancies_found"
        summary["clarification_deadline"] = (
            datetime.utcnow() + timedelta(days=15)
        ).strftime("%Y-%m-%d")

    summary["discrepancy_score"] = min(summary["discrepancies"] * 5, 100)
    return summary

def classify_severity(result):
    if result.get("critical") and result.get("variance", 0) > 20:
        return "CRITICAL"
    if result.get("variance", 0) > 20:
        return "HIGH"
    if result.get("variance", 0) > 5:
        return "MEDIUM"
    return "LOW"
