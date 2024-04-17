from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
action = ActionChains(driver=driver)
driver.get("https://yahoo.com")

search_box = driver.find_element("id", "ybar-sbq")
#********************keydown with send key
# search_box.send_keys("selenium"+Keys.ENTER)
# action.key_down(Keys.CONTROL).send_keys("a").perform()
#********************keydown with send key to element
# action.key_down(Keys.SHIFT).send_keys_to_element(search_box,"selenium").perform()
#********************keydup with send key to element
# action.key_down(Keys.SHIFT).send_keys_to_element(search_box,"selenium").key_up(Keys.SHIFT).send_keys(" selenium").perform()
#*********************clear textbox
action.key_down(Keys.SHIFT).send_keys_to_element(search_box,"selenium").key_up(Keys.SHIFT).send_keys(" selenium").perform()
sleep(3)
#1) search_box.clear()
#2)
# search_box.click()
action.key_down(Keys.CONTROL).send_keys("a").send_keys(Keys.DELETE).perform()
sleep(3)