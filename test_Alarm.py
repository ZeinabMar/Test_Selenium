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


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
action = ActionChains(driver=driver)


def enter_to_plate_alarm(driver_nms):
    Fault = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='alarm-menu']//span")
    Fault.click() 
    Current_Alarm = Wait_For_Appearance(driver_nms,'xpath',"//div[@data-test-id='alarm_page']//div[@data-node-key='currentAlarms']")  
    assert Current_Alarm.text=="currentAlarms"
    Current_Alarm.click()
    assert Current_Alarm.get_attribute('class') == 'ant-tabs-tab ant-tabs-tab-active'
    footer = driver.find_element('xpath', "//div[@data-test-id='alarm_page']//div[@data-test-id='alarm_footer'']")
    rows = driver.find_element('xpath', "//div[@data-test-id='alarm_page']//div[@data-test-id='alarm_footer']//div[@data-test-id='total-rows']//span")
    assert rows.text != '0' and rows.text != ''
    item = driver.find_element('xpath', "//div[@data-test-id='alarm_page']//div[@data-test-id='alarm_footer']//div[@data-test-id='selected-rows']//span")
    assert item.get_attribute('data-value') == '0'
    #************************** Tset Scroll *************************************************
    el1 = driver_nms.find_element('xpath', "//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr[1]")
    el2 = driver_nms.find_element('xpath', "//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr[last()]")
    # table = driver_nms.find_elements('xpath', "//div[@class='ant-table-body']//tbody[@class='ant-table-tbody//tr[:]']")
    # logger.info(f"table {table}")
    # data_row_key = el2.get_attribute('data-row-key')
    # logger.info(f"numbeeer {data_row_key}")
    
    # table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
    if table !=None: 
        lenOfTable_before_scroll = driver_nms.execute_script("return document.querySelector('.ant-table-tbody').rows.length")
        logger.info(f"lenOfTable {lenOfTable_before_scroll}")
        sleep(3)
        driver_nms.execute_script("document.querySelector('div tbody tr:last-child td:last-child').scrollIntoView()")
        table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
        sleep(10)
        lenOfTable_after_scroll = driver_nms.execute_script("return document.querySelector('.ant-table-tbody').rows.length")
        assert lenOfTable_after_scroll!=lenOfTable_before_scroll
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
    sleep(10)
    



def test_alarm(driver=driver):
    LOGIN(driver, login(1,{'url':'http://192.168.5.190:3000/auth/login', 'password' :"root", 'user':'root'}, 'Pass'))
#     enter_to_plate_alarm(driver)
    enter_to_plate_alarm(driver_nms=driver)
