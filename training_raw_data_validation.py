import os
import shutil
import json
import pandas as pd
import re
from datetime import datetime
from logger import logger

class raw_data_validation:
    def __init__(self,path):
        self.raw_folder_path=path
        self.schema_path='schema_training.json'
        self.log=logger()

    def values_from_schema(self):
        try:
            f=open(self.schema_path, 'r')
            d=json.load(f)
            f.close()
            pattern=d["SampleFileName"]
            date=d["LengthOfDateStampInFile"]
            time=d["LengthOfTimeStampInFile"]
            number_of_col=d["NumberofColumns"]
            column_name=d["ColName"]
            msg='important information about our data loaded for checking'
            if not os.path.isdir('Training_Logs/'):
                os.makedirs('Training_Logs/')
            self.log.apply_log("Training_Logs/Genarel_log.txt", msg=msg)
            return pattern,date,time,number_of_col,column_name
        except Exception as e:
               raise e

    def manual_regex_creation(self):
        try:
            regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
            msg='regular expression created for checking file name'
            if not os.path.isdir('Training_Logs/'):
                os.makedirs('Training_Logs/')
            self.log.apply_log("Training_Logs/Genarel_log.txt",msg=msg)
            return regex
        except Exception as e:
               raise e

    def delete_existing_good_data_training_folder(self):
        try:
            path='Training_raw_checking_file/'
            if os.path.isdir(path+'good_csv_files'):
                shutil.rmtree(path+'good_csv_files')
                msg='deleted existing good data csv files'
                if not os.path.isdir('Training_Logs/'):
                    os.makedirs('Training_Logs/')
                self.log.apply_log("Training_Logs/Genarel_log.txt", msg=msg)
            else:
                msg='no previous prediction, so no existing good csv file'
                if not os.path.isdir('Training_Logs/'):
                    os.makedirs('Training_Logs/')
                self.log.apply_log("Training_Logs/Genarel_log.txt", msg=msg)
        except Exception as e:
               raise e


    def delete_existing_bad_data_training_folder(self):
        try:
           path = 'Training_raw_checking_file/'
           if os.path.isdir(path + 'bad_csv_files'):
               shutil.rmtree(path + 'bad_csv_files')
               msg = 'deleted existing bad data csv files'
               if not os.path.isdir('Training_Logs/'):
                   os.makedirs('Training_Logs/')
               self.log.apply_log("Training_Logs/Genarel_log.txt",msg=msg)
           else:
               msg = 'no previous prediction, so no existing bad csv file'
               if not os.path.isdir('Training_Logs/'):
                   os.makedirs('Training_Logs/')
               self.log.apply_log("Training_Logs/Genarel_log.txt",msg=msg)
        except Exception as e:
            raise e

    def create_folder_good_bad_data(self):
       try:
            path=os.path.join('Training_raw_checking_file/','good_csv_files/')
            if not os.path.isdir(path):
                os.makedirs(path)
            path=os.path.join('Training_raw_checking_file/','bad_csv_files/')
            if not os.path.isdir(path):
                os.makedirs(path)
            msg='directory for good csv files and bad csv files created'
            if not os.path.isdir('Training_Logs/'):
                os.makedirs('Training_Logs/')
            self.log.apply_log("Training_Logs/Genarel_log.txt",msg=msg)
       except Exception as e:
           raise e

    def move_bad_files_to_archive(self):
        now=datetime.now()
        date=now.date()
        time=now.strftime('%H:%M:%S')
        try:
            source="Training_raw_checking_file/bad_csv_files/"
            if os.path.isdir(source):
                path='Training_archive_bad_data'
                if not os.path.isdir(path):
                    os.makedirs(path)
                dest='Training_archive_bad_data/bad_data_'+str(date)+' :: '+str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files=os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source+f,dest)
                self.log.apply_log("Training_Logs/Genarel_log.txt",msg="bad csv files moved to archive")
                if os.path.isdir(source):
                    os.removedirs(source)
                self.log.apply_log("Training_Logs/Genarel_log.txt",msg='bad csv files folder removed')
        except Exception as e:
            raise e


    def validation_name_raw(self, regex, length_of_date,length_of_time):
        self.log.apply_log("Training_Logs/Genarel_log.txt", msg='name pattern validation started')
        self.delete_existing_good_data_training_folder()
        self.delete_existing_bad_data_training_folder()
        self.create_folder_good_bad_data()
        print(self.raw_folder_path)
        l=[f for f in os.listdir(self.raw_folder_path)]
        print(l)
        for file in l:
            if re.match(regex,file):
                l1=re.split('.csv',file)
                l1=re.split('_',l1[0])
                if len(l1)==3 and len(l1[0])==5:
                    if len(l1[1])==length_of_date:
                        if len(l1[2])==length_of_time:
                            shutil.copy('Training_Batch_Files/'+file,'Training_raw_checking_file/good_csv_files')
                            self.log.apply_log("Training_Logs/Genarel_log.txt",msg='{} copied into good folder'.format(file))
                        else:
                             shutil.copy('Training_Batch_Files/' + file, 'Training_raw_checking_file/bad_csv_files')
                             self.log.apply_log("Training_Logs/Genarel_log.txt",msg='{} copied into bad folder'.format(file))
                    else:
                        shutil.copy('Training_Batch_Files/' + file, 'Training_raw_checking_file/bad_csv_files')
                        self.log.apply_log("Training_Logs/Genarel_log.txt",msg='{} copied into bad folder'.format(file))
                else:
                    shutil.copy('Training_Batch_Files/' + file, 'Training_raw_checking_file/bad_csv_files')
                    self.log.apply_log("Training_Logs/Genarel_log.txt",msg='{} copied into bad folder'.format(file))

    def validation_col_length_raw(self, col_length):
        try:
            self.good_data_path='Training_raw_checking_file/good_csv_files'
            self.log.apply_log("Training_Logs/Genarel_log.txt", msg='column length validation started')
            for f in os.listdir(self.good_data_path):
                df=pd.read_csv(self.good_data_path+'/'+f)
                if df.shape[1]==col_length:
                    pass
                else:
                    shutil.move('Training_raw_checking_file/good_csv_files/'+f, 'Training_raw_checking_file/bad_csv_files')
                    self.log.apply_log("Training_Logs/Genarel_log.txt",msg='{} copied to bad folder'.format(f))
        except Exception as e:
            raise e

    def check_null_column(self):
        try:
            self.log.apply_log("Training_Logs/Genarel_log.txt", msg='null column validation started')
            for f in os.listdir(self.good_data_path):
                count=0
                df=pd.read_csv(self.good_data_path+'/'+f)
                for i in df:
                    if df[i].count()==0:
                        shutil.move(self.good_data_path+'/'+f,'Training_raw_checking_file/bad_csv_files')
                        self.log.apply_log("Training_Logs/Genarel_log.txt",msg='{} copied to bad folder'.format(f))
                        count=count+1
                        break
                if count==0:
                    df.rename(columns={"Unnamed: 0": "Wafer"},inplace=True)
                    df.to_csv('Training_raw_checking_file/good_csv_files/'+f, index=None,header=True)
        except Exception as e:
            raise e

    def data_type_validation(self):
         try:
             self.log.apply_log("Training_Logs/Genarel_log.txt", msg='data type validation started')
             for f in os.listdir(self.good_data_path):
                 df=pd.read_csv(self.good_data_path+'/'+f)
                 if df.dtypes.iloc[0]!='object':
                    shutil.move(self.good_data_path+'/'+f,'Training_raw_checking_file/bad_csv_files')
                    self.log.apply_log("Training_Logs/Genarel_log.txt", msg='{} copied to bad folder'.format(f))
                 for i in range(1,len(df.dtypes)-1):
                    if df.dtypes.iloc[i] not in ['float','float64','float32','float16']:
                        shutil.move(self.good_data_path+'/' + f, 'Training_raw_checking_file/bad_csv_files')
                        self.log.apply_log("Training_Logs/Genarel_log.txt", msg='{} copied to bad folder'.format(f))
                 if df.dtypes.iloc[-1] not in ['int','int64','int32','int16']:
                    shutil.move('Training_raw_checking_file/good_csv_files' + f, 'Training_raw_checking_file/bad_csv_files')
                    self.log.apply_log("Training_Logs/Genarel_log.txt", msg='{} copied to bad folder'.format(f))
         except Exception as e:
            raise e

