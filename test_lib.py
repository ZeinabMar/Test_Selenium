
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


pytestmark = [pytest.mark.env_name("NMS_env"), pytest.mark.web_dev("olt_nms")]

def test_selenium(web_interface_module):
    web_interface_module.get_url()
    sleep(3)
    hide_advance_key = Wait_For_Appearance(web_interface_module.driver, "xpath", "//button[@id='details-button']")
    hide_advance_key.click()
    new_ip = Wait_For_Appearance(web_interface_module.driver, "id", "proceed-link")
    new_ip.click()
    User = Wait_For_Appearance(web_interface_module.driver,'xpath',"//form[@id='nms_login']//input[@id='nms_login_username']")  
    User.send_keys("root")
    Password = Wait_For_Appearance(web_interface_module.driver,'xpath',"//form[@id='nms_login']//input[@id='nms_login_password']")  
    Password.send_keys("root")
    enter_key = Wait_For_Appearance(web_interface_module.driver,'xpath',"//form[@id='nms_login']//button[@type='submit']")  
    sleep(2)
    enter_key.click() 
    sleep(0.5)