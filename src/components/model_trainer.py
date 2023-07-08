import os 
import sys
import pandas as pd 
import numpy as np
from dataclasses import dataclass

from constant import *
from src.exceptions import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_model,read_yaml

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

@dataclass
class ModelTrainerConfig:
    artifact_folder = os.path.join('artifacts')
    trained_model = os.path.join(artifact_folder,'model.pkl')
    expected_accuracy = 0.6
    model_config_file_path = os.path.join('config','model.yaml')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_initiate = ModelTrainerConfig()


    def hyper_parameter_tunning(self,best_model_obj:object,best_model_name,X_train,y_train)->object:
        '''
            Desc: This function will responsible for hyperparameter tunning
        '''
        try:
            model_params_grid = read_yaml(file_path=self.model_trainer_initiate.model_config_file_path)['models'][best_model_name]['hyperparameters']
            logging.info('Hyper parameter tuning started for model training')
            if best_model_name == 'logistic':
            # Specify the solvers that support 'l1' penalty for logistic regression
                solvers = ['liblinear', 'saga']
                model_params_grid['solver'] = solvers
            grid_search = GridSearchCV(best_model_obj,param_grid=model_params_grid,cv=5,n_jobs=-1,verbose=1,error_score='raise')
            grid_search.fit(X_train,y_train)
            # To get best model
            best_params = grid_search.best_params_
            logging.info(f'We got the best params: {best_params} for model {grid_search.best_estimator_}')
            finetuned_model = best_model_obj.set_params(**best_params)
            return finetuned_model
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            X_train,y_train,X_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models = {
                        'logistic': LogisticRegression(),
                        'svc': SVC(),
                        'knn': KNeighborsClassifier(),
                        'kernel_svm': SVC(kernel='rbf'),
                        'naive_bayes': GaussianNB(),
                        'dt': DecisionTreeClassifier(),
                        'random_forest': RandomForestClassifier()
                    }
            
            model_report:dict = evaluate_model(
                                            X_train=X_train,X_test=X_test,
                                            y_train=y_train,y_test=y_test,
                                            models=models
                                            )
            # To get best model from model_report
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(models.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            best_model = self.hyper_parameter_tunning(
                best_model_name=best_model_name,
                best_model_obj=best_model,
                X_train=X_train,
                y_train=y_train
            )
            best_model.fit(X_train,y_train)
            # predicting
            y_pred = best_model.predict(X_test)
            best_model_score = accuracy_score(y_test,y_pred)
            logging.info(f'Best model found: {best_model_name} with accuracy score: {best_model_score}')
            if best_model_score < self.model_trainer_initiate.expected_accuracy:
                raise Exception('No model found with accuracy greater than threshold 0.6')
            logging.info('Saving model.....')
            save_object(
                file_path=self.model_trainer_initiate.trained_model,
                obj=best_model
            )
            return self.model_trainer_initiate.trained_model
        except Exception as e:
            raise CustomException(e,sys)




    