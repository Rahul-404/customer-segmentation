from typing import Tuple
from pandas import DataFrame

from customer_segmentation.exception import CustomerException
from customer_segmentation.logger import logging
import os, sys

# input for function
from customer_segmentation.entity.config_entity import (DataIngestionConfig,
                                                        DataValidationConfig)

# function
from customer_segmentation.component.data_ingestion import DataIngestion
from customer_segmentation.component.data_validation import DataValidation

# output for function
from customer_segmentation.entity.artifact_entity import (DataIngestionArtifact,
                                                          DataValidationArtifact)


class TrainPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()


    def start_data_ingestion(self) -> DataIngestionArtifact:

        logging.info("Entered the start_data_ingestion method of TrainPipeline class")

        try:
            logging.info("Getting the data from mongodb")

            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got the train_set and train_set from mongodb")

            logging.info(
                "Executed the start_data_ingestion method of trainPipeline class"
            )

            return data_ingestion_artifact
        
        except Exception as e:
            raise CustomerException(e, sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise CustomerException(e, sys) from e
        
    def run_pipeline(self) -> None:
        logging.info("Entered the run_pipeline method of TrainPipeline class")

        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact = data_ingestion_artifact
            )

        except Exception as e:
            raise CustomerException(e, sys)