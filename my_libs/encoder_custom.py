from sklearn.base import BaseEstimator, TransformerMixin
from category_encoders import TargetEncoder, OneHotEncoder
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

import pandas as pd
class EncoderCustom(BaseEstimator, TransformerMixin):
    def __init__(self, cols_target_encoded=[], cols_onehot_encoded=[], trace=False):
        self.trace = trace
        self.cols_target_encoded = cols_target_encoded
        self.target_encoder = TargetEncoder()

        self.encoder_target = TargetEncoder(cols=cols_target_encoded)
        self.encoder_onehot = OneHotEncoder(cols=cols_onehot_encoded)
        self.scaler = StandardScaler()
        self.sampler = SMOTE()
        # sampler        = RandomUnderSampler()
        # sampler        = RandomOverSampler()

    def fit(self, X, y):
        return self

    def transform(self, X, y, datatype='Train'):
        if datatype == 'Train':
            X_te = self.encoder_target.fit_transform(X, y)
            X_oh = self.encoder_onehot.fit_transform(X_te, y)
            X_sc = self.scaler.fit_transform(X_oh)
            X_rs, y_rs = self.sampler.fit_resample(X_sc, y)
        if datatype == 'Test':
            X_te  = self.encoder_target.transform(X)
            X_oh  = self.encoder_onehot.transform(X_te)
            X_sc  = self.scaler.transform(X_oh)
            X_rs, y_rs = self.sampler.fit_resample(X_sc, y)

        # return pd.DataFrame(data=X_sc, columns=X_oh.columns), y
        return pd.DataFrame(data=X_rs, columns=X_oh.columns), y_rs
