class RuleEngine:
    """
    Deterministic Rule-Based Decision Logic Engine.
    Checks campaign metrics against defined thresholds to generate rule-level triggers.
    """
    def evaluate_rules(self, campaign_metrics, fraud_score=0.0):
        """
        Evaluates campaign metrics against business logic rules.
        """
        triggered_rules = []

        budget_used_pct = campaign_metrics.get('budget_used_percentage', 0.0)
        ctr = campaign_metrics.get('ctr', 0.0)
        target_ctr = campaign_metrics.get('target_ctr', 6.0)
        cpc = campaign_metrics.get('cpc', 0.0)
        acceptable_cpc = campaign_metrics.get('acceptable_cpc', 0.65)
        roi = campaign_metrics.get('roi', 0.0)
        target_roi = campaign_metrics.get('target_roi', 250.0)

        # Rule 1: IF budget_used_percentage > 90
        if budget_used_pct >= 90.0:
            triggered_rules.append({
                "rule_id": "RULE_BUDGET_EXHAUSTED",
                "alert_type": "Budget Alert",
                "title": "Budget Almost Exhausted",
                "severity": "High",
                "problem": f"{budget_used_pct}% of total campaign budget has been consumed.",
                "reason": "Campaign budget is approaching full allocation limit, risking premature ad pause."
            })

        # Rule 2: IF CTR < target_CTR
        if ctr < target_ctr:
            triggered_rules.append({
                "rule_id": "RULE_LOW_CTR",
                "alert_type": "Low CTR Alert",
                "title": "Campaign Click-Through Rate Below Target",
                "severity": "Medium" if (target_ctr - ctr) < 2.0 else "High",
                "problem": f"Current CTR ({ctr}%) is lower than target goal ({target_ctr}%).",
                "reason": "Lower CTR reduces Quality Score and increases overall bidding costs."
            })

        # Rule 3: IF CPC > acceptable_CPC
        if cpc > acceptable_cpc:
            triggered_rules.append({
                "rule_id": "RULE_HIGH_CPC",
                "alert_type": "High CPC Alert",
                "title": "Average Cost Per Click Exceeds Maximum Target",
                "severity": "Medium",
                "problem": f"Average CPC (${cpc}) exceeds the maximum acceptable target (${acceptable_cpc}).",
                "reason": "Overpaying per click reduces profit margin per conversion."
            })

        # Rule 4: IF fraud_score > 0.80 or suspicious traffic flagged
        if fraud_score >= 0.65:
            triggered_rules.append({
                "rule_id": "RULE_SUSPICIOUS_TRAFFIC",
                "alert_type": "Fraud Alert",
                "title": "Suspicious Click Activity Detected",
                "severity": "High",
                "problem": f"AI Anomaly Engine detected abnormal click bursts (Fraud Score: {fraud_score}).",
                "reason": "Repeated clicks from identical proxy IPs or bot user agents deplete ad budget with zero conversion intent."
            })

        # Rule 5: Sub-optimal ROI Performance
        if roi < target_roi * 0.85:
            triggered_rules.append({
                "rule_id": "RULE_LOW_ROI",
                "alert_type": "Performance Alert",
                "title": "Campaign ROI Below Revenue Benchmark",
                "severity": "Medium",
                "problem": f"Current campaign ROI ({roi}%) is running below target revenue benchmark ({target_roi}%).",
                "reason": "Conversion rates or landing page conversion efficiency are below expectation."
            })

        return triggered_rules
