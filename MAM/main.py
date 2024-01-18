import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os


path = r'/Users/i0557167/Documents/Git/Statistical-Forecasting/MAM/data/' # use your path

agregated_kpi = pd.read_excel(path+'agregated_kpi.xlsx')
monthly_kpi = pd.read_excel(path+'monthly_kpis.xlsx')
forecastability = pd.read_csv(path+'SQL_Review_forecastability_2023_12_14.csv')



kr_YTD  = agregated_kpi.loc[(agregated_kpi.MARKET == 'KOREA')].sort_values(by=['Sales with Stat Fcst'], ascending=False)

kr_YTD.Volume = kr_YTD.Volume*100

top10KR = kr_YTD.GMID.head(13)



#df_forecastable = df.loc[(df.is_forecastable == True)]
#df_coverage = df.loc[(df.is_forecastable == True) & (df.item_usage_rule == 'Use')]
#df_adherence = df_coverage.loc[df_coverage.baseline == '2. Statistical']
#df_not_adherence = df_coverage.loc[df_coverage.baseline == '1. Manual']


#number_items = len(df)
#number_forecastable = len(df_forecastable)
#number_coverage = len(df_coverage)
#adherence = len(df_adherence)



#df_test_new_items = df_forecastable.loc[(df_forecastable.item_usage_rule == 'Ignore') & (df_forecastable.intermit < 0.3)]