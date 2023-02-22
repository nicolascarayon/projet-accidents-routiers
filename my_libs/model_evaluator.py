import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report


class ModelEvaluator:

    def __init__(self, model_type, params, X_train, y_train, X_test, y_test):
        self.model_type, self.params = model_type, params
        self.X_train, self.y_train, self.X_test, self.y_test = X_train, y_train, X_test, y_test

    def evaluate(self):
        start_time = time.time()

        if self.model_type == 'DecisionTreeClassifier'     : model = DecisionTreeClassifier(**self.params)
        if self.model_type == 'RandomForestClassifier'     : model = RandomForestClassifier(**self.params)
        if self.model_type == 'GradientBoostingClassifier' : model = GradientBoostingClassifier(**self.params)
        if self.model_type == 'CatBoostClassifier'         : model = CatBoostClassifier(**self.params)

        model.fit(self.X_train, self.y_train)

        y_pred = model.predict(self.X_test)

        print(f"\n--- Model {self.model_type} fit and trained in %s seconds ---" % (time.time() - start_time))
        print(f"--- Params : {self.params}")

        display(pd.crosstab(self.y_test, y_pred, rownames=['Classe réelle'], colnames=['Classe prédite']))

        print("\nClassification report :")
        print(classification_report(self.y_test, y_pred))

        return model