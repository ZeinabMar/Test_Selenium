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


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
action = ActionChains(driver=driver)

def go_to_current_Alarm(driver_nms):
    Fault = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='alarm-menu']//span")
    Fault.click() 
    Current_Alarm = Wait_For_Appearance(driver_nms,'xpath',"//div[@data-test-id='alarm_page']//div[@data-node-key='currentAlarms']")  
    assert Current_Alarm.text=="currentAlarms"
    Current_Alarm.click()
    assert Current_Alarm.get_attribute('class') == 'ant-tabs-tab ant-tabs-tab-active'
    footer = driver.find_element('xpath', "//div[@data-test-id='alarm_page']//div[@data-test-id='alarm_footer']")
    rows = driver.find_element('xpath', "//div[@data-test-id='alarm_page']//div[@data-test-id='alarm_footer']//div[@data-test-id='total-rows']//span")
    logger.info(f"rooow {rows.get_attribute('data-value')}")
    number_of_alarm = rows.get_attribute('data-value')
    assert number_of_alarm != '0' and number_of_alarm != ''
    item = driver.find_element('xpath', "//div[@data-test-id='alarm_page']//div[@data-test-id='alarm_footer']//div[@data-test-id='selected-rows']//span")
    assert item.get_attribute('data-value') == '0'
    table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
    assert table != None


def scroll_action(driver_nms):
    counter_before_scroll = 0
    counter_after_scroll = 0
    table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
    rows = driver_nms.find_elements('xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    logger.info(f"rows {rows}")
    if table !=None: 
        lenOfTable = driver_nms.execute_script("return document.querySelector('.ant-table-tbody').rows.length")
        for row in rows:
            if row.is_displayed():
                counter_before_scroll = counter_before_scroll+1
        driver_nms.execute_script("document.querySelector('div tbody tr:last-child td:last-child').scrollIntoView()")
        sleep(3)
        for row in rows:
            if row.is_displayed():
                counter_after_scroll = counter_after_scroll+1
        if counter_before_scroll <101:
            assert counter_after_scroll==counter_before_scroll 
        else:
            assert counter_after_scroll!=counter_before_scroll 

    sleep(3)           
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

def sort_click(driver_nms, action, number_of_th):
    sort_element = driver_nms.find_element('xpath',f"//div[@class='ant-table-header']//thead[@class='ant-table-thead']//tr//th[{number_of_th}]")
    action.click(sort_element).perform()
    table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']") 
    rows = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")

def read_content_of_row(driver_nms, number_of_td):
    text_of_rows = []
    rows = driver_nms.find_elements('xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    for i in range(0,len(rows)):
        text_of_element = driver_nms.find_element('xpath', f"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr[{i+1}]//td[{number_of_td}]//div").text
        text_of_rows.append(text_of_element)
    return  text_of_rows   

def Sort_Process_For_Any_Column(driver_nms, action, number_of_td_th):
    read_before_sort = []
    read_after_sort = []
    sorted_given_content = []
    rows_after_sort = [] 
    rows_before_sort =[]

    rows_before_sort = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    assert len(rows_before_sort)!=0
    read_content_of_row_before_sort = read_content_of_row(driver_nms, number_of_td = number_of_td_th)
    assert len(read_content_of_row_before_sort)!=0
    sort_click(driver_nms= driver_nms, action=action, number_of_th=number_of_td_th)
    rows_after_sort = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    assert len(rows_after_sort) != 0
    assert len(rows_after_sort) == len(rows_before_sort)
    sorted_given_content = sorted(read_content_of_row_before_sort)
    read_content_of_row_after_sort = read_content_of_row(driver_nms, number_of_td = number_of_td_th)

    assert len(sorted_given_content) != 0
    logger.info(f"read_content_of_row_after_sort{read_content_of_row_after_sort}")
    logger.info(f"read_content_of_row_before_sort {read_content_of_row_before_sort}")
    logger.info(f"sorted_given_content {sorted_given_content}")
    assert len(rows_before_sort)==len(rows_after_sort)==len(sorted_given_content)
    for i in range(50):
        assert read_content_of_row_after_sort[i]==sorted_given_content[i], f"not match in {i+1} st ROW"    


def Manage_Sort_In_All_Columns(driver_nms, act, category):
    if category == "Alarm Name":
        Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=4)
    if category == "Alarm Category":
        Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=5)
    if category == "Time Accurance":
        Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=6)       
    if category == "Node IP":
        Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=8)            
    if category == "Address":
        Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=9)            
    if category == "Clear Time":
        Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=10)  
    if category == "Acknowledge User":
        Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=11)              
    

    


def test_alarm(driver=driver):
    LOGIN(driver, login(1,{'url':'http://192.168.5.190:3000/auth/login', 'password' :"root", 'user':'root'}, 'Pass'))
    go_to_current_Alarm(driver_nms=driver)
    Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Alarm Name")
    Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Alarm Category")
    Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Acknowledge User")
    Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Node IP")
    Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Address")
    Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Clear Time")
    Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Time Accurance")




    # scroll_action(driver_nms=driver)
