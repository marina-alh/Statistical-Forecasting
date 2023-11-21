import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os


path = r'/Users/i0557167/Documents/Git/Statistical-Forecasting/MAM/data/' # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))

df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
df_forecastable = df.loc[(df.is_forecastable == True) & (df.item_usage_rule == 'Use')]


