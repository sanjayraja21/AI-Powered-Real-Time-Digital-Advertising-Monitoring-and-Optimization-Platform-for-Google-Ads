import pandas as pd
import numpy as np

def clean_campaign_metrics(raw_data):
    """
    Cleans raw campaign dictionary or DataFrame and ensures valid numerical bounds.
    Calculates derived metrics (CTR, Conv Rate, ROI, CPC).
    """
    if isinstance(raw_data, dict):
        cleaned = raw_data.copy()
        impressions = max(1, int(cleaned.get('impressions', 0)))
        clicks = int(cleaned.get('clicks', 0))
        cost = max(0.0, float(cleaned.get('cost', 0.0)))
        conversions = int(cleaned.get('conversions', 0))
        budget = max(1.0, float(cleaned.get('budget', 1.0)))
        
        cleaned['impressions'] = impressions
        cleaned['clicks'] = clicks
        cleaned['cost'] = cost
        cleaned['conversions'] = conversions
        cleaned['budget'] = budget

        # Calculate derived metrics
        cleaned['ctr'] = round((clicks / impressions) * 100, 2) if impressions > 0 else 0.0
        cleaned['cpc'] = round(cost / clicks, 3) if clicks > 0 else 0.0
        cleaned['conv_rate'] = round((conversions / clicks) * 100, 2) if clicks > 0 else 0.0
        cleaned['roi'] = float(cleaned.get('roi', 0.0))
        
        # Calculate budget used percentage
        cleaned['budget_used_percentage'] = round((cost / budget) * 100, 1)
        
        return cleaned

    elif isinstance(raw_data, pd.DataFrame):
        df = raw_data.copy()
        df.fillna(0, inplace=True)
        df['ctr'] = np.where(df['impressions'] > 0, (df['clicks'] / df['impressions']) * 100, 0.0)
        df['cpc'] = np.where(df['clicks'] > 0, df['spend'] / df['clicks'], 0.0)
        df['conv_rate'] = np.where(df['clicks'] > 0, (df['conversions'] / df['clicks']) * 100, 0.0)
        return df

    return raw_data
