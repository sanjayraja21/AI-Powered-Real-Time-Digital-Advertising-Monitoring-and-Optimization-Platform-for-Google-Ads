import unittest
from decision_engine.rule_engine import RuleEngine
from decision_engine.decision_manager import HybridDecisionManager

class TestDecisionEngine(unittest.TestCase):

    def setUp(self):
        self.rule_engine = RuleEngine()
        self.decision_manager = HybridDecisionManager()

    def test_rule_evaluations(self):
        metrics = {
            "budget": 5000.0,
            "cost": 4600.0,
            "budget_used_percentage": 92.0,
            "ctr": 4.5,
            "target_ctr": 6.0,
            "cpc": 0.85,
            "acceptable_cpc": 0.65,
            "roi": 245.0,
            "target_roi": 250.0
        }
        triggered = self.rule_engine.evaluate_rules(metrics, fraud_score=0.85)
        rule_ids = [r["rule_id"] for r in triggered]
        self.assertIn("RULE_BUDGET_EXHAUSTED", rule_ids)
        self.assertIn("RULE_LOW_CTR", rule_ids)
        self.assertIn("RULE_HIGH_CPC", rule_ids)
        self.assertIn("RULE_SUSPICIOUS_TRAFFIC", rule_ids)

    def test_full_hybrid_decision_manager(self):
        campaign_data = {
            "budget": 5000.0,
            "cost": 4600.0,
            "impressions": 124500,
            "clicks": 6225,
            "conversions": 311,
            "target_ctr": 6.0,
            "acceptable_cpc": 0.65,
            "target_roi": 250.0
        }
        keywords = [{"keyword_text": "buy dell inspiron 15", "ctr": 8.4, "roi": 300.0, "clicks": 100, "cpc": 0.5, "cost": 50, "conversions": 20}]
        click_logs = [{"timestamp": "2026-07-28T10:00:00", "ip_address": "192.168.1.1", "user_agent": "Mozilla/5.0", "device": "Desktop", "click_interval_sec": 45.0}]

        diagnosis = self.decision_manager.run_full_diagnosis(campaign_data, keywords, click_logs)
        self.assertIn("ai_analysis", diagnosis)
        self.assertIn("decision_engine", diagnosis)
        self.assertIn("alerts", diagnosis)
        self.assertIn("recommendations", diagnosis)

if __name__ == '__main__':
    unittest.main()
