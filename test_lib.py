
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
    hide_advance_key = Wait_For_Appearance(web_interface_module.driver, "xpath", "//button[@id='details-button']")
    sleep(2)
    hide_advance_key.click()