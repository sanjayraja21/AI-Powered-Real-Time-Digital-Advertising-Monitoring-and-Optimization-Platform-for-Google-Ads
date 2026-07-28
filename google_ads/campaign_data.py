import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_demo_campaign_data():
    """Returns static metadata for demo campaigns."""
    return [
        {
            "google_campaign_id": "CMP-2026-DELL-15",
            "name": "Dell Laptop Sale 2026",
            "product_name": "Dell Inspiron 15 Laptop",
            "business_name": "ABC Electronics",
            "status": "ELIGIBLE",
            "budget": 5000.0,
            "budget_used": 4600.0, # 92% budget used -> triggers Budget Alert!
            "impressions": 124500,
            "clicks": 6225,
            "ctr": 5.0,
            "cpc": 0.739,
            "cost": 4600.0,
            "conversions": 311,
            "conv_rate": 5.0,
            "roi": 245.0, # Target 250% -> triggers ROI recommendation!
            "target_ctr": 6.0,
            "acceptable_cpc": 0.65, # CPC 0.739 > 0.65 -> triggers High CPC Alert!
            "target_roi": 250.0
        },
        {
            "google_campaign_id": "CMP-2026-ACC-MEGA",
            "name": "Smart Electronics & Accessories",
            "product_name": "Laptop Accessories & Monitors",
            "business_name": "ABC Electronics",
            "status": "ELIGIBLE",
            "budget": 3500.0,
            "budget_used": 1850.0,
            "impressions": 88000,
            "clicks": 4928,
            "ctr": 5.6,
            "cpc": 0.375,
            "cost": 1850.0,
            "conversions": 295,
            "conv_rate": 6.0,
            "roi": 310.0,
            "target_ctr": 5.5,
            "acceptable_cpc": 0.45,
            "target_roi": 280.0
        },
        {
            "google_campaign_id": "CMP-2026-GAMING-Q3",
            "name": "Dell Alienware & Gaming Laptops",
            "product_name": "Alienware x16 Gaming Laptop",
            "business_name": "ABC Electronics",
            "status": "ELIGIBLE",
            "budget": 8000.0,
            "budget_used": 4200.0,
            "impressions": 65000,
            "clicks": 2470,
            "ctr": 3.8, # CTR 3.8 < 4.5 -> triggers Low CTR Alert!
            "cpc": 1.70,
            "cost": 4200.0,
            "conversions": 112,
            "conv_rate": 4.5,
            "roi": 190.0,
            "target_ctr": 4.5,
            "acceptable_cpc": 1.50,
            "target_roi": 220.0
        }
    ]

def get_demo_keywords(campaign_name="Dell Laptop Sale 2026"):
    """Returns sample keywords for the campaign."""
    if "Dell Laptop" in campaign_name:
        return [
            {
                "keyword_text": "buy dell inspiron 15",
                "match_type": "EXACT",
                "clicks": 1850,
                "impressions": 22000,
                "ctr": 8.41,
                "cpc": 0.58,
                "cost": 1073.00,
                "conversions": 142,
                "roi": 340.0,
                "performance_tier": "High",
                "recommendation": "Keep keyword - Increase bid"
            },
            {
                "keyword_text": "dell laptop sale 2026",
                "match_type": "PHRASE",
                "clicks": 1420,
                "impressions": 21000,
                "ctr": 6.76,
                "cpc": 0.62,
                "cost": 880.40,
                "conversions": 89,
                "roi": 290.0,
                "performance_tier": "High",
                "recommendation": "Keep keyword"
            },
            {
                "keyword_text": "best 15 inch laptop for business",
                "match_type": "PHRASE",
                "clicks": 980,
                "impressions": 19500,
                "ctr": 5.02,
                "cpc": 0.74,
                "cost": 725.20,
                "conversions": 45,
                "roi": 210.0,
                "performance_tier": "Average",
                "recommendation": "Improve ad copy & landing page"
            },
            {
                "keyword_text": "cheap laptops online discount",
                "match_type": "BROAD",
                "clicks": 1250,
                "impressions": 42000,
                "ctr": 2.98,
                "cpc": 0.95,
                "cost": 1187.50,
                "conversions": 25,
                "roi": 95.0,
                "performance_tier": "Low",
                "recommendation": "Replace or pause keyword - Low conversion rate"
            },
            {
                "keyword_text": "free laptop giveaways 2026",
                "match_type": "BROAD",
                "clicks": 725,
                "impressions": 20000,
                "ctr": 3.62,
                "cpc": 1.01,
                "cost": 732.25,
                "conversions": 10,
                "roi": 40.0,
                "performance_tier": "Low",
                "recommendation": "Remove keyword - High cost, very low intent"
            }
        ]
    else:
        return [
            {
                "keyword_text": "gaming laptop deals",
                "match_type": "EXACT",
                "clicks": 920,
                "impressions": 15000,
                "ctr": 6.13,
                "cpc": 1.45,
                "cost": 1334.0,
                "conversions": 55,
                "roi": 260.0,
                "performance_tier": "High",
                "recommendation": "Keep keyword"
            },
            {
                "keyword_text": "alienware discount code",
                "match_type": "PHRASE",
                "clicks": 650,
                "impressions": 18000,
                "ctr": 3.61,
                "cpc": 1.85,
                "cost": 1202.5,
                "conversions": 22,
                "roi": 140.0,
                "performance_tier": "Low",
                "recommendation": "Improve keyword match type"
            }
        ]

def generate_synthetic_click_logs(count=120):
    """
    Generates synthetic click logs containing both normal user behavior
    and suspicious click bursts (fraud bot patterns).
    """
    logs = []
    base_time = datetime.utcnow() - timedelta(hours=6)
    
    ip_pool = ["192.168.1.10", "10.0.4.15", "172.16.8.99", "45.33.21.101"]
    suspicious_bot_ip = "185.220.101.5" # Concentrated bot IP address!
    
    for i in range(count):
        # Inject suspicious bot burst in middle of data
        if 40 <= i <= 65:
            # High frequency clicks from same IP within sub-seconds
            time_offset = timedelta(seconds=(i - 40) * 0.8 + random.uniform(0.1, 0.4))
            ip = suspicious_bot_ip
            interval = random.uniform(0.2, 1.1) # extremely rapid interval
            user_agent = "Python-requests/2.31.0 (Automated Scraper)"
            device = "Bot Server"
        else:
            time_offset = timedelta(seconds=i * random.uniform(30, 180))
            ip = random.choice(ip_pool)
            interval = random.uniform(15.0, 300.0)
            user_agent = random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) Mobile/15E148"
            ])
            device = random.choice(["Desktop", "Mobile", "Tablet"])
            
        click_time = base_time + time_offset
        logs.append({
            "timestamp": click_time,
            "ip_address": ip,
            "user_agent": user_agent,
            "device": device,
            "location": "US-East" if ip != suspicious_bot_ip else "Proxy-Vulkan",
            "click_interval_sec": round(interval, 2)
        })
    return logs

def generate_historical_time_series(days=90):
    """
    Generates historical daily performance data for training ML regression models.
    """
    records = []
    start_date = datetime.utcnow() - timedelta(days=days)
    
    for d in range(days):
        current_date = start_date + timedelta(days=d)
        
        # Simulate realistic fluctuations and correlations
        daily_budget = random.uniform(120.0, 180.0)
        cpc = random.uniform(0.60, 0.95)
        spend = daily_budget * random.uniform(0.85, 0.98)
        clicks = int(spend / cpc)
        ctr = round(random.uniform(3.5, 7.2), 2)
        impressions = int((clicks / (ctr / 100)))
        
        # Conversions non-linearly depend on CTR and Clicks
        conv_rate = round(random.uniform(3.0, 7.5), 2)
        conversions = int(clicks * (conv_rate / 100))
        
        # ROI correlates with conversion rate and lower CPC
        revenue = conversions * random.uniform(45.0, 65.0)
        roi = round(((revenue - spend) / spend) * 100, 2) if spend > 0 else 0.0
        
        records.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "daily_budget": round(daily_budget, 2),
            "impressions": impressions,
            "clicks": clicks,
            "ctr": ctr,
            "cpc": round(cpc, 3),
            "spend": round(spend, 2),
            "conversions": conversions,
            "conv_rate": conv_rate,
            "roi": roi
        })
        
    return pd.DataFrame(records)
