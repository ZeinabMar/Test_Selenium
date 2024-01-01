from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
action = ActionChains(driver=driver)
driver.get("https://trytestingthis.netlify.app/")
sleep(0.5)
#********************
el = driver.find_element("xpath", "//button[text()='Double click me']")
action.double_click(el).perform()
driver.find_element("xpath", "//*[text()='Your Sample Double Click worked']")
sleep(10)
#*******************Right click
# el = driver.find_element('id',"fname")
# action.context_click(el).perform()
# sleep(2)
#********Move the cursor
# el = driver.find_element("xpath", "//*[@class='tooltip']")
# action.move_to_element(el).perform()
# sleep(3)
#**********click and hold
# action.click_and_hold(el).pause(3).release().click_and_hold(el2).pause(3).perform()
#***********drag and drop
# action.move_to_element(e1).click_and_hold().move_to_element(e2).release().perform()
# sleep(3)
# #**or
# action.drag_and_drop(e1, e2).perform()
#************ click on nothing section in page4
#get coordinate
# offset = driver.find_element(xpath,"...").location
# action.drag_and_drop_by_offset(e1, offset["x"],offset["y"])
# action.move_by_offset(offset["x"],offset["y"]).click().perform()
