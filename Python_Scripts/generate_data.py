import pandas as pd 
import numpy as np
import random
from datetime import datetime

np.random.seed(42) # reproducible results

# ---- CONFIG ----
departments = ['R&D','Sales & Marketing','G&A','COGS']
categories = ['Salaries','Software','Travel','Marketing','Other']
months = pd.date_range('2024-01-01', periods=12, freq='MS')

# ---- BUDGET TABLE ----
budget_base = {'R&D':{'Salaries':420000,'Software':25000,'Travel':8000,'Marketing':2000,'Other':5000},
'Sales & Marketing':{'Salaries':280000,'Software':15000,'Travel':30000,'Marketing':85000,'Other':8000},
'G&A':{'Salaries':150000,'Software':12000,'Travel':5000,'Marketing':1000,'Other':10000},
'COGS':{'Salaries':90000,'Software':40000,'Travel':2000,'Marketing':0,'Other':6000}
}

rows = []
for m in months:
    for dept in departments:
        for cat in categories:
            base = budget_base[dept][cat]
            rows.append({'month':m.strftime('%Y-%m'),'department':dept,'category':cat,'budget_amount':base})

budget_df = pd.DataFrame(rows)
budget_df.to_csv('Raw_Data/budget_2024.csv', index=False)

# ---- ACTUALS TABLE (budget + realistic noise) ----
actuals_df = budget_df.copy()
noise = np.random.uniform(-0.20, 0.25, size=len(actuals_df))
actuals_df['actual_amount'] = (actuals_df['budget_amount'] * (1 + noise)).round(0)
actuals_df = actuals_df.drop(columns='budget_amount')
actuals_df.to_csv('Raw_Data/actuals_2024.csv', index=False)

# ---- MRR TABLE ----
mrr_rows = []
total_mrr = 1400000  # start at $1.4M MRR
for m in months:
    new_arr    = round(random.uniform(60000, 120000), 0)
    expansion  = round(random.uniform(20000, 50000), 0)
    churn      = round(random.uniform(15000, 35000), 0)
    total_mrr  = total_mrr + new_arr + expansion - churn
    mrr_rows.append({'month': m.strftime('%Y-%m'), 'new_arr': new_arr,
                     'expansion_arr': expansion, 'churn_arr': churn, 'total_mrr': total_mrr})

mrr_df = pd.DataFrame(mrr_rows)
mrr_df.to_csv('Raw_Data/mrr_data.csv', index=False)
print('Data generated successfully!')