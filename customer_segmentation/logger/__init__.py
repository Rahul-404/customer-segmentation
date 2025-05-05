import logging
import os

from from_root import from_root

from customer_segmentation.constant.trainin_pipeline import ARTIFACT_DIR, LOG_DIR, LOG_FILE, PIPELINE_NAME

log_path= os.path.join(from_root(), PIPELINE_NAME, ARTIFACT_DIR, LOG_DIR)

os.makedirs(log_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="w",
    format= "[%(asctime)s] \t%(levelname)s \t%(lineno)d \t%(filename)s \t%(funcName)s( ) \t%(message)s",
    level=logging.INFO
)