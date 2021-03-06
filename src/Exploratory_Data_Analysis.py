# *coding=utf-8*
 
import statsmodels.api as sm

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import model_selection, preprocessing
import xgboost as xgb
import datetime
import scipy as sp
#import missingno as msno
from scipy.stats import mode

 
# Read data
macro = pd.read_csv('../input/macro.csv')
train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')

print(mode(train['num_room']))

train['area_km']=train['area_m']/1000000
train['desity']=train['raion_popul']/train['area_km']

print(train['full_sq'].unique())
print(train['full_sq'].describe())

# bad_index = train[train.sub_area =='Poselenie Krasnopahorskoe'].index
# print(mode(train.ix[bad_index,'build_year']).mode[0])
# print(train.ix[11271])
# print(train.ix[19127])


#查询price的分布,找出outliners
plt.figure(figsize=(8,6))
plt.scatter(range(train.shape[0]), np.sort(train.price_doc.values))
plt.xlabel('index', fontsize=12)
plt.ylabel('price', fontsize=12)
plt.show()


#查询缺失值
missing_df = train.isnull().sum(axis=0).reset_index()
missing_df.columns = ['column_name', 'missing_count']
missing_df = missing_df.ix[missing_df['missing_count']>0]
ind = np.arange(missing_df.shape[0])
width = 0.9
fig, ax = plt.subplots(figsize=(12,18))
rects = ax.barh(ind, missing_df.missing_count.values, color='y')
ax.set_yticks(ind)
ax.set_yticklabels(missing_df.column_name.values, rotation='horizontal')
ax.set_xlabel("Count of missing values")
ax.set_title("Number of missing values in each column")
plt.show()


#箱形图显示floor和price
fig,ax= plt.subplots()
fig.set_size_inches(20,8)
sns.boxplot(x="floor", y="price_doc", data=train,ax=ax)
ax.set(ylabel='Price Doc',xlabel="Floor",title="Floor Vs Price Doc")
plt.show()

##找出各个floor number的数量
plt.figure(figsize=(12,8))
sns.countplot(x="floor", data=train)
plt.ylabel('Count', fontsize=12)
plt.xlabel('floor number', fontsize=12)
plt.xticks(rotation='vertical')
plt.show()


#correlation matrix
train['market_shop']=1/train['market_shop_km']
train['old']=2018-train['build_year']

#热点图找出特征的关联度
sns.heatmap(train[['area_m' ,'desity','raion_popul','sport_objects_raion','park_km','big_market_km','market_shop_km','market_shop','old',
                  'price_doc']].corr(),annot=True)

plt.show()
