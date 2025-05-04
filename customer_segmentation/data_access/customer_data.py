import sys
from typing import Optional

import numpy as np
import pandas as pd


from customer_segmentation.configuration.mongo_db_connection import MongoDBClient
from customer_segmentation.constant.database import DATABASE_NAME
from customer_segmentation.exception import CustomerException

class CustomerData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        try:
            # initoate the mongo client database
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise CustomerException(e, sys)

    def export_data_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """ 
        export entire collection as dataframe: return pd.DataFrame of collection
        """
        try:
            if database_name is None:
                # if database name not give use default
                collection = self.mongo_client.database[collection_name]
            else:
                # if database name given
                collection = self.mongo_client[database_name][collection_name]

            # fetching all records once and converting to dataframe
            df = pd.DataFrame(list(collection.find()))

            # dropping extra column from dataframe, it's id generated from mongo
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            # replacing 'na' from mongo to processable nan info for dataframe format
            df.replace({"na": np.nan}, inplace=True)

            return df
        
        except Exception as e:
            raise CustomerException(e, sys)
