from Network_Security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Network_Security.entity.config_entity import DataValidationConfig

from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

from Network_Security.constants.training_pipepline import SCHEMA_FILE_PATH
from Network_Security.utils.main_utils.utils import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import os
import sys

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException (e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException (e,sys)
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            schema_columns = self._schema_config["numerical_columns"]

            logging.info(f"Required number of columns: {len(schema_columns)}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")

            return len(dataframe.columns) == len(schema_columns)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


        
    def validate_numerical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            schema_numerical_cols = set(self._schema_config["numerical_columns"])
            dataframe_numerical_cols = set(
                dataframe.select_dtypes(include="number").columns
            )

            logging.info(f"Schema numerical columns: {schema_numerical_cols}")
            logging.info(f"DataFrame numerical columns: {dataframe_numerical_cols}")

            return schema_numerical_cols.issubset(dataframe_numerical_cols)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

        
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            drift_status = True
            report = {}

            for column in base_df.select_dtypes(include="number").columns:
                d1 = base_df[column]
                d2 = current_df[column]

                ks_result = ks_2samp(d1, d2)
                drift_detected = ks_result.pvalue < threshold

                report[column] = {
                    "p_value": float(ks_result.pvalue),
                    "drift_status": drift_detected
                }

                if drift_detected:
                    drift_status = False

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(drift_report_file_path, report)

            return drift_status

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            # read train and test data
            train_df = self.read_data(
                self.data_ingestion_artifact.trained_file_path
            )
            test_df = self.read_data(
                self.data_ingestion_artifact.test_file_path
            )

            status = True

            # column validations
            status &= self.validate_number_of_columns(train_df)
            status &= self.validate_number_of_columns(test_df)

            # numerical column validation
            status &= self.validate_numerical_columns_exist(train_df)
            status &= self.validate_numerical_columns_exist(test_df)

            # drift detection
            drift_status = self.detect_dataset_drift(
                base_df=train_df,
                current_df=test_df
            )
            if not drift_status:
                logging.warning(
                    "Dataset drift detected. Proceeding with transformation because drift is being ignored."
                )

            # create validation directories
            os.makedirs(
                os.path.dirname(self.data_validation_config.valid_train_file_path),
                exist_ok=True
            )

            # save validated data
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True
            )

            return DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)


