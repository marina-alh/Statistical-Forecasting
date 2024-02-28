import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
#sanofi_colors = ["#7A00E6","#CA8FFF",₢,"#F38DE4","#62d488","#ed6c4e","#f6c243","#ca99f5"]
sanofi_colors = ["#23004c","#7A00E6","#62d488","#ed6c4e","#f6c243","#ca99f5"]
marina_market_codes = {"INDIA": 'IN', "BRAZIL": 'BR', "KOREA": 'KR', "HONG KONG": 'HK', "PHILIPPINES": 'PH'}
sns.set_palette(sns.color_palette(sanofi_colors))

path = r'/Users/i0557167/Documents/Git/Statistical-Forecasting/MAM/data/' # use your path


monthly_kpi = pd.read_excel(path+'all_markets_YTD.xlsx')
my_scope = pd.read_excel(path+'Configuration_ALL.xlsx', skiprows=3)
leg1leg3 = pd.read_excel(path+'LEG1LEG3.xlsx')
forecastability = pd.read_excel(path+'forecastability.xlsx')


my_scope.columns = my_scope.columns.str.upper()
my_scope.columns = my_scope.columns.str.replace(' ','_')

columns_to_drop = ['ABC', 'XYZ']
my_scope['COUNTRY_CODE'] = my_scope['ITEM'].str[:2]
unnamed_columns = my_scope.columns[my_scope.columns.str.contains('^UNNAMED')]
columns_to_drop.extend(unnamed_columns)



my_scope.drop(columns=columns_to_drop, axis=1, inplace=True)
nan_columns = my_scope.columns[my_scope.isna().any()].tolist()


# OVERVIEW OF MY SCOPE. THE GOAL IS TO TRACK THE CHANGES OVER THE MONTHS; 
#   PLOT DONUTS PLOTS WITH ITEMS UNDER MANUAL - STAT - USE AND IGNORE 
# Count the occurrences of each class
filtered_my_scope = my_scope[my_scope['COUNTRY_CODE'] == 'BR'].reset_index(drop=True)
active_baseline_class = filtered_my_scope['ACTIVE_BASELINE'].value_counts()
usage_rule_class = filtered_my_scope['USAGE_RULE'].value_counts()

# Set up the plot
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
axarr[1].set_title('Usage Rule: USE VS Ignore')

""" axarr[1].pie(usage_rule_class, labels=usage_rule_class.index, colors=sanofi_colors,
              autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
centre_circle = plt.Circle((0, 0), 0.7, fc='white')
axarr[1].add_artist(centre_circle)
axarr[1].set_title('Usage Rule: USE VS Ignore')
 """
# Show the plot
plt.axis('equal')  # Equal aspect ratio ensures a circular plot
plt.show()

#kr_YTD  = agregated_kpi.loc[(agregated_kpi.MARKET == 'KOREA')].sort_values(by=['Sales with Stat Fcst'], ascending=False)

#kr_YTD.Volume = kr_YTD.Volume*100

#top10KR = kr_YTD.GMID.head(13)


 
#my_scope_forecastable =my_scope.loc[my_scope.is_forecastable == True)]
#my_scope_coverage =my_scope.loc[my_scope.is_forecastable == True) & my_scope.item_usage_rule == 'Use')]
#my_scope_adherence =my_scope_coverage.locmy_scope_coverage.baseline == '2. Statistical']
#my_scope_not_adherence =my_scope_coverage.locmy_scope_coverage.baseline == '1. Manual']


#number_items = lenmy_scope)
#number_forecastable = lenmy_scope_forecastable)
#number_coverage = lenmy_scope_coverage)
#adherence = lenmy_scope_adherence)



#my_scope_test_new_items =my_scope_forecastable.loc[my_scope_forecastable.item_usage_rule == 'Ignore') & my_scope_forecastable.intermit < 0.3)]