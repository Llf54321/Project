# Read and save the crawled data
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
    num_fragmenhts = data['npoints']
    if 'cas registry no' in data.keys():
        cas = data['cas registry no']
    else:
        cas = str(np.nan)
    nist_mass_spec_num = data['$nist mass spec no']
    return {name:{'charge_mass_ratio':charge_mass_ratio,'peak_height':peak_height,'formula':formula,'num_fragmenhts':num_fragmenhts,'cas':cas,'nist_mass_spec_num':nist_mass_spec_num}}

p = Path("/Users/46003/Desktop/project/data") 
 
FileList=list(p.glob("*Mass.jdx"))

data_dict={}
for f in tqdm(FileList):
    original_data=jcamp.JCAMP_reader(f)
    extracted_data = extract_data(original_data)
    data_dict.update(extracted_data)

np.save('original_data.npy', data_dict)

# Plot the graphs
original_data = np.load('original_data.npy', allow_pickle=True).item()

part_data = {}
d_total_num_atom = {}
d_part_atom_num = {}
d_total_atom_num = {}
for j in original_data.keys():
    formula = original_data[j]['formula']

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
    
    a_num = np.sum(l_atom_num)
    if a_num <= 20: # Set the limit number of atoms in one molecule
        part_data[j] = original_data[j]
        for i in range(num_atoms):
            if l_atom_name[i] in d_part_atom_num.keys():
                d_part_atom_num[l_atom_name[i]] += l_atom_num[i]
            else:
                d_part_atom_num[l_atom_name[i]] = l_atom_num[i]
    
    if a_num not in d_total_num_atom.keys():
        d_total_num_atom[a_num] = 1
    else:
        d_total_num_atom[a_num] += 1

np.save('new_data.npy', part_data)

# The number of atoms in the whole collection data against their formula
import matplotlib.pyplot as plt

fig_1 = plt.figure(figsize=(16,9))
x = d_total_atom_num.keys()
y = d_total_atom_num.values()
plt.plot(x,y)
plt.yticks(size=14)
plt.xticks(size=10)

plt.ylim(bottom=0.)
plt.savefig("num_of_atoms_in_whole_collection.png")
plt.show()

# The number of molecules against the number of atoms in the molecule
fig_2 = plt.figure(figsize=(16,9))
x = d_total_num_atom.keys()
y = d_total_num_atom.values()
plt.bar(x,y)
plt.yticks(size=14)
plt.xticks(size=10)

plt.ylim(bottom=0.)
plt.savefig("num_of_atoms_in_molecule.png")
plt.show()

# The number of atoms in the part of collection data against their formula
fig_3 = plt.figure(figsize=(16,9))
x = d_part_atom_num.keys()
y = d_part_atom_num.values()
plt.plot(x,y)
plt.yticks(size=14)
plt.xticks(size=10)

plt.ylim(bottom=0.)
plt.savefig("num_of_atoms_in_part_collection.png")
plt.show()
