import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from preprocessing.feature_engineering import extract_click_features
from config import Config

class FraudDetectionEngine:
    """
    AI Anomaly Detection Engine using Scikit-Learn IsolationForest.
    Analyzes click stream behavior, request frequencies, and time intervals
    to compute a Fraud Risk Score (0.0 to 1.0) and flag suspicious bot activity.
    """
    def __init__(self, contamination=0.15):
        self.model_path = os.path.join(Config.MODELS_DIR, 'isolation_forest_fraud.pkl')
        self.contamination = contamination
        self.model = IsolationForest(contamination=self.contamination, random_state=42, n_estimators=100)
        self._is_trained = False
        self._load_or_train_default()

    def _load_or_train_default(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self._is_trained = True
                return
            except Exception:
                pass
        
        # Train default model on synthetic baseline distribution
        synthetic_features = []
        # Normal traffic: intervals 10s to 300s, low ip count 1-3, no burst, no bot user agent
        for _ in range(300):
            interval = np.random.uniform(10.0, 300.0)
            ip_count = np.random.randint(1, 4)
            synthetic_features.append([interval, ip_count, 0, 0])
        
        # Fraud traffic: intervals < 2s, high ip count 10-50, rapid burst=1, bot user agent=1
        for _ in range(50):
            interval = np.random.uniform(0.1, 1.8)
            ip_count = np.random.randint(10, 50)
            synthetic_features.append([interval, ip_count, 1, 1])

        X = np.array(synthetic_features)
        self.model.fit(X)
        self._is_trained = True

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)

    def analyze_click_logs(self, click_logs):
        """
        Analyzes a list of click log dictionaries.
        Returns:
        {
            "fraud_risk_score": float (0.0 - 1.0),
            "suspicious_click_count": int,
            "total_clicks": int,
            "abnormal_click_frequency": str,
            "risk_level": "Low" | "Medium" | "High",
            "flagged_ips": list[str],
            "fraud_detected": bool
        }
        """
        if not click_logs:
            return {
                "fraud_risk_score": 0.05,
                "suspicious_click_count": 0,
                "total_clicks": 0,
                "abnormal_click_frequency": "Normal",
                "risk_level": "Low",
                "flagged_ips": [],
                "fraud_detected": False
            }

        X = extract_click_features(click_logs)
        if len(X) == 0:
            return {
                "fraud_risk_score": 0.05,
                "suspicious_click_count": 0,
                "total_clicks": len(click_logs),
                "abnormal_click_frequency": "Normal",
                "risk_level": "Low",
                "flagged_ips": [],
                "fraud_detected": False
            }

        # IsolationForest decision function gives negative scores for anomalies
        # Predict: -1 for outlier/anomaly, 1 for inlier
        preds = self.model.predict(X)
        scores = self.model.decision_function(X) # lower score = more anomalous

        suspicious_indices = np.where(preds == -1)[0]
        suspicious_count = len(suspicious_indices)
        total_clicks = len(click_logs)
        fraud_ratio = suspicious_count / total_clicks if total_clicks > 0 else 0.0

        # Calculate normalized score between 0.0 and 1.0
        # Map decision function values: typically ranges -0.3 (high anomaly) to +0.3 (normal)
        avg_anomaly_score = np.mean(scores[suspicious_indices]) if len(suspicious_indices) > 0 else 0.2
        raw_risk_score = float(fraud_ratio * 0.7 + (0.3 - min(0.3, max(-0.3, avg_anomaly_score))) * 0.5)
        fraud_risk_score = round(min(1.0, max(0.0, raw_risk_score)), 2)

        # Determine Risk Level
        if fraud_risk_score > 0.65 or suspicious_count > 15:
            risk_level = "High"
            abnormal_freq = "CRITICAL: Multiple rapid click bursts detected from suspicious proxy IPs"
        elif fraud_risk_score > 0.35 or suspicious_count > 5:
            risk_level = "Medium"
            abnormal_freq = "MODERATE: Elevated click frequency observed in short time intervals"
        else:
            risk_level = "Low"
            abnormal_freq = "NORMAL: Natural human user click distribution verified"

        # Gather flagged IP addresses
        flagged_ips = list(set([click_logs[i]['ip_address'] for i in suspicious_indices]))

        return {
            "fraud_risk_score": fraud_risk_score,
            "suspicious_click_count": suspicious_count,
            "total_clicks": total_clicks,
            "abnormal_click_frequency": abnormal_freq,
            "risk_level": risk_level,
            "flagged_ips": flagged_ips,
            "fraud_detected": (risk_level in ["Medium", "High"] or fraud_risk_score > 0.40)
        }
