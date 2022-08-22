#%%
import sqlite3
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import scipy.stats as ss
from sklearn import preprocessing

mass_abundance = np.load('mass_abundance.npy',allow_pickle=True).item()
name_ae = np.load('name_AE.npy', allow_pickle=True).item()

banned_molecules=['1,2-Ethanediol','Toluene','Benzenethiol','Acetaldehyde, hydroxy-','Fluoroacetic acid','Propiolic acid','Ethanol, 2-bromo-','Propanoic acid, 2-chloro-','Disulfide, dimethyl','Ethanol','Methyl Alcohol','Methylamine','Acetic acid, oxo-, methyl ester','Acetic acid, hydroxy-, methyl ester','1,3-Dioxolan-2-one']
total_branching_ratio=[]
total_mean_ae=[]
l_result = []
for n in tqdm(name_ae.keys()):
    if "'" in n:
        continue
    if n in banned_molecules:
        continue
    conn = sqlite3.connect('data-20.db')
    cur = conn.cursor()
    cur.execute("select charge_mass_ratio,branch_ratio,optional_fragment from main_data where name='{0}'".format(n))
    rows = cur.fetchall()
    a_df = pd.DataFrame(rows, columns=['charge_mass_ratio','branch_ratio','optional_fragment'])
    conn.close()
    a_df_ae = name_ae[n]
    l_ion = list(a_df_ae['ion'])
    if len(l_ion) == 1:
        continue
    l_ae = list(a_df_ae['AE'])
    l_mean_ae=[]
    for i in l_ae:
        l_mean_ae.append(float(re.findall(r'-?\d+\.?\d*e?-?\d*?', i)[0]))

    l_branch_ratio = []
    ind = 0
    for f in l_ion:
        d_possible_mass = {}
        if '[' not in f:
            if f == 'MOC3O3+':
                f = 'MoC3O3+'
            f = re.sub( r"([A-Z])", r" \1", f).split()
            f[-1] = f[-1][:-1]
        else:
            del l_mean_ae[ind]
            continue
        main_possible = 0
        for a_formula in f:
            a_atom = re.sub(u'([^\u0041-\u007a])','',a_formula)
            a_num = re.sub(u'([^\u0030-\u0039])','',a_formula)
            if a_num == '':
                a_num = 1
            main_possible += mass_abundance[a_atom]['main'][0][0]*int(a_num)
        d_possible_mass[main_possible] = 1

        for a_formula in f:
            a_atom = re.sub(u'([^\u0041-\u007a])','',a_formula)
            a_num = re.sub(u'([^\u0030-\u0039])','',a_formula)
            l_other_mass = mass_abundance[a_atom]['other']
            if l_other_mass != []:
                for a_other in l_other_mass:
                    if a_other[1] == 0:
                        continue
                    elif a_other[0]-mass_abundance[a_atom]['main'][0][0]+main_possible not in d_possible_mass.keys():
                        d_possible_mass[a_other[0]-mass_abundance[a_atom]['main'][0][0]+main_possible] = 1
                    else:
                        d_possible_mass[a_other[0]-mass_abundance[a_atom]['main'][0][0]+main_possible] +=1

        a_branch_ratio = 0
        for a_possible_mass in d_possible_mass.keys():
            if a_possible_mass not in a_df['charge_mass_ratio'].values:
                continue
            num_optional_fragment = len(str(a_df[a_df['charge_mass_ratio']==a_possible_mass]['optional_fragment'].values[0]).split(','))
            if d_possible_mass[a_possible_mass] > num_optional_fragment:
                continue
            else:
                a_branch_ratio += a_df[a_df['charge_mass_ratio']==a_possible_mass]['branch_ratio'].values[0]*d_possible_mass[a_possible_mass]/num_optional_fragment
        if a_branch_ratio == 0:
            del l_mean_ae[ind]
            continue
        l_branch_ratio.append(a_branch_ratio)
        ind +=1

    total_branching_ratio.extend(l_branch_ratio)
    total_mean_ae.extend(l_mean_ae)


#%%
branching_ratio=np.array(total_branching_ratio)
mean_ae=np.array(total_mean_ae)
# %%
import matplotlib.pylab as plt
from numpy import polyfit, poly1d
from scipy.optimize import curve_fit
import math
def __sst(y_no_fitting):
    y_mean = sum(y_no_fitting) / len(y_no_fitting)
    s_list =[(y - y_mean)**2 for y in y_no_fitting]
    sst = sum(s_list)
    return sst

def __ssr(y_fitting, y_no_fitting):
    y_mean = sum(y_no_fitting) / len(y_no_fitting)
    s_list =[(y - y_mean)**2 for y in y_fitting]
    ssr = sum(s_list)
    return ssr

def r_squared(y_no_fitting, y_fitting):
    SSR = __ssr(y_fitting, y_no_fitting)
    SST = __sst(y_no_fitting)
    rr = 1 - SSR /SST
    return rr

def compute_rms(mu_1, mu_2):
    MSE = np.square(mu_1-mu_2).sum()/len(mu_1)
    RMSE = np.sqrt(MSE)
    return RMSE

def f1(x,a,b,c):
    result = a*x**2+b*x+c
    return result
def f2(x,a,b):
    result = a*x+b
    return result
def f3(x, a,u, sig):
    result = a*np.exp(-(x - u) ** 2 / (2 * sig ** 2)) / (sig * math.sqrt(2 * math.pi))
    return result
def f4(x,a,b):
    result = a*x**(-3)+b
    return result
def regression(x,y,function):
    mean = sum(x * y) / sum(y)
    sigma = np.sqrt(sum(y * (x - mean)**2) / sum(y))
    p_est, err_est = curve_fit(function, x, y,maxfev=360000)

    plt.figure(figsize=(20,8))
    plt.plot(np.sort(x), function(np.sort(x), *p_est), "k--")
    plt.scatter(x,y)
    plt.xlabel('appearance energy')
    plt.ylabel('branching ratio')
    if function == f1:
        plt.savefig('quadratic regression')
    elif function == f2:
        plt.savefig('linear regression')
    elif function == f3:
        plt.savefig('Gaussian regression')
    plt.show()
    
    print('params:',p_est)
    print('Root Mean Square Error =',compute_rms(y,function(x, *p_est)))
    print('R_squared =',r_squared(y,function(x, *p_est)))

regression(mean_ae,branching_ratio,f1)
regression(mean_ae,branching_ratio,f2)
regression(mean_ae,branching_ratio,f3)
regression(mean_ae,branching_ratio,f4)
r,p = ss.pearsonr(mean_ae,branching_ratio)
print('Correlation coefficient =',r,'p-value =',p)

# %%
