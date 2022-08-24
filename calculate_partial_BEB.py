import sqlite3
from selenium import webdriver
from tqdm import tqdm
import pandas as pd
import numpy as np

# find the main name 
options = webdriver.ChromeOptions()
options.add_argument('blink-settings=imagesEnabled=false')
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',options=options)

dict_main_name_total_beb = {}

conn = sqlite3.connect('data-20.db')
cur = conn.cursor()
cur.execute("select * from energy_vs_total_beb where energy='70'")
for row in tqdm(cur):
    a_original_name = row[0]
    driver.get("https://webbook.nist.gov/chemistry/name-ser/")
    driver.find_element_by_id('cMS').click()
    driver.find_element_by_id('cIE').click()

    search_text = driver.find_element_by_id('Name') 
    search_text.send_keys(a_original_name) 
    search_text.submit()
    try:
        a_main_name = driver.find_element_by_id('Top').text
    except:
        continue
    a_tot_beb = row[3]
    dict_main_name_total_beb[a_main_name] = a_tot_beb

driver.close()
conn.close()

# calculate the partial BEB
df = pd.DataFrame()
conn = sqlite3.connect('data-20.db')
cur = conn.cursor()
for a_main_name in dict_main_name_total_beb.keys():
    cur.execute("select name,formula,charge_mass_ratio,branch_ratio,optional_fragment from main_data where name='{0}'".format(a_main_name))
    rows = cur.fetchall()
    if rows != []:
        a_df = pd.DataFrame(rows, columns=['name','formula','charge_mass_ratio','branch_ratio','optional_fragment'])
        a_branch_ratio = np.array(a_df['branch_ratio'])
        a_partial_beb = a_branch_ratio*dict_main_name_total_beb[a_main_name]
        a_df['partial_beb'] = a_partial_beb
        df = df.append(a_df)
conn.close()

# save data as a table in the database
table_name = "partial_beb"
conn = sqlite3.connect('data-20.db')
cur = conn.cursor()

fields_name = "name, formula, charge_mass_ratio, branch_ratio, partial_beb, optional_fragment"

table = '''CREATE TABLE partial_beb (name TEXT,formula TEXT,charge_mass_ratio TEXT,branch_ratio NUMBER,partial_beb NUMBER, optional_fragment TEXT)'''

cur.execute(table)

for index, row in df.iterrows():
    a = row["name"]
    b = row['formula']
    c = row['charge_mass_ratio']
    d = row["branch_ratio"]
    e = row['partial_beb']
    f = row['optional_fragment']
    fields_value = "'{0}', '{1}', '{2}', {3}, {4}, '{5}'".format(a, b, c, d, e, f)
    sql = "Insert Into {0} ({1}) Values({2})".format(table_name, fields_name, fields_value)

    cur.execute(sql)
    conn.commit()

conn.close()
