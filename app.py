import os
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from config import Config
from database.database import db, init_db
from database.models import User, GoogleAdsAccount, Campaign, Keyword, ClickLog, Alert, Recommendation
from google_ads.campaign_data import get_demo_campaign_data, get_demo_keywords, generate_synthetic_click_logs
from decision_engine.decision_manager import HybridDecisionManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Database
    init_db(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.campaigns import campaigns_bp
    from routes.analytics import analytics_bp
    from routes.alerts import alerts_bp
    from routes.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(reports_bp)

    @app.route('/settings')
    def settings():
        return render_template('settings.html')

    # Seed Database on initialization if empty
    with app.app_context():
        seed_demo_data()

    return app

def seed_demo_data():
    """Seeds the SQLite database with realistic ABC Electronics demo data if empty."""
    if User.query.first() is not None:
        return # Database already seeded

    print("Seeding SQLite database with AI AdMonitor demo dataset...")

    # Create default demo business owner user
    demo_user = User(
        email='owner@abcelectronics.com',
        full_name='Alex Rivera (CEO, ABC Electronics)',
        company_name='ABC Electronics',
        is_demo_mode=True
    )
    demo_user.set_password('demo1234')
    db.session.add(demo_user)
    db.session.commit()

    # Create Google Ads Account
    ads_account = GoogleAdsAccount(
        user_id=demo_user.id,
        customer_id='892-410-9921',
        account_name='ABC Electronics (Google Ads Account)',
        is_connected=True,
        connection_type='DEMO'
    )
    db.session.add(ads_account)
    db.session.commit()

    # Create Demo Campaigns
    demo_campaigns = get_demo_campaign_data()
    decision_manager = HybridDecisionManager()

    for c_data in demo_campaigns:
        campaign = Campaign(
            account_id=ads_account.id,
            google_campaign_id=c_data['google_campaign_id'],
            name=c_data['name'],
            product_name=c_data['product_name'],
            business_name=c_data['business_name'],
            status=c_data['status'],
            budget=c_data['budget'],
            budget_used=c_data['budget_used'],
            impressions=c_data['impressions'],
            clicks=c_data['clicks'],
            ctr=c_data['ctr'],
            cpc=c_data['cpc'],
            cost=c_data['cost'],
            conversions=c_data['conversions'],
            conv_rate=c_data['conv_rate'],
            roi=c_data['roi'],
            target_ctr=c_data['target_ctr'],
            acceptable_cpc=c_data['acceptable_cpc'],
            target_roi=c_data['target_roi']
        )
        db.session.add(campaign)
        db.session.commit()

        # Add Demo Keywords for this campaign
        keywords_data = get_demo_keywords(campaign.name)
        for kw_data in keywords_data:
            kw = Keyword(
                campaign_id=campaign.id,
                keyword_text=kw_data['keyword_text'],
                match_type=kw_data['match_type'],
                clicks=kw_data['clicks'],
                impressions=kw_data['impressions'],
                ctr=kw_data['ctr'],
                cpc=kw_data['cpc'],
                cost=kw_data['cost'],
                conversions=kw_data['conversions'],
                roi=kw_data['roi'],
                performance_tier=kw_data['performance_tier'],
                recommendation=kw_data['recommendation']
            )
            db.session.add(kw)

        # Add Click Logs (normal + suspicious bot activity)
        click_logs = generate_synthetic_click_logs(count=100 if "Dell Laptop" in campaign.name else 40)
        for log in click_logs:
            cl = ClickLog(
                campaign_id=campaign.id,
                timestamp=log['timestamp'],
                ip_address=log['ip_address'],
                user_agent=log['user_agent'],
                device=log['device'],
                location=log['location'],
                click_interval_sec=log['click_interval_sec']
            )
            db.session.add(cl)

        db.session.commit()

        # Run AI Diagnosis to generate real Alerts and Recommendations in database
        click_logs_dict = [cl.__dict__ for cl in ClickLog.query.filter_by(campaign_id=campaign.id).all()]
        kw_dict = [k.__dict__ for k in Keyword.query.filter_by(campaign_id=campaign.id).all()]
        diagnosis = decision_manager.run_full_diagnosis(
            campaign_data=campaign.__dict__,
            keywords_list=kw_dict,
            click_logs=click_logs_dict
        )

        # Save AI Alerts
        for a_data in diagnosis['alerts']:
            alert = Alert(
                campaign_id=campaign.id,
                alert_type=a_data['alert_type'],
                title=a_data['title'],
                problem=a_data['problem'],
                severity=a_data['severity']
            )
            db.session.add(alert)
        db.session.commit()

        # Save AI Recommendations
        for r_data in diagnosis['recommendations']:
            rec = Recommendation(
                campaign_id=campaign.id,
                category=r_data['category'],
                problem=r_data['problem'],
                reason=r_data['reason'],
                ai_analysis=r_data['ai_analysis'],
                recommended_action=r_data['recommended_action'],
                priority=r_data['priority'],
                status='Pending'
            )
            db.session.add(rec)
        db.session.commit()

    print("Demo dataset seeded successfully!")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
