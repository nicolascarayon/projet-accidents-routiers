import time
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from category_encoders import TargetEncoder, OneHotEncoder

class EncoderCustom(BaseEstimator, TransformerMixin):
    def __init__(self, cols_target_encoded=[], cols_onehot_encoded=[], trace=False):
        self.trace = trace
        self.cols_target_encoded = cols_target_encoded
        self.cols_onehot_encoded = cols_onehot_encoded
        self.encoder_target = TargetEncoder(cols=cols_target_encoded)
        self.encoder_onehot = OneHotEncoder(cols=cols_onehot_encoded)
    def fit(self, X, y):
        return self

    def transform(self, X, y, datatype='Train'):

        start_time = time.time()

        if datatype == 'Train':

            if len(self.cols_target_encoded) > 0:
                X = self.encoder_target.fit_transform(X, y)
                print(f"Columns target encoded : {list(self.cols_target_encoded)}")

            if len(self.cols_onehot_encoded) > 0:
                X = self.encoder_onehot.fit_transform(X, y)
                print(f"Columns one hot encoded : {list(self.cols_onehot_encoded)}")

        if datatype == 'Test':
            X = self.encoder_target.transform(X)
            X = self.encoder_onehot.transform(X)

        time_spent = time.time() - start_time
        print(f"--- {datatype} set - features encoding performed in {time_spent:.2f} seconds ---")

        return pd.DataFrame(data=X, columns=self.encoder_onehot.get_feature_names()), y

# %%
