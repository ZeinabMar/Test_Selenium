#!/usr/bin/env python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from collections import namedtuple
from time import sleep
import time
import pytest
import logging
from conftest import *
from collections import namedtuple
from test_login import LOGIN,login
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
# action = ActionChains(driver=driver)

pytestmark = [pytest.mark.env_name("NMS_env"), pytest.mark.web_dev("olt_nms")]


def read_special_row(driver_nms, row):
    text_of_one_row_in_all_columns_of_its  = []
    rows = Wait_For_Appearance_whole_of_something(driver_nms, 'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    logger.info(f"len of rows {len(rows)}")
    index = (4,5,8,9,11)
    for i in index:
        text_of_element = Wait_For_Appearance(driver_nms,'xpath', f"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr[{row}]//td[{i}]//div[@class='record']").text
        text_of_one_row_in_all_columns_of_its .append(text_of_element)
    return  text_of_one_row_in_all_columns_of_its  

def go_to_current_Alarm(web_interface_module):
    driver_nms = web_interface_module.driver
    Fault = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='alarm-menu']//span")
    Fault.click() 
    Current_Alarm = Wait_For_Appearance(driver_nms,'xpath',"//div[@data-test-name='Current Alarm']")  
    Current_Alarm_label = Wait_For_Appearance(driver_nms,'xpath',"//div[@data-node-key='currentAlarm']")  
    assert Current_Alarm.text=="Current Alarm"
    Current_Alarm_label.click()
    assert Current_Alarm_label.get_attribute('class') == 'ant-tabs-tab ant-tabs-tab-active'
    
    footer = Wait_For_Appearance(driver_nms,'id', "//div[@data-test-id='alarm_page']//div[@data-test-id='alarm_footer']")
    total_alarm_in_footer = Wait_For_Appearance(driver_nms, "xpath", "//div[@data-test-id='total-rows']")
    number_of_total_alarm = total_alarm_in_footer.get_attribute('data-value')
    logger.info(f"number_of_total_alarm {number_of_total_alarm}")

    assert number_of_total_alarm != '0' and number_of_total_alarm != ''
    item = Wait_For_Appearance(driver_nms, "xpath", "//div[@data-test-id='selected-rows']//span")
    assert item.get_attribute('data-value') == '0'
    # table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
    rows = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@cl//div[@data-test-name='current_alarm_table']//tbody[@class='ant-table-tbody']//tr")
    assert rows != None

    
def read_content_of_column(driver_nms, number_of_column):
    text_of_rows = []
    rows = driver_nms.find_elements('xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    logger.info(f"len of rows {len(rows)}")
    for i in range(1,len(rows)):
        text_of_element = Wait_For_Appearance(driver_nms,'xpath', f"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr[{i+1}]//td[{number_of_column}]//div[@class='record']").text
        text_of_rows.append(text_of_element)
    driver_nms.implicitly_wait(20)
    return  text_of_rows 

def scroll_action(web_interface_module, number_of_td_th):
    driver_nms = web_interface_module.driver
    counter_before_scroll = 0
    counter_after_scroll = 0
    sleep(2)
    table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
    rows_before_scroll = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    assert rows_before_scroll != 0
    read_content_of_row_before_scroll = read_content_of_column(driver_nms, number_of_column = number_of_td_th)
    if table != None:
        first_row_before_scroll = read_special_row(driver_nms, 2)       
    for i in range(0,3):
        driver_nms.execute_script("document.querySelector('div tbody tr:last-child td:last-child').scrollIntoView()")        
    sleep(2)
    rows_after_scroll = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
    if table != None:
        first_row_after_scroll = read_special_row(driver_nms, 2)
    assert len(rows_after_scroll) != 0
    assert first_row_after_scroll != first_row_before_scroll   
    read_content_of_row_after_scroll = read_content_of_column(driver_nms, number_of_column = number_of_td_th)
    assert read_content_of_row_after_scroll != read_content_of_row_before_scroll
    # logger.info(f"rows {rows}")
    # if table !=None: 
    #     lenOfTable = driver_nms.execute_script("return document.querySelector('.ant-table-tbody').rows.length")
    #     for row in rows:
    #         if row.is_displayed():
    #             counter_before_scroll = counter_before_scroll+1
    #     driver_nms.execute_script("document.querySelector('div tbody tr:last-child td:last-child').scrollIntoView()")
    #     sleep(3)
    #     for row in rows:
    #         if row.is_displayed():
    #             counter_after_scroll = counter_after_scroll+1
    #     if counter_before_scroll <101:
    #         assert counter_after_scroll==counter_before_scroll 
    #     else:
    #         assert counter_after_scroll!=counter_before_scroll 
    # sleep(3)           
        # hey = Sort_(driver_nms, rows, "Alarm Name")
        # for row in rows:
        #     element = driver_nms.find_element('xpath', f"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr[2]//td[3]//div")
        # logger.info(f"lenOfTable {lenOfTable_before_scroll}")
        # sleep(3)
        # driver_nms.execute_script("document.querySelector('div tbody tr:last-child td:last-child').scrollIntoView()")
        # table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
        # sleep(10)
        # lenOfTable_after_scroll = driver_nms.execute_script("return document.querySelector('.ant-table-tbody').rows.length")
        # assert lenOfTable_after_scroll!=lenOfTable_before_scroll
        
    # row = []
    # for i in range(lenOfTable):
    #     row[i] = driver.find_element('xpath',f"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr[{i+2}]")
    
    #******************************* Check number of Row shown as 0 item/ ... rows    
    # NumberOfRowInNMsShown = driver.find_element('xpath', "//div[@class='flex-col h-full']//div[@class='sc-khAlqs hycrtN']//p").text
    # logger.info(f"NumberOfRowInNMsShown {NumberOfRowInNMsShown}")
    # assert NumberOfRowInNMsShown.find(f"{lenOfTable}")
    
    

    # el2 = driver.find_element('css')data-row-key
    # driver.execute_script("document.querySelector('.ant-table-body').scrollT(0,600)")
    # driver.execute_script("document.querySelector('div tbody tr:last-child td:last-child').scrollIntoView()")

    # action.move_to_element(el1).click_and_hold().move_to_element(el2).release().perform()
    # action.scroll_to_element(el2)



def test_Current_Alarm_Scroll(web_interface_module):
    web_interface_module.get_url()
    LOGIN(web_interface_module, login(1,{'password' :"root", 'user':'root'}, 'Pass'))
    go_to_current_Alarm(web_interface_module)
    scroll_action(web_interface_module, number_of_td_th=4)
