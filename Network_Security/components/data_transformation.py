import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from Network_Security.constants.training_pipepline import TARGET_COLUMN
from Network_Security.constants.training_pipepline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from Network_Security.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from Network_Security.entity.config_entity import DataTransformationConfig
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.utils.main_utils.utils import save_numpy_array_data, save_object

 
class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(self) -> Pipeline:
        try:
            logging.info("Creating data transformer object")
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor = Pipeline(steps=[("imputer", imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")

            if not self.data_validation_artifact.validation_status:
                raise ValueError(
                    "Data validation failed. Transformation aborted."
                )

            train_df = self.read_data(
                self.data_validation_artifact.valid_train_file_path
            )
            test_df = self.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]

            preprocessor = self.get_data_transformer_object()

            input_feature_train_arr = preprocessor.fit_transform(
                input_feature_train_df
            )
            input_feature_test_arr = preprocessor.transform(
                input_feature_test_df
            )

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                train_arr,
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                test_arr,
            )
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor,
            )

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info("Data transformation completed successfully")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
