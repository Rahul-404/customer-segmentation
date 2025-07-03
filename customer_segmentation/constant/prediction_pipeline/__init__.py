import os
from customer_segmentation.constant.s3_bucket import (PREDICTION_BUCKET_NAME,
                                       TRAINING_BUCKET_NAME)
from customer_segmentation.constant.training_pipeline import PIPELINE_NAME

PRED_SCHEMA_FILE_PATH = os.path.join(PIPELINE_NAME, 'configuration', 'prediction_schema.yaml')

PREDICTION_DATA_BUCKET = "customer-segmentation-bucket"
PREDICTION_INPUT_FILE_NAME = "customer_pred_data.csv"
PREDICTION_OUTPUT_FILE_NAME = "customer_predictions.csv"
MODEL_BUCKET_NAME = TRAINING_BUCKET_NAME