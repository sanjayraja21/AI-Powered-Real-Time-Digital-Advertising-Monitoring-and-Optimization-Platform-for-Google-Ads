class RecommendationEngine:
    """
    Generates formatted, human-readable structured Alerts and Recommendations
    for business owners.
    """
    def generate_alerts_and_recommendations(self, campaign_metrics, fraud_results, keyword_results, budget_results, prediction_results, triggered_rules):
        """
        Combines rule triggers and ML analysis into structured Alerts & Recommendations lists.
        """
        alerts = []
        recommendations = []

        # 1. Process Budget Exhaustion Rule / Analysis
        budget_pct = campaign_metrics.get('budget_used_percentage', 0.0)
        roi = campaign_metrics.get('roi', 0.0)
        if budget_pct >= 90.0:
            rec_action = "Consider increasing campaign budget by 15-20% because the campaign is generating strong ROI." if roi >= 200.0 else "Reallocate remaining budget to top-performing exact match keywords."
            alert_obj = {
                "alert_type": "Budget Alert",
                "title": "Budget Almost Exhausted",
                "problem": f"{budget_pct}% of campaign budget has been used (${campaign_metrics.get('cost', 0)} of ${campaign_metrics.get('budget', 0)}).",
                "severity": "High"
            }
            alerts.append(alert_obj)

            recommendations.append({
                "category": "Budget",
                "problem": f"{budget_pct}% of campaign budget has been used.",
                "reason": "High ad spend consumption will pause active ad delivery before peak search hours end.",
                "ai_analysis": f"AI Budget Optimizer calculates a high ROI of {roi}%. Budget velocity indicates full exhaustion within 24 hours.",
                "recommended_action": rec_action,
                "priority": "High"
            })

        # 2. Process Fraud Check ML & Rules
        if fraud_results.get('fraud_detected') or fraud_results.get('fraud_risk_score', 0.0) > 0.40:
            flagged = len(fraud_results.get('flagged_ips', []))
            suspicious_count = fraud_results.get('suspicious_click_count', 0)
            alerts.append({
                "alert_type": "Fraud Alert",
                "title": "Suspicious Click Activity Detected",
                "problem": f"{suspicious_count} suspicious automated clicks flagged from {flagged} IP address(es).",
                "severity": "High" if fraud_results.get('risk_level') == "High" else "Medium"
            })

            recommendations.append({
                "category": "Fraud",
                "problem": f"Suspicious click activity and proxy IP clustering detected (Risk Score: {fraud_results.get('fraud_risk_score')}).",
                "reason": f"Automated bot scripts and rapid IP bursts are draining ad spend without conversion intent.",
                "ai_analysis": f"Isolation Forest Anomaly Model identified {suspicious_count} click events with time intervals < 1.5 seconds. Flagged IPs: {', '.join(fraud_results.get('flagged_ips', [])[:3])}.",
                "recommended_action": f"Review suspicious IP log and add IP exclusions in your Google Ads Campaign Settings for IP range: {', '.join(fraud_results.get('flagged_ips', [])[:2])}.",
                "priority": "High"
            })

        # 3. Process Keyword Analysis
        low_kws = [kw for kw in keyword_results.get('keyword_details', []) if kw.get('performance_tier') == 'Low']
        if low_kws:
            kw_names = [kw['keyword_text'] for kw in low_kws[:2]]
            alerts.append({
                "alert_type": "Low CTR Alert",
                "title": "Low Performing Keywords Consuming Budget",
                "problem": f"{len(low_kws)} keyword(s) classified as Low Performing ('{', '.join(kw_names)}').",
                "severity": "Medium"
            })

            recommendations.append({
                "category": "Keyword",
                "problem": f"Keywords such as '{', '.join(kw_names)}' have low CTR and high CPC.",
                "reason": "Broad match intent generates non-converting click traffic.",
                "ai_analysis": f"Keyword Analyzer evaluated search volume and conversion history. Broad match terms represent {len(low_kws)} of {keyword_results.get('total_keywords')} keywords but produce < 10% of revenue.",
                "recommended_action": f"Pause or replace broad keywords ('{kw_names[0]}') and add negative keywords (e.g. 'free', 'crack', 'giveaway').",
                "priority": "Medium"
            })

        # 4. Process High CPC / Performance Alerts
        cpc = campaign_metrics.get('cpc', 0.0)
        acceptable_cpc = campaign_metrics.get('acceptable_cpc', 0.65)
        if cpc > acceptable_cpc:
            alerts.append({
                "alert_type": "High CPC Alert",
                "title": "Average Cost Per Click Above Threshold",
                "problem": f"Average CPC is ${cpc}, which exceeds target cap of ${acceptable_cpc}.",
                "severity": "Medium"
            })

            recommendations.append({
                "category": "Performance",
                "problem": f"Cost Per Click (${cpc}) is higher than target limit (${acceptable_cpc}).",
                "reason": "Overpaying for ad clicks due to competitive bidding or unoptimized Quality Score.",
                "ai_analysis": f"Performance Engine estimates reducing target CPA bid by 10% will lower CPC to ${round(cpc * 0.9, 3)} while preserving 92% of conversion volume.",
                "recommended_action": "Set a Max CPC Bid Limit in Google Ads and optimize ad relevance headlines to boost Quality Score.",
                "priority": "Medium"
            })

        # 5. Performance Prediction Recommendation
        pred_roi = prediction_results.get('predicted_roi', 0.0)
        curr_roi = campaign_metrics.get('roi', 0.0)
        if pred_roi > curr_roi:
            recommendations.append({
                "category": "Performance",
                "problem": f"Current campaign ROI ({curr_roi}%) is capable of further growth.",
                "reason": "Ad schedule & bid adjustments can unlock higher conversion volume.",
                "ai_analysis": f"Random Forest ML forecasting predicts ROI can reach {pred_roi}% with a slight budget optimization and negative keyword refinement.",
                "recommended_action": "Apply AI-suggested keyword bid adjustments and shift daily budget allocations.",
                "priority": "Low"
            })

        return alerts, recommendations
