def check_element_exists(driver, element):
    """
    Determines whether the element exists on the web page

    parameters
    -------
    driver: be used to simulate operations on the web
    element: str
    the xpath which need to be determined
    Returns
    -------
    True or False
    """
    try:
        driver.find_element_by_xpath(element)
        return True
    except Exception as e:
        return False

def download_data(driver):
    """
    Download the .jdx file

    parameters
    -------
    driver: be used to simulate operations on the web
    Returns
    -------
    Download the data
    """
    
    
    if check_element_exists(driver,'/html/body/main/div[3]/p[3]/a'):
        driver.find_element_by_xpath('/html/body/main/div[3]/p[3]/a').click()
        driver.back()
    else:
        driver.back()


def find_data(driver,formula):
    """
    Find and download the data of the formula

    parameters
    -------
    driver: be used to simulate operations on the web
    formula: str
    the formula needed to be scraped
    Returns
    -------
    formula: str
    the formula has been scraped
    """
    
    
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    driver.find_element_by_id('cMS').click()

    search_text = driver.find_element_by_id('Formula') 
    search_text.clear()
    search_text.send_keys(formula) 
    search_text.submit()

    if check_element_exists(driver, '/html/body/main/p[4]/a[1]'):
        try:
            driver.find_element_by_xpath('/html/body/main/div[3]/p[3]/a').click()
            driver.back()
        except:
            driver.back()
        driver.find_element_by_id('cMS').click()

    else:
        if check_element_exists(driver,'/html/body/main/p[2]/a'):
            driver.find_element_by_xpath('/html/body/main/p[2]/a').click()

        elif check_element_exists(driver,'/html/body/main/ol/li[1]/a'):
            driver.find_element_by_xpath('/html/body/main/ol/li[1]/a').click()
            download_data(driver)
            
            WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'/html/body/main/ol/li[2]/a')))

            driver.find_element_by_xpath('/html/body/main/ol/li[2]/a').click()
            download_data(driver)
            i = 3
            xpath = '/html/body/main/ol/li['+str(i)+']/a'
            while check_element_exists(driver,xpath) == True:
                driver.find_element_by_xpath(xpath).click()
                download_data(driver)
                i = i+1
                xpath = '/html/body/main/ol/li['+str(i)+']/a'
            driver.back()
            driver.find_element_by_id('cMS').click()
        
    return formula

def get_energy_vs_total_beb_table(driver,ind):
    """
    scrape the data of a molecule

    parameters
    -------
    driver: be used to simulate operations on the web
    ind: int
    the index of the molecule list
    Returns
    -------
    a_df: DataFrame
    the data table
    """
    
    
    import pandas as pd
    driver.get("https://physics.nist.gov/PhysRefData/Ionization/molTable.html")
    driver.find_element_by_xpath('/html/body/div[3]/div/table/tbody/tr/td[1]/form/select/option['+str(ind+1) +']').click()
    driver.find_element_by_xpath('/html/body/div[3]/div/table/tbody/tr/td[1]/form/input').click()
    name_formula = driver.find_element_by_xpath('/html/body/font/b').text
    l_n_f = name_formula.split('(')
    a_name = l_n_f[0][:-1]
    a_formula = l_n_f[1][:-1]
    driver.find_element_by_xpath('/html/body/p/table/tbody/tr[1]/td[1]/form/table/tbody/tr[3]/td/p/a[1]').click()
    table = driver.find_element_by_xpath('/html/body/table/tbody')
    rows = table.find_elements_by_tag_name("tr")

    name = [a_name]*len(rows)
    formula = [a_formula]*len(rows)
    energy = []
    beb = []
    for i in range(1,len(rows)):
        a_row = rows[i].find_elements_by_tag_name("td")
        energy.append(float(a_row[0].text))
        beb.append(float(a_row[1].text))

    a_df = pd.DataFrame(list(zip(name,formula,energy,beb)), columns = ['name','formula','energy','beb'])
    return a_df

def get_AE_table(driver,name):
    """
    scrape the AE data of a molecule and clean the table

    parameters
    -------
    driver: be used to simulate operations on the web
    name: str
    the molecule name
    Returns
    -------
    a_df_clear: DataFrame
    the table of cleaned AE data
    """
    
    
    import pandas as pd
    import re
    l_ion = []
    l_appearance_energy = []
    l_ion_formula= []
    driver.get("https://webbook.nist.gov/chemistry/name-ser/")
    driver.find_element_by_id('cIE').click()
    search_text = driver.find_element_by_id('Name') 
    search_text.send_keys(name) 
    search_text.submit()

    a_df_clear = pd.DataFrame()
    if check_element_exists(driver, "/html/body/main/table[@aria-label='Appearance energy determinations']/tbody"):
        table = driver.find_element_by_xpath("/html/body/main/table[@aria-label='Appearance energy determinations']/tbody")
        rows = table.find_elements_by_tag_name("tr")
        names = [name]*len(rows)
        for i in range(1,len(rows)):
            a_row = rows[i].find_elements_by_tag_name("td")
            l_ion.append(a_row[0].text)
            l_appearance_energy.append(a_row[1].text)
            if a_row[0].text not in l_ion_formula:
                l_ion_formula.append(a_row[0].text)
        
        a_df_unclear = pd.DataFrame(list(zip(names,l_ion,l_appearance_energy)), columns = ['name','ion','AE'])
        for a_ion_formula in l_ion_formula:
            a_part_df = a_df_unclear[a_df_unclear['ion']==a_ion_formula]
            a_mean_AE=[]
            for i in a_part_df['AE']:
                a_mean_AE.append(re.findall(r'-?\d+\.?\d*e?-?\d*?', i)[0])
            a_df_clear = a_df_clear.append(dict(a_part_df.iloc[a_mean_AE.index(min(a_mean_AE))]),ignore_index=True) # choose the lowest AE
    return a_df_clear