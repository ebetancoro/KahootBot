import json
import openai
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://kahoot.it/")

def InitializeAPI():
    data = json.load(open("API.json","r"))
    API_Key = data["API-Key"]
    Model_Name = data["Model-Name"]
    System_Role = data["System-Role"]

    openai.api_key = API_Key
    return Model_Name,System_Role

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
    aiResponse = Get_AI_Answer(answers,question)
    print("Correct answer index: " + aiResponse)
    
    answers[int(aiResponse)].click()


def TestDetetctionFunctions(answers,question):
    print("____________________________________")
    count = 0
    for i in answers:
        print("Answer" + str(count) + ": " + i.text)
        count = count + 1
    print("Question: " + question.text)
    print("____________________________________")

def Get_AI_Answer(answers,question):
    response = openai.ChatCompletion.create( 
        model = Model_Name,
        messages = [
            {"role": "system", "content": System_Role},
            {"role": "user", "content": AI_PromptGenerator(answers,question)}
        ]   
    )

    return response['choices'][0]['message']['content']

def AI_PromptGenerator(answers,question):
    cont = 0
    prompt = "[Q: '" + question.text + "']"
    for i in answers:
        prompt = prompt + "[A" + str(cont) + ": '" + i.text + "']"
        cont = cont + 1

    return prompt

def Start():
    EnterGame()
    
    input("Start the game ... ")
    
    while True:
        DoRound()
        i = input("Next Round (y/n): ")
        if i == "n":
            break

Model_Name, System_Role = InitializeAPI()
Start()

driver.close()
input("Thanks for using Kahoot-God service ... ")