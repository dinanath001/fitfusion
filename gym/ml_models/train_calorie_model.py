# train_calorie_model.py

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 1. Simulated larger dataset
np.random.seed(42)
num_samples = 100

data = {
    'age': np.random.randint(18, 60, size=num_samples),
    'weight': np.random.randint(50, 100, size=num_samples),  # kg
    'height': np.random.randint(150, 200, size=num_samples),  # cm
    'gender': np.random.randint(0, 2, size=num_samples),  # 0 = Male, 1 = Female
    'activity_level': np.random.randint(1, 4, size=num_samples),  # 1=low, 2=medium, 3=high
    'body_fat_percent': np.round(np.random.uniform(10, 35, size=num_samples), 1),
    'sleep_hours': np.round(np.random.uniform(5, 9, size=num_samples), 1)
}

df = pd.DataFrame(data)

# 2. Compute derived feature: BMI
df['height_m'] = df['height'] / 100
df['bmi'] = df['weight'] / (df['height_m'] ** 2)

# 3. Simulate calorie output (example formula)
df['calories'] = (
    10 * df['weight'] +
    6.25 * df['height'] -
    5 * df['age'] +
    df['gender'].map({0: 5, 1: -161}) +
    df['activity_level'] * 100 +
    (8 - df['sleep_hours']) * 20 +
    (df['body_fat_percent'] - 20) * 10 +
    np.random.normal(0, 100, size=num_samples)
)

# 4. Features and target
features = ['age', 'weight', 'height', 'gender', 'activity_level', 'bmi', 'body_fat_percent', 'sleep_hours']
X = df[features]
y = df['calories']

# 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluate model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f} calories")

# 8. Save the model
joblib.dump(model, 'calorie_predictor_model.pkl')
print("Model saved successfully!")
