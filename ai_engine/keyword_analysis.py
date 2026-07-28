class KeywordAnalyzer:
    """
    AI Keyword Analysis Engine.
    Evaluates Clicks, CTR, CPC, Cost, Conversions, and ROI for each keyword
    to classify efficiency tiers and generate optimization recommendations.
    """
    def analyze_keywords(self, keywords_list):
        """
        Analyzes a list of keyword dictionaries or ORM objects.
        Returns detailed classification summary and recommendations.
        """
        results = []
        high_perf = 0
        avg_perf = 0
        low_perf = 0

        for kw in keywords_list:
            if isinstance(kw, dict):
                k_text = kw.get('keyword_text', '')
                match_type = kw.get('match_type', 'EXACT')
                clicks = kw.get('clicks', 0)
                ctr = kw.get('ctr', 0.0)
                cpc = kw.get('cpc', 0.0)
                cost = kw.get('cost', 0.0)
                conversions = kw.get('conversions', 0)
                roi = kw.get('roi', 0.0)
            else:
                k_text = kw.keyword_text
                match_type = kw.match_type
                clicks = kw.clicks
                ctr = kw.ctr
                cpc = kw.cpc
                cost = kw.cost
                conversions = kw.conversions
                roi = kw.roi

            # Scoring composite performance metric
            # High Tier: CTR >= 6.0%, ROI >= 220% or high conversions with good ROI
            if (ctr >= 6.0 and roi >= 200.0) or (conversions >= 50 and roi >= 220.0):
                tier = "High"
                recommendation = "Keep keyword - Scale budget and increase bid for top positions"
                action_code = "KEEP_SCALE"
                high_perf += 1
            elif (ctr >= 4.0 and roi >= 150.0) or (conversions >= 20):
                tier = "Average"
                recommendation = "Improve keyword - Optimize ad copy relevance & refine match type"
                action_code = "IMPROVE"
                avg_perf += 1
            elif roi < 100.0 or (cost > 500.0 and conversions < 15):
                tier = "Low"
                recommendation = "Consider removing or pausing low-performing keyword to prevent ad spend waste"
                action_code = "REMOVE"
                low_perf += 1
            else:
                tier = "Low"
                recommendation = "Replace keyword - Test alternative high-intent search terms"
                action_code = "REPLACE"
                low_perf += 1

            results.append({
                "keyword_text": k_text,
                "match_type": match_type,
                "clicks": clicks,
                "ctr": ctr,
                "cpc": cpc,
                "cost": cost,
                "conversions": conversions,
                "roi": roi,
                "performance_tier": tier,
                "recommendation": recommendation,
                "action_code": action_code
            })

        return {
            "keyword_details": results,
            "high_performing_count": high_perf,
            "average_performing_count": avg_perf,
            "low_performing_count": low_perf,
            "total_keywords": len(keywords_list),
            "summary_recommendation": f"Found {high_perf} high performing, {avg_perf} average, and {low_perf} low performing keywords."
        }
