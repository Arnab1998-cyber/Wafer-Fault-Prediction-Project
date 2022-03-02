import os.path

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from model_file_operation import file_operation
from logger import logger
from preprocessing_for_training import get_data


class k_means_clustering:
    def __init__(self, data):
        self.log=logger()
        self.data=data
        self.data_label="Output"
        self.pre_process=get_data()
        self.file=file_operation()


    def elbow_plot(self):
        wcss=[]
        try:
            for i in range(1,11):
                kmeans=KMeans(n_clusters=i, random_state=42)
                kmeans.fit(self.data)
                wcss.append(kmeans.inertia_)
            plt.plot(range(1,11), wcss)
            plt.title('elbow plot')
            plt.xlabel('number of clusters')
            plt.ylabel('WCSS')
            if not os.path.isdir('preprocessing_data'):
                os.mkdir('preprocessing_data')
            plt.savefig('preprocessing_data/K-Means_Elbow.PNG')
            self.kn=KneeLocator(range(1,11), wcss,curve='convex', direction='decreasing')
            self.log.apply_log("Training_Logs/Genarel_log.txt",msg='successfully created {} number of clusters'.format(self.kn.knee))
            return self.kn.knee
        except Exception as e:
            raise e

    def create_clusters(self,no_of_cluster):
        clusters=no_of_cluster
        self.kmeans=KMeans(n_clusters=clusters,random_state=42)
        self.y_kmeans=self.kmeans.fit_predict(self.data)
        self.file.save_cluster_model(model=self.kmeans)
        self.log.apply_log("Training_Logs/Genarel_log.txt",msg='clustering model saved in file')
        new_df=self.pre_process.integrate_column_in_data(data=self.data, col_name='cluster',column=self.y_kmeans)
        self.log.apply_log("Training_Logs/Genarel_log.txt",msg='clusters of data created')
        return new_df,self.kmeans