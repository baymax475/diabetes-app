from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from app.models import DiabetesData
from app.extensions import db
from app.forms import PredictionForm, LoginForm, SignupForm
from app.models import User
import pickle

# Load your trained model
with open('diabetes_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define Blueprints
main_routes = Blueprint('main_routes', __name__)
auth_routes = Blueprint('auth_routes', __name__)
dashboard_routes = Blueprint('dashboard_routes', __name__)
predict_routes = Blueprint('predict_routes', __name__)

# Main Routes
@main_routes.route('/')
def index():
    return render_template('index.html')

# Authentication Routes
@auth_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth_routes.login'))
    return render_template('signup.html', form=form)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard_routes.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_routes.index'))

# Dashboard Routes
@dashboard_routes.route('/dashboard')
@login_required
def dashboard():
    data = DiabetesData.query.all()
    return render_template('dashboard.html', data=data)

# Prediction Routes
@predict_routes.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form = PredictionForm()

    if form.validate_on_submit():
        pregnancies = form.pregnancies.data
        glucose = form.glucose.data
        blood_pressure = form.blood_pressure.data
        skin_thickness = form.skin_thickness.data
        insulin = form.insulin.data
        bmi = form.bmi.data
        diabetes_pedigree_function = form.diabetes_pedigree_function.data
        age = form.age.data

        prediction_result = predict_diabetes(
            pregnancies, glucose, blood_pressure, skin_thickness,
            insulin, bmi, diabetes_pedigree_function, age
        )

        return render_template('predict.html', form=form, prediction=prediction_result)

    return render_template('predict.html', form=form)

# Prediction Function
def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age):
    input_data = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]]
    prediction = model.predict(input_data)
    return "Diabetic" if prediction[0] == 1 else "Not Diabetic"

# Error Handlers
@main_routes.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@main_routes.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500