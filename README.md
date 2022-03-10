# Wafer Fault Prediction


## Overview
This is a flask app based project, which predicts, based on the signals of a wafer, the wafer is good or bad.
Good for +1 and bad for -1.

## Problem statement
It is not possible to check all the wafer manually. So we build a system where based on the signals, we can know which wafer is good or bad, and we can act accordingly.

## Technologies:
Sklearn, Pandas, Matplotlib

## Database:
MySql

## Data Visualization:
Vizualise the data using principal component analysis, on 2 features.
#### tools:
Matplotlib, Seaborn

## Algorithms
#### Missing Values: 
KNN Imputer
#### Clustering:
K-Means Clustering
#### Prediction:
Random Forest, Support Vector Machine


## Description

we are given a set of csv files with vaarious wafer data for training purpose. But here is a problem.
In that data many descrepencies can be found. For that reason we first created a training pipeline which includes data validation process.
In validation stage we check the naming convension of each files, check whether there is any null column, number of columns. Based on these, the given training data goes to good or bad csv files.

The Good files are integrated and we dump that data into mysql database. Now this data is ready for training our machine learning model.

First we clustered the data and for each cluster we use a machine learning model. As we know model performs well when variation in the dataset is less.

Now we have Prediction files also. We first send those files for validation, and divide them into good and bad csv files.
The good data is dumped into database and from there we create a csv file. The csv file is goes into the cluster model, we saved after training. After dividing the data into clusters, each cluster goes into the specific model, we specified for that cluster.
We create output files with prediction.
