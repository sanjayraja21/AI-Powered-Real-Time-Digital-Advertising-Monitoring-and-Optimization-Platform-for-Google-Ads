class BudgetOptimizer:
    """
    AI Budget Optimization Engine.
    Analyzes budget allocation, burn rate, spend efficiency, and campaign ROI
    to recommend optimal budget adjustments and cross-campaign reallocations.
    """
    def analyze_budget(self, total_budget, budget_used, cost, conversions, roi, target_roi=250.0):
        """
        Calculates burn rate metrics and returns structured budget guidance.
        """
        remaining_budget = max(0.0, total_budget - budget_used)
        budget_used_percentage = round((budget_used / total_budget) * 100, 1) if total_budget > 0 else 0.0
        cost_per_conversion = round(cost / conversions, 2) if conversions > 0 else cost

        recommendation_action = "Maintain budget"
        reallocation_target = None
        priority = "Low"
        reason = ""

        # Logic for high budget utilization (> 90%)
        if budget_used_percentage >= 90.0:
            if roi >= target_roi * 0.9: # Good ROI
                recommendation_action = "Increase budget"
                priority = "High"
                reason = f"{budget_used_percentage}% of total budget used. Campaign is generating high ROI ({roi}%). Increasing budget will capture remaining high-intent search volume."
            else:
                recommendation_action = "Reallocate budget"
                priority = "Medium"
                reason = f"Budget is {budget_used_percentage}% exhausted but ROI ({roi}%) is below target ({target_roi}%). Reallocate remaining funds to higher-converting keyword sets or campaigns."
        elif budget_used_percentage <= 40.0:
            if roi < 120.0:
                recommendation_action = "Reduce budget"
                priority = "Medium"
                reason = f"Low budget utilization ({budget_used_percentage}%) with sub-par ROI ({roi}%). Reduce allocated daily limit to minimize waste while optimizing targeting."
            else:
                recommendation_action = "Maintain budget"
                priority = "Low"
                reason = f"Healthy remaining budget reserves (${round(remaining_budget, 2)}) with solid ROI ({roi}%)."
        else:
            if roi >= target_roi:
                recommendation_action = "Increase budget"
                priority = "Medium"
                reason = f"Campaign performs well above target ROI ({roi}% vs {target_roi}% target). Consider expanding budget by 15-25% to maximize sales."
            else:
                recommendation_action = "Maintain budget"
                priority = "Low"
                reason = "Current budget burn rate and ROI are operating within normal baseline limits."

        return {
            "total_budget": total_budget,
            "budget_used": budget_used,
            "remaining_budget": round(remaining_budget, 2),
            "budget_used_percentage": budget_used_percentage,
            "cost_per_conversion": cost_per_conversion,
            "roi": roi,
            "recommendation_action": recommendation_action,
            "priority": priority,
            "reason": reason,
            "suggested_budget_adjustment": self._calculate_suggested_delta(budget_used_percentage, roi, total_budget)
        }

    def _calculate_suggested_delta(self, budget_used_pct, roi, current_budget):
        if budget_used_pct >= 90.0 and roi >= 200.0:
            return round(current_budget * 0.20, 2) # Recommend +20% increase
        elif roi < 100.0:
            return -round(current_budget * 0.15, 2) # Recommend -15% reduction
        return 0.0
