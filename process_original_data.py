#%%
'''
    Read and save the crawled data
'''

import jcamp
from pathlib import Path
from tqdm import tqdm
import numpy as np
import re

def extract_data(data):
    name = data['title']
    charge_mass_ratio = data['x']
    peak_height = data['y']
    formula = data['molform']
    num_atoms = data['npoints']
    return {name:{'charge_mass_ratio':charge_mass_ratio,'peak_height':peak_height,'formula':formula,'num_atoms':num_atoms}}

#%%
p = Path("/Users/46003/Desktop/project/data") 
 
FileList=list(p.glob("*Mass.jdx"))

data_dict={}
for f in tqdm(FileList):
    original_data=jcamp.JCAMP_reader(f)
    extracted_data = extract_data(original_data)
    data_dict.update(extracted_data)

np.save('original_data.npy', data_dict)

#%%
'''
    Plot the graph, the number of atoms in the whole collection data against their formula
'''
original_data = np.load('original_data.npy', allow_pickle=True).item()

d_total_atom_num = {}
for j in original_data.values():
    formula = j['formula']

    num_atoms = len(formula.split())

    l_atom_name = []
    l_atom_num = []
    for i in formula.split():
        l_atom_name.append(re.findall(r'[0-9]+|[^0-9]+',i)[0])
        try:
            l_atom_num.append(int(re.findall(r'[0-9]+|[^0-9]+',i)[1]))
        except:
            l_atom_num.append(1)

    for i in range(num_atoms):
        if l_atom_name[i] in d_total_atom_num.keys():
            d_total_atom_num[l_atom_name[i]] += l_atom_num[i]
        else:
            d_total_atom_num[l_atom_name[i]] = l_atom_num[i]

# %%
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(16,9))
x = d_total_atom_num.keys()
y = d_total_atom_num.values()
plt.plot(x,y)
plt.yticks(size=14)
plt.xticks(size=10)

plt.ylim(bottom=0.)
plt.savefig("num_of_total_atoms.png")
plt.show()


# %%
