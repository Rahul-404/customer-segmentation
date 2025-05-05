import shutil
import sys
from typing import Dict, Tuple
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import linear_model
import yaml

from pandas import DataFrame
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import all_estimators
from yaml import safe_dump

from customer_segmentation.constant.trainin_pipeline import *
from customer_segmentation.exception import CustomerException
from customer_segmentation.logger import logging

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path : str location of file to load
    return    : np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomerException(e, sys)
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomerException(e, sys)
    
class MainUtils:

    def __init__(self) -> None:
        pass


    def read_yaml_file(self, filename: str) -> dict:
        try:
            with open(filename, "rb") as yaml_file:
                return yaml.safe_load(yaml_file)

        except Exception as e:
            raise CustomerException(e, sys)
        
    def read_schema_config_file(self) -> dict:
        try:
            schema_config = self.read_yaml_file(SCHEMA_FILE_PATH)

            return schema_config
        except Exception as e:
            raise CustomerException(e, sys)