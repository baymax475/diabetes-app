from flask import Flask,render_template
from config import Config
from app.routes import main_routes
from app.extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main_routes, auth_routes, dashboard_routes, predict_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(predict_routes)
    app.register_blueprint(dashboard_routes)

    with app.app_context():
        db.create_all()

    return app

import pickle

# Load your trained model
with open('diabetes_model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age):
    # Prepare input data for the model
    input_data = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]]
    
    # Make a prediction
    prediction = model.predict(input_data)
    
    # Return the result
    return "Diabetic" if prediction[0] == 1 else "Not Diabetic"

@main_routes.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@main_routes.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
