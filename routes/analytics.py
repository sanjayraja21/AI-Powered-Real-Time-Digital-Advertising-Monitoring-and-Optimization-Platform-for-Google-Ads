from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from database.models import Campaign, Keyword, ClickLog
from google_ads.campaign_data import generate_historical_time_series

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/')
@login_required
def index():
    campaigns = Campaign.query.all()
    # Generate 90-day time series for charts
    df_ts = generate_historical_time_series(days=30)
    time_series_data = df_ts.to_dict(orient='records')
    
    return render_template('analytics/index.html', campaigns=campaigns, time_series=time_series_data)

@analytics_bp.route('/api/time-series')
@login_required
def api_time_series():
    df_ts = generate_historical_time_series(days=30)
    return jsonify(df_ts.to_dict(orient='records'))
