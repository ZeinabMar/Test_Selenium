#!/usr/bin/env python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytest
import logging
from conftest import *
from collections import namedtuple
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
action = ActionChains(driver=driver)


login = namedtuple('login', ['index', 'expected_result_Set', 'result'])
login.__new__.__defaults__ = (None, {}, None)

login_data = (login(1,{'url':'http://192.168.5.190:3000/auth/login', 'password' :"root", 'user':'root'}, 'Pass'),
              login(2,{'url':'http://192.168.5.190:3000/auth/login', 'password' :"root", 'user':'4567'}, 'Fail'),)
# hide_advance_key = driver.find_element("id", "details-button")
# hide_advance_key.click()

# new_ip = driver.find_element("id", "proceed-link")
# new_ip.click()
def LOGIN(driver_nms, data_login):
    driver_nms.maximize_window()
    sleep(4)
    data_set = data_login.expected_result_Set
    driver_nms.get(data_set['url'])
    sleep(3)
    # hide_advance_key = Wait_For_Appearance(driver_nms, "xpath", "//button[@id='details-button']")
    # hide_advance_key.click()
    # new_ip = Wait_For_Appearance(driver_nms, "id", "proceed-link")
    # new_ip.click()
    User = Wait_For_Appearance(driver_nms,'xpath',"//form[@id='nms_login']//input[@id='nms_login_username']")  
    User.send_keys(data_set['user'])
    Password = Wait_For_Appearance(driver_nms,'xpath',"//form[@id='nms_login']//input[@id='nms_login_password']")  
    Password.send_keys(data_set['password'])
    enter_key = Wait_For_Appearance(driver_nms,'xpath',"//form[@id='nms_login']//button[@type='submit']")  
    sleep(2)
    enter_key.click() 
    sleep(0.5)   
    if data_login.result=="Pass":
        menue = Wait_For_Appearance(driver_nms,'xpath',"//div[@class='ant-layout-sider-children']")  
        dashboard = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='dashboard-menu']//span").text
        assert dashboard== "DASHBOARD"
        topology = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='topology-menu']//span").text
        assert topology== "TOPOLOGHY"
        alarm = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='alarm-menu']//span").text
        assert alarm== "FAULTS"
        performance = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='performance-menu']//span").text
        assert performance== "PERFORMANCE"
        service = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='services-menu']//span").text
        assert service== "SERVICES"
        usermanagement = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='userManagement-menu']//span").text
        assert usermanagement== "USER MANAGEMENT"
    else:
        assert not(driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='dashboard-menu']//span"))
        # error_message = driver_nms.find_element('xpath', "//aside[@data-test-id='sidbar']//li[@data-test-id='userManagement-menu']//span").text
        # assert error_message == "The desired user could not be found, error code: 10038."

def test_Login(driver=driver):
    for data in login_data:
        LOGIN(driver,data)

