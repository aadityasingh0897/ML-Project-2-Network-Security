import sys
from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.components.data_validation import DataValidation
from Network_Security.components.data_transformation import DataTransformation
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig
from Network_Security.logging.logger import logging

if __name__ == '__main__':
    try:
                                                
        training_pipeline_config = TrainingPipelineConfig()

        # DATA INGESTION
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        logging.info("Data Ingestion Started")
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")

        print(data_ingestion_artifact)

        # DATA VALIDATION 
        data_validation_config = DataValidationConfig(training_pipeline_config)
        logging.info("Data Validation Started")

        data_validation = DataValidation(
            data_validation_config=data_validation_config,
            data_ingestion_artifact=data_ingestion_artifact
        )

        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")
        print(data_validation_artifact)

        # DATA TRANSFORMATION
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        logging.info("Data Transformation Started")
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data Transformation completed")
        print(data_transformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
