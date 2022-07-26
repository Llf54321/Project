import camelot
import re
import numpy as np

# get the information the table of Isotopic Masses and Natural Abundances
def add_mass_abundance(page, mass_abundance):
    """
    get the information from the table of Isotopic Masses and Natural Abundances

    parameters
    -------
    page: int
    the page number of stable-isotopes.pdf
    mass_abundance: dict
    atom formula - (mass, abundance)
    Returns
    -------
    expand the mass_abundance dict
    """
    
    
    tables = camelot.read_pdf('stable-isotopes.pdf',flavor='stream',pages=str(page))

    for i in range(3,len(tables[0].df[2])):
        x = re.findall(r'[0-9]+|[^0-9]+',tables[0].df[2].values[i])
        y = re.findall(r'[0-9]+|[^0-9]+',tables[0].df[7].values[i])
        if x != []:
            mass_1 = int(x[0])
            form_1 = x[1]
            if tables[0].df[4].values[i] != '*':
                abundance_1 = float(tables[0].df[4].values[i])
                if form_1 not in mass_abundance.keys():
                    mass_abundance[form_1] = [(mass_1,abundance_1)]
                else:
                    mass_abundance[form_1].append((mass_1,abundance_1))
            else:
                if form_1 not in mass_abundance.keys():
                    mass_abundance[form_1] = [(mass_1,0)]
                else:
                    mass_abundance[form_1].append((mass_1,0))
        if y != []:
            mass_2 = int(y[0])
            form_2 = y[1]
            if tables[0].df[9].values[i] != '*':
                abundance_2 = float(tables[0].df[9].values[i])
                if form_2 not in mass_abundance.keys():
                    mass_abundance[form_2] = [(mass_2,abundance_2)]
                else:
                    mass_abundance[form_2].append((mass_2,abundance_2))
            else:
                if form_2 not in mass_abundance.keys():
                    mass_abundance[form_2] = [(mass_2,0)]
                else:
                    mass_abundance[form_2].append((mass_2,0))

mass_abundance = {}

tables = camelot.read_pdf('stable-isotopes.pdf',flavor='stream',pages='1')

for i in range(5,len(tables[1].df[2])):
    x = re.findall(r'[0-9]+|[^0-9]+',tables[1].df[2].values[i])
    y = re.findall(r'[0-9]+|[^0-9]+',tables[1].df[7].values[i])
    if x != []:
        mass_1 = int(x[0])
        form_1 = x[1]
        if tables[1].df[4].values[i] != '*':
            abundance_1 = float(tables[1].df[4].values[i])
            if form_1 not in mass_abundance.keys():
                mass_abundance[form_1] = [(mass_1,abundance_1)]
            else:
                mass_abundance[form_1].append((mass_1,abundance_1))
        else:
            if form_1 not in mass_abundance.keys():
                mass_abundance[form_1] = [(mass_1,0)]
            else:
                mass_abundance[form_1].append((mass_1,0))
    if y != []:
        mass_2 = int(y[0])
        form_2 = y[1]
        if tables[1].df[9].values[i] != '*':
            abundance_2 = float(tables[1].df[9].values[i])
            if form_2 not in mass_abundance.keys():
                mass_abundance[form_2] = [(mass_2,abundance_2)]
            else:
                mass_abundance[form_2].append((mass_2,abundance_2))
        else:
            if form_2 not in mass_abundance.keys():
                mass_abundance[form_2] = [(mass_2,0)]
            else:
                mass_abundance[form_2].append((mass_2,0))

add_mass_abundance(2,mass_abundance)
add_mass_abundance(3,mass_abundance)
add_mass_abundance(4,mass_abundance)

tables = camelot.read_pdf('stable-isotopes.pdf',flavor='stream',pages='5')

for i in range(6,len(tables[0].df[2])):
    x = re.findall(r'[0-9]+|[^0-9]+',tables[0].df[2].values[i])

    if x != []:
        mass_1 = int(x[0])
        form_1 = x[1]
        if tables[0].df[4].values[i] != '*':
            abundance_1 = float(tables[0].df[4].values[i])
            if form_1 not in mass_abundance.keys():
                mass_abundance[form_1] = [(mass_1,abundance_1)]
            else:
                mass_abundance[form_1].append((mass_1,abundance_1))
        else:
            if form_1 not in mass_abundance.keys():
                mass_abundance[form_1] = [(mass_1,0)]
            else:
                mass_abundance[form_1].append((mass_1,0))

# Distinguish the main abundance mass
d_mass_abundance = dict.fromkeys(mass_abundance.keys(),{'main':[],'other':[]})

for mass in mass_abundance.keys():
    l_abundance = []
    for i in mass_abundance[mass]:
        l_abundance.append(i[1])
    main_index = l_abundance.index(max(l_abundance))

    d_mass_abundance[mass] = {'main':[mass_abundance[mass][main_index]]}
    del mass_abundance[mass][main_index]
    d_mass_abundance[mass]['other'] = mass_abundance[mass]

np.save('mass_abundance.npy', d_mass_abundance)
