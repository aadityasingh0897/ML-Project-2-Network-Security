from Network_Security.constants.training_pipepline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os
import sys

from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def predict(self, X):
        try:
            X_transform = self.preprocessor.transform(X)
            predictions = self.model.predict(X_transform)
            return predictions
        except Exception as e:
            raise NetworkSecurityException(e, sys)