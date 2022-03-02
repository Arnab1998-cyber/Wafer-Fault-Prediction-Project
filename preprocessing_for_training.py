import numpy as np
import pandas as pd
from logger import logger
from sklearn.impute import KNNImputer
from model_file_operation import file_operation
import os

class get_data:
    def __init__(self):
        self.data_path='training_file_from_db/input_file.csv'
        self.log=logger()
        self.file=file_operation()


    def data(self):
        try:
            df=pd.read_csv(self.data_path)
            print(df)
            self.log.apply_log(file_name='Training_Logs/Genarel_log.txt',msg='data get loaded from csv file to pandas dataframe')
            return df
        except Exception as e:
            self.log.apply_log(file_name='Training_Logs/Genarel_log.txt',msg='cannot load data')
            raise e

    def remove_col(self,data,col_name):
        df=data
        df1=df.drop(columns=col_name)
        self.log.apply_log(file_name='Training_Logs/Genarel_log.txt',msg='deleted unnecessarry columns')
        return df1

    def separate_label_feature(self,data,label_col):
        df=data
        x=df.drop(columns=label_col)
        y=df[label_col]
        self.log.apply_log(file_name='Training_Logs/Genarel_log.txt',msg='{} column get separated'.format(label_col))
        return x,y

    def impute_missing_values(self, data):
        df=data
        count=0
        df.replace(to_replace='NULL',value=np.nan,inplace=True)
        self.log.apply_log(file_name='Training_Logs/Genarel_log.txt',msg='again replace "NULL" with NaN in dataframe')
        knn=KNNImputer(n_neighbors=5,weights='distance')
        new_array=knn.fit_transform(df)
        new_data=pd.DataFrame(new_array, columns=df.columns)
        self.log.apply_log(file_name='Training_Logs/Genarel_log.txt',msg='handeled missing values by knn imputer')
        self.file.save_impute_model(model=knn)
        self.log.apply_log(file_name='Training_Logs/Genarel_log.txt',msg='impute knn model saved into file')
        return new_data,knn

    def get_columns_with_zero_standered_deviation(self, data):
        df=data
        self.columns_to_drop=[]
        l=df.describe()
        for i in df.columns:
            if l[i]['std']==0:
                self.columns_to_drop.append(i)
        self.log.apply_log(file_name='Training_Logs/Genarel_log.txt',msg='got columns with zero deviation')
        return self.columns_to_drop

    def integrate_column_in_data(self,data, col_name,column):
        df=data
        df[col_name]=column
        self.log.apply_log('Training_Logs/Genarel_log.txt',msg='{} column integrated with data'.format(col_name))
        return df





