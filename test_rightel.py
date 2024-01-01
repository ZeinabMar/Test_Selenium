#!/usr/bin/env python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import logging
from selenium.webdriver.common.action_chains import ActionChains
logging.basicConfig(level=logging.DEBUG)

def test_rightel():
    phone_number = input("Enter your phone number 09:")
    national_code = input("Enter your National code:")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    action = ActionChains(driver=driver)
    driver.get("https://shop.rightel.ir")
    action = ActionChains(driver=driver)
    driver.set_window_size(2000, 694)
    sleep(3)
    el1 = driver.find_element('xpath',"//div[@id='customTab']//a[1]")
    action.click(el1).perform()
    sleep(1)
    check_text = driver.find_element('xpath',"//div[@class='customPane fade show activePan']//div[@class='cardPlan'][1]//div[@class='cardPlanBody']//p[@class='card-description']").text
    assert check_text == "خرید سیم‌کارت با شماره دلخواه و بسته های جذاب اینترنت تا 100 گیگابایت (ویژه هواداران استقلال)"
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
    sleep(3)
    el2 = driver.find_element('xpath', "//div[@class='customPane fade show activePan']//div[@class='cardPlan'][1]//button[@class='rightelBtn planBtn'][1]")
    action.click(el2).perform()
    sleep(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
    sleep(3)
    el3 = driver.find_element('xpath', "//div[@class='productCard'][1]//div[@class='productCard'][1]//button")
    action.click(el3).perform()
    sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/5);")
    # check_text = driver.find_element('xpath',"//div[@class='productCard'][1]//div[@class='productCard'][1]//div[@class='productPrice font-22-medium'][1]").text
    # assert check_text == "اینترنت: 40 گیگابایت"
    sleep(3)
    click = driver.find_element('xpath',"//div[@id='contentDiv']")
    secure = input("Enter secure Code:")
    sleep(3)
    # check_text_1 = driver.find_element('xpath',"//div[@class='fieldItemDiv w100 maxw100'][1]//label[@class='floating-label']//span").text
    # assert check_text_1 == " کد ملی"
    national = driver.find_element("xpath", "//div[@class='input-grp']//div[@class='contralContent']//input[@minlength='10']")
    sleep(3)
    national.send_keys(f"{national_code}")
    sleep(2)
    phone = driver.find_element("xpath", "//div[@class='input-grp']//div[@class='contralContent']//input[@minlength='9']")
    sleep(2)
    phone.send_keys(f"{phone_number}")
    sleep(4)
    el = driver.find_element('xpath',"//div[@class='form-check form-check-inline m-0']//input[@type='checkbox']")
    sleep(2)
    action.click(el).perform()
    secure_code = driver.find_element("xpath", "//div[@class='input-grp']//div[@class='contralContent mr15']//input[@minlength='6']")
    sleep(6)
    secure_code.send_keys(f"{secure}")
    sleep(5)
    enter = driver.find_element("xpath", "//button[@class='rightelBtn loginButton']//div[@id='contentDiv']")
    action.click(enter).perform()
    sleep(2)
    for i in range(5):
        sms_code = input(f"Enter number {i+1} of your SMS:")
        sms = driver.find_element("xpath",f"//div[@class='wrapper']//input[{i+1}]")
        sms.send_keys(f"{sms_code}")
        sleep(2)
    enter2 = driver.find_element("xpath", f"//button[@class='rightelBtn loginButton']//div[@id='contentDiv']")
    action.click(enter2)
    sleep(2)
    logger.info('Enrollment is completed.')
    find_element_in_last_page = driver.find_element('xpath',"//div[@class='cardBodyMsisdn']")
    sleep(6)