from preprocessing_for_prediction import get_data
from model_file_operation import file_operation
from prediction_raw_data_validation import raw_data_validation
from DB_Operation_prediction import db_operation
from logger import logger
import os
import shutil
import pandas as pd
import json

class prediction:
    def __init__(self,prediction_files):
        self.prediction_files=prediction_files
        if os.path.isdir('Prediction_Logs/'):
            shutil.rmtree('Prediction_Logs/')
        self.log_file='Prediction_Logs/Genarel_log.txt'
        if not os.path.isdir('Prediction_Logs/'):
            os.mkdir('Prediction_Logs/')
        self.log=logger()
        self.file=file_operation()
        self.raw_data=raw_data_validation(path=self.prediction_files)
        self.db=db_operation()
        self.data=get_data()

    def get_prediction(self,columns_to_drop):
        try:
            #a,b,c,d,e=self.raw_data.values_from_schema()
            #regex=self.raw_data.manual_regex_creation()
            #self.raw_data.validation_name_raw(regex=regex,length_of_date=b,length_of_time=c)
            #self.raw_data.validation_col_length_raw(col_length=d)
            #self.raw_data.check_null_column()
            #conn=self.db.data_base_connection(database_name='prediction')
            #self.db.create_table(database_name='prediction',column_name=e)
            #self.db.replace_missing_values_with_null()
            #self.db.insert_good_data_into_table(database='prediction')
            #self.db.upload_data_from_table_into_final_csv(database='prediction')
            df=self.data.data()
            df=self.data.impute_missing_values(data=df)[0]
            df=self.data.remove_col(data=df,col_name=columns_to_drop)
            kmeans=self.file.load_cluster_model()
            df_without_wafer=self.data.remove_col(data=df,col_name='Wafer')
            cluster=kmeans.predict(df_without_wafer)
            df_with_cluster=self.data.integrate_column_in_data(data=df,col_name='cluster',column=cluster)
            l=list(df_with_cluster['cluster'].unique())
            l.sort()
            count=0
            if os.path.isdir('prediction_output_files'):
                shutil.rmtree('prediction_output_files')
            os.mkdir('prediction_output_files')
            for i in l:
                df2=df_with_cluster[df_with_cluster['cluster']==i]
                df2_without_cluster=self.data.remove_col(data=df2,col_name='cluster')
                df2_without_cluster_wafer=self.data.remove_col(data=df2_without_cluster,col_name='Wafer')
                wafer=df2['Wafer']
                model=self.file.find_correct_model_for_cluster(cluster_number=i)[1]
                y=model.predict(df2_without_cluster_wafer)
                df3=self.data.integrate_column_in_data(data=df2_without_cluster,col_name='Output',column=y)
                df3.to_csv('prediction_output_files/wafer_fault_result_cluster{}.csv'.format(i))
                if count==0:
                    df3.to_csv('prediction_output_files/wafer_fault_final_result.csv',mode='a+')
                    count=count+1
                else:
                    df3.to_csv('prediction_output_files/wafer_fault_final_result.csv',mode='a+',header=False)
            new_df=pd.read_csv('prediction_output_files/wafer_fault_final_result.csv')
            result=pd.DataFrame(new_df[['Wafer','Output']],columns=['Wafer','Output'])
            self.log.apply_log('Prediction_Logs/Genarel_log.txt','predicted value inserted to csv file')
            outcome_path='prediction_output_files/wafer_fault_final_result.csv'
            return result.head().to_json(orient='records'), outcome_path
        except Exception as e:
            raise e




