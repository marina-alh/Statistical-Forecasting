import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os


path = r'/Users/i0557167/Documents/Git/Statistical-Forecasting/zero-touch-analysis/data' # use your path
all_files = glob.glob(os.path.join(path, "*.xlsx"))

df_monthly = pd.read_excel(path+"/monthlydata.xlsx")
df_cumulative = pd.read_excel(path+"/cumulativedata.xlsx")

# change all column names to uppercase
df_monthly.columns = df_monthly.columns.str.upper()
df_cumulative.columns = df_cumulative.columns.str.upper()

# remove spaces from column names
df_monthly.columns = df_monthly.columns.str.replace(" ", "_")
df_cumulative.columns = df_cumulative.columns.str.replace(" ", "_")

# remove - to 0 

df_monthly = df_monthly.replace('-', 0)
df_cumulative = df_cumulative.replace('-', 0)


# select country
df_country = df_cumulative[(df_cumulative.MARKET == 'INDIA')]
df_stat_mape_on_target = df_country[df_country.STAT_MAPE < 0.30].reset_index(drop=True)

# select negative enrichments
df_negative_enrichments = df_stat_mape_on_target[df_stat_mape_on_target.DELTA_MAPE_VARIATION < 0].sort_values(by="VOLUME", ascending=False).reset_index(drop=True)


#--------------------------- count of the enrichments -----------------------


#list of gmids to analyse

gmid_list = df_negative_enrichments.GMID.reset_index(drop=True)

for gmid in gmid_list:
    print(df_monthly[df_monthly.GMID == gmid].sort_values(by=['STARTDATE']).reset_index(drop= True)["DELTA_MAPE_VARIATION"])



#top10 volumes
#top10_GMID = df_country.nlargest(n=10, columns=['VOLUME']).GMID.reset_index(drop= True)


# get all dates



#df_monthly[df_monthly.GMID == 724619].sort_values(by=['STARTDATE']).reset_index(drop= True)



#df_forecastable = df.loc[(df.is_forecastable == True) & (df.item_usage_rule == 'Use')]

