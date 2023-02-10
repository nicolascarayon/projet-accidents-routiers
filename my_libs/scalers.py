from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
class FeaturesScaler(TransformerMixin):

    def __init__(self, trace=False, cols_target_encoded=['jour', 'age', 'dep']):
        self.trace = trace
        self.cols_target_encoded = cols_target_encoded
        self.sc = StandardScaler()

    def fit(self, X, y):
        self.sc.fit(X[self.cols_target_encoded])

        return self

    def transform(self, X):
        X_sc = X
        X_sc[self.cols_target_encoded] = self.sc.transform(X[self.cols_target_encoded])
        if self.trace: print(f"Columns {self.cols_target_encoded} have been normalized with Standard Scaler")
        return X_sc
