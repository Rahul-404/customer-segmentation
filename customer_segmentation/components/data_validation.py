import json
import sys
from typing import Tuple, Union
import pandas as pd

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from pandas import DataFrame

from customer_segmentation.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from customer_segmentation.entity.config_entity import DataValidationConfig

# from customer_segmentation.components.data_ingestion import DataIngestion

from customer_segmentation.exception import CustomerException
from customer_segmentation.logger import logging
from customer_segmentation.utils.main_utils import MainUtils, write_yaml_file

class DataValidation:

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.utils = MainUtils()
        self._schema_config = self.utils.read_schema_config_file()

    def validate_schema_columns(self, dataframe: DataFrame) -> bool:
        """ 
        Method Name : validate_schema_columns
        Description : This method validate the schema columns for the particular dataframe

        Output      : True or False value is returned based on the schema
        On Failure  : Write an exception log and then raise an exception

        Version     : 0.1
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required column present [{status}]")
            return status
        except Exception as e:
            raise CustomerException(e, sys)
        
    def validate_dataset_schema_columns(self, train_set, test_set) -> Tuple[bool, bool]:
        """ 
        Method Name : validate_dataset_schema_columns
        Description : This methos validate the schema for shcem columns for both train and test set

        Output      : True or False value is returned based on the schema
        On Failure  : Write an exception log and then raise an exception
        Version     : 0.1
        """
        logging.info("Entered validate_dataset_schema_columns method of DataValidationClass")
        try:
            logging.info("Validating dataset schema columns")
            train_schema_status = self.validate_schema_columns(train_set)
            logging.info("Validated dataset schema columns on the train set")
            test_schema_status = self.validate_schema_columns(test_set)
            logging.info("Validated dataset schema columns")

            return train_schema_status, test_schema_status
        
        except Exception as e:
            raise CustomerException(e, sys)
        
    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame)-> bool:
        """ 
        Method Name : detect_dataset_drift
        Description : This method deetcts the dataset droft using the reference and production dataframe

        Output      : Returns bool or float value based on the get_ration parameter
        On Failure  : Write an exception log and then raise an exception

        Version     : 0.1
        """
        try:
            data_drift_profile = Report([DataDriftPreset()])
            data_drift_profile.run(reference_data=reference_df, current_data=current_df)
            report = data_drift_profile.json()
            json_report = json.loads(report)
            # writing the report as json
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

            n_features = json_report["metrics"][0]["result"]["number_of_columns"]

            n_drifted_features = json_report["metrics"][0]["result"]["number_of_drifted_columns"]
            
            logging.info(f"{n_drifted_features}/{n_features} drift detected.")

            drift_status = json_report["metrics"][0]["result"]["dataset_drift"]

            return drift_status

        except Exception as e:
            raise CustomerException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomerException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   0.1
        """
        logging.info("Entered initiate_data_validation method of Data_Validation class")

        try:
            logging.info("Initiated data validation for the dataset")

            train_df, test_df = (DataValidation.read_data(file_path = self.data_ingestion_artifact.train_file_path),
                                DataValidation.read_data(file_path = self.data_ingestion_artifact.test_file_path))
            
            
            
            drift = self.detect_dataset_drift(train_df, test_df)

            (
                schema_train_col_status,
                schema_test_col_status,
            ) = self.validate_dataset_schema_columns(train_set=train_df, test_set=test_df)

            logging.info(
                f"Schema train cols status is {schema_train_col_status} and schema test cols status is {schema_test_col_status}"
            )

            logging.info("Validated dataset schema columns")

            

            if (
                schema_train_col_status is True
                and schema_test_col_status is True
                and drift is False
            ):
                logging.info("Dataset schema validation completed")

                validation_status = True
            else:
                validation_status = False
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact
        except Exception as e:
            raise CustomerException(e, sys)
        
# if __name__ == "__main__":
#     data_ingestion_object = DataIngestion()
#     data_ingestion_artifact = data_ingestion_object.initiate_data_ingestion()

#     data_validation_object = DataValidation(data_ingestion_artifact=data_ingestion_artifact, 
#                                             data_validation_config=DataValidationConfig)
#     data_validation_artifact = data_validation_object.initiate_data_validation()
#     print(data_validation_artifact)