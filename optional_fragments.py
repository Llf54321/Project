#%%
import numpy as np
import re
from tqdm import tqdm

def find_possible_combination(possible_mass, mass_list):
    """
    Find combinations of multiple series that sum to a specific value

    parameters
    -------
    possible_mass: list
    the possible mass of an atom
    mass_list: list
    the list of target mass
    Returns
    -------
    l_charge_mass_ratio: list
    The list of target mass that has been found
    combination_mass: list
    The list of possible combination mass
    """
    
    
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

def build_cl_br_formula(mass, atom_name):
    """
    find the Cl or Br formula based on the mass of Cl or Br

    parameters
    -------
    mass: int
    the mass of Cl or Br in the optional fragment
    atom_name: str
    'Cl' or 'Br'
    Returns
    -------
    formula: str
    the formula of Cl or Br in the optional fragment
    """
        
    subscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    formula=''

    if atom_name not in ['Cl','Br']:
        raise ValueError('atom should be Cl or Br.')

    if atom_name == 'Cl':
        if mass%35 == 0:
            num_cl37 = 0
            num_cl35 = mass/35
        else:
            num_cl37 = (mass%35)/2
            num_cl35 = (mass-num_cl37*37)/35

        if num_cl35 != 0:
            if num_cl35 == 1:
                formula += '35'.translate(subscript) + 'Cl'
            else:
                formula += '35'.translate(subscript) + 'Cl' + str(int(num_cl35))
        if num_cl37 != 0:
            if num_cl37 == 1:
                formula += '37'.translate(subscript) + 'Cl'
            else:
                formula += '37'.translate(subscript) + 'Cl' + str(int(num_cl37))

    elif atom_name == 'Br':
        if mass%79 == 0:
            num_br81 = 0
            num_br79 = mass/79
        else:
            num_br81 = (mass%79)/2
            num_br79 = (mass-num_br81*81)/79

        if num_br79 != 0:
            if num_br79 == 1:
                formula += '79'.translate(subscript) + 'Br'
            else:
                formula += '79'.translate(subscript) + 'Br' + str(int(num_br79))
        if num_br81 != 0:
            if num_br81 == 1:
                formula += '81'.translate(subscript) + 'Br'
            else:
                formula += '81'.translate(subscript) + 'Br' + str(int(num_br81))

    return formula

def find_atom_name_num(formula):
    """
    find the atom name and number in the molecule

    parameters
    -------
    formula: str
    the molecule formula
    Returns
    -------
    l_atom_name: list
    the list of atom names
    l_atom_num: list
    the list of atom numbers
    """
    
    
    l_atom_name = []
    l_atom_num = []
    for i in formula.split():
        l_atom_name.append(re.findall(r'[0-9]+|[^0-9]+',i)[0])
        try:
            l_atom_num.append(int(re.findall(r'[0-9]+|[^0-9]+',i)[1]))
        except:
            l_atom_num.append(1)
    return l_atom_name,l_atom_num
        
def find_optional_fragments(data,name):
    """
    find the optional fragments of a molecule

    parameters
    -------
    data: dict
    conclude all imformation of original data
    name: str
    the molecule name
    Returns
    -------
    d_mass_main_formula: dict
    charge/mass ratio - optional fragments
    possible_main_mass: list
    charge/mass ratio which can be found by atoms with the most abundance
    """
    
    
    subscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    formula = data[name]['formula']
    num_atoms = len(formula.split())
    l_atom_name,l_atom_num = find_atom_name_num(formula)
    
    l_other_mass = []
    l_main_mass = []
    for atom in l_atom_name:
        l_other_mass.append(mass_abundance[atom]['other'])
        l_main_mass.append(mass_abundance[atom]['main'][0][0])

    # All atoms in the formula are the most abundance
    index_cl = -1
    index_br = -1

    possible_main_mass = []
    for index_atoms in range(num_atoms):
        a_possible_mass = []
        for n in range(l_atom_num[index_atoms]+1):
            a_possible_mass.append(n*l_main_mass[index_atoms])
            if l_atom_name[index_atoms] == 'Cl':
                index_cl = index_atoms
                for k in range(n+1):
                    if k != 0:
                        a_possible_mass.append(n*l_main_mass[index_atoms]+2*k)
            elif l_atom_name[index_atoms] == 'Br':
                index_br = index_atoms
                for k in range(n+1):
                    if k != 0:
                        a_possible_mass.append(n*l_main_mass[index_atoms]+2*k)
        possible_main_mass.append(a_possible_mass)

    l_charge_mass_ratio, combination_mass = find_possible_combination(possible_main_mass, data[name]['charge_mass_ratio'])

    l_cl_formula = []
    l_br_formula = []
    for a_combination in combination_mass:
        for index_atoms in range(num_atoms):
            if index_atoms == index_cl:
                if a_combination[index_atoms] != 0:
                    cl_formula = build_cl_br_formula(a_combination[index_atoms],'Cl')
                    l_cl_formula.append(cl_formula)
                else:
                    l_cl_formula.append(0)

            elif index_atoms == index_br:
                if a_combination[index_atoms] != 0:
                    br_formula=build_cl_br_formula(a_combination[index_atoms],'Br')
                    l_br_formula.append(br_formula)
                else:
                    l_br_formula.append(0)

            else:
                a_combination[index_atoms] = int(a_combination[index_atoms]/l_main_mass[index_atoms])

    d_mass_main_formula = {}
    for index_combination in range(len(combination_mass)):
        a_formula = ''
        for index_atoms in range(num_atoms):
            if index_atoms == index_cl and l_cl_formula[index_combination] != 0:
                a_formula += l_cl_formula[index_combination]
            elif index_atoms == index_br and l_br_formula[index_combination] != 0:
                a_formula += l_br_formula[index_combination]
            else:
                if combination_mass[index_combination][index_atoms] != 0:
                    if combination_mass[index_combination][index_atoms] == 1: 
                        a_formula += (str(l_main_mass[index_atoms]).translate(subscript) + l_atom_name[index_atoms])
                    else:
                        a_formula += (str(l_main_mass[index_atoms]).translate(subscript) + l_atom_name[index_atoms]) + str(combination_mass[index_combination][index_atoms])
        if l_charge_mass_ratio[index_combination] not in d_mass_main_formula.keys():
            d_mass_main_formula[l_charge_mass_ratio[index_combination]] = [a_formula]
        else:
            d_mass_main_formula[l_charge_mass_ratio[index_combination]].append(a_formula)




    # One atom with minorabundance mass in the formula

    l_rest_mass = []
    for a_charge_mass_ratio in data[name]['charge_mass_ratio']:
        if a_charge_mass_ratio not in d_mass_main_formula.keys():
            l_rest_mass.append(a_charge_mass_ratio)

    index_special_atoms = [index_br,index_cl]
    for index_atoms in range(num_atoms):
        if index_atoms in index_special_atoms:
            continue
        else:
            if l_other_mass[index_atoms] != []:
                for a_other in l_other_mass[index_atoms]:
                    if a_other[1] == 0:
                        continue
                    else:
                        minority_mass = a_other[0]

                        changed_atom = list(np.array(possible_main_mass[index_atoms])[1:] - l_main_mass[index_atoms] + minority_mass)
                        changed_atom.insert(0,0)
                        possible_mass_1 = possible_main_mass.copy()
                        possible_mass_1[index_atoms] = changed_atom

                        l_charge_mass_ratio, combination_mass = find_possible_combination(possible_mass_1, l_rest_mass)


                        for k in combination_mass:
                            for h in range(num_atoms):
                                if h == index_atoms:
                                    if k[index_atoms] != 0:
                                        k[index_atoms] = int((k[h]-minority_mass)/l_main_mass[h])
                                elif h == index_cl:
                                    if k[h] != 0:
                                        cl_formula=build_cl_br_formula(k[h],'Cl')
                                elif h == index_br:
                                    if k[h] != 0:
                                        br_formula=build_cl_br_formula(k[h],'Br')

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
                                    if h == index_atoms:
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

def process_data(data, min_branching_ratio):
    """
    Find the optional fragments and branching ratio for all molecules

    parameters
    -------
    data: dict
    conclude all imformation of original data
    min_branching_ratio: float
    the minimum proportion of branching ratio
    Returns
    -------
    processed_data: dict
    the original data with optional fragments and branching ratio
    """
    
    
    processed_data = {}
    for a_name in tqdm(data.keys()):
        l_atoms_name,l_atoms_num = find_atom_name_num(data[a_name]['formula'])
        if 'D' in l_atoms_name:
            continue

        total_peak_hegiht = np.sum(data[a_name]['peak_height'])
        branch_ratio = []
        l_most_mass = []
        for j in range(len(data[a_name]['charge_mass_ratio'])):
            a_ratio = data[a_name]['peak_height'][j]/total_peak_hegiht
            branch_ratio.append(a_ratio)
            if a_ratio >= min_branching_ratio:      # Set the minimum proportion of branching ratio
                l_most_mass.append(data[a_name]['charge_mass_ratio'][j])

        d_mass_formula, possible_main_mass = find_optional_fragments(data,a_name)

        l_rest_mass = []
        new_l_rest_mass = []
        for a_mass in l_most_mass:
            if a_mass not in d_mass_formula.keys():
                l_rest_mass.append(a_mass)
        if l_rest_mass != []:
            new_l_rest_mass = [i*2 for i in l_rest_mass]

            l_charge_mass_ratio, combination_mass = find_possible_combination(possible_main_mass, new_l_rest_mass)
            
            if list(set(l_charge_mass_ratio)).sort() == new_l_rest_mass.sort():
                pass
            else:
                print(a_name, data[a_name]['formula'], l_rest_mass)
        


        l_optional_fragments = []
        for m in data[a_name]['charge_mass_ratio']:
            if m in d_mass_formula.keys():
                l_optional_fragments.append(d_mass_formula[m])
            elif m not in l_most_mass:
                l_optional_fragments.append('the branch ratio is less than 1%')
            else:
                l_optional_fragments.append('possible double ionisation peak')
        
        processed_data[a_name] = data[a_name]
        processed_data[a_name]['optional_fragments'] = l_optional_fragments
        processed_data[a_name]['branch_ratio'] = branch_ratio

    return processed_data

# %%
if __name__ == '__main__':
    original_data = np.load('new_data.npy', allow_pickle=True).item()
    mass_abundance = np.load('mass_abundance.npy',allow_pickle=True).item()

    processed_data = process_data(original_data,0.01)
    np.save('processed_data.npy', processed_data)
