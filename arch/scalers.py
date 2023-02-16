from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
class FeaturesScaler(TransformerMixin):

    def __init__(self, trace=False, cols=['age', 'dep']):
        self.trace = trace
        self.cols = cols
        self.sc = StandardScaler()

    def fit(self, X, y=None):

        return self

    def transform(self, X):
        X_sc = X
        X_sc[self.cols] = self.sc.fit_transform(X[self.cols])
        if self.trace: print(f"Columns {self.cols} have been normalized with Standard Scaler")
        return X_sc
