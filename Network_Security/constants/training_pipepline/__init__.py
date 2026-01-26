import os
import sys
import numpy as np
import pandas as pd

"""Define all the constant variables for training pipeline here  """

TAREGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "Network_Security"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

"""data ingestion related constant start with DATA_INGESTION_VAR_NAME"""

DATA_INGESTION_COLLECTION_NAME: str = "Phishing_Data"
DATA_INGESTION_DATABASE_NAME: str = "Network_Security"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

