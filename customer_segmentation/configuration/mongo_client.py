from pymongo.mongo_client import MongoClient
from customer_segmentation.constant.env_variable import env_var


mongo_client = MongoClient(env_var.mongo_db_url)