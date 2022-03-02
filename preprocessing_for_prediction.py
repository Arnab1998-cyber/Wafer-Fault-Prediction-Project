import os.path
import shutil

import numpy as np
import pandas as pd
from logger import logger
from sklearn.impute import KNNImputer
from model_file_operation import file_operation

class get_data:
    def __init__(self):
        self.data_path='prediction_file_from_db/input_file.csv'
        self.log=logger()
        self.file=file_operation()
        self.impute_model='knn_imputer'


    def data(self):
        try:
            df=pd.read_csv(self.data_path)
            self.log.apply_log(file_name='Prediction_Logs/Genarel_log.txt',msg='data get loaded from csv file to pandas dataframe')
            return df
        except Exception as e:
            self.log.apply_log(file_name='Prediction_Logs/Genarel_log.txt',msg='cannot load data')
            if not os.path.isdir('Prediction_Logs/Genarel_log.txt'):
                os.makedirs('Prediction_Logs/')
            raise e

    def remove_col(self,data,col_name):
        df=data
        df1=df.drop(columns=col_name)

        self.log.apply_log(file_name='Prediction_Logs/Genarel_log.txt',msg='deleted unnecessarry columns')
        return df1



    def impute_missing_values(self, data):
        df=data
        df.replace(to_replace='NULL',value=np.nan,inplace=True)
        self.log.apply_log(file_name='Prediction_Logs/Genarel_log.txt',msg='again replace "NULL" with NaN in dataframe')
        knn=self.file.load_impute_model()
        new_array=knn.transform(df)
        new_data=pd.DataFrame(new_array, columns=df.columns)
        self.log.apply_log(file_name='Prediction_Logs/Genarel_log.txt',msg='handeled missing values by knn imputer')
        return new_data,knn

    def get_columns_with_zero_standered_deviation(self, data):
        df=data
        self.columns_to_drop=[]
        l=df.describe()
        for i in df.columns:
            if l[i]['std']==0:
                self.columns_to_drop.append(i)
        self.log.apply_log(file_name='Prediction_Logs/Genarel_log.txt',msg='got columns with zero deviation')
        return self.columns_to_drop

    def integrate_column_in_data(self,data, col_name,column):
        df=data
        df[col_name]=column
        self.log.apply_log('Prediction_Logs/Genarel_log.txt',msg='{} column integrated with data'.format(col_name))
        return df

