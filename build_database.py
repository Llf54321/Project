import sqlite3
import numpy as np


processed_data = np.load('processed_data.npy', allow_pickle=True).item()

l_rows = []
for name in list(processed_data.keys()):
    for i in range(len(processed_data[name]['peak_height'])):
        a_row = []
        a_row.append(name)
        a_row.append(processed_data[name]['cas'])
        a_row.append(processed_data[name]['formula'].replace(' ',''))
        a_row.append(processed_data[name]['charge_mass_ratio'][i])
        a_row.append(processed_data[name]['peak_height'][i])
        a_row.append(processed_data[name]['branch_ratio'][i])
        opt_fragment = ''
        if type(processed_data[name]['optional_fragments'][i]) == list:
            for a_fragment in processed_data[name]['optional_fragments'][i]:
                opt_fragment += a_fragment + ','
            opt_fragment = opt_fragment[:-1]
        else:
            opt_fragment = processed_data[name]['optional_fragments'][i]
        a_row.append(opt_fragment)

        l_rows.append(tuple(a_row))

conn = sqlite3.connect('data-20.db')

cur = conn.cursor()

table = '''CREATE TABLE name (name TEXT,cas TEXT,formula TEXT, charge_mass_ratio NUMBER, peak_height NUMBER,branch_ratio NUMBER, optional_fragment TEXT)'''

cur.execute(table)


cur.executemany('INSERT INTO name VALUES (?,?,?,?,?,?,?)', l_rows)
conn.commit()

cur.close()
conn.close()
