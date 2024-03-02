#!/usr/bin/env python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import pytest
import logging
from collections import namedtuple
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

def Wait_For_Appearance(driver, by_find_element, context_of_by):
    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((by_find_element,context_of_by)))
        return element
    except: return None


def Wait_For_Appearance_whole_of_something(driver, by_find_element, context_of_by):
    try:
        elements = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((by_find_element,context_of_by)))
        return elements
    except: return None

