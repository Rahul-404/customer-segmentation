import sys, os
from pandas import DataFrame
from typing import Tuple
import numpy as np
from sklearn.model_selection import train_test_split
from customer_segmentation.logger import logging
from customer_segmentation.exception import CustomerException
from customer_segmentation.constant.database import DATABASE_NAME, COLLECTION_NAME
from customer_segmentation.entity.config_entity import DataIngestionConfig
from customer_segmentation.entity.artifact_entity import DataIngestionArtifact
from customer_segmentation.data_access.customer_data import CustomerData
from customer_segmentation.utils.main_utils import MainUtils


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        self.data_ingestion_config = data_ingestion_config
        self.utils = MainUtils()

    def export_data_into_feature_store(self)->DataFrame:
        """
        Method Name : export_data_into_feature_store
        Description : This method reads data from mongodb and saves it into artifacts.

        Output      : dataset is returned as a DataFrame
        On Failure  : Write an exception log and then raise an exception

        Version     : 0.1 
        """
        try:
            logging.info("Exporting data from mongodb")
            # customer data object
            customer_data = CustomerData()
            # using object fetching data from mongodb give a collection name
            customer_dataframe = customer_data.export_data_collection_as_dataframe(
                collection_name = COLLECTION_NAME
            )
            # logging the shape of data
            logging.info(f"Shape of dataframe: {customer_dataframe.shape}")
            # preparing path to store data
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # converting it to be a directory
            dir_path = os.path.dirname(feature_store_file_path)
            # creating the directory to store data if not exists
            os.makedirs(dir_path, exist_ok= True)
            # logging the store data path
            logging.info(f"Saving exported data into feature store file path : {feature_store_file_path}")
            # saving the fetched dataset
            customer_dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return customer_dataframe
        except Exception as e:
            raise CustomerException(e, sys)
        
    def split_data_as_train_test(self, dataframe: DataFrame) -> Tuple[DataFrame, DataFrame]:
        """
        Method Name : split_data_as_train_test
        Descrption  : This method splits the dataframe into train set and test set based on split ratio

        Output      : Folder is created in s3 bucket
        On Failure  : Write an expectation log and then raise an exception

        Version     : 0.1
        """
        logging.info("Entered split_data_as_train_test method of DataIngestion class")
        try:
            # splitting data into train test 
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Exited split_data_as_train_test method of DataIngestion class")
            # path to store train test data
            ingested_data_dir = self.data_ingestion_config.ingested_data_dir
            # creating directory
            os.makedirs(ingested_data_dir, exist_ok=True)
            # saving training data
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            logging.info("Training data has been saved")
            # saving testing data
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info("Testing data has been saved")
        except Exception as e:
            raise CustomerException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name : initialize_data_ingestion
        Description : This method initiated the data ingestion components of training pipeline

        Output      : train set and test set are returned as the artifacts of data ingestion components
        On Failure  : write an exception log and then raise an execution

        Version     : 1.0
        Revisions   : moved setup to closed 
        """
        logging.info("Entered initiate_data_ingestion method of DataIngestion class")

        try:
            dataframe = self.export_data_into_feature_store()

            _schema_config = self.utils.read_schema_config_file()

            dataframe = dataframe.drop(_schema_config["drop_columns"], axis=1)

            logging.info("Got the data from mongodb")

            self.split_data_as_train_test(dataframe)

            logging.info("Exited initiate_data_ingestion method of DataIngestion class")

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise CustomerException(e, sys)