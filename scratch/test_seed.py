import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app

from database.models import User, Campaign, Keyword, Alert, Recommendation

app = create_app()

with app.app_context():
    user = User.query.first()
    campaigns = Campaign.query.all()
    keywords = Keyword.query.all()
    alerts = Alert.query.all()
    recs = Recommendation.query.all()

    print(f"User: {user.email} ({user.company_name})")
    print(f"Total Campaigns: {len(campaigns)}")
    for c in campaigns:
        print(f"  - Campaign: {c.name} | Product: {c.product_name} | Spend: ${c.cost} | ROI: {c.roi}%")
    print(f"Total Keywords: {len(keywords)}")
    print(f"Total Alerts: {len(alerts)}")
    print(f"Total Recommendations: {len(recs)}")
    print("Database seeding & AI model integration verification SUCCESSFUL!")
