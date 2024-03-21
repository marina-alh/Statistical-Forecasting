import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

#data path
path = r'/Users/i0557167/Documents/Git/Statistical-Forecasting/MAM/data/' 

#sanofi_colors = ["#7A00E6","#CA8FFF",₢,"#F38DE4","#62d488","#ed6c4e","#f6c243","#ca99f5"]
sanofi_colors = ["#23004c","#7A00E6","#62d488","#ed6c4e","#f6c243","#ca99f5"]
sns.set_palette(sns.color_palette(sanofi_colors))


monthly_kpi = pd.read_excel(path+'all_my_markets_YTD.xlsx') 
my_scope = pd.read_excel(path+'Configuration_ALL.xlsx', skiprows=3)
leg1leg3 = pd.read_excel(path+'LEG1LEG3.xlsx')
forecastability = pd.read_excel(path+'forecastability.xlsx')


# Cleaning KNX file


# standarizing column names and droping not useful columns
my_scope.columns = my_scope.columns.str.upper()
my_scope.columns = my_scope.columns.str.replace(' ','_')
columns_to_drop = ['ABC', 'XYZ' ]
my_scope['COUNTRY_CODE'] = my_scope['ITEM'].str[:2]
unnamed_columns = my_scope.columns[my_scope.columns.str.contains('^UNNAMED')]
columns_to_drop.extend(unnamed_columns)
my_scope.drop(columns=columns_to_drop, axis=1, inplace=True)
#nan_columns = my_scope.columns[my_scope.isna().any()].tolist()









# Initial setup for my forecast scope

marina_market_codes = {"INDIA": 'IN', "BRAZIL": 'BR', "KOREA": 'KR', "HONG KONG": 'HK', "PHILIPPINES": 'PH'}

# OVERVIEW OF MY SCOPE. THE GOAL IS TO TRACK THE CHANGES OVER THE MONTHS; 
#   PLOT DONUTS PLOTS WITH ITEMS UNDER MANUAL - STAT - USE AND IGNORE 
# Count the occurrences of each class
filtered_my_scope = my_scope[my_scope['COUNTRY_CODE'] == 'PH'].reset_index(drop=True)
active_baseline_class = filtered_my_scope['ACTIVE_BASELINE'].value_counts()
usage_rule_class = filtered_my_scope['USAGE_RULE'].value_counts()


# Set up the plot
fig, axarr = plt.subplots(1, 2, figsize=(12, 6))  # Create a 1x2 grid of subplots


# Create the pie chart
axarr[0].pie(active_baseline_class, labels=active_baseline_class.index, colors=sanofi_colors,
        autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})

# Draw a white circle at the center to create the donut effect
centre_circle = plt.Circle((0, 0), 0.7, fc='white')
axarr[0].add_artist(centre_circle)
axarr[0].set_title('Active Baseline: Stat VS Manual')

axarr[1].pie(usage_rule_class, labels=usage_rule_class.index, colors=sanofi_colors,
              autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
centre_circle = plt.Circle((0, 0), 0.7, fc='white')
axarr[1].add_artist(centre_circle)
axarr[1].set_title('Usage Rule: Use VS Ignore')


# ITEMS THAT MARKED AS "SWITCH" IN BUT SET UP AS "MANUAL" BASE LINE
#   PRINT A LIST OF GMID THAT FIT THAT CONDITION

columns_to_keep = ['ITEM','BUCKETS','LOCAL_DESCRIPTION','ACTIVE_BASELINE','USAGE_RULE','TYPE','OTHER_ITEMS' ]
my_scope_simple = filtered_my_scope[columns_to_keep]


#filtered_switch_dataset = switch_dataset[(switch_dataset['TYPE'] == 'Switch-In') & & (switch_dataset['OTHER_ITEMS'].isin(switch_dataset.loc[switch_dataset['USAGE_RULE'] == '2. Statistical', 'ITEM']))]
#filtered_switch_dataset =switch_dataset[(switch_dataset['TYPE'] == 'Switch-In') & (switch_dataset['ACTIVE_BASELINE'] == '1. Manual') & (switch_dataset['OTHER_ITEMS'].isin(switch_dataset.loc[switch_dataset['ACTIVE_BASELINE'] == '2. Statistical', 'ITEM']))]



# 2/. FORECASTABILITY CHECK 
# list of forecastable items but under ignore and manual
new_forecastable = forecastability[(forecastability.baseline == '1. Manual') & (forecastability.is_forecastable == True) & (forecastability.item_usage_rule == 'Ignore')]
# new forecastable items keys
new_forecastable_items_list = new_forecastable['forecast_item'].tolist()
# filtering rows from the config file with only the new forecastable items
configuration_new_forecastable = my_scope_simple[my_scope_simple['ITEM'].isin(new_forecastable_items_list)].reset_index(drop=True)
# merging the info from config file with the acov and intermit columns by GMID key
configuration_new_forecastable = pd.merge(configuration_new_forecastable,new_forecastable[['forecast_item','acov','intermit']],left_on="ITEM", right_on="forecast_item", how="outer").drop(columns=['forecast_item'])



# 3/. OVERVIEW OF MY SCOPE
# 3.1/. My active scope
my_active_scope = my_scope_simple[(my_scope_simple.ACTIVE_BASELINE =='2. Statistical')&(my_scope_simple.TYPE != 'Prunned')].reset_index(drop=True)
# geting the keys to match items from the forecastability table
my_active_scope_items_list = my_active_scope['ITEM'].tolist()
#getting only those rows with items in my active scope
matching_rows_my_active_scope_forecastability = forecastability[forecastability['forecast_item'].isin(my_active_scope_items_list)].reset_index(drop=True)
# merge the acov and intermitance info from forecastability table with my config table
my_active_scope = pd.merge(my_active_scope,matching_rows_my_active_scope_forecastability[['forecast_item','acov','intermit']],left_on="ITEM", right_on="forecast_item", how="outer").drop(columns=['forecast_item'])
my_active_scope.columns = my_active_scope.columns.str.upper()
#number of items I have active
number_active_scope = len(my_active_scope)

# 3.2/. Check if I have manual items in use
my_manual_use = my_scope_simple[(my_scope_simple.ACTIVE_BASELINE =='1. Manual')&(my_scope_simple.TYPE != 'Prunned') & (my_scope_simple.USAGE_RULE == 'Use')].reset_index(drop=True)

# 3.3/. Check if I have stat items in ignore
my_statistical_ignore = my_scope_simple[(my_scope_simple.ACTIVE_BASELINE =='2. Statistical')&(my_scope_simple.TYPE != 'Prunned') & (my_scope_simple.USAGE_RULE == 'Ignore')].reset_index(drop=True)

#4/. TOP 10 BEST AND TOP 10 OFFENDERS

#5/. LEG 1 AND LEG3 EVAL FOR NEW CHANGED ALGOS

#6/. ZERO TOUCH LIST AND CHECK



# Create a folder in the MAM with the files and extration and the report