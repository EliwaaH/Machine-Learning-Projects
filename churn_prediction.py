# -*- coding: utf-8 -*-
"""Churn Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZKTNL2D3PlkqHh0TE4FJVgdiwsw6MO5s
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = 'https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-03-churn-prediction/WA_Fn-UseC_-Telco-Customer-Churn.csv'

!wget $data -O data-week-3.csv

df = pd.read_csv('data-week-3.csv')
df.head()

df.columns = df.columns.str.lower().str.replace(' ', '_')

categroical_columns = list(df.dtypes[df.dtypes == 'object'].index)

for c in categroical_columns:
  df[c] = df[c].str.lower().str.replace(' ', '_')

df.head().T

df.dtypes

df.totalcharges = pd.to_numeric(df.totalcharges, errors = 'coerce')
df.totalcharges

df.totalcharges = df.totalcharges.fillna(0)

df.churn = (df.churn == 'yes').astype(int)

df.churn

from sklearn.model_selection import train_test_split

full_train , test = train_test_split(df, test_size = 0.2, random_state = 1)

train , val  = train_test_split(full_train, test_size = 0.25, random_state= 1)

len(train), len(val), len(test)

full_train = full_train.reset_index(drop = True)
train = train.reset_index(drop = True)
test = test.reset_index(drop = True)
val = val.reset_index(drop = True)

y_train = train['churn'].values
y_val = val['churn'].values
y_test = test['churn'].values

del train['churn']
del test['churn']
del val['churn']

len(y_train), len(y_val), len(y_test)

full_train.isnull().sum()

full_train.churn.value_counts(normalize = True)

full_train.columns

categorical =['gender', 'seniorcitizen', 'partner', 'dependents',
       'phoneservice', 'multiplelines', 'internetservice',
       'onlinesecurity', 'onlinebackup', 'deviceprotection', 'techsupport',
       'streamingtv', 'streamingmovies', 'contract', 'paperlessbilling',
       'paymentmethod']

numerical  = ['tenure', 'totalcharges', 'monthlycharges']

from IPython.display import display
for c in categorical:
  print(c)
  df_group = full_train.groupby(c).churn.agg(['mean', 'count'])
  df_group['diff'] = df_group['mean'] - full_train['churn'].mean()
  df_group['risk'] = df_group['mean'] / full_train['churn'].mean()
  display(df_group)
  print()
  print()

from sklearn.metrics import mutual_info_score

def mutual_info_scroe_fun(series):
  
  return mutual_info_score(series, full_train.churn)

muti = full_train[categorical].apply(mutual_info_scroe_fun)
muti.sort_values(ascending = False)

full_train[numerical].corrwith(full_train.churn).abs()

from sklearn.feature_extraction import DictVectorizer

dv = DictVectorizer(sparse = False)

train_dict = train[categorical + numerical].to_dict(orient = 'records')
X_train = dv.fit_transform(train_dict)

val_dict = val[categorical + numerical].to_dict(orient='records')
X_val = dv.transform(val_dict)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(solver='lbfgs')
model.fit(X_train, y_train)

model.intercept_[0]

model.coef_[0].round(3)

y_pred = model.predict_proba(X_val)[:, 1]

churn_decision = (y_pred >= 0.5)

(y_val == churn_decision).mean()

dict(zip(dv.get_feature_names(), model.coef_[0].round(3)))

full_train_dict = full_train[categorical + numerical].to_dict(orient = 'records')
X_full_train = dv.fit_transform(full_train_dict)

y_full_train = full_train.churn.values

full_model = LogisticRegression(solver = 'lbfgs')
full_model.fit(X_full_train, y_full_train)

dict_test = test[categorical + numerical].to_dict(orient = 'records')
X_test = dv.transform(dict_test)

y_full_pred = full_model.predict_proba(X_test)[:, 1]

churn_decision = (y_full_pred >= 0.5)

(y_test == churn_decision).mean()

customer = dict_test[470]
customer

customer_test = dv.transform(customer)

full_model.predict_proba(customer_test)[0,1]

y_test[470]

for i in range(100):
  print(test.customerid[i])
  customer_id = dict_test[i]
  customer_id_test = dv.transform([customer_id])
  predicition = full_model.predict_proba(customer_id_test)[0,1]
  print(y_test[i])
  print(predicition)
  #dis = pd.DataFrame()
  #dis['predicition'] = predicition
  #dis['Real'] = y_test[i]
  #display(dis)
  print()
  print()