import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import os
from app.core.config import settings

class F1Regressor:
    def __init__(self):
        self.model = None
        self.model_path = settings.MODEL_PATH
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print("Model loaded successfully.")
        else:
            print("No model found. Please train first.")

    def train(self, data: pd.DataFrame):
        """
        Train the model using the provided dataframe.
        Expected columns: 'driver', 'constructor', 'grid', 'points', etc.
        """
        # Feature Engineering (Basic example)
        X = data[['grid', 'driver', 'constructor']]
        y = data['points']

        # Preprocessing
        numeric_features = ['grid']
        categorical_features = ['driver', 'constructor']

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        # Pipeline
        self.model = Pipeline(steps=[('preprocessor', preprocessor),
                                     ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

        self.model.fit(X, y)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")

    def predict(self, driver: str, constructor: str, grid: int) -> float:
        if not self.model:
            raise ValueError("Model not trained.")
        
        input_data = pd.DataFrame({
            'driver': [driver],
            'constructor': [constructor],
            'grid': [grid]
        })
        
        prediction = self.model.predict(input_data)
        return prediction[0]

# Singleton instance
regressor = F1Regressor()
