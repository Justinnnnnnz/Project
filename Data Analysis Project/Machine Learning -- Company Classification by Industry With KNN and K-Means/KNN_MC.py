# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 21:32:49 2021
"""

import pandas as pd
df=pd.read_csv('constituents-financials_csv.csv')

df = df.dropna(axis=0)
df['volatility']=df['52 Week High']-df['52 Week Low']

y = df[["Sector"]]
features1=df.drop(['Symbol','Sector'],axis=1)
features2=df[['Price/Earnings','Price/Sales','Price/Book']] #Price Ratios
features3=df[['volatility','Dividend Yield']] #Size Variables
features4=df[['EBITDA','Market Cap']]
features5=df[['Price/Earnings','Price/Sales','Price/Book','volatility','Dividend Yield','EBITDA','Market Cap']]

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


results = {'Model':[],'N':[],'Score':[]}
dfresults =pd.DataFrame(results)

for i in range(100):
    
    x_train1, x_test1, y_train1, y_test1 = train_test_split(features1,y,
                                                    test_size=0.3)
    x_train2, x_test2, y_train2, y_test2 = train_test_split(features2,y,
                                                    test_size=0.3)
    x_train3, x_test3, y_train3, y_test3 = train_test_split(features3,y,
                                                    test_size=0.3)
    x_train4, x_test4, y_train4, y_test4 = train_test_split(features4,y,
                                                    test_size=0.3)
    x_train5, x_test5, y_train5, y_test5 = train_test_split(features5,y,
                                                    test_size=0.3)
    neighbs=[1,2,3,4,5,6,7,8,9,10]
    for n in neighbs:
        
        KNN1=KNeighborsClassifier(n_neighbors=n)
        KNN2=KNeighborsClassifier(n_neighbors=n)
        KNN3=KNeighborsClassifier(n_neighbors=n)
        KNN4=KNeighborsClassifier(n_neighbors=n)
        KNN5=KNeighborsClassifier(n_neighbors=n)
        
    
        KNN1.fit(x_train1,y_train1)
        KNN2.fit(x_train2,y_train2)
        KNN3.fit(x_train3,y_train3)
        KNN4.fit(x_train4,y_train4)
        KNN5.fit(x_train5,y_train5)
        
        s1=KNN1.score(x_test1,y_test1)
        s2=KNN2.score(x_test2,y_test2)
        s3=KNN3.score(x_test3,y_test3)
        s4=KNN4.score(x_test4,y_test4)
        s5=KNN5.score(x_test5,y_test5)
        
        df1 = {'Model': 1,'N':n,'Score':s1}
        df2 = {'Model': 2,'N':n,'Score':s2}
        df3 = {'Model': 3,'N':n,'Score':s3}
        df4 = {'Model': 4,'N':n,'Score':s4}
        df5 = {'Model': 5,'N':n,'Score':s5}
        
        dfresults = dfresults.append(df1, ignore_index = True)
        dfresults = dfresults.append(df2, ignore_index = True)
        dfresults = dfresults.append(df3, ignore_index = True)
        dfresults = dfresults.append(df4, ignore_index = True)
        dfresults = dfresults.append(df5, ignore_index = True)

meanscores = dfresults.groupby('Model', as_index=False)['Score'].mean()






