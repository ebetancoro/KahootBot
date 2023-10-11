import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://kahoot.it/")

def EnterGame():
    driver.find_element("id" , "game-input").send_keys(input("Enter Gamecode: "))
    driver.find_element("id" , "game-input").submit()

    while driver.title.__contains__("PIN"):
        continue
    
    driver.find_element("id","nickname").send_keys(input("Enter Nickname: "))
    driver.find_element("id","nickname").submit()

def DetectAnswers():
    answer0 = driver.find_element("css selector" , "[data-functional-selector='question-choice-text-0']")
    answer1 = driver.find_element("css selector" , "[data-functional-selector='question-choice-text-1']")
    answer2 = driver.find_element("css selector" , "[data-functional-selector='question-choice-text-2']")
    answer3 = driver.find_element("css selector" , "[data-functional-selector='question-choice-text-3']")

    return [answer0,answer1,answer2,answer3]

def DetectQuestion():
    question = driver.find_element("css selector" , "[data-functional-selector='block-title']")

    return question

def DoRound():
    answers = DetectAnswers()
    question = DetectQuestion()

    TestDetetctionFunctions(answers,question)

def TestDetetctionFunctions(answers,question):
    for i in answers:
        print(i.text)
    print(question.text)

def Start():
    EnterGame()
    
    input("Start the game? ")
    
    while True:
        DoRound()
        i = input("Next Round? (y/n)")
        if i == "n":
            break

Start()

input("Thanks for using Kahoot-God service ... ")