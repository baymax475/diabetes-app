from flask import Blueprint, render_template
from flask_login import login_required
from app.models import DiabetesData

dashboard_routes = Blueprint('dashboard_routes', __name__)

@dashboard_routes.route('/dashboard')
@login_required
def dashboard():
    data = DiabetesData.query.all()
    return render_template('dashboard.html', data=data)