import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the dataset
df = pd.read_csv('diabetes.csv')

# Split into features (X) and target (y)
X = df.drop('Outcome', axis=1)  # Features
y = df['Outcome']  # Target

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model to a .pkl file
with open('diabetes_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved as diabetes_model.pkl")