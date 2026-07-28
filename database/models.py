from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from database.database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), default='ABC Electronics')
    is_demo_mode = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    accounts = db.relationship('GoogleAdsAccount', backref='owner', lazy=True, cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class GoogleAdsAccount(db.Model):
    __tablename__ = 'google_ads_accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_id = db.Column(db.String(50), nullable=False, default='892-410-9921')
    account_name = db.Column(db.String(100), nullable=False, default='ABC Electronics Google Ads Account')
    is_connected = db.Column(db.Boolean, default=True)
    connection_type = db.Column(db.String(20), default='DEMO') # DEMO or LIVE_API
    developer_token = db.Column(db.String(100), nullable=True)
    refresh_token = db.Column(db.String(256), nullable=True)
    connected_at = db.Column(db.DateTime, default=datetime.utcnow)

    campaigns = db.relationship('Campaign', backref='account', lazy=True, cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('google_ads_accounts.id'), nullable=False)
    google_campaign_id = db.Column(db.String(50), nullable=False, default='CMP-2026-DELL-15')
    name = db.Column(db.String(150), nullable=False, default='Dell Laptop Sale 2026')
    product_name = db.Column(db.String(100), default='Dell Inspiron 15 Laptop')
    business_name = db.Column(db.String(100), default='ABC Electronics')
    status = db.Column(db.String(20), default='ELIGIBLE') # ELIGIBLE, PAUSED, ENDED
    
    budget = db.Column(db.Float, nullable=False, default=5000.0) # Total allocated budget ($)
    budget_used = db.Column(db.Float, nullable=False, default=4600.0) # Spend so far ($)
    impressions = db.Column(db.Integer, default=124500)
    clicks = db.Column(db.Integer, default=6225)
    ctr = db.Column(db.Float, default=5.0) # % (5.0%)
    cpc = db.Column(db.Float, default=0.739) # Average Cost per click ($)
    cost = db.Column(db.Float, default=4600.0)
    conversions = db.Column(db.Integer, default=311)
    conv_rate = db.Column(db.Float, default=5.0) # %
    roi = db.Column(db.Float, default=245.0) # % ROI

    # Performance Thresholds for Decision Engine
    target_ctr = db.Column(db.Float, default=6.0)
    acceptable_cpc = db.Column(db.Float, default=0.65)
    target_roi = db.Column(db.Float, default=250.0)

    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    keywords = db.relationship('Keyword', backref='campaign', lazy=True, cascade='all, delete-orphan')
    click_logs = db.relationship('ClickLog', backref='campaign', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='campaign', lazy=True, cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='campaign', lazy=True, cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def budget_used_percentage(self):
        if self.budget > 0:
            return round((self.budget_used / self.budget) * 100, 1)
        return 0.0

    @property
    def remaining_budget(self):
        return max(0.0, self.budget - self.budget_used)

class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    keyword_text = db.Column(db.String(100), nullable=False)
    match_type = db.Column(db.String(20), default='EXACT') # EXACT, PHRASE, BROAD
    clicks = db.Column(db.Integer, default=0)
    impressions = db.Column(db.Integer, default=0)
    ctr = db.Column(db.Float, default=0.0)
    cpc = db.Column(db.Float, default=0.0)
    cost = db.Column(db.Float, default=0.0)
    conversions = db.Column(db.Integer, default=0)
    roi = db.Column(db.Float, default=0.0)
    performance_tier = db.Column(db.String(20), default='Average') # High, Average, Low
    recommendation = db.Column(db.String(100), default='Keep keyword') # Keep, Improve, Replace, Remove

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ClickLog(db.Model):
    __tablename__ = 'click_logs'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(255), default='Mozilla/5.0')
    device = db.Column(db.String(30), default='Desktop')
    location = db.Column(db.String(50), default='US-East')
    click_interval_sec = db.Column(db.Float, default=12.5) # Time gap from previous click
    fraud_score = db.Column(db.Float, default=0.15) # Anomaly score from Isolation Forest
    is_suspicious = db.Column(db.Boolean, default=False)
    risk_level = db.Column(db.String(10), default='Low') # Low, Medium, High

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False) # Fraud Alert, Budget Alert, Low CTR Alert, High CPC Alert, Performance Alert
    title = db.Column(db.String(150), nullable=False)
    problem = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='Medium') # High, Medium, Low
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    recommendations = db.relationship('Recommendation', backref='alert', lazy=True, cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    alert_id = db.Column(db.Integer, db.ForeignKey('alerts.id'), nullable=True)
    category = db.Column(db.String(50), default='General') # Budget, Keyword, Fraud, Performance
    problem = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    ai_analysis = db.Column(db.Text, nullable=False)
    recommended_action = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='Medium') # High, Medium, Low
    status = db.Column(db.String(20), default='Pending') # Pending, Applied, Dismissed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
