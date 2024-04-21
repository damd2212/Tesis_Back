from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

# El pipeline guardado no contiene las definiciones de los transformadores
class ColumnExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, columns, output_type="matrix"):
        self.columns = columns
        self.output_type = output_type

    def transform(self, X, **transform_params):
        if isinstance(X, list):
            X = pd.DataFrame.from_dict(X)
        if self.output_type == "matrix":
            return X[self.columns].values
        elif self.output_type == "dataframe":
            return X[self.columns]

    def fit(self, X, y=None, **fit_params):
        return self