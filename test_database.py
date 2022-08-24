import pytest
import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path
from crawler_method import *
from selenium import webdriver
from optional_fragments import *

def test_atom_number_of_mass_abundances_table():
    d_mass_abundance = np.load('mass_abundance.npy', allow_pickle=True).item()
    assert len(d_mass_abundance) == 115

def test_sum_of_branching_ratio():
    conn = sqlite3.connect('data-20.db')
    cur = conn.cursor()
    cur.execute("select name, SUM(branch_ratio) from main_data GROUP BY name")
    rows = cur.fetchall()
    conn.close()
    df = pd.DataFrame(rows,columns=['name', 'sum_branching_ratio'])
    num_names = len(df['name'].values)
    branching_ratio = list(df['sum_branching_ratio'].values)
    for i in range(len(branching_ratio)):
        branching_ratio[i] = round(branching_ratio[i],5)
    assert branching_ratio == [1.0]*num_names

def test_number_of_molecules():
    conn = sqlite3.connect('data-20.db')
    cur = conn.cursor()
    cur.execute("select distinct name from partial_beb")
    num_molecule_with_partial_beb = len(list(cur))
    cur.execute("select distinct name from energy_vs_total_beb")
    num_molecule_with_total_beb = len(list(cur))
    cur.execute("select distinct name from appearance_energy_of_all_molecules")
    num_molecule_with_AE = len(list(cur))
    cur.execute("select distinct name from main_data")
    num_molecule_in_main_data = len(list(cur))
    conn.close()

    assert num_molecule_with_partial_beb == 41
    assert num_molecule_with_total_beb == 94
    assert num_molecule_with_AE == 1004
    assert num_molecule_in_main_data == 7122

def test_number_of_read_original_data():
    original_data = np.load('original_data.npy', allow_pickle=True).item()
    p = Path("/Users/46003/Desktop/project/data") 
    FileList=list(p.glob("*Mass.jdx"))
    assert len(original_data.keys()) == len(FileList)-2 # 17.alpha.-Hydroxyprogesterone and Uridine, 2TMS, TBDMS derivative have 2 Structures

def test_check_element_exists():
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': r'C:\Users\46003\Desktop\project\data'}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',options=options)

    driver.get("https://webbook.nist.gov/cgi/cbook.cgi?Formula=ch3bo&NoIon=on&Units=SI")
    assert check_element_exists(driver, '/html/body/main/p[4]/a[1]') == False
    assert check_element_exists(driver,'/html/body/main/p[2]/a') == False
    assert check_element_exists(driver,'/html/body/main/ol/li[1]/a') == True
    driver.close()

def test_get_energy_vs_total_beb_table():
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': r'C:\Users\46003\Desktop\project\data'}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',options=options)
    a_df = get_energy_vs_total_beb_table(driver,0)
    expected_beb = [0.0, 0.037, 0.1, 0.165, 0.231, 0.296, 0.36, 0.424, 0.583, 0.743, 0.901, 1.057, 1.21, 1.358, 1.503, 1.653, 1.8, 1.943, 2.082, 2.215, 2.344, 2.468, 2.587, 2.702, 2.812, 2.918, 3.019, 3.117, 3.211, 3.548, 3.834, 4.074, 4.289, 4.499, 4.683, 4.842, 4.979, 5.242, 5.416, 5.526, 5.587, 5.614, 5.614, 5.594, 5.561, 5.516, 5.464, 5.405, 5.343, 5.278, 5.211, 5.143, 5.075, 5.006, 4.938, 4.87, 4.803, 4.737, 4.672, 4.546, 4.424, 4.308, 4.197, 4.091, 3.989, 3.893, 3.801, 3.714, 3.63, 3.265, 2.969, 2.725, 2.52, 2.345, 2.195, 2.064, 1.949, 1.847, 1.756, 1.674, 1.6, 1.533, 1.471, 1.415, 1.315, 1.229, 1.155, 1.089, 1.031, 0.98, 0.933, 0.891, 0.853, 0.818, 0.787, 0.757, 0.73, 0.705, 0.682, 0.66, 0.64, 0.621, 0.603, 0.587, 0.461, 0.382]
    
    assert len(a_df.values) == 106
    assert a_df['name'][0] == 'Boron monochloride'
    assert a_df['formula'][0] == 'BCl'
    assert list(a_df['beb'].values) == expected_beb

def test_build_cl_br_formula():
    assert build_cl_br_formula(35, 'Cl') == '³⁵Cl'
    with pytest.raises(ValueError) as e:
        build_cl_br_formula(35, 'H')
    assert e.match('atom should be Cl or Br.')

def test_find_possible_combination():
    l_we_can_get, l_combination = find_possible_combination([[0,1,2,3],[3,6]], [5,6,10])
    assert l_we_can_get == [6, 5, 6]
    assert l_combination == [[0, 6], [2, 3], [3, 3]]
