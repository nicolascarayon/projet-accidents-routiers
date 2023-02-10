from sklearn.base import BaseEstimator, TransformerMixin
from category_encoders import TargetEncoder
import pandas as pd

class FeaturesEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, trace=False, cols_target_encoded=['jour', 'age', 'dep']):
        self.trace = trace
        self.cols_target_encoded = cols_target_encoded

    def fit(self, X, y):
        self.y = y
        return self

    def transform(self, X):
        # target encoding
        X_enc = X
        for col in self.cols_target_encoded:
            # X = self.encode_target_col(X, col, self.y)
            X_enc[f"{col}"] = TargetEncoder().fit_transform(X[col].astype('str'), self.y)
            if self.trace: print(f"Column {col} has been target encoded")

        # hot encoding for other columns
        for col in X_enc.columns:
            if not (col in self.cols_target_encoded):
                if col in X_enc.columns:
                    X_enc = X_enc.join(pd.get_dummies(X_enc[col], prefix=col))
                    X_enc = X_enc.drop(columns=[col], axis=1)
                    if self.trace: print(f"Column {col} has been dummy encoded")

        return X_enc

    # def fit_transform(self, X, y=None, **fit_params):
    #     if y is None:
    #         # fit method of arity 1 (unsupervised transformation)
    #         return self.fit(X, **fit_params).transform(X, y)
    #     else:
    #         # fit method of arity 2 (supervised transformation)
    #         return self.fit(X, y, **fit_params).transform(X, y)
