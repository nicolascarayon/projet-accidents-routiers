import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import make_column_transformer
from category_encoders import TargetEncoder, OneHotEncoder
from pandas import get_dummies
class FeaturesEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, trace=False, cols_target_encoded=['dep'], cols_continuous=['age']):
        self.trace = trace
        self.cols_target_encoded = cols_target_encoded
        self.cols_continuous = cols_continuous
        self.target_encoder = TargetEncoder()
    def fit(self, X, y):
        self.y = y
        return self

    def transform(self, X):

        self.cols_onehot_encoded = X.columns.drop(self.cols_target_encoded).drop(self.cols_continuous)

        # not encoded variables
        X_enc = X[self.cols_continuous].copy()

        # target encoded variables
        for col in self.cols_target_encoded:

            if len(self.y) == X.shape[0]:
                X_enc.loc[:, col] = self.target_encoder.fit_transform(X[col].astype('str'), self.y)
            else:
                X_enc.loc[:, col] = self.target_encoder.transform(X[col].astype('str'))
            if self.trace: print(f'Column {col} has been target encoded')


        # one hot encoded variables
        for col in self.cols_onehot_encoded:
            X_enc = X_enc.join(pd.get_dummies(X[col], prefix=col))
            if self.trace: print(f'Column {col} has been one hot encoded')
        return X_enc
