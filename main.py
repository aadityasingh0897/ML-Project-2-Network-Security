import sys
from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.components.data_validation import DataValidation
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from Network_Security.logging.logger import logging

if __name__ == '__main__':
    try:
                                                
        training_pipeline_config = TrainingPipelineConfig()

        # DATA INGESTION
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        # DATA VALIDATION 
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
            data_validation_config=data_validation_config,
            data_ingestion_artifact=data_ingestion_artifact
        )

        data_validation_artifact = data_validation.initiate_data_validation()                       

        
    except Exception as e:
        raise NetworkSecurityException(e, sys)
