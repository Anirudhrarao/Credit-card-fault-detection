import os
import sys
from src.logger import logging
from src.exceptions import CustomException
from src.utils import save_object

import pandas as pd 
import numpy as np 

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


class DataTransformationConfig:
    artifact_folder = os.path.join('artifacts')
    preprocessor_file = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self,store_file_path):
        self.data_transformation_config = DataTransformationConfig()
        self.store_file_path = store_file_path

    def get_data_transformer_object(self):
        '''
            Desc: This function responsible for data transformation
            and than it will save our pickle file as preprocessor.pkl 
        '''
        try:
            logging.info('Data transformation started')
            numerical_columns = [
                                "LIMIT_BAL",
                                "AGE",
                                "BILL_AMT1",
                                "BILL_AMT2",
                                "BILL_AMT3",
                                "BILL_AMT4",
                                "BILL_AMT5",
                                "BILL_AMT6",
                                "PAY_AMT1",
                                "PAY_AMT2",
                                "PAY_AMT3",
                                "PAY_AMT4",
                                "PAY_AMT5",
                                "PAY_AMT6",
                                "SEX",
                                "EDUCATION",
                                "MARRIAGE",
                                "PAY_0",
                                "PAY_2",
                                "PAY_3",
                                "PAY_4",
                                "PAY_5",
                                "PAY_6"]
            numerical_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            preprocessor = ColumnTransformer(
                [
                    ('Numerical_pipeline',numerical_pipeline,numerical_columns)
                ]
            )
            logging.info('Data transformation completed successfully')
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_data = pd.read_csv(train_path) 
            test_data = pd.read_csv(test_path)
            numerical_columns = [
                                "LIMIT_BAL",
                                "AGE",
                                "BILL_AMT1",
                                "BILL_AMT2",
                                "BILL_AMT3",
                                "BILL_AMT4",
                                "BILL_AMT5",
                                "BILL_AMT6",
                                "PAY_AMT1",
                                "PAY_AMT2",
                                "PAY_AMT3",
                                "PAY_AMT4",
                                "PAY_AMT5",
                                "PAY_AMT6",
                                "SEX",
                                "EDUCATION",
                                "MARRIAGE",
                                "PAY_0",
                                "PAY_2",
                                "PAY_3",
                                "PAY_4",
                                "PAY_5",
                                "PAY_6"]
            preprocessor = self.get_data_transformer_object()
            target_column = 'default payment next month'
            drop_column = [target_column]
            logging.info('Splitting train data into independent and dependent data')
            input_feature_train_data = train_data.drop(columns=drop_column,axis=1)
            target_feature_train_data = train_data[target_column]
            logging.info('Splitting test data into independent and dependent data')
            input_feature_test_data = test_data.drop(columns=drop_column,axis=1)
            target_feature_test_data = test_data[target_column]
            logging.info('Data transformation started')
            input_train_arr = preprocessor.fit_transform(input_feature_train_data)
            input_test_arr = preprocessor.transform(input_feature_test_data)
            logging.info('Concatenation transform data with target feature')
            train_arr = np.c_[input_train_arr,np.array(target_feature_train_data)] 
            test_arr = np.c_[input_test_arr,np.array(target_feature_test_data)]
            save_object(file_path=self.data_transformation_config.preprocessor_file,
                        obj=preprocessor)
            logging.info('Data transformation completed')
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_file
            )
            
        except Exception as e:
            raise CustomException(e,sys)