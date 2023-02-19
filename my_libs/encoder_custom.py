import time
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
        self.cols_onehot_encoded = cols_onehot_encoded
        self.target_encoder = TargetEncoder()
        self.encoder_target = TargetEncoder(cols=cols_target_encoded)
        self.encoder_onehot = OneHotEncoder(cols=cols_onehot_encoded)
        self.scaler = StandardScaler()
        # self.sampler = SMOTE()
        self.sampler = SMOTEN()
        # self.sampler        = RandomUnderSampler()
        # self.sampler        = RandomOverSampler()

    def fit(self, X, y):
        return self

    def transform(self, X, y, datatype='Train'):

        start_time = time.time()

        if datatype == 'Train':
            X, y = self.sampler.fit_resample(X, y)
            print("Classes cardinality after resampling :")
            print(y.value_counts())
            print(f"X shape : {X.shape}")

            if len(self.cols_target_encoded)>0:
                print(f"Columns target encoded : {self.cols_target_encoded}")
                X = self.encoder_target.fit_transform(X, y)

            X = self.encoder_onehot.fit_transform(X, y)
            print(f"Columns one hot encoded : {self.cols_onehot_encoded}")

            X = self.scaler.fit_transform(X)
            print(f"Features normalized")



        if datatype == 'Test':
            X  = self.encoder_target.transform(X)
            X  = self.encoder_onehot.transform(X)
            X = self.scaler.transform(X)

        time_spent = time.time() - start_time
        print(f"--- {datatype} set - features encoding performed in {time_spent:.2f} seconds ---")

        return pd.DataFrame(data=X, columns=self.encoder_onehot.get_feature_names()), y

#%%
