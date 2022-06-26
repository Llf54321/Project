def check_element_exists(driver, element):
    try:
        driver.find_element_by_xpath(element)
        return True
    except Exception as e:
        return False

def download_data(driver):
    if check_element_exists(driver,'/html/body/main/div[3]/p[3]/a'):
        driver.find_element_by_xpath('/html/body/main/div[3]/p[3]/a').click()
        driver.back()
    else:
        driver.back()


def find_data(driver,formula):
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