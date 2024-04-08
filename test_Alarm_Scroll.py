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
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
action = ActionChains(driver=driver)



def read_special_row(driver_nms, row):
    text_of_one_row_in_all_columns_of_its  = []
    rows = Wait_For_Appearance_whole_of_something(driver_nms, 'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    logger.info(f"len of rows {len(rows)}")
    index = (4,5,8,9,11)
    for i in index:
        text_of_element = Wait_For_Appearance(driver_nms,'xpath', f"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr[{row}]//td[{i}]//div[@class='record']").text
        text_of_one_row_in_all_columns_of_its .append(text_of_element)
    return  text_of_one_row_in_all_columns_of_its  

def go_to_current_Alarm(driver_nms):
    Fault = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='alarm-menu']//span")
    Fault.click() 
    Current_Alarm = Wait_For_Appearance(driver_nms,'xpath',"//div[@data-node-key='currentAlarm'][contains(.,'Current Alarm')]")  
    assert Current_Alarm.text=="Current Alarm"
    Current_Alarm.click()
    assert Current_Alarm.get_attribute('class') == 'ant-tabs-tab ant-tabs-tab-active'
    footer = Wait_For_Appearance(driver_nms,'id', "//div[@data-test-id='alarm_page']//div[@data-test-id='alarm_footer']")
    
    current_alarm = Wait_For_Appearance(driver_nms, "xpath", "//div[@data-test-id='current-rows']")
    number_of_current_alarm = current_alarm.get_attribute('data-value')
    logger.info(f"number_of_current_alarm {number_of_current_alarm}")

    total_alarm = Wait_For_Appearance(driver_nms, "xpath", "//div[@data-test-id='total-rows']")
    number_of_total_alarm = total_alarm.get_attribute('data-value')
    logger.info(f"number_of_total_alarm {number_of_total_alarm}")

    assert number_of_current_alarm != '0' and number_of_current_alarm != ''
    assert number_of_total_alarm != '0' and number_of_total_alarm != ''
    assert int(number_of_current_alarm) <= int(number_of_total_alarm) 

    item = Wait_For_Appearance(driver_nms, "xpath", "//div[@data-test-id='selected-rows']//span")
    assert item.get_attribute('data-value') == '0'
    table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
    assert table != None
    rows = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")


def scroll_action(driver_nms):
    counter_before_scroll = 0
    counter_after_scroll = 0
    table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
    rows_before_scroll = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    assert rows_before_scroll != 0
    if table != None:
        first_row_before_scroll = read_special_row(driver_nms, 2)
    for i in range(0,25):
        driver_nms.execute_script("document.querySelector('div tbody tr:last-child td:last-child').scrollIntoView()")        
    rows_after_scroll = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
    if table != None:
        first_row_after_scroll = read_special_row(driver_nms, 2)
    assert len(rows_after_scroll) != 0
    assert first_row_after_scroll != first_row_before_scroll    
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



def test_alarm_scroll(driver=driver):
    LOGIN(driver, login(1,{'url':'http://192.168.5.183/auth/login', 'password' :"root", 'user':'root'}, 'Pass'))
    go_to_current_Alarm(driver_nms=driver)
    scroll_action(driver_nms=driver)
