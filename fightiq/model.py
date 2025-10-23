"""
model.py: Contains FightIQModel class for UFC fight outcome prediction.

The FightIQModel loads historical fight data from a CSV file, filters draws,
extracts numeric features, trains a logistic regression classifier,
and provides methods to predict outcomes for new fights.
"""

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class FightIQModel:
    """Machine learning model for predicting UFC fight outcomes using logistic regression."""

    def __init__(self):
        """Initialize the pipeline with feature scaling and logistic regression classifier."""
        self.pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000))
        ])

    def load_data(self, csv_path: str):
        """
        Load fight data from a CSV file and prepare features and labels.

        Parameters
        ----------
        csv_path : str
            Path to the CSV file containing fight records. The file must
            include a 'Winner' column specifying the winning corner ('Red' or 'Blue').

        Returns
        -------
        X : pandas.DataFrame
            Numeric feature matrix.
        y : pandas.Series
            Binary label series where 1 represents a Blue win and 0 represents a Red win.
        """
        df = pd.read_csv(csv_path)
        if "Winner" not in df.columns:
            raise ValueError("CSV must contain a 'Winner' column.")
        # Keep only fights with a decisive winner
        df = df[df["Winner"].isin(["Red", "Blue"])] .copy()
        y = (df["Winner"] == "Blue").astype(int)
        X = df.drop(columns=["Winner"]).select_dtypes(include=[np.number]).fillna(0)
        return X, y

    def train(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42) -> float:
        """
        Train the logistic regression model and return the test accuracy.

        Parameters
        ----------
        X : pandas.DataFrame
            Numeric feature matrix.
        y : pandas.Series
            Binary label series.
        test_size : float, optional
            Fraction of the data to reserve for testing, by default 0.2.
        random_state : int, optional
            Random seed for reproducibility, by default 42.

        Returns
        -------
        float
            Accuracy of the model on the test set.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        self.pipeline.fit(X_train, y_train)
        y_pred = self.pipeline.predict(X_test)
        return accuracy_score(y_test, y_pred)

    def predict(self, X: pd.DataFrame):
        """
        Predict fight outcomes for new data.

        Parameters
        ----------
        X : pandas.DataFrame
            Numeric feature matrix.

        Returns
        -------
        numpy.ndarray
            Array of predictions where 1 indicates a Blue win and 0 indicates a Red win.
        """
        return self.pipeline.predict(X)
