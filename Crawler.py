from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

RECORD_SELECTOR = "#qs-rankings_length > label > select"
TAG_XPATH ="//*[@id=\"block-system-main\"]/div/div/div/div[1]/div/div/div[13]/div/div/ul/li[2]/a"
SELECT_XPATH = """//*[@id="qs-rankings_length"]/label/select/option[@value='-1']"""
print(SELECT_XPATH)
# Create a new instance of the Firefox driver""
driver = webdriver.Chrome()

# go to the google home page
driver.get("https://www.topuniversities.com/university-rankings/world-university-rankings/2018")
driver.implicitly_wait(5)


try:
    
    
    driver.execute_script("document.getElementsByName('qs-rankings_length')[0].removeAttribute('class');")
    time.sleep(3)
    driver.execute_script("document.getElementsByName('qs-rankings_length')[0].value=-1;")
    element = driver.find_element_by_xpath(TAG_XPATH)
    driver.execute_script("arguments[0].click();", element)

    # driver.execute_script("arguments[0].click();", _select)
    #_option = driver.find_element_by_xpath(SELECT_XPATH)
   
    data_rows = driver.find_elements_by_css_selector("#qs-rankings-indicators > tbody tr")
    for item in data_rows:
        _rowArray = item.text.split('\n')
        print([t for t in _rowArray])
finally:
    driver.quit()