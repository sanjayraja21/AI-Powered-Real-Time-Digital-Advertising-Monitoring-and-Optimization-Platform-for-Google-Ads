from ai_engine.fraud_detection import FraudDetectionEngine
from ai_engine.keyword_analysis import KeywordAnalyzer
from ai_engine.budget_optimizer import BudgetOptimizer
from ai_engine.performance_prediction import PerformancePredictor
from decision_engine.rule_engine import RuleEngine
from decision_engine.ml_engine import MLEngine
from decision_engine.recommendation_engine import RecommendationEngine
from preprocessing.data_cleaning import clean_campaign_metrics

class HybridDecisionManager:
    """
    Hybrid Decision Engine orchestrator combining:
    1. AI Analysis Engine (Fraud, Keyword, Budget, Prediction)
    2. Deterministic Rule-Based Logic
    3. Machine Learning Signal Synthesis
    4. Structured Alerts & Actionable Recommendations
    """
    def __init__(self):
        self.fraud_engine = FraudDetectionEngine()
        self.keyword_analyzer = KeywordAnalyzer()
        self.budget_optimizer = BudgetOptimizer()
        self.performance_predictor = PerformancePredictor()
        self.rule_engine = RuleEngine()
        self.ml_engine = MLEngine()
        self.recommendation_engine = RecommendationEngine()

    def run_full_diagnosis(self, campaign_data, keywords_list=None, click_logs=None, budget_sim_pct=0.0):
        """
        Executes complete AI pipeline and Decision Engine workflow.
        Returns a comprehensive diagnostic dictionary.
        """
        # Step 1: Preprocess and clean campaign metrics
        cleaned_metrics = clean_campaign_metrics(campaign_data)

        # Step 2: Run AI Analysis Engine Modules
        fraud_results = self.fraud_engine.analyze_click_logs(click_logs or [])
        keyword_results = self.keyword_analyzer.analyze_keywords(keywords_list or [])
        budget_results = self.budget_optimizer.analyze_budget(
            total_budget=cleaned_metrics['budget'],
            budget_used=cleaned_metrics['cost'],
            cost=cleaned_metrics['cost'],
            conversions=cleaned_metrics['conversions'],
            roi=cleaned_metrics['roi'],
            target_roi=cleaned_metrics.get('target_roi', 250.0)
        )
        prediction_results = self.performance_predictor.predict_performance(
            current_metrics=cleaned_metrics,
            budget_adjustment_pct=budget_sim_pct
        )

        # Step 3: Run Rule-Based Decision Logic
        triggered_rules = self.rule_engine.evaluate_rules(
            campaign_metrics=cleaned_metrics,
            fraud_score=fraud_results.get('fraud_risk_score', 0.0)
        )

        # Step 4: Run Machine Learning Integrator
        ml_signals = self.ml_engine.synthesize_ml_signals(
            fraud_results=fraud_results,
            keyword_results=keyword_results,
            budget_results=budget_results,
            prediction_results=prediction_results
        )

        # Step 5: Synthesize Alerts & Recommendations
        alerts, recommendations = self.recommendation_engine.generate_alerts_and_recommendations(
            campaign_metrics=cleaned_metrics,
            fraud_results=fraud_results,
            keyword_results=keyword_results,
            budget_results=budget_results,
            prediction_results=prediction_results,
            triggered_rules=triggered_rules
        )

        return {
            "campaign_metrics": cleaned_metrics,
            "ai_analysis": {
                "fraud_check": fraud_results,
                "keyword_analysis": keyword_results,
                "budget_optimization": budget_results,
                "performance_prediction": prediction_results
            },
            "decision_engine": {
                "triggered_rules": triggered_rules,
                "ml_signals": ml_signals,
                "rule_count": len(triggered_rules),
                "status": "REQUIRES_ATTENTION" if (alerts or fraud_results.get('fraud_detected')) else "OPTIMAL"
            },
            "alerts": alerts,
            "recommendations": recommendations
        }
