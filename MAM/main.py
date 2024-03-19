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



# FORECASTABILITY CHECK 
# list of forecastable items but under ignore and manual

new_forecastable = forecastability[(forecastability.baseline == '1. Manual') & (forecastability.is_forecastable == True) & (forecastability.item_usage_rule == 'Ignore')]

new_forecastable_items = new_forecastable['forecast_item'].tolist()
configuration_new_forecastable = my_scope_simple[my_scope_simple['ITEM'].isin(new_forecastable_items)].reset_index(drop=True)

# Filter df1 to keep only rows with matching keys
matching_rows_forecastability = forecastability[forecastability['forecast_item'].isin(new_forecastable_items)].reset_index(drop=True)


configuration_new_forecastable1 = pd.concat([configuration_new_forecastable,matching_rows_forecastability[['acov','intermit']]],axis=1).sort_values(by='acov',ascending=False)