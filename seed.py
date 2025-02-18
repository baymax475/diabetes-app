import pandas as pd
from app.__init__ import create_app
from app.extensions import db
from app.models import DiabetesData

app = create_app()
app.app_context().push()

def seed_data():
    # Load the diabetes dataset
    df = pd.read_csv('diabetes.csv')

    # Insert data into the database
    for _, row in df.iterrows():
        data = DiabetesData(
            Pregnancies=row['Pregnancies'],
            Glucose=row['Glucose'],
            BloodPressure=row['BloodPressure'],
            SkinThickness=row['SkinThickness'],
            Insulin=row['Insulin'],
            BMI=row['BMI'],
            DiabetesPedigreeFunction=row['DiabetesPedigreeFunction'],
            Age=row['Age'],
            Outcome=row['Outcome']
        )
        db.session.add(data)
    db.session.commit()
    print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()