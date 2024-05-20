
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
from selenium.webdriver.chrome.service import Service as ChromeService

# pytestmark = [pytest.mark.env_name("NMS_env"), pytest.mark.web_dev("olt_nms")]
# Chromer_Driver_Path = 
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# service = ChromeService(Chromer_Driver_Path)
# options = ChromeOptions()
# service=service, options=options
driver = webdriver.Firefox()

driver = webdriver.Firefox(executable_path=F().install())
action = ActionChains(driver=driver)

# def test_selenium(driver):
driver.get("http://192.168.5.183/auth/login")
sleep(3)
hide_advance_key = Wait_For_Appearance(driver, "xpath", "//button[@id='details-button']")
hide_advance_key.click()
new_ip = Wait_For_Appearance(driver, "id", "proceed-link")
new_ip.click()
User = Wait_For_Appearance(driver,'xpath',"//form[@id='nms_login']//input[@id='nms_login_username']")  
User.send_keys("root")
Password = Wait_For_Appearance(driver,'xpath',"//form[@id='nms_login']//input[@id='nms_login_password']")  
Password.send_keys("root")
enter_key = Wait_For_Appearance(driver,'xpath',"//form[@id='nms_login']//button[@type='submit']")  
sleep(2)
enter_key.click() 
sleep(0.5)