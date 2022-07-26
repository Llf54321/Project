from tqdm import tqdm
from selenium import webdriver
import pandas as pd
from crawler_method import get_energy_vs_total_beb_table

# crawl energy vs BEB data
options = webdriver.ChromeOptions()

options.add_argument('blink-settings=imagesEnabled=false')
driver = webdriver.Chrome('F:\chromedriver_win32\chromedriver.exe',options=options)

df = pd.DataFrame()

driver.get("https://physics.nist.gov/PhysRefData/Ionization/molTable.html")
num_molecule = len(driver.find_element_by_xpath("/html/body/div[3]/div/table/tbody/tr/td[1]/form/select").find_elements_by_tag_name("option"))

for i in tqdm(range(num_molecule)):
    a_df = get_energy_vs_total_beb_table(driver,i)

    df = df.append(a_df)

driver.close()

# save data to database as a table
import sqlite3
table_name = "energy_vs_total_beb"
conn = sqlite3.connect('data-20.db')
cur = conn.cursor()

fields_name = "name, formula, energy, beb"

table = '''CREATE TABLE energy_vs_total_beb (name TEXT,formula TEXT,energy NUMBER,beb NUMBER)'''

cur.execute(table)

for index, row in df.iterrows():
    a = row["name"]
    b = row['formula']
    c = row["energy"]
    d = row['beb']
    fields_value = "'{0}', '{1}', {2}, {3}".format(a, b, c,d)
    sql = "Insert Into {0} ({1}) Values({2})".format(table_name, fields_name, fields_value)

    cur.execute(sql)
    conn.commit()

conn.close()
