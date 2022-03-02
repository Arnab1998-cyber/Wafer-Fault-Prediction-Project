import pickle
import os
import shutil
from logger import logger

class file_operation:
    def __init__(self):
        self.model_directory='models/'
        self.impute_model_directory='impute_models/'
        self.cluster_model_directory='cluster_models/'
        self.log=logger()

    def save_model(self, model,file_name):
        try:
            path=os.path.join(self.model_directory+file_name)
            if not os.path.isdir(self.model_directory):
                os.mkdir(self.model_directory)
            with open(path+'.pkl', 'wb') as f:
                pickle.dump(model,f)
            self.log.apply_log('Training_Logs/Genarel_log.txt','the model saved into file {}'.format(file_name))
        except Exception as e:
            raise e

    def save_impute_model(self,model,file_name='knn_imputer'):
        try:
            path=os.path.join(self.impute_model_directory+file_name)
            if os.path.isdir(self.impute_model_directory):
                shutil.rmtree(self.impute_model_directory)
            os.mkdir(self.impute_model_directory)
            with open(path+'.pkl', 'wb') as f:
                pickle.dump(model,f)
            self.log.apply_log('Training_Logs/Genarel_log.txt','the impute model saved into file {}'.format(file_name))
        except Exception as e:
            raise e

    def save_cluster_model(self,model,file_name='kmeans_clustering'):
        try:
            path=os.path.join(self.cluster_model_directory+file_name)
            if os.path.isdir(self.cluster_model_directory):
                shutil.rmtree(self.cluster_model_directory)
            os.mkdir(self.cluster_model_directory)
            with open(path+'.pkl', 'wb') as f:
                pickle.dump(model,f)
            self.log.apply_log('Training_Logs/Genarel_log.txt','the cluster model saved into file {}'.format(file_name))
        except Exception as e:
            raise e

    def load_model(self,file_name):
        try:
            with open(self.model_directory+file_name+'.pkl', 'rb') as f:
                self.log.apply_log('Training_Logs/Genarel_log.txt','saved model loaded')
                return pickle.load(f)
        except Exception as e:
            self.log.apply_log('Training_Logs/Genarel_log.txt','get trouble in loading model')

    def load_impute_model(self,file_name='knn_imputer'):
        try:
            with open(self.impute_model_directory+file_name+'.pkl', 'rb') as f:
                self.log.apply_log('Training_Logs/Genarel_log.txt','saved impute model loaded')
                return pickle.load(f)
        except Exception as e:
            self.log.apply_log('Training_Logs/Genarel_log.txt','get trouble in loading imputation model')


    def load_cluster_model(self,file_name='kmeans_clustering'):
        try:
            with open(self.cluster_model_directory+file_name+'.pkl', 'rb') as f:
                self.log.apply_log('Training_Logs/Genarel_log.txt','saved cluster model loaded')
                return pickle.load(f)
        except Exception as e:
            self.log.apply_log('Training_Logs/Genarel_log.txt','get trouble in loading clustering model')


    def find_correct_model_for_cluster(self,cluster_number):
        list_of_model=os.listdir(self.model_directory)
        print(len(list_of_model))
        for i in range(len(list_of_model)):
            if i==cluster_number:
                self.model_name=list_of_model[i]
                print(self.model_name)
                f=open(self.model_directory+self.model_name, 'rb')
                model=pickle.load(f)
                self.model_name = self.model_name.split('.')[0]
                self.log.apply_log('Training_logs/Genarel_log.txt',
                                   'correct model found for cluster number {}'.format(cluster_number))
                return self.model_name, model





