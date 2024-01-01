from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
action = ActionChains(driver=driver)
# driver.get("https://trytestingthis.netlify.app/")
sleep(0.5)

# ************** scroll with java script
driver.execute_script("window.scrollBy(0,200)")
sleep(3)
# **********scroll to given point
drive.execute_script("window.scrollTo(0,500)")
sleep(3)
# ********** for seeing given object
# 1)
e1 = driver.find_element("Link text", "the film")
driver.execute_script("argument[0].scrollIntoView():", e1)
# 2)
def scrool_to_find_element(locator,pixel):
    for i in range(10):
        try:
            driver.find_element(locator[0],locator[1])
            return True
        except:
            driver.execute_script(f"window.scrollby(0,{pixel})")
    return False
result = scrool_to_find_element(["link text", "ffffjl"],200)  
# ********* find element
driver.execute_script("document.querySelector(#quantity).scrollIntoView()")
driver.execute_script("document.getElementById('quantity').scrollIntoView()")
sleep(10)
# ********** horizontal scroll for finding special element
driver.execute_script("document.querySelector('#table td:last-child').scrollIntoView()")
sleep(10)
# ********* displayed element
driver.get("https://www.imdb.com/chart/top/")
element = driver.find_element("Link text", "Andrei Rublev")
print(element)
result= element.is_displayed()
print(result)
# ********* scroll with action chain
driver.get("https://trytestingthis.netlify.app/")
el1 = driver.find_elements("xpath", "//*[@name='message']")
el2 = driver.find_element("id", "fname")
action.move_to_element(el2).click_and_hold().move_to_element(el1).release().perform()
sleep(3)
# ************* scroll with keyword
driver.get("https://trytestingthis.netlify.app/")
page_el = driver.find_element("xpath",'//html')
