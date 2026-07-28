import unittest
from ai_engine.fraud_detection import FraudDetectionEngine
from ai_engine.keyword_analysis import KeywordAnalyzer
from ai_engine.budget_optimizer import BudgetOptimizer
from ai_engine.performance_prediction import PerformancePredictor

class TestAIEngine(unittest.TestCase):

    def setUp(self):
        self.fraud_engine = FraudDetectionEngine()
        self.keyword_analyzer = KeywordAnalyzer()
        self.budget_optimizer = BudgetOptimizer()
        self.predictor = PerformancePredictor()

    def test_fraud_detection_normal_and_anomalous(self):
        # Normal click logs
        normal_logs = [
            {"timestamp": "2026-07-28T10:00:00", "ip_address": "192.168.1.1", "user_agent": "Mozilla/5.0", "device": "Desktop", "click_interval_sec": 45.0},
            {"timestamp": "2026-07-28T10:02:00", "ip_address": "192.168.1.2", "user_agent": "Mozilla/5.0", "device": "Mobile", "click_interval_sec": 120.0}
        ]
        normal_res = self.fraud_engine.analyze_click_logs(normal_logs)
        self.assertIn("fraud_risk_score", normal_res)
        self.assertLess(normal_res["fraud_risk_score"], 0.60)

        # Suspicious bot burst
        suspicious_logs = [
            {"timestamp": "2026-07-28T10:00:00", "ip_address": "185.220.101.5", "user_agent": "Python-requests/2.31.0", "device": "Bot", "click_interval_sec": 0.2}
            for _ in range(25)
        ]
        fraud_res = self.fraud_engine.analyze_click_logs(suspicious_logs)
        self.assertGreaterEqual(fraud_res["suspicious_click_count"], 1)

    def test_keyword_analysis_classification(self):
        keywords = [
            {"keyword_text": "buy dell inspiron 15", "ctr": 8.4, "roi": 300.0, "clicks": 100, "cpc": 0.5, "cost": 50, "conversions": 20},
            {"keyword_text": "free laptops online", "ctr": 1.2, "roi": 20.0, "clicks": 100, "cpc": 1.2, "cost": 120, "conversions": 1}
        ]
        res = self.keyword_analyzer.analyze_keywords(keywords)
        self.assertEqual(res["high_performing_count"], 1)
        self.assertEqual(res["low_performing_count"], 1)

    def test_budget_optimizer(self):
        # 92% budget used with high ROI -> should recommend budget increase
        res = self.budget_optimizer.analyze_budget(
            total_budget=5000.0,
            budget_used=4600.0,
            cost=4600.0,
            conversions=300,
            roi=245.0,
            target_roi=250.0
        )
        self.assertEqual(res["recommendation_action"], "Increase budget")
        self.assertEqual(res["priority"], "High")

    def test_performance_prediction_simulation(self):
        metrics = {"budget": 5000.0, "cost": 4600.0, "cpc": 0.739, "ctr": 5.0, "conv_rate": 5.0, "roi": 245.0}
        sim_res = self.predictor.predict_performance(metrics, budget_adjustment_pct=20.0)
        self.assertIn("predicted_roi", sim_res)
        self.assertIn("predicted_ctr", sim_res)
        self.assertEqual(sim_res["simulated_budget"], 6000.0)

if __name__ == '__main__':
    unittest.main()
