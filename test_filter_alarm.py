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

def demontration_of_filter_toolbar(driver_nms):
    filter_icon = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-header']//th[@class='ant-table-cell filter-head']")  
    filter_icon.click()
    toolbars_filter = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-header']//tfoot[@class='ant-table-summary']")  
    all_element_in_filter_toolbar = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-header']//tfoot[@class='ant-table-summary']//tr[1]//td")  
    assert len(all_element_in_filter_toolbar) == 12


def apply_special_filter_in_one_column(driver_nms, action, number_of_column):
    read_before_sort = []
    read_after_sort = []
    sorted_given_content = []
    rows_after_sort = [] 
    rows_before_sort =[]

    select_filter_icon_for_this_column = Wait_For_Appearance(driver_nms,'xpath',f"//div[@class='ant-table-header']//tfoot[@class='ant-table-summary']//tr[1]//td{number_of_column}")  
    select_filter_icon_for_this_column.click()
    kind_of_filters_menu = Wait_For_Appearance(driver_nms,'xpath',f"//body/div/div[@class='ant-select-dropdown ant-slide-up-enter ant-slide-up-enter-active ant-slide-up custom-dropdown css-1xp7hiy ant-select-dropdown-placement-bottomLeft']")  
    all_filters = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-select-dropdown ant-slide-up-enter ant-slide-up-enter-active ant-slide-up custom-dropdown css-1xp7hiy ant-select-dropdown-placement-bottomLeft']//div//div[@class='rc-virtual-list']//div[@class='rc-virtual-list-holder']//div//div")  
    for number_of_filter in range(len(all_filters)):
        one_filter = Wait_For_Appearance(driver_nms,'xpath',f"//div[@class='ant-select-dropdown ant-slide-up-enter ant-slide-up-enter-active ant-slide-up custom-dropdown css-1xp7hiy ant-select-dropdown-placement-bottomLeft']//div//div[@class='rc-virtual-list']//div[@class='rc-virtual-list-holder']//div//div{number_of_filter}")  
        title_of_filter = one_filter.get_attribute('title')
        one_filter.click()
        apply_button = Wait_For_Appearance(driver_nms,'xpath',"//span[normalize-space()='Apply Filter']")
        apply_button.click()
        content_of_column = read_content_of_column(driver_nms, "//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr", "//div", number_of_column)
        for label in content_of_column:
            assert label == one_filter, f"filter has not been applied correctly."

def apply_filter_in_special_column(driver_nms, act, category):
    if category == "Alarm Name":
        apply_special_filter_in_one_column(driver_nms, action =act, number_of_td_th=4)
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
    LOGIN(driver, login(1,{'url':'http://192.168.5.190:3000/auth/login', 'password' :"root", 'user':'root'}, 'Pass'))
    go_to_current_Alarm(driver_nms=driver)
    demontration_of_filter_toolbar(driver_nms=driver)
    apply_filter_in_special_column(driver_nms=driver, act=action, category= "Alarm Name")
    
