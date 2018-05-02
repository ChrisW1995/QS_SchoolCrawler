from selenium import webdriver
import xlsxwriter
from itertools import groupby
from operator import itemgetter
import time
import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0



web_local_str = ""
_groupCol = ["Year", "SchoolName", "Rank"] #For Group Use
_rowArray = []
_allRowsArray = []
RECORD_SELECTOR = "#qs-rankings_length > label > select"
TAG_XPATH = "//*[@id=\"block-system-main\"]/div/div/div/div[1]/div/div/div[13]/div/div/ul/li[2]/a"
SELECT_XPATH = """//*[@id="qs-rankings_length"]/label/select/option[@value='-1']"""
COLUMN_THEAD_XPATH = ""
now_year = int(datetime.datetime.now().year)
workbook = None
bold = None
driver = None

def getYear(_year):
    if _year == now_year:
        return _year
    else:
        return _year - 1

def getLocal(num):
    if num == 1:
        return ("""//*[@id="qs-rankings-indicators_wrapper"]/div[2]/div[2]/div[1]/div/table/thead/tr""", "asian")
    elif num == 2:
        return ("""//*[@id="qs-rankings-indicators_wrapper"]/div[2]/div[2]/div[1]/div/table/thead/tr""", "world")

while True:
    try:
        (COLUMN_THEAD_XPATH, web_local_str) = getLocal(int(input("Which data do you need? (1: asian; 2: world)：")))
        if web_local_str != "":
            _yearRangeArr = input("Enter what years range do you wanna get (seperate from space):").split(' ')
            if len(_yearRangeArr) != 2:
                print("Error range. Make sure you entered a correct range!")
            else:
                workbook = xlsxwriter.Workbook('QS SchoolRank_{0} {1}-{2}.xlsx'.format(web_local_str, _yearRangeArr[0], _yearRangeArr[1]))
                bold = workbook.add_format({'bold': True})           
                break
    except:
        print("Plz enter a correct string")
    
try:
    for _year in range(int(_yearRangeArr[0]), int(_yearRangeArr[1])+1):
        worksheet = workbook.add_worksheet(str(_year))
        print("---------------", _year, "---------------")
        web_year = getYear(_year)
        driver = webdriver.Chrome()
        driver.get("https://www.topuniversities.com/university-rankings/%s-university-rankings/%d" % (web_local_str, web_year))
        driver.implicitly_wait(2)  

        #Remove hidden class ensure select item could be click
        driver.execute_script("document.getElementsByName('qs-rankings_length')[0].removeAttribute('class');")
        driver.execute_script("document.getElementsByName('qs-rankings_length')[0].value=-1;")
        
        #Click the tag on the table to get all records
        element = driver.find_element_by_class_name("quicktabs-tab-rankings_tabs-1")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2)

        #Get all column
        column_rows = driver.find_element_by_xpath(COLUMN_THEAD_XPATH)
        _colArray = column_rows.text.split('\n')
        del _colArray[1] #del second column because it display current year.

        #Create excel column.
        _index = 0
        for item in (_colArray):
            worksheet.write_string(0, _index, item, bold)
            worksheet.set_column(0 , _index, len(item))
            _index += 1 
    
        data_rows = driver.find_elements_by_css_selector("#qs-rankings-indicators > tbody tr")    
        #Get data row from web and write to excel file
        print("|----------------------|", end = "\r")
        for _row in data_rows:
            _arr = _row.text.split('\n')
            print("|%s%d%s" % ("==" * int((len(_rowArray) / len(data_rows) * 10)), int(len(_rowArray) / len(data_rows) * 100) + 1, "%"), end="\r")
            _rowArray.append(_arr)
            _allRowsArray.append([_arr[1], _arr[0], _year])
            # print([t for t in _rowArray])
        print()
        row = 1
        col = 0
        for item in (_rowArray):
            print("Writing data...{0}/{1}".format(row , len(_rowArray)), end = "\r")       
            for index in range(0, len(item)):
                worksheet.write_string(row, col+index, item[index])
            row+=1
        _rowArray = []
        driver.quit()  
        print("\n")
finally:
   
    print("analyzing...")
    worksheet = workbook.add_worksheet("analysis")
    _allRowsArray = sorted(_allRowsArray, key=itemgetter(0))
    grouped = groupby(_allRowsArray, lambda x: x[0])

    col = 1
    for _year in range(int(_yearRangeArr[0]), int(_yearRangeArr[1])+1):
        worksheet.write_string(0, col, str(_year))
        col += 1
    
    row = 1
    for key, group in grouped:
        worksheet.write_string(row, 0, key)
        for thing in group:
            worksheet.write_string(row, thing[2] - int(_yearRangeArr[0]) + 1 , thing[1])
        row += 1
        
    workbook.close()
    driver.quit()
    print("Fetch data successfully. Enter any key to exit.")
    input()