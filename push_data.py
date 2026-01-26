import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def cv_to_json(self, file_path: str):
        """
        This function converts a CSV file to a JSON string.
        :param file_path: Path to the CSV file
        :return: JSON string
        """
        try:
            df = pd.read_csv(file_path)
            records = df.to_dict(orient="records")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mangodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mando_client=pymongo.MongoClient(MONGO_DB_URL)

            self.database = self.mando_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    FILE_PATH ="C:\\Users\\singh\\Documents\\Data Science Projects\\Practice\\Network Security\\Network_Data\\phisingData.csv"
    DATABASE="Network_Security"
    COLLECTION="Phishing_Data"
    networkobj=NetworkDataExtract()
    records=networkobj.cv_to_json(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mangodb(records=records,database=DATABASE,collection=COLLECTION)
    print(f"Number of records inserted: {no_of_records}")