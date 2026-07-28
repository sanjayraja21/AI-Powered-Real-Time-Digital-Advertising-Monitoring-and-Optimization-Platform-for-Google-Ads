from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from database.database import db
from database.models import Alert, Recommendation, Campaign

alerts_bp = Blueprint('alerts', __name__, url_prefix='/alerts')

@alerts_bp.route('/')
@login_required
def index():
    severity_filter = request.args.get('severity', 'all')
    category_filter = request.args.get('category', 'all')

    alert_query = Alert.query
    if severity_filter != 'all':
        alert_query = alert_query.filter_by(severity=severity_filter.capitalize())

    alerts = alert_query.order_by(Alert.created_at.desc()).all()

    rec_query = Recommendation.query
    if category_filter != 'all':
        rec_query = rec_query.filter_by(category=category_filter.capitalize())

    recommendations = rec_query.order_by(Recommendation.priority.asc()).all()

    return render_template(
        'alerts/index.html',
        alerts=alerts,
        recommendations=recommendations,
        selected_severity=severity_filter,
        selected_category=category_filter
    )

@alerts_bp.route('/recommendations')
@login_required
def recommendations():
    recommendations = Recommendation.query.order_by(Recommendation.priority.asc()).all()
    return render_template('alerts/recommendations.html', recommendations=recommendations)

@alerts_bp.route('/recommendations/<int:rec_id>/apply', methods=['POST'])
@login_required
def apply_recommendation(rec_id):
    rec = Recommendation.query.get_or_404(rec_id)
    rec.status = 'Applied'
    db.session.commit()
    flash(f"Optimization recommendation for '{rec.category}' marked as Applied! You can now execute this change in Google Ads.", 'success')
    return redirect(url_for('alerts.index'))

@alerts_bp.route('/alerts/<int:alert_id>/dismiss', methods=['POST'])
@login_required
def dismiss_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    alert.is_read = True
    db.session.commit()
    flash('Alert dismissed.', 'info')
    return redirect(url_for('alerts.index'))
