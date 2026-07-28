from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from database.models import Campaign, Keyword, Alert, Recommendation, ClickLog
from decision_engine.decision_manager import HybridDecisionManager
from google_ads.campaign_data import generate_synthetic_click_logs, get_demo_keywords
import random

dashboard_bp = Blueprint('dashboard', __name__)
decision_manager = HybridDecisionManager()

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    campaigns = Campaign.query.all()
    if not campaigns:
        # Fallback empty state handling
        return render_template('dashboard/index.html', campaigns=[], kpis={}, diagnosis={})

    main_campaign = campaigns[0]
    keywords = Keyword.query.filter_by(campaign_id=main_campaign.id).all()
    click_logs = [cl.__dict__ for cl in ClickLog.query.filter_by(campaign_id=main_campaign.id).all()]

    # Run AI Analysis and Decision Engine
    diagnosis = decision_manager.run_full_diagnosis(
        campaign_data=main_campaign.__dict__,
        keywords_list=[kw.__dict__ for kw in keywords],
        click_logs=click_logs
    )

    # Compute Aggregate Dashboard KPIs across all campaigns
    total_campaigns = len(campaigns)
    active_campaigns = len([c for c in campaigns if c.status == 'ELIGIBLE'])
    total_clicks = sum([c.clicks for c in campaigns])
    avg_ctr = round(sum([c.ctr for c in campaigns]) / total_campaigns, 2) if total_campaigns > 0 else 0.0
    total_spend = round(sum([c.cost for c in campaigns]), 2)
    avg_roi = round(sum([c.roi for c in campaigns]) / total_campaigns, 1) if total_campaigns > 0 else 0.0
    total_fraud_alerts = Alert.query.filter_by(alert_type='Fraud Alert').count()
    total_recs = Recommendation.query.filter_by(status='Pending').count()

    kpis = {
        "total_campaigns": total_campaigns,
        "active_campaigns": active_campaigns,
        "total_clicks": total_clicks,
        "avg_ctr": avg_ctr,
        "total_spend": total_spend,
        "avg_roi": avg_roi,
        "fraud_alerts": total_fraud_alerts,
        "recommendations": total_recs
    }

    recent_alerts = Alert.query.order_by(Alert.created_at.desc()).limit(5).all()
    recent_recs = Recommendation.query.order_by(Recommendation.priority.asc()).limit(5).all()

    return render_template(
        'dashboard/index.html',
        campaigns=campaigns,
        main_campaign=main_campaign,
        kpis=kpis,
        diagnosis=diagnosis,
        alerts=recent_alerts,
        recommendations=recent_recs
    )

@dashboard_bp.route('/api/realtime-metrics')
@login_required
def realtime_metrics():
    """
    API Endpoint for simulated real-time metric polling.
    Adds realistic jitter/increment to simulate live traffic stream.
    """
    campaign = Campaign.query.first()
    if not campaign:
        return jsonify({"status": "error", "message": "No campaign found"})

    # Simulate realistic micro-increments
    click_delta = random.choice([0, 1, 2, 3])
    impression_delta = random.choice([15, 25, 45])
    cost_delta = round(click_delta * campaign.cpc, 2)

    campaign.clicks += click_delta
    campaign.impressions += impression_delta
    campaign.cost += cost_delta
    campaign.budget_used += cost_delta

    if campaign.impressions > 0:
        campaign.ctr = round((campaign.clicks / campaign.impressions) * 100, 2)

    return jsonify({
        "status": "success",
        "clicks": campaign.clicks,
        "impressions": campaign.impressions,
        "cost": campaign.cost,
        "ctr": campaign.ctr,
        "cpc": campaign.cpc,
        "conversions": campaign.conversions,
        "budget_used_percentage": campaign.budget_used_percentage,
        "roi": campaign.roi,
        "click_delta": click_delta,
        "timestamp": campaign.last_updated.strftime("%H:%M:%S")
    })
