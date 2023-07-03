import os
import sys 
import pandas as pd 
import numpy as np 
from pymongo import MongoClient
from zipfile import Path
from constant import *

from src.exceptions import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer



class DataIngestionConfig():
    def __init__(self,artifact_folder:str = os.path.join('artifacts'),
                train_data_path:str = os.path.join('artifacts','train.csv'),
                test_data_path:str = os.path.join('artifacts','test.csv')):
        self.artifact_folder = artifact_folder
        self.train_data_path = train_data_path
        self.test_data_path = test_data_path


class DataIngestion():
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def export_collection_from_db_as_dataframe(self,database_name,collection_name):
        '''
            Desc: This function will responsible for extracting collections from mongo db 
            as data frame
        '''
        try:
            logging.info('Data ingestion started')
            client = MongoClient(URL)
            logging.info('Connecting with mongo db atlas')
            collection = client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=['_id'],axis=1,inplace=True)
            logging.info('Data ingestion completed')
            return df
        except Exception as e:
            raise CustomException(e,sys)
        
    def export_data_into_file_path(self)->pd.DataFrame:
        '''
            Desc: This method reads data from mongodb and saves it into artifacts.
        '''
        try:
            logging.info('Data exporting started')
            raw_file_path = self.data_ingestion_config.artifact_folder
            os.makedirs(raw_file_path,exist_ok=True)
            credit_data = self.export_collection_from_db_as_dataframe(
                DATABASE_NAME,
                COLLECTION_NAME
            )
            logging.info(f'Saving data into folder: {raw_file_path}')
            store_file_path = os.path.join(raw_file_path,'credit_card.csv')
            credit_data.to_csv(store_file_path,index=False)
            return store_file_path
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_ingestion(self)->Path:
        '''
            Desc: This method initiates the data ingestion components of training pipeline
        '''
        try:
            store_file_path = self.export_data_into_file_path()
            logging.info('Got the data from db and saved under artifact folder')
            data = pd.read_csv(store_file_path)
            logging.info('Data read as data frame after saved successfully')
            logging.info('Data splitting started "Train Test Split"')
            train_set, test_set = train_test_split(data,test_size=0.2,random_state=42)
            train_set.to_csv(self.data_ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.test_data_path,index=False,header=True)
            logging.info('Data splitted successfully')
            return (
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path,
                store_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data,store_file_path = obj.initiate_data_ingestion()
    dt = DataTransformation(store_file_path=store_file_path)
    train_arr,test_arr,_ = dt.initiate_data_transformation(train_path=train_data,test_path=test_data)
    model_trainer_obj = ModelTrainer()
    model_trainer_obj.initiate_model_trainer(train_arr=train_arr,test_arr=test_arr)