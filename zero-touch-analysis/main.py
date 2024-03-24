import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os


path = r'/Users/i0557167/Library/CloudStorage/OneDrive-Sanofi/Documents/Market/MAM/2024/MAR24/zero-touch/data' # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))

df_forecastability = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

df_forecastability.market_code.fillna('NA', inplace=True)



df_forecastability['forecast_item'] = df_forecastability['forecast_item'].map(lambda x: str(x)[4:])

df_forecastable = df_forecastability.loc[(df_forecastability.is_forecastable == True) & (df_forecastability.item_usage_rule == 'Use')]

df_acov = df_forecastable.loc[:,['market_code','forecast_item','acov']]
df_acov.rename(columns={'market_code': 'MARKET', 'forecast_item': 'GMID','acov':'ACOV'}, inplace=True)

df_monthly = pd.read_excel(path+"/monthly_PH.xlsx")
df_cumulative = pd.read_excel(path+"/cumulative_PH.xlsx")


# change all column names to uppercase
df_monthly.columns = df_monthly.columns.str.upper()
df_cumulative.columns = df_cumulative.columns.str.upper()

# remove spaces from column names
df_monthly.columns = df_monthly.columns.str.replace(" ", "_")
df_cumulative.columns = df_cumulative.columns.str.replace(" ", "_")

# remove - to 0 

df_monthly = df_monthly.replace('-', 0)
df_cumulative = df_cumulative.replace('-', 0)

#marina_market_codes = {"INDIA": 'IN', "BRAZIL": 'BR', "KOREA": 'KR', "HONG KONG": 'HK', "PHILIPPINES": 'PH'}
marina_market_codes = { "BRAZIL": 'BR', "KOREA": 'KR', "HONG KONG": 'HK', "PHILIPPINES": 'PH'}
#marina_market = {"INDIA": 0.40, "BRAZIL": 0.45, "KOREA": 0.31, "HONG KONG": 0.36, "PHILIPPINES": 0.33}
marina_market = {"BRAZIL": 0.45, "KOREA": 0.31, "HONG KONG": 0.36, "PHILIPPINES": 0.33}
nurdos_market = {"ALGERIA": 0.46, "EGYPT": 0.47, "MOROCCO": 0.35, "SOUTH AFRICA": 0.38, "TUNISIA": 0.35, "UNITED ARAB EMIRATES": 0.53, "SAUDI ARABIA": 0.53, "TURKEY": 0.53, "JAPAN": 0.19}
romina_market = {"ARGENTINA": 0.32, "POLAND": 0.45, "ROMANIA": 0.45, "HUNGARY": 0.35, "SLOVAKIA": 0.50, "CZECH REPUBLIC": 0.50, "MOLDOVA": 0.55}


final_df = pd.DataFrame()



for key in marina_market: 
# select country
    df_country = df_cumulative[(df_cumulative.MARKET == key)]
    df_stat_mape_YTD_on_target = df_country[df_country.STAT_MAPE_YTD < marina_market[key]]

# select negative enrichments
    df_negative_enrichments = df_stat_mape_YTD_on_target[df_stat_mape_YTD_on_target.DELTA_MAPE_VARIATION < 0].sort_values(by="VOLUME", ascending=False)


#--------------------------- count of the enrichments -----------------------


#list of gmids to analyse

    gmid_list = df_negative_enrichments.GMID
    
    for gmid in gmid_list:
        stage_df = df_monthly[df_monthly.GMID == gmid].sort_values(by=['STARTDATE']).loc[:,["MARKET","GMID","STARTDATE",'DELTA_MAPE_VARIATION','STAT_MAPE','FINAL_MAPE']]
        final_df = pd.concat([final_df,stage_df])


for key in marina_market_codes:
    final_df.MARKET.replace(key,marina_market_codes[key], inplace=True)

df_acov['GMID'] = df_acov['GMID'].astype('int64')
final_df = pd.merge(final_df,df_acov)
stat_MAPE_YTD_final = df_negative_enrichments.loc[:,["GMID","STAT_MAPE_YTD","FINAL_MAPE_YTD"]]
final_df = pd.merge(final_df,stat_MAPE_YTD_final)

#final_df.merge(df_acov, left_on = 'GMID', right_on = 'GMID')


final_df.reset_index(drop=True).to_excel(path+"/marina_zerotouch_PH.xlsx",index=False)




#top10 volumes
#top10_GMID = df_country.nlargest(n=10, columns=['VOLUME']).GMID.reset_index(drop= True)


# get all dates



#df_monthly[df_monthly.GMID == 724619].sort_values(by=['STARTDATE']).reset_index(drop= True)



#df_forecastable = df.loc[(df.is_forecastable == True) & (df.item_usage_rule == 'Use')]

