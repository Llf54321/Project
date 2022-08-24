from crawler_method import find_data
from tqdm import tqdm
from selenium import webdriver

# Obtain the list of formulas
def obtain_list_of_formulas(species_list):
    """
    Obtain the list of formulas

    parameters
    -------
    species_list: txt file
    a txt file contains species list data
    
    Returns
    -------
    l_formula: list
    the list of species formula is needed to search in the website
    """

    with open(species_list,'r',encoding='utf-8') as f:
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
    return l_formula

# Crawl the data from the website
def crawl_data(l_formula, path_folder_to_store, chrome_driver_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'):
    """
    Scrawl original .jdx files from website.

    parameters
    -------
    l_formula: list
    the list of formula need to be scraped
    path_folder_to_store: string
    the path of the folder to store original data
    chrome_driver_path: string
    the path of Chrome driver
    
    Returns
    -------
    not_been_found_f: list
    the list of formula were not scraped due to some bug
    """
    
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': path_folder_to_store}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome(chrome_driver_path,options=options)

    driver.get("https://webbook.nist.gov/chemistry/form-ser/")

    not_been_found_f=[]
    for f in tqdm(l_formula):
        try:
            find_data(driver,f)
        except:
            not_been_found_f.append(f)

            driver.close()

            driver = webdriver.Chrome(chrome_driver_path,options=options)
            driver.get("https://webbook.nist.gov/chemistry/form-ser/")
    driver.close()

    return not_been_found_f

if __name__ == '__main__':
    l_formula = obtain_list_of_formulas('species.txt')
    not_been_found_formula = crawl_data(l_formula,r'C:\Users\46003\Desktop\project\data','F:\chromedriver_win32\chromedriver.exe')

    while not_been_found_formula != []:
        not_been_found_formula = crawl_data(not_been_found_formula)
    print('Finished')
