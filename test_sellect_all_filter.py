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
from test_Alarm_Sort import go_to_current_Alarm
from selenium.webdriver.support.ui import Select



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=options)
driver.delete_all_cookies()
# driver.fullscreen_window()
action = ActionChains(driver=driver)

multi_filter_of_alarm_name = ["ONU_OFF", "PON_LOS", "OLT_PON_Unconfig_ONU"]
multi_filter_of_severity = []
multi_filter_of_alarm_category = ["EQUIPMENT", "QOS"]
multi_filter_of_node_name = []
multi_filter_of_node_ip = ["10.41.84.6", "10.50.39.3"]
multi_filter_of_address = []
multi_filter_of_acknowledge_user = []

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
     

def select_all_filter(driver_nms, number_of_column, number_of_all_filters):
    sroll =  Wait_For_Appearance(driver_nms, 'xpath', "//div[contains(@class,'ant-select-dropdown ant-slide-up-enter ant-slide-up-enter-active')]//div[@class='rc-virtual-list']//div[@class='rc-virtual-list-scrollbar rc-virtual-list-scrollbar-vertical']")
    rows_without_filter = read_content_of_column(driver_nms, number_of_column = number_of_column)
    filter_menues = Wait_For_Appearance(driver_nms, 'xpath', "//div[contains(@class,'ant-select-dropdown ant-slide-up-enter ant-slide-up-enter-active')]//div[@class='rc-virtual-list']//div[@class='rc-virtual-list-holder-inner']")
    select_filter_menu(driver_nms, number_of_column=number_of_column)
    filter_element = Wait_For_Appearance(driver_nms, 'xpath', f"//div[@class='rc-virtual-list-holder-inner']//div[@title='Select All']//div[@class='ant-select-item-option-content']//label") 
    driver.execute_script("arguments[0].click();", filter_element)
    apply_icon = WebDriverWait(driver_nms, 30).until(EC.element_to_be_clickable(('xpath', "//span[contains(.,'Apply Filter')]")))
    apply_icon.click()
    sleep(4)   
    rows_after_unapplied_filter = read_content_of_column(driver_nms, number_of_column = number_of_column)
    assert rows_without_filter == rows_after_unapplied_filter 
    number_of_filter_title = Wait_For_Appearance(driver_nms, 'xpath', f"//div[@class='ant-table-header']//tfoot[@class='ant-table-summary']//tr[1]//td[4]//span[@title='{number_of_all_filters} items']")
    assert number_of_filter_title!= None  
 
    

def unselect_select_all_filter(driver_nms, rows_without_filter, number_of_column, number_of_all_filters, with_close_icon):
    if with_close_icon == False:
        select_filter_menu(driver_nms, number_of_column=number_of_column)
        filter_element = Wait_For_Appearance(driver_nms, 'xpath', f"//div[@class='rc-virtual-list-holder-inner']//div[@title='Select All']//div[@class='ant-select-item-option-content']//label") 
        driver_nms.execute_script("arguments[0].click();", filter_element)
        apply_icon = WebDriverWait(driver_nms, 30).until(EC.element_to_be_clickable(('xpath', "//span[contains(.,'Apply Filter')]")))
        apply_icon.click()
        sleep(4)
    else:
        close_icon = Wait_For_Appearance(driver_nms, 'xpath', f"//span[@class='anticon anticon-close']") 
        close_icon.click()
        apply_icon = WebDriverWait(driver_nms, 30).until(EC.element_to_be_clickable(('xpath', "//span[contains(.,'Apply Filter')]")))
        apply_icon.click()
        sleep(4)
    sleep(4)       
    rows_without_filter_unappliying = read_content_of_column(driver_nms, number_of_column = number_of_column)
    assert rows_without_filter == rows_without_filter_unappliying
    number_of_filter_title = Wait_For_Appearance(driver_nms, 'xpath', f"//div[@class='ant-table-header']//tfoot[@class='ant-table-summary']//tr[1]//td[4]//span[@title='{number_of_all_filters} items']")
    assert number_of_filter_title == None  

def apply_filter_in_special_column(driver_nms, act, category, all_filters):
    
    if category == "Alarm Name":
        rows_without_filter = read_content_of_column(driver_nms, number_of_column = 4)
        select_filter_menu(driver_nms, number_of_column=4)
        select_all_filter(driver_nms, number_of_column=4 , number_of_all_filters=38)
        unselect_select_all_filter(driver_nms, rows_without_filter = rows_without_filter, number_of_column=4 , number_of_all_filters=38 ,with_close_icon=False)
    
    elif category == "Alarm Category":
        rows_without_filter = read_content_of_column(driver_nms, number_of_column = 5)
        select_filter_menu(driver_nms, number_of_column=5)
        select_all_filter(driver_nms, number_of_column=5 , number_of_all_filters=38)
        unselect_select_all_filter(driver_nms, rows_without_filter = rows_without_filter, number_of_column=5 , number_of_all_filters=7,with_close_icon=False)
    
    # elif category == "Time Accurance":
    #     rows_without_filter = read_content_of_column(driver_nms, number_of_column = 6)
    #     select_filter_menu(driver_nms, number_of_column=6)
    #     select_multi_filter_in_one_column(driver_nms, action = act, number_of_column=6 , all_filters=all_filters)     
    #     unselect_multi_filter_in_one_column(driver_nms, rows_without_filter = rows_without_filter, number_of_column=6 , all_filters=all_filters, with_close_icon=False)

    # elif category == "Node IP":
    #     rows_without_filter = read_content_of_column(driver_nms, number_of_column = 8)
    #     select_filter_menu(driver_nms, number_of_column=8)
    #     select_multi_filter_in_one_column(driver_nms, action = act, number_of_column=8 , all_filters=all_filters) 
    #     unselect_multi_filter_in_one_column(driver_nms, rows_without_filter = rows_without_filter, number_of_column=8 , all_filters=all_filters, with_close_icon=True)           
    
    # elif category == "Address":
    #     rows_without_filter = read_content_of_column(driver_nms, number_of_column = 10)
    #     select_filter_menu(driver_nms, number_of_column=10)
    #     select_multi_filter_in_one_column(driver_nms, action = act, number_of_column=10 , all_filters=all_filters)  
    #     unselect_multi_filter_in_one_column(driver_nms, rows_without_filter = rows_without_filter, number_of_column=10 , all_filters=all_filters, with_close_icon=False)

    # elif category == "Acknowledge User":
    #     rows_without_filter = read_content_of_column(driver_nms, number_of_column = 11)
    #     select_filter_menu(driver_nms, number_of_column=11)
    #     select_multi_filter_in_one_column(driver_nms, action = act, number_of_column=11 , all_filters=all_filters)          
    #     unselect_multi_filter_in_one_column(driver_nms, rows_without_filter = rows_without_filter, number_of_column=11 , all_filters=all_filters, with_close_icon=False)

   
def test_multi_filter(driver=driver, action=action):
    LOGIN(driver, login(1,{'url':'http://192.168.5.183/auth/login', 'password' :"root", 'user':'root'}, 'Pass'))
    go_to_current_Alarm(driver_nms=driver)
    demontration_of_filter_toolbar(driver_nms=driver)
    apply_filter_in_special_column(driver_nms=driver, act=action, category= "Alarm Name")
    # apply_filter_in_special_column(driver_nms=driver, act=action, category= "Alarm Category")
    # apply_filter_in_special_column(driver_nms=driver, act=action, category= "Node IP")


