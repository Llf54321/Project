#%%
from tqdm import tqdm
import sqlite3
from selenium import webdriver
import pandas as pd
from crawler_method import get_AE_table
import numpy as np

# find the name list
df_clear = pd.DataFrame()
conn = sqlite3.connect('data-20.db')
cur = conn.cursor()
cur.execute("select distinct name from main_data")
l_name = list(cur)
conn.close()

# crawl AE data
options = webdriver.ChromeOptions()
options.add_argument('blink-settings=imagesEnabled=false')
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',options=options)

d_name_ae = {}
for a_name in tqdm(l_name):
    a_name = a_name[0]

    a_df = get_AE_table(driver,a_name)
    df_clear = df_clear.append(a_df)
    if not a_df.empty:
        d_name_ae[a_name]=a_df
driver.close()

np.save('name_AE.npy', d_name_ae)

# save data as a table in database
table_name = "appearance_energy_of_all_molecules"
conn = sqlite3.connect('data-20.db')
cur = conn.cursor()

fields_name = "name, ion, AE"

table = '''CREATE TABLE appearance_energy_of_all_molecules (name TEXT,ion TEXT,AE TEXT)'''

cur.execute(table)

rows = []
for index, row in df_clear.iterrows():
    a_row = tuple(row)
    rows.append(a_row)
cur.executemany('INSERT INTO appearance_energy_of_all_molecules VALUES (?,?,?)', rows)
conn.commit()

conn.close()


# %%
