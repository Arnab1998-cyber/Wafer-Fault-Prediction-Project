from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from logger import logger
from preprocessing_for_training import get_data


class get_model:
    def __init__(self, data):
        self.df=data
        self.rf=RandomForestClassifier()
        self.svm=SVC()
        self.lg=LogisticRegression()
        self.get_data=get_data()
        self.x,self.y=self.get_data.separate_label_feature(self.df,'Output')
        self.train_x,self.test_x,self.train_y,self.test_y=train_test_split(self.x,self.y,test_size=0.2,random_state=42)
        self.log=logger()

    def get_best_param_for_random_forest(self):
        param_grid={"n_estimators": [10, 50, 100], "criterion": ['gini', 'entropy'],
                               "max_depth": range(2, 4)}
        grid=GridSearchCV(estimator=self.rf, param_grid=param_grid, cv=5)
        grid.fit(self.train_x,self.train_y)
        n_estimators=grid.best_params_['n_estimators']
        criterion=grid.best_params_['criterion']
        max_depth=grid.best_params_['max_depth']
        self.rf=RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth)
        self.rf.fit(self.train_x,self.train_y)
        self.log.apply_log('Training_Logs/Genarel_log.txt',msg='random forest model get trained')
        print('rf')
        return self.rf
    def get_best_param_for_svc(self):
        param_grid=grid={'gamma':['scale', 'auto',.001,.02,.1]}
        grid=GridSearchCV(estimator=self.svm, param_grid=param_grid,cv=5)
        grid.fit(self.train_x,self.train_y)
        gamma=grid.best_params_['gamma']
        self.svm=SVC(gamma=gamma, decision_function_shape='ovo')
        self.svm.fit(self.train_x,self.train_y)
        self.log.apply_log("Training_Logs/Genarel_log.txt",msg='svm model get trained')
        print('svm')
        return self.svm
    def get_best_param_for_logistic(self):
        param_grid={'penalty':['l2']}
        grid=GridSearchCV(estimator=self.lg,param_grid=param_grid, cv=5)
        grid.fit(self.train_x,self.train_y)
        penalty=grid.best_params_['penalty']
        self.lg=LogisticRegression(penalty)
        self.lg.fit(self.train_x,self.train_y)
        self.log.apply_log('Training_Logs/Genarel_log.txt',msg='logistic regression model got trained')
        print('lg')
        return self.lg

    def get_best_model(self):
         rf=self.get_best_param_for_random_forest()
         pred_rf=rf.predict(self.test_x)
         accuracy_score_rf=accuracy_score(self.test_y,pred_rf)
         svm=self.get_best_param_for_svc()
         pred_svm=svm.predict(self.test_x)
         accuracy_score_svm=accuracy_score(self.test_y,pred_svm)
         l=[accuracy_score_rf,accuracy_score_svm]
         m=max(l)
         i=l.index(m)
         if i==0:
             self.log.apply_log('Training_Logs/Genarel_log.txt', msg='best model random forest classifier founded')
             return accuracy_score_rf,rf
         if i==1:
             self.log.apply_log('Training_Logs/Genarel_log.txt', msg='best model support vector machine founded')
             return accuracy_score_svm,svm




