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
from test_Alarm import go_to_current_Alarm
from selenium.webdriver.support.ui import Select



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
action = ActionChains(driver=driver)

filter_of_alarm_name = ["PON_LOS"]
filter_of_severity = []
filter_of_alarm_category = []
filter_of_node_name = []
filter_of_node_ip = []
filter_of_address = []
filter_of_acknowledge_user = []



def demontration_of_filter_toolbar(driver_nms):
    filter_icon = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-header']//th[@class='ant-table-cell filter-head']")  
    filter_icon.click()
    toolbars_filter = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-header']//tfoot[@class='ant-table-summary']")  
    all_element_in_filter_toolbar = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-header']//tfoot[@class='ant-table-summary']//tr[1]//td")  
    assert len(all_element_in_filter_toolbar) == 12
    

def read_content_of_column(driver_nms, number_of_column):
    text_of_rows = []
    rows = Wait_For_Appearance_whole_of_something(driver_nms, 'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    logger.info(f"len of rows {len(rows)}")
    for i in range(1,len(rows)):
        text_of_element = Wait_For_Appearance(driver_nms,'xpath', f"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr[{i+1}]//td[{number_of_column}]//div[@class='record']").text
        text_of_rows.append(text_of_element)
    return  text_of_rows   

def select_filter_menu(driver_nms, number_of_column):
    select_filter_icon_for_this_column = Wait_For_Appearance(driver_nms,'xpath',f"//div[@class='ant-table-header']//tfoot[@class='ant-table-summary']//tr[1]//td[{number_of_column}]")  
    select_filter_icon_for_this_column.click()

def correctness_applying_filter_check(driver_nms, filter, number_of_column):
    rows= []
    rows_text = read_content_of_column(driver_nms=driver_nms, number_of_column=number_of_column)
    for row in rows_text:
        assert row.find(filter)!=-1


def select_filter_in_one_column(driver_nms, action, number_of_column, all_filters):
    sroll =  Wait_For_Appearance(driver_nms, 'xpath', "//div[contains(@class,'ant-select-dropdown ant-slide-up-enter ant-slide-up-enter-active')]//div[@class='rc-virtual-list']//div[@class='rc-virtual-list-scrollbar rc-virtual-list-scrollbar-vertical']")
    filter_menues = Wait_For_Appearance(driver_nms, 'xpath', "//div[contains(@class,'ant-select-dropdown ant-slide-up-enter ant-slide-up-enter-active')]//div[@class='rc-virtual-list']//div[@class='rc-virtual-list-holder-inner']")
    for filter in all_filters:
        logger.info(f"my filter is {filter}")
        logger.info(f"//div[@title='{filter}']")
        filter_element = Wait_For_Appearance(driver_nms, 'xpath', f"//div[@title= '{filter}']")
        filter_element.click()
        apply_icon = Wait_For_Appearance(driver_nms, 'xpath', "//span[contains(.,'Apply Filter')]")
        apply_icon.click()
        sleep(2)
        correctness_applying_filter_check(driver_nms, filter, number_of_column)


def apply_filter_in_special_column(driver_nms, act, category, filters):
    if category == "Alarm Name":
        select_filter_menu(driver_nms, number_of_column=4)
        select_filter_in_one_column(driver_nms, action =act , number_of_column=4, all_filters=filters)
    # if category == "Alarm Category":
    #     Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=5)
    # if category == "Time Accurance":
    #     Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=6)       
    # if category == "Node IP":
    #     Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=8)            
    # if category == "Address":
    #     Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=9)            
    # if category == "Clear Time":
    #     Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=10)  
    # if category == "Acknowledge User":
    #     Sort_Process_For_Any_Column(driver_nms, action =act, number_of_td_th=11)              
    

def test_alarm(driver=driver):
    LOGIN(driver, login(1,{'url':'http://192.168.5.183/auth/login', 'password' :"root", 'user':'root'}, 'Pass'))
    go_to_current_Alarm(driver_nms=driver)
    demontration_of_filter_toolbar(driver_nms=driver)
    apply_filter_in_special_column(driver_nms=driver, act=action, category= "Alarm Name", filters=filter_of_alarm_name)
    
