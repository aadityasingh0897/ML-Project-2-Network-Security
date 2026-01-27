import sys
from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from Network_Security.logging.logger import logging

if __name__ == '__main__':
    try:
        # ✅ CREATE OBJECTS (not classes)
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(
            training_pipeline_config=trainingpipelineconfig
        )

        # ✅ PASS CONFIG INTO COMPONENT
        data_ingestion = DataIngestion(
            data_ingestion_config=dataingestionconfig
        )

        logging.info("Data Ingestion Started")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
