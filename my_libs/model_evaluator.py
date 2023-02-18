import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from imblearn.metrics import classification_report_imbalanced
from sklearn.metrics import classification_report


class ModelEvaluator:

    def __init__(self, model_type, params, X_train, y_train, X_test, y_test):
        self.model_type = model_type
        self.params = params
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def evaluate(self):
        start_time = time.time()

        if self.model_type == 'DecisionTreeClassifier':
            model = DecisionTreeClassifier(max_depth=self.params['max_depth'],
                                           criterion=self.params['criterion'],
                                           max_features=self.params['max_features'],
                                           min_samples_split=self.params['min_samples_split'])

        if self.model_type == 'RandomForestClassifier':
            model = RandomForestClassifier(n_estimators=self.params['n_estimators'],
                                           criterion=self.params['criterion'],
                                           max_depth=self.params['max_depth'],
                                           min_samples_split=self.params['min_samples_split'])

        model.fit(self.X_train, self.y_train)

        y_pred = model.predict(self.X_test)

        print(f"--- Model {self.model_type} fit and trained in %s seconds ---" % (time.time() - start_time))
        print(f"--- Params : {self.params}")

        display(pd.crosstab(self.y_test, y_pred, rownames=['Classe réelle'], colnames=['Classe prédite']))

        print("Classification report :")
        print(classification_report(self.y_test, y_pred))
        # print(classification_report_imbalanced(self.y_test, y_pred))
