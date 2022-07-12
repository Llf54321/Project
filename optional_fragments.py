#%%
import numpy as np
import re
from tqdm import tqdm

original_data = np.load('new_data.npy', allow_pickle=True).item()
mass_abundance = np.load('mass_abundance.npy',allow_pickle=True).item()

def find_possible_combination(possible_mass, mass_list):
    l_charge_mass_ratio = []
    combination_mass = []
    shape = [len(layer) for layer in possible_mass]
    offsets = [0] * len(shape)
    has_next = True
    while has_next:
        record = [possible_mass[i][off] for i,off in enumerate(offsets)]
        if np.sum(record) in mass_list:
            l_charge_mass_ratio.append(np.sum(record))
            combination_mass.append(record)
        
        for i in range(len(shape) - 1, -1, -1):
            if offsets[i] + 1 >= shape[i]:
                offsets[i] = 0  
                if i == 0:
                    has_next = False  
            else:
                offsets[i] += 1
                break

    return l_charge_mass_ratio, combination_mass

#%%
processed_data = {}
def find_optional_fragments(name):
    subscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    formula = original_data[name]['formula']
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

    # All atoms in the formula are the most abundance
    index_cl = -1
    index_br = -1

    possible_main_mass = []
    for i in range(num_atoms):
        a_possible_mass = []
        for n in range(l_atom_num[i]+1):
            a_possible_mass.append(n*l_main_mass[i])
            if l_atom_name[i] == 'Cl':
                index_cl = i
                for k in range(n+1):
                    if k != 0:
                        a_possible_mass.append(n*l_main_mass[i]+2*k)
            if l_atom_name[i] == 'Br':
                index_br = i
                for k in range(n+1):
                    if k != 0:
                        a_possible_mass.append(n*l_main_mass[i]+2*k)
        possible_main_mass.append(a_possible_mass)

    l_charge_mass_ratio, combination_mass = find_possible_combination(possible_main_mass, original_data[name]['charge_mass_ratio'])

    l_cl_formula = []
    l_br_formula = []
    for i in combination_mass:
        for j in range(num_atoms):
            if j == index_cl:
                if i[j] != 0:
                    cl_formula=''

                    if i[j]%35 == 0:
                        num_cl37 = 0
                        num_cl35 = i[j]/35
                    else:
                        num_cl37 = (i[j]%35)/2
                        num_cl35 = (i[j]-num_cl37*37)/35

                    if num_cl35 != 0:
                        if num_cl35 == 1:
                            cl_formula += '35'.translate(subscript) + 'Cl'
                        else:
                            cl_formula += '35'.translate(subscript) + 'Cl' + str(int(num_cl35))
                    if num_cl37 != 0:
                        if num_cl37 == 1:
                            cl_formula += '37'.translate(subscript) + 'Cl'
                        else:
                            cl_formula += '37'.translate(subscript) + 'Cl' + str(int(num_cl37))
                    l_cl_formula.append(cl_formula)
                else:
                    l_cl_formula.append(0)

            if j == index_br:
                if i[j] != 0:
                    br_formula=''

                    if i[j]%79 == 0:
                        num_br81 = 0
                        num_br79 = i[j]/79
                    else:
                        num_br81 = (i[j]%79)/2
                        num_br79 = (i[j]-num_br81*81)/79

                    if num_br79 != 0:
                        if num_br79 == 1:
                            br_formula += '79'.translate(subscript) + 'Br'
                        else:
                            br_formula += '79'.translate(subscript) + 'Br' + str(int(num_br79))
                    if num_br81 != 0:
                        if num_br81 == 1:
                            br_formula += '81'.translate(subscript) + 'Br'
                        else:
                            br_formula += '81'.translate(subscript) + 'Br' + str(int(num_br81))
                    l_br_formula.append(br_formula)
                else:
                    l_br_formula.append(0)

            else:
                i[j] = int(i[j]/l_main_mass[j])

    d_mass_main_formula = {}
    for i in range(len(combination_mass)):
        a_formula = ''
        for j in range(num_atoms):
            if j == index_cl and l_cl_formula[i] != 0:
                a_formula += l_cl_formula[i]
            elif j == index_br and l_br_formula[i] != 0:
                a_formula += l_br_formula[i]
            else:
                if combination_mass[i][j] != 0:
                    if combination_mass[i][j] == 1: 
                        a_formula += (str(l_main_mass[j]).translate(subscript) + l_atom_name[j])
                    else:
                        a_formula += (str(l_main_mass[j]).translate(subscript) + l_atom_name[j]) + str(combination_mass[i][j])
        if l_charge_mass_ratio[i] not in d_mass_main_formula.keys():
            d_mass_main_formula[l_charge_mass_ratio[i]] = [a_formula]
        else:
            d_mass_main_formula[l_charge_mass_ratio[i]].append(a_formula)
    #print(d_mass_main_formula.items())




    # One atom with minorabundance mass in the formula

    l_rest_mass = []
    for i in original_data[name]['charge_mass_ratio']:
        if i not in d_mass_main_formula.keys():
            l_rest_mass.append(i)

    index_special_atoms = [index_br,index_cl]
    for i in range(num_atoms):
        if i in index_special_atoms:
            continue
        else:
            if l_other_mass[i] != []:
                for j in l_other_mass[i]:
                    minority_mass = j[0]

                    changed_atom = list(np.array(possible_main_mass[i])[1:] - l_main_mass[i] + minority_mass)
                    changed_atom.insert(0,0)
                    possible_mass_1 = possible_main_mass.copy()
                    possible_mass_1[i] = changed_atom

                    l_charge_mass_ratio, combination_mass = find_possible_combination(possible_mass_1, l_rest_mass)


                    for k in combination_mass:
                        for h in range(num_atoms):
                            if h == i:
                                if k[i] != 0:
                                    k[i] = int((k[h]-minority_mass)/l_main_mass[h])
                            elif h == index_cl:
                                if k[h] != 0:
                                    cl_formula=''
                                    if k[h]%35 == 0:
                                        num_cl37 = 0
                                        num_cl35 = k[h]/35
                                    else:
                                        num_cl37 = (k[h]%35)/2
                                        num_cl35 = (k[h]-num_cl37*37)/35

                                    if num_cl35 != 0:
                                        if num_cl35 == 1:
                                            cl_formula += '35'.translate(subscript) + 'Cl'
                                        else:
                                            cl_formula += '35'.translate(subscript) + 'Cl' + str(int(num_cl35))
                                    if num_cl37 != 0:
                                        if num_cl37 == 1:
                                            cl_formula += '37'.translate(subscript) + 'Cl'
                                        else:
                                            cl_formula += '37'.translate(subscript) + 'Cl' + str(int(num_cl37))
                            elif h == index_br:
                                if k[h] != 0:
                                    br_formula=''

                                    if k[h]%79 == 0:
                                        num_br81 = 0
                                        num_br79 = k[h]/79
                                    else:
                                        num_br81 = (k[h]%79)/2
                                        num_br79 = (k[h]-num_br81*81)/79

                                    if num_br79 != 0:
                                        if num_br79 == 1:
                                            br_formula += '79'.translate(subscript) + 'Br'
                                        else:
                                            br_formula += '79'.translate(subscript) + 'Br' + str(int(num_br79))
                                    if num_br81 != 0:
                                        if num_br81 == 1:
                                            br_formula += '81'.translate(subscript) + 'Br'
                                        else:
                                            br_formula += '81'.translate(subscript) + 'Br' + str(int(num_br81))

                            else:
                                k[h] = int(k[h]/l_main_mass[h])


                    for k in range(len(combination_mass)):
                        a_formula = ''
                        for h in range(num_atoms):
                            if h == index_cl and cl_formula != '':
                                a_formula += cl_formula
                            elif h == index_br and br_formula != '':
                                a_formula += br_formula
                            else:
                                if h == i:
                                    a_formula += str(minority_mass).translate(subscript)+ l_atom_name[h]
                                if combination_mass[k][h] != 0:
                                    if combination_mass[k][h] != 1:
                                        a_formula += (str(l_main_mass[h]).translate(subscript)+ l_atom_name[h]) + str(combination_mass[k][h])
                                    else:
                                        a_formula += (str(l_main_mass[h]).translate(subscript)+ l_atom_name[h])
                        if l_charge_mass_ratio[k] not in d_mass_main_formula.keys():
                            d_mass_main_formula[l_charge_mass_ratio[k]] = [a_formula]
                        else:
                            d_mass_main_formula[l_charge_mass_ratio[k]].append(a_formula)
            
    return d_mass_main_formula, possible_main_mass
#%%
for i in tqdm(original_data.keys()):
    try:
        total_peak_hegiht = np.sum(original_data[i]['peak_height'])
        branch_ratio = []
        l_most_mass = []
        for j in range(len(original_data[i]['charge_mass_ratio'])):
            a_ratio = original_data[i]['peak_height'][j]/total_peak_hegiht
            branch_ratio.append(a_ratio)
            if a_ratio >= 0.01:      # Set the minimum proportion of branching ratio
                l_most_mass.append(original_data[i]['charge_mass_ratio'][j])

        d_mass_formula, possible_main_mass = find_optional_fragments(i)

        l_rest_mass = []
        new_l_rest_mass = []
        for k in l_most_mass:
            if k not in d_mass_formula.keys():
                l_rest_mass.append(k)
        if l_rest_mass != []:
            new_l_rest_mass = [i*2 for i in l_rest_mass]

            l_charge_mass_ratio, combination_mass = find_possible_combination(possible_main_mass, new_l_rest_mass)
            
            if list(set(l_charge_mass_ratio)).sort() == new_l_rest_mass.sort():
                pass
            else:
                print(i, original_data[i]['formula'], l_rest_mass)
        


        l_optional_fragments = []
        for m in original_data[i]['charge_mass_ratio']:
            if m in d_mass_formula.keys():
                l_optional_fragments.append(d_mass_formula[m])
            elif m not in l_most_mass:
                l_optional_fragments.append('not important')
            else:
                l_optional_fragments.append('not found')
        
        processed_data[i] = original_data[i]
        processed_data[i]['optional_fragments'] = l_optional_fragments
        processed_data[i]['branch_ratio'] = branch_ratio

    except:
        print(i)
 # %%
find_optional_fragments('Benzene-D6')
find_optional_fragments('Silicon tetrachloride')
find_optional_fragments('Methane')
find_optional_fragments('Borane carbonyl')
find_optional_fragments('Benzene, chloro-') # C6 H5 Cl [56.0]
find_optional_fragments('Benzene, 1,2-propadienyl-') #C9 H8 [58.0]
find_optional_fragments('3,5-Diamino-1,2,4-triazole') #C2 H5 N5 [10.0]
find_optional_fragments('Naphthalene, 1,2,3,6,7,8-hexachloro-') #C10 H2 Cl6 [79.0, 115.0]
find_optional_fragments('Benzene,(chloroethynyl)-') #C8 H5 Cl [68.0, 69.0]
find_optional_fragments('Benzene, 1-bromo-2-fluoro-') #C6 H4 Br F [87.0, 88.0]
# %%
np.save('processed_data.npy', processed_data)
# %%
processed_data = np.load('processed_data.npy', allow_pickle=True).item()
# %%
