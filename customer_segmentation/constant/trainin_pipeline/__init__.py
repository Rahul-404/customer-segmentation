# pipeline name and root directory constant
import os
from datetime import datetime
from customer_segmentation.constant.s3_bucket import TRAINING_BUCKET_NAME

TARGET_COLUMN = "cluster"
PIPELINE_NAME: str = "customer_segmentation"
ARTIFACT_DIR: str = "artifact"
LOG_DIR = "logs"
LOG_FILE = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# common file name

FILE_NAME: str = "customer.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME = "model.pkl"
SCHEMA_FILE_PATH = os.path.join(PIPELINE_NAME, "configuration", "schema.yaml")


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = ""
DATA_INGESTION_DIR_NAME: str  = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
