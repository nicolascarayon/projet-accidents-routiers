from sklearn.base import BaseEstimator, TransformerMixin
from category_encoders import TargetEncoder, OneHotEncoder
from imblearn.over_sampling import SMOTEN, SMOTE, SMOTENC, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
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
        # self.sampler = SMOTENC()
        # self.sampler        = RandomUnderSampler()
        # self.sampler        = RandomOverSampler()

    def fit(self, X, y):
        return self

    def transform(self, X, y, datatype='Train'):

        self.sampler = SMOTEN()

        if datatype == 'Train':
            X, y = self.sampler.fit_resample(X, y)
            X = self.encoder_target.fit_transform(X, y)
            X = self.encoder_onehot.fit_transform(X, y)
            X = self.scaler.fit_transform(X)

        if datatype == 'Test':
            X  = self.encoder_target.transform(X)
            X  = self.encoder_onehot.transform(X)
            X = self.scaler.transform(X)

        return pd.DataFrame(data=X, columns=self.encoder_onehot.get_feature_names()), y

#%%
