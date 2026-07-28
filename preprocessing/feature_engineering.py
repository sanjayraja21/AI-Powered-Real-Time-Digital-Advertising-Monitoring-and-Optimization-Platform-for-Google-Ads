import pandas as pd
import numpy as np

def extract_click_features(click_logs_list):
    """
    Transforms raw click log dictionaries or model objects into a feature matrix
    suitable for Scikit-Learn IsolationForest anomaly detection.
    Features extracted:
    - click_interval_sec: time delta from preceding click
    - ip_click_count: count of clicks originating from the same IP address
    - is_bot_user_agent: binary flag for bot or scraping user-agents
    - rapid_burst_flag: binary flag if interval < 2.0 seconds
    """
    if not click_logs_list:
        return np.array([])

    df = pd.DataFrame(click_logs_list)
    
    # Calculate IP frequency count
    ip_counts = df['ip_address'].value_counts().to_dict()
    df['ip_click_count'] = df['ip_address'].map(ip_counts)

    # Calculate rapid burst flag (< 2 seconds interval)
    df['rapid_burst_flag'] = (df['click_interval_sec'] < 2.0).astype(int)

    # Check user-agent bot keywords
    bot_keywords = ['bot', 'scraper', 'python', 'curl', 'wget', 'automated', 'server']
    df['is_bot_user_agent'] = df['user_agent'].astype(str).str.lower().apply(
        lambda ua: 1 if any(k in ua for k in bot_keywords) else 0
    )

    # Extract numerical feature array
    features = df[['click_interval_sec', 'ip_click_count', 'rapid_burst_flag', 'is_bot_user_agent']].values
    return features

def extract_campaign_regression_features(df):
    """
    Extracts features for performance prediction model.
    Features: daily_budget, spend, cpc, ctr, conv_rate
    """
    features = df[['daily_budget', 'spend', 'cpc', 'ctr', 'conv_rate']].values
    targets = df[['ctr', 'conversions', 'roi', 'cpc']].values
    return features, targets
