from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

from Network_Security.entity.config_entity import DataIngestionConfig
from Network_Security.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pymongo
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            database = self.mongo_client[self.data_ingestion_config.database_name]
            collection = database[self.data_ingestion_config.collection_name]

            df = pd.DataFrame(list(collection.find()))
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set, test_test = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            
            logging.info("Perform train test split on the dataframe")

            logging.info("Exited split_data_as_train_test method of Data Igestion Class")

            dir_path=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train and test file path")

            train_set.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_test.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)

            logging.info(f"Exported Train and Test data")

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()

            # save train / test files ...

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)