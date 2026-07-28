from flask import Blueprint, render_template, request
from flask_login import login_required
from database.models import Campaign, Keyword, Alert, Recommendation, ClickLog
from decision_engine.decision_manager import HybridDecisionManager
from datetime import datetime

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
decision_manager = HybridDecisionManager()

@reports_bp.route('/')
@login_required
def index():
    report_type = request.args.get('type', 'performance')
    campaigns = Campaign.query.all()
    selected_campaign = campaigns[0] if campaigns else None

    report_data = {}
    if selected_campaign:
        keywords = Keyword.query.filter_by(campaign_id=selected_campaign.id).all()
        click_logs = [cl.__dict__ for cl in ClickLog.query.filter_by(campaign_id=selected_campaign.id).all()]
        diagnosis = decision_manager.run_full_diagnosis(
            campaign_data=selected_campaign.__dict__,
            keywords_list=[kw.__dict__ for kw in keywords],
            click_logs=click_logs
        )
        report_data = {
            "campaign": selected_campaign,
            "diagnosis": diagnosis,
            "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }

    return render_template('reports/index.html', report_type=report_type, campaigns=campaigns, data=report_data)
