class MLEngine:
    """
    Machine Learning Decision Integrator.
    Synthesizes predictions and anomaly classifications from the AI Analysis Engine modules.
    """
    def synthesize_ml_signals(self, fraud_results, keyword_results, budget_results, prediction_results):
        """
        Synthesizes AI model outputs into decision signals.
        """
        ml_signals = []

        # 1. Fraud ML Signal
        fraud_score = fraud_results.get('fraud_risk_score', 0.0)
        if fraud_score > 0.40:
            ml_signals.append({
                "signal_type": "FRAUD_ANOMALY",
                "source": "IsolationForest Anomaly Model",
                "score": fraud_score,
                "summary": f"Isolation Forest model detected {fraud_results.get('suspicious_click_count', 0)} anomalous bot clicks across {len(fraud_results.get('flagged_ips', []))} IPs.",
                "action_needed": True
            })

        # 2. Performance Prediction ML Signal
        predicted_roi = prediction_results.get('predicted_roi', 0.0)
        roi_change = prediction_results.get('roi_change_pct', 0.0)
        if roi_change > 5.0 or predicted_roi > 250.0:
            ml_signals.append({
                "signal_type": "PREDICTION_OPTIMIZATION_RECOMMENDED",
                "source": "RandomForest Performance Predictor",
                "score": predicted_roi,
                "summary": f"Random Forest regression models predict ROI can improve by +{roi_change}% if budget allocation is adjusted.",
                "action_needed": True
            })

        # 3. Keyword ML Signal
        low_kw_count = keyword_results.get('low_performing_count', 0)
        if low_kw_count > 0:
            ml_signals.append({
                "signal_type": "KEYWORD_INEFFICIENCY",
                "source": "Keyword Classification Engine",
                "score": low_kw_count,
                "summary": f"Identified {low_kw_count} low-performing keywords consuming ad spend with low conversion intent.",
                "action_needed": True
            })

        return ml_signals
