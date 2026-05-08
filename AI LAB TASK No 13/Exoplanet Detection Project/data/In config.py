In config.py

import os

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "..", "data", "cumulative.csv")
    CLEANED_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned_cumulative.csv")


In data_cleaner.py

import pandas as pd
from config import Config


class DataCleaner:

    def __init__(self, file_path=None):
        self.__file_path = file_path or Config.DATA_PATH
        self.__raw_data = None
        self.__cleaned_data = None
        self.cleaning_log = []

        self.__clean_columns_used = [
            "koi_period", "koi_duration", "koi_depth", "koi_prad",
            "koi_teq", "koi_insol", "koi_model_snr", "koi_steff",
            "koi_slogg", "koi_srad", "koi_kepmag", "koi_disposition"
        ]


    def load_data(self):
        try:
            self.__raw_data = pd.read_csv(self.__file_path)
            self.cleaning_log.append("Data loaded successfully")
        except Exception as e:
            raise Exception(f"Error loading file: {e}")


    def selected_columns(self):
        self.__cleaned_data = self.__raw_data[self.__clean_columns_used].copy()
        self.cleaning_log.append("Columns selected")

   
    def drop_missing(self):
        self.__cleaned_data.dropna(inplace=True)
        self.cleaning_log.append("Missing values removed")

    
    def filter_classes(self):
        self.__cleaned_data = self.__cleaned_data[
            self.__cleaned_data["koi_disposition"].isin(["CONFIRMED", "FALSE POSITIVE"])
        ]
        self.cleaning_log.append("Filtered valid classes")

    
    def encode_target(self):
        self.__cleaned_data["koi_disposition"] = self.__cleaned_data["koi_disposition"].map({
            "CONFIRMED": 1,
            "FALSE POSITIVE": 0
        })
        self.cleaning_log.append("Target encoded")

    
    def clean_all(self):
        self.load_data()
        self.selected_columns()
        self.filter_classes()
        self.drop_missing()
        self.encode_target()

        return self.__cleaned_data

    
    def save_cleaned_data(self, output_path=None):
        path = output_path or Config.CLEANED_DATA_PATH
        self.__cleaned_data.to_csv(path, index=False)
        return f"Saved to {path}"
    

In train_test_splitting.py

from sklearn.model_selection import train_test_split

class DataSplitter:

    def __init__(self, data, target_column="koi_disposition", test_size=0.2, random_state=42):
        self.__data = data
        self.__target_column = target_column
        self.__test_size = test_size
        self.__random_state = random_state

        self.__X_train = None
        self.__X_test = None
        self.__y_train = None
        self.__y_test = None


    def split(self):
        if self.__data is None:
            raise ValueError("No data provided for splitting")

        X = self.__data.drop(self.__target_column, axis=1)
        y = self.__data[self.__target_column]

        self.__X_train, self.__X_test, self.__y_train, self.__y_test = train_test_split(
            X, y,
            test_size=self.__test_size,
            random_state=self.__random_state,
            stratify=y
        )

    def get_train_data(self):
        return self.__X_train, self.__y_train

    def get_test_data(self):
        return self.__X_test, self.__y_test


In base_model.py

from abc import ABC, abstractmethod
import pickle

class BaseModel(ABC):
    def __init__(self):
        self._model = None

        
    @abstractmethod
    def train(self, X_train, y_train):
        pass

    @abstractmethod
    def predict(self, X_test):
        pass

    def save_model(self, file_path):
        if self._model is None:
            raise ValueError("No model to save")

        with open(file_path, 'wb') as f:
            pickle.dump(self._model, f)

    def load_model(self, file_path):
        with open(file_path, 'rb') as f:
            pickle.load(self._model, f)
            self._model = pickle.load(f)
        

In random_forest_model.py

from sklearn.ensemble import RandomForestClassifier
from base_model import BaseModel

class RandomForestModel(BaseModel):
    def __init__(self, n_estimators = 100, max_depth = None, random_state = 42):
        super().__init__()
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state

    def train(self, X_train, y_train):
        self._model = RandomForestClassifier(
            n_estimators = self.n_estimators,
            max_depth = self.max_depth,
            random_state = self.random_state
        )

        self._model.fit(X_train, y_train)

    def predict(self, X_test):
        if self._model is None:
            raise ValueError('Model has not been trained yet')
        return self._model.predict(X_test)


In prediction.py

import numpy as np

class PredictionService:
    def __init__(self, model):
        self.__model = model

    def validate_input(self, input_data):
        if input_data is None:
            raise ValueError("Input cannot be None")

        if not isinstance(input_data, (list, tuple)):
            raise TypeError("Input must be a list or tuple")

        if len(input_data) != 11:
            raise ValueError("Expected 11 features")

    def preprocess(self, input_data):
        return np.array([input_data])

    def predict(self, input_data):
        self.validate_input(input_data)
        processed = self.preprocess(input_data)
        prediction = self.__model.predict(processed)

        return self.decode_prediction(prediction[0])

    def decode_prediction(self, pred):
        mapping = {0: "FALSE POSITIVE", 1: "CONFIRMED"}
        return mapping.get(pred, "UNKNOWN")


In accuracy.py

from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report

class ModelEvaluator:
    def __init__(self, y_true, y_pred):
        self.__y_true = y_true
        self.__y_pred = y_pred
    def accuracy(self):
        return accuracy_score(self.__y_true, self.__y_pred)

    def precision(self):
        return precision_score(self.__y_true, self.__y_pred)
    
    def recall(self):
        return recall_score(self.__y_true, self.__y_pred)
    
    def confusion_matrix(self):
        return confusion_matrix(self.__y_true, self.__y_pred)
    
    def classification_report(self):
        return classification_report(self.__y_true, self.__y_pred)

    def summary(self):
        return {
            "accuracy": self.accuracy(),
            "precision": self.precision(),
            "recall": self.recall()
        }


In main.py

from numpy import rint
from sklearn.metrics import accuracy_score
from data_cleaner import DataCleaner
from train_test_splitting import DataSplitter
from base_model import BaseModel
from random_forest_model import RandomForestModel
from accuracy import ModelEvaluator
from prediction import PredictionService

def main():
    cleaner = DataCleaner()
    exoplanet_data = cleaner.clean_all()

    if exoplanet_data is not None:
        print("Data Loaded & Cleaned Successfully\n")
        print(exoplanet_data.head())
        print(exoplanet_data.info())  
    else:
        print("Data cleaning failed")

    splitter = DataSplitter(exoplanet_data)
    splitter.split()

    X_train, y_train = splitter.get_train_data()
    X_test, y_test = splitter.get_test_data()

    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)

    model = RandomForestModel()
    model.train(X_train, y_train)
    print("Model trained successfully")

    predictions = model.predict(X_test)
    
    service = PredictionService(model)
    sample_input = X_test.iloc[0].tolist()
    result = service.predict(sample_input)
    print("Prediction via service:", result)


    evaluator = ModelEvaluator(y_test, predictions)
    print("Accuracy:", evaluator.accuracy())
    print("Precision:", evaluator.precision())
    print("Recall:", evaluator.recall())

    print("\nConfusion Matrix:\n", evaluator.confusion_matrix())
    print("\nClassification Report:\n", evaluator.classification_report())

if __name__ == "__main__":
    main()