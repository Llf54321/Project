#%%
import numpy as np
import re
from tqdm import tqdm

original_data = np.load('original_data.npy', allow_pickle=True).item()
mass_abundance = np.load('mass_abundance.npy',allow_pickle=True).item()

def test_layers(layers, mass_list):
    l_charge_mass_ratio = []
    combination_mass = []
    shape = [len(layer) for layer in layers]
    offsets = [0] * len(shape)
    has_next = True
    while has_next:
        record = [layers[i][off] for i,off in enumerate(offsets)]
        if np.sum(record) in mass_list:
            l_charge_mass_ratio.append(np.sum(record))
            combination_mass.append(record)
        
        for i in range(len(shape) - 1, -1, -1):
            if offsets[i] + 1 >= shape[i]:
                offsets[i] = 0  # 重置并进位
                if i == 0:
                    has_next = False  # 全部占满，退出
            else:
                offsets[i] += 1
                break

    return l_charge_mass_ratio, combination_mass

#%%
formula = original_data['Dibenzofuran, 2,8-dibromo-']['formula']
num_atoms = len(formula.split())

l_atom_name = []
l_atom_num = []
for i in formula.split():
    l_atom_name.append(re.findall(r'[0-9]+|[^0-9]+',i)[0])
    try:
        l_atom_num.append(int(re.findall(r'[0-9]+|[^0-9]+',i)[1]))
    except:
        l_atom_num.append(1)

l_other_mass = []
l_main_mass = []
for atom in l_atom_name:
    l_other_mass.append(mass_abundance[atom]['other'])
    l_main_mass.append(mass_abundance[atom]['main'][0][0])
#%%
# All atoms in the formula are the most abundance

possible_mass = []
for i in range(num_atoms):
    a_possible_mass = []
    for n in range(l_atom_num[i]+1):
        a_possible_mass.append(n*l_main_mass[i])
    possible_mass.append(a_possible_mass)

l_charge_mass_ratio, combination_mass = test_layers(possible_mass, original_data['Dibenzofuran, 2,8-dibromo-']['charge_mass_ratio'])

for i in combination_mass:
    for j in range(num_atoms):
        i[j] = int(i[j]/l_main_mass[j])

d_mass_main_formula = {}
for i in range(len(combination_mass)):
    a_formula = ''
    for j in range(num_atoms):
        if combination_mass[i][j] != 0:
            a_formula += (str(l_main_mass[j]) + l_atom_name[j]) * combination_mass[i][j]
    if l_charge_mass_ratio[i] not in d_mass_main_formula.keys():
        d_mass_main_formula[l_charge_mass_ratio[i]] = [a_formula]
    else:
        d_mass_main_formula[l_charge_mass_ratio[i]].append(a_formula)
#print(d_mass_main_formula.items())

#%%
# One atom with minorabundance mass in the formula

l_rest_mass = []
for i in original_data['Dibenzofuran, 2,8-dibromo-']['charge_mass_ratio']:
    if i not in d_mass_main_formula.keys():
        l_rest_mass.append(i)


for i in range(num_atoms):
    if l_other_mass[i] != []:
        for j in l_other_mass[i]:
            minority_mass = j[0]

            changed_atom = list(np.array(possible_mass[i])[1:] - l_main_mass[i] + minority_mass)
            changed_atom.insert(0,0)
            possible_mass_1 = possible_mass.copy()
            possible_mass_1[i] = changed_atom

            l_charge_mass_ratio, combination_mass = test_layers(possible_mass_1, l_rest_mass)

            for k in combination_mass:
                for h in range(num_atoms):
                    if h == i:
                        if k[i] != 0:
                            k[i] = int((k[h]-minority_mass)/l_main_mass[h])
                    else:
                        k[h] = int(k[h]/l_main_mass[h])

            
            for k in range(len(combination_mass)):
                a_formula = ''
                for h in range(num_atoms):
                    if h == i:
                        a_formula += str(minority_mass)+ l_atom_name[h]
                    if combination_mass[k][h] != 0:
                        a_formula += (str(l_main_mass[h])+ l_atom_name[h]) * combination_mass[k][h]
                if l_charge_mass_ratio[k] not in d_mass_main_formula.keys():
                    d_mass_main_formula[l_charge_mass_ratio[k]] = [a_formula]
                else:
                    d_mass_main_formula[l_charge_mass_ratio[k]].append(a_formula)


# %%
# Two atom with minorabundance mass in the formula

l_rest_mass = []
for i in original_data['Dibenzofuran, 2,8-dibromo-']['charge_mass_ratio']:
    if i not in d_mass_main_formula.keys():
        l_rest_mass.append(i)

for i in range(num_atoms):
    if l_other_mass[i] != []:
        for j in l_other_mass[i]:
            minority_mass_1 = j[0]

            changed_atom = list(np.array(possible_mass[i])[1:] - l_main_mass[i] + minority_mass_1)
            changed_atom.insert(0,0)
            possible_mass_1 = possible_mass.copy()
            possible_mass_1[i] = changed_atom

            for m in range(num_atoms):
                if m == i:
                    if l_atom_num[m] == 1:
                        continue

                if l_other_mass[m] != []:
                    for n in l_other_mass[m]:
                        minority_mass_2 = n[0]
                        if m == i:
                            changed_atom = list(np.array(possible_mass_1[i])[2:] - l_main_mass[i] + minority_mass_2)
                            possible_mass_2 = possible_mass_1.copy()
                            possible_mass_2[i] = changed_atom

                        else:
                            changed_atom = list(np.array(possible_mass[m])[1:] - l_main_mass[m] + minority_mass_2)
                            possible_mass_2 = possible_mass_1.copy()
                            possible_mass_2[m] = changed_atom

                l_charge_mass_ratio, combination_mass = test_layers(possible_mass_2, l_rest_mass)

                for k in combination_mass:
                    for h in range(num_atoms):
                        if h == i and h == m:
                            if k[i] != 0:
                                k[i] = int((k[h]-minority_mass_1-minority_mass_2)/l_main_mass[h])
                        elif h == i:
                            if k[i] != 0:
                                k[i] = int((k[h]-minority_mass_1)/l_main_mass[h])
                        elif h == m:
                            if k[m] != 0:
                                k[m] = int((k[h]-minority_mass_2)/l_main_mass[h])
                        else:
                            k[h] = int(k[h]/l_main_mass[h])

                
                for k in range(len(combination_mass)):
                    a_formula = ''
                    for h in range(num_atoms):
                        if h == i:
                            a_formula += str(minority_mass_1)+ l_atom_name[h]
                        if h == m:
                            a_formula += str(minority_mass_2)+ l_atom_name[h]
                        if combination_mass[k][h] != 0:
                            a_formula += (str(l_main_mass[h])+ l_atom_name[h]) * combination_mass[k][h]
                    if l_charge_mass_ratio[k] not in d_mass_main_formula.keys():
                        d_mass_main_formula[l_charge_mass_ratio[k]] = [a_formula]
                    else:
                        d_mass_main_formula[l_charge_mass_ratio[k]].append(a_formula)
                #print(d_mass_main_formula.items())
# %%
# Check if it works for all possible charge/mass ratio
l_rest_mass = []
for i in original_data['Dibenzofuran, 2,8-dibromo-']['charge_mass_ratio']:
    if i not in d_mass_main_formula.keys():
        l_rest_mass.append(i)
if l_rest_mass != []:
    print('Dibenzofuran, 2,8-dibromo-', original_data['Dibenzofuran, 2,8-dibromo-']['formula'], l_rest_mass)
