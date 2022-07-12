from crawler_function import find_data
from tqdm import tqdm
from selenium import webdriver
import os

# Obtain the list of formulas
with open('species.txt','r',encoding='utf-8') as f:
    lines = f.read().splitlines()

name = []
formula = []
cas = []
for line in tqdm(lines):
    a = line.split('\t')
    name.append(a[0])
    formula.append(a[1])
    cas.append(a[2])

l_formula = list(set(formula))
l_formula.sort(key=formula.index)

# Crawl the data from the website
def crawl_data(options, l_formula):
    driver = webdriver.Chrome('F:\chromedriver_win32\chromedriver.exe',options=options)

    driver.get("https://webbook.nist.gov/chemistry/form-ser/")

    not_been_found_f=[]
    for f in tqdm(l_formula):
        try:
            find_data(driver,f)
        except:
            not_been_found_f.append(f)

            driver.close()

            driver = webdriver.Chrome('F:\chromedriver_win32\chromedriver.exe',options=options)
            driver.get("https://webbook.nist.gov/chemistry/form-ser/")
    driver.close()

    return not_been_found_f

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': r'C:\Users\46003\Desktop\project\data'}
options.add_experimental_option("prefs", prefs)
options.add_argument('blink-settings=imagesEnabled=false')


not_been_found_formula = crawl_data(options, l_formula)

while not_been_found_formula != []:
    not_been_found_formula = crawl_data(options, not_been_found_formula)
