# UTF-8
# python 3.11.4


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os


path = r'/Users/i0557167/Documents/Git/Statistical-Forecasting/adjcov-dist/data/' # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))

df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
df_forecastable = df.loc[df.is_forecastable == True]
df_forecastable.fillna('NA', inplace=True) # pandas is reading the string 'NA' as a NaN values.
#aux = pd.read_csv('/Users/i0557167/Documents/Git/Statistical-Forecasting/adjcov-dist/data/dataRO.csv', keep_default_na=False, na_values=['_'])
#df_forecastable.loc[df_forecastable.market_code.isna()]['market_code'] = 'NA'

#df = pd.read_csv('/Users/i0557167/Documents/Git/Statistical-Forecasting/adjcov-dist/data/dataMA.csv')

sanofi_colors = ["#7A00E6","#23004C","#CA8FFF","#007FAD","#F38DE4"]
sns.set_palette(sns.color_palette(sanofi_colors))

latam = ['BR','AR']
asea = ['AE','DZ','EG','MA','NA','SA','TN','TR','ZA','CN','HK','IN','KR','TH','JP']
europe = ['AE', 'AT', 'BE', 'CH', 'CY', 'DE', 'GB', 'GR', 'NL', 'IE','DT', 'ES', 'FR', 'IT', 'PT','CZ', 'HU', 'MD', 'PL', 'RO', 'SK', 'TN']
north_america = ['CA','US' ]

# filter rows

df_forecastable_latam = df_forecastable.loc[df_forecastable.market_code.isin(latam),['market_code','acov']]
df_forecastable_asea = df_forecastable.loc[df_forecastable.market_code.isin(asea),['market_code','acov']]
df_forecastable_europe = df_forecastable.loc[df_forecastable.market_code.isin(europe),['market_code','acov']]
df_forecastable_north_america = df_forecastable.loc[df_forecastable.market_code.isin(north_america),['market_code','acov']]



df_forecastable_latam.index.name = 'index'
df_forecastable_asea.index.name = 'index'
df_forecastable_europe.index.name = 'index'
df_forecastable_north_america.index.name = 'index'

df_forecastable_latam = pd.pivot_table(df_forecastable_latam, values='acov',columns=['market_code'],index='index')
df_forecastable_asea = pd.pivot_table(df_forecastable_asea, values='acov',columns=['market_code'],index='index')
df_forecastable_europe= pd.pivot_table(df_forecastable_europe, values='acov',columns=['market_code'],index='index')
df_forecastable_north_america = pd.pivot_table(df_forecastable_north_america, values='acov',columns=['market_code'],index='index')

# df_forecastable_BR = df.loc[(df.is_forecastable == True) & (df.market_code == 'BR')] 
# df_forecastable_KR = df.loc[(df.is_forecastable == True) & (df.market_code == 'KR')] 
# df_forecastable_TH = df.loc[(df.is_forecastable == True) & (df.market_code == 'TH')] 
# df_forecastable_HK = df.loc[(df.is_forecastable == True) & (df.market_code == 'HK')] 
# df_forecastable_IN = df.loc[(df.is_forecastable == True) & (df.market_code == 'IN')] 

# selec columns
# df_BR = df_forecastable_BR.loc[:,['acov']]
# df_KR = df_forecastable_KR.loc[:,['acov']]
# df_TH = df_forecastable_TH.loc[:,['acov']]
# df_HK = df_forecastable_HK.loc[:,['acov']]
# df_IN = df_forecastable_IN.loc[:,['acov']]

# bind columns into a new dataframe


#df_forecastable_sort = df_forecastable.sort_values(by='acov')

#df_final = df_forecastable_sort.loc[:,['forecast_item','acov']]

#df_final.describe()

ax_latam = sns.boxplot(data=df_forecastable_latam)
ax_asea = sns.boxplot(data=df_forecastable_asea)
ax_europe = sns.boxplot(data=df_forecastable_europe)
ax_north_america = sns.boxplot(data=df_forecastable_north_america)

#x, y = ax.lines[0].get_data()



#x = sorted(x.tolist())
#y = sorted(y.tolist())

#gmid_dict = {'DORFLEX': 619108,'NOVALGINA': 333533,'OS_CAL_D': 779523,'DERMACYD': 549502}

#df_final['forecast_item'] = df_final['forecast_item'].map(lambda x: str(x)[4:])
#df_final

#for gmid in gmid_dict.values():
    
 #   x = df_final.loc[df_final.forecast_item == str(gmid)]['acov'].values[0]
  #  ax.text(x, 1+x , list(gmid_dict.keys())[list(gmid_dict.values()).index(gmid)])
   # ax.axvline(x, ymax = 0.35, ls = '--')


#ax.axhline(0.65,ls = '--')


