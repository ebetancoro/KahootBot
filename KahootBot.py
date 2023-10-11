import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://kahoot.it/")

def EnterGame():
    driver.find_element("id" , "game-input").send_keys(input("Enter Gamecode: "))
    driver.find_element("id" ," game-input").submit()

    while driver.title.__contains__("PIN"):
        continue
    
    driver.find_element("id","nickname").send_keys(input("Enter Nickname: "))
    driver.find_element("id","nickname").submit()
def DetectAnswers():
    answer0 = driver.find_element("css selector" , "['']")
    answer1
    answer2
    answer3

EnterGame()

input()