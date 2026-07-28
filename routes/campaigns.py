from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from database.database import db
from database.models import Campaign, Keyword, ClickLog, Alert, Recommendation, GoogleAdsAccount
from decision_engine.decision_manager import HybridDecisionManager
from google_ads.google_ads_api import GoogleAdsAPIClient

campaigns_bp = Blueprint('campaigns', __name__, url_prefix='/campaigns')
decision_manager = HybridDecisionManager()

@campaigns_bp.route('/')
@login_required
def index():
    account = GoogleAdsAccount.query.filter_by(user_id=current_user.id).first()
    campaigns = Campaign.query.all()
    return render_template('campaigns/index.html', account=account, campaigns=campaigns)

@campaigns_bp.route('/connect', methods=['GET', 'POST'])
@login_required
def connect():
    account = GoogleAdsAccount.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        dev_token = request.form.get('dev_token')
        mode = request.form.get('connection_type', 'DEMO')

        if account:
            account.customer_id = customer_id
            account.developer_token = dev_token
            account.connection_type = mode
            account.is_connected = True
        else:
            account = GoogleAdsAccount(
                user_id=current_user.id,
                customer_id=customer_id,
                account_name=f"{current_user.company_name} Ads",
                connection_type=mode,
                is_connected=True
            )
            db.session.add(account)

        db.session.commit()
        flash(f'Google Ads Account settings updated ({mode} mode active).', 'success')
        return redirect(url_for('campaigns.index'))

    api_client = GoogleAdsAPIClient()
    account_summary = api_client.fetch_account_summary()
    campaigns = Campaign.query.all()

    return render_template('campaigns/connect.html', account=account, summary=account_summary, campaigns=campaigns)

@campaigns_bp.route('/<int:campaign_id>')
@login_required
def detail(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    keywords = Keyword.query.filter_by(campaign_id=campaign.id).all()
    click_logs = ClickLog.query.filter_by(campaign_id=campaign.id).all()
    click_logs_dict = [cl.__dict__ for cl in click_logs]

    # Run full AI diagnosis
    diagnosis = decision_manager.run_full_diagnosis(
        campaign_data=campaign.__dict__,
        keywords_list=[kw.__dict__ for kw in keywords],
        click_logs=click_logs_dict
    )

    alerts = Alert.query.filter_by(campaign_id=campaign.id).order_by(Alert.created_at.desc()).all()
    recommendations = Recommendation.query.filter_by(campaign_id=campaign.id).all()

    return render_template(
        'campaigns/detail.html',
        campaign=campaign,
        keywords=keywords,
        click_logs=click_logs,
        diagnosis=diagnosis,
        alerts=alerts,
        recommendations=recommendations
    )

@campaigns_bp.route('/<int:campaign_id>/simulate-prediction', methods=['POST'])
@login_required
def simulate_prediction(campaign_id):
    """
    API endpoint for what-if scenario simulator.
    Receives budget_adjustment_pct from frontend slider and returns updated ML predictions.
    """
    campaign = Campaign.query.get_or_404(campaign_id)
    data = request.get_json() or {}
    budget_sim_pct = float(data.get('budget_adjustment_pct', 0.0))

    prediction_results = decision_manager.performance_predictor.predict_performance(
        current_metrics=campaign.__dict__,
        budget_adjustment_pct=budget_sim_pct
    )

    return jsonify({"status": "success", "prediction": prediction_results})
