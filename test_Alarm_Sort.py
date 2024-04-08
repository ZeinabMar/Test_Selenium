#!/usr/bin/env python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from collections import namedtuple
from time import sleep
import time
import json
import ast
import pytest
import requests
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
driver.delete_all_cookies()
action = ActionChains(driver=driver)
pytestmark = [pytest.mark.env_name("REST_env"), pytest.mark.rest_dev("olt_nms")]

def read_all_rows_of_one_column():
    Severity = []
    Alarm_Category = []
    Acknowledge_User = []
    Node_IP = []
    Address = []
    Alarm_Name = []
    Time_Accurance = []
    Clear_Time = []

    read_data = requests.get("https://192.168.5.183/api/gponalarm/active/getPage?page=0&size=1730&sort=createTime,desc")
    # input_data = json.loads(read_data.text)
    logger.info(f"input {read_data}")
    # input_data = ast.literal_eval(input_data)
    for data in input_data["content"]:
        for key in data.keys():
            if key == "severity":
                Severity.append(data[key])
            elif key == "type":
                Alarm_Category.append(data[key])
            elif key == "acknowledgeUser":
                Acknowledge_User.append(data[key])
            elif key == "ip":
                Node_IP.append(data[key])
            elif key == "sourceName":
                Address.append(data[key]) 
            elif key == "alarmName":
                Alarm_Name.append(data[key])   
            elif key == "createTime":
                Time_Accurance.append(data[key])   
            elif key == "acknowledgeTime":
                Clear_Time.append(data[key])                  
    return Severity, Alarm_Name, Alarm_Category, Acknowledge_User, Node_IP, Address, Time_Accurance, Clear_Time


def go_to_current_Alarm(driver_nms):
    Fault = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='alarm-menu']//span")
    Fault.click() 
    Current_Alarm = Wait_For_Appearance(driver_nms,'xpath',"//div[@data-test-name='Current Alarm']")  
    Current_Alarm_label = Wait_For_Appearance(driver_nms,'xpath',"//div[@data-node-key='currentAlarm']")  
    assert Current_Alarm.text=="Current Alarm"
    Current_Alarm_label.click()
    assert Current_Alarm_label.get_attribute('class') == 'ant-tabs-tab ant-tabs-tab-active'
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


def sort_click(driver_nms, action, number_of_th):
    sort_element = driver_nms.find_element('xpath',f"//div[@class='ant-table-header']//thead[@class='ant-table-thead']//tr//th[{number_of_th}]")
    action.click(sort_element).perform()
    table = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']")
    rows = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")


def read_content_of_column_Ui(driver_nms, number_of_column):
    text_of_rows = []
    rows = driver_nms.find_elements('xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    logger.info(f"len of rows {len(rows)}")
    for i in range(1,len(rows)):
        text_of_element = Wait_For_Appearance(driver_nms,'xpath', f"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr[{i+1}]//td[{number_of_column}]//div[@class='record']").text
        text_of_rows.append(text_of_element)
    driver_nms.implicitly_wait(20)
    return  text_of_rows   

def Sort_Process_For_Any_Column(driver_nms, action, number_of_td_th):
    read_before_sort = []
    read_after_sort = []
    sorted_given_content = []
    rows_after_sort = [] 
    rows_before_sort =[]
    rows_before_sort = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    assert len(rows_before_sort)!=0
    read_content_of_row_before_sort = read_content_of_column(driver_nms, number_of_column = number_of_td_th)
    assert len(read_content_of_row_before_sort)!=0
    sort_click(driver_nms= driver_nms, action=action, number_of_th=number_of_td_th)
    driver_nms.implicitly_wait(30)
    rows_after_sort = Wait_For_Appearance_whole_of_something(driver_nms,'xpath',"//div[@class='ant-table-body']//tbody[@class='ant-table-tbody']//tr")
    assert len(rows_after_sort) != 0
    assert len(rows_after_sort) == len(rows_before_sort)
    sorted_given_content = sorted(read_content_of_row_before_sort)
    read_content_of_row_after_sort = read_content_of_column(driver_nms, number_of_column = number_of_td_th)
    assert len(sorted_given_content) != 0
    logger.info(f"read_content_of_row_after_sort{read_content_of_row_after_sort}")
    logger.info(f"read_content_of_row_before_sort {read_content_of_row_before_sort}")
    logger.info(f"sorted_given_content {sorted_given_content}")
    # assert len(rows_before_sort)-1==len(sorted_given_content)-1 #== len(rows_after_sort)-1
    for i in range(25):
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
    LOGIN(driver, login(1,{'url':'http://192.168.5.183/auth/login', 'password' :"root", 'user':'root'}, 'Pass'))
    go_to_current_Alarm(driver_nms=driver)
    Severity, Alarm_Name, Alarm_Category, Acknowledge_User, Node_IP, Address, Time_Accurance, Clear_Time = read_all_rows_of_one_column()
    logger.info(f"{Severity}")
    logger.info(f"{Alarm_Name}")
    logger.info(f"{Alarm_Category}")
    logger.info(f"{Acknowledge_User}")
    logger.info(f"{Time_Accurance}")
    # Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Alarm Name")
    # Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Alarm Category")
    # Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Acknowledge User")
    # Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Node IP")
    # Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Address")
    # Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Clear Time")
    # Manage_Sort_In_All_Columns(driver_nms=driver, act=action, category= "Time Accurance")




    # scroll_action(driver_nms=driver)
