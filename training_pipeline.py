from training_raw_data_validation import raw_data_validation
from DB_Operation_training import db_operation
from get_model_training import get_model
from preprocessing_for_training import get_data
from model_file_operation import file_operation
from clustering_training_data import k_means_clustering
from logger import logger
import os
import shutil

class training_pipeline:
    def __init__(self,training_files):
        self.training_files=training_files
        self.label = "Output"
        self.log=logger()
        if os.path.isdir('Training_Logs/'):
            shutil.rmtree('Training_Logs')
        self.log_file='Training_Logs/Genarel_log.txt'
        if not os.path.isdir('Training_Logs/'):
            os.mkdir('Training_Logs/')
        self.file_op=file_operation()
        self.raw_data = raw_data_validation(self.training_files)
        self.db=db_operation()
        self.data=get_data()

    def trainig_pipeline(self):
        try:
            #a,b,c,d,e=self.raw_data.values_from_schema()
            #regex=self.raw_data.manual_regex_creation()
            #self.raw_data.create_folder_good_bad_data()
            #self.raw_data.validation_name_raw(regex=regex,length_of_date=b,length_of_time=c)
            #self.raw_data.validation_col_length_raw(col_length=d)
            #self.raw_data.check_null_column()
            #conn=self.db.data_base_connection(database_name='training')
            #self.db.create_table(database_name='training',column_name=e)
            #self.db.replace_missing_values_with_null()
            #self.db.insert_good_data_into_table(database='training')
            #self.db.upload_data_from_table_into_final_csv(database='training')
            df=self.data.data()
            df_without_label,label=self.data.separate_label_feature(data=df,label_col=self.label)
            df_without_label=self.data.impute_missing_values(df_without_label)[0]
            columns_to_drop=self.data.get_columns_with_zero_standered_deviation(df_without_label)
            df_without_label=self.data.remove_col(data=df_without_label, col_name=columns_to_drop)
            df_without_label_wafer,wafer=self.data.separate_label_feature(data=df_without_label,label_col='Wafer')
            kmeans=k_means_clustering(data=df_without_label_wafer)
            number_of_clusters=kmeans.elbow_plot()
            df_without_label_wafer_with_cluster,kmean_model=kmeans.create_clusters(no_of_cluster=number_of_clusters)
            list_of_clusters=list(df_without_label_wafer_with_cluster['cluster'].unique())
            list_of_clusters.sort()
            new_df=self.data.integrate_column_in_data(data=df_without_label_wafer_with_cluster,col_name=self.label,column=label)
            for i in list_of_clusters:
                clustered_data=new_df[new_df['cluster']==i] #without wafer column, with cluster and label column
                clustered_dataframe=self.data.separate_label_feature(data=clustered_data,label_col='cluster')[0]
                training=get_model(clustered_dataframe) # without cluster
                accurecy_score=training.get_best_model()[0]
                print(accurecy_score)
                model=training.get_best_model()[1]
                self.file_op.save_model(model=model,file_name='model_cluster_{}'.format(i))
            self.log.apply_log(self.log_file,'successfully trained model saved')
            return columns_to_drop
        except Exception as e:
            self.log.apply_log(self.log_file,'model training unseccessfull')
            raise e

