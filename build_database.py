import sqlite3
import numpy as np


def find_tb():
    cur.execute("select * from name limit 0,50")
    return cur.fetchall()

processed_data = np.load('processed_data.npy', allow_pickle=True).item()

rows = []
for n in list(processed_data.keys()):
    for i in range(len(processed_data[n]['peak_height'])):
        b = []
        b.append(n)
        b.append(processed_data[n]['cas'])
        b.append(processed_data[n]['nist_mass_spec_num'])
        b.append(processed_data[n]['formula'])
        b.append(processed_data[n]['charge_mass_ratio'][i])
        b.append(processed_data[n]['peak_height'][i])
        b.append(processed_data[n]['branch_ratio'][i])
        c = ''
        if type(processed_data[n]['optional_fragments'][i]) == list:
            for f in processed_data[n]['optional_fragments'][i]:
                c += f + ','
            c = c[:-1]
        else:
            c = processed_data[n]['optional_fragments'][i]
        b.append(c)
        a = tuple(b)
        rows.append(a)

conn = sqlite3.connect('data-20.db')

cur = conn.cursor()

table_name = '''CREATE TABLE name (name TEXT,cas TEXT,nist_mass_spec_num TEXT,formula TEXT, charge_mass_ratio NUMBER, peak_height NUMBER,branch_ratio NUMBER, optional_fragment TEXT)'''

cur.execute(table_name)


cur.executemany('INSERT INTO name VALUES (?,?,?,?,?,?,?,?)', rows)
conn.commit()

