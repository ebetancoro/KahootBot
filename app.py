from selenium import webdriver
from openai import OpenAI
import requests
import time
import json
import os

def Initialize():
    with open("config.json","r") as file:
        data = json.load(file)
    
    model = data["Model-Name"]
    sys_role_text = data["System-Role-Text"]
    sys_role_image = data["System-Role-Image"]

    api_key = os.environ.get("OPENAI_API_KEY")
    driver = webdriver.Chrome()
    client = OpenAI(api_key=api_key)

    return model, sys_role_text, sys_role_image, api_key, driver, client

def DetectTextData():
    try:
        answer0 = driver.find_element("css selector" , "[data-functional-selector='question-choice-text-0']")
        answer1 = driver.find_element("css selector" , "[data-functional-selector='question-choice-text-1']")
        answer2 = driver.find_element("css selector" , "[data-functional-selector='question-choice-text-2']")
        answer3 = driver.find_element("css selector" , "[data-functional-selector='question-choice-text-3']")
        question = driver.find_element("css selector" , "[data-functional-selector='block-title']")

        return [answer0,answer1,answer2,answer3], question
    except:
        return [answer0,answer1,answer2,answer3],question
def AI_PromptGenerator(answers,question):
    cont = 0
    prompt = "[Q: '" + question.text + "']"
    for i in answers:
        if i != None:
            prompt = prompt + "[A" + str(cont) + ": '" + i.text + "']"
        else:
            prompt = prompt + "[A" + str(cont) + ": '" + "None" + "']"
        cont = cont + 1

    return prompt
def GetAiResponseText(answers,question):
    response = client.chat.completions.create( 
        model = model,
        messages = [
            {"role": "system", "content": sys_role_text},
            {"role": "user", "content": AI_PromptGenerator(answers,question)}
        ]   
    )

    return response.choices[0].message

def GetAiResponseImage():
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": model,
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": sys_role_image
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{driver.get_screenshot_as_base64()}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def EnterGame():
    os.system("clear")
    url_mode = input("URL => [M]anual [P]in [S]kip: ").lower()
    if url_mode == "m":
        driver.get(input("Enter the URL: "))
        return
    elif url_mode == "p":
        driver.get("https://kahoot.it")
        driver.find_element("id" , "game-input").send_keys(input("Enter Gamecode: "))
        driver.find_element("id" , "game-input").submit()

        while driver.title.__contains__("PIN"):
            continue
        
        driver.find_element("id","nickname").send_keys(input("Enter Nickname: "))
        driver.find_element("id","nickname").submit()
        return
    elif url_mode == "s":
        return
def DoRound():
    mode = input("[T]ext or [I]mage mode (0 to exit): ").lower()
    if mode == "t":
        answers, question = DetectTextData()
        response = GetAiResponseText(answers,question)
        print("choosing " + response)
        answers[int(response)].click()
    elif mode == "i":
        answers, question = DetectTextData()
        response = GetAiResponseImage()
        print("choosing " + response)
        answers[int(response)].click()
    elif mode == "0":
        return 0
def DoRoundAutomatic(sleep):
    while True:
        time.sleep(int(sleep))
        try:
            answers, question = DetectTextData()
            response = GetAiResponseImage()
            print("choosing " + response)
            answers[int(response)].click()
        except:
            continue



model, sys_role_text, sys_role_image, api_key, driver, client = Initialize()
EnterGame()
sys_mode = input("[M]anual or [A]utomatic answering: ").lower()
if sys_mode == "m":
    while True:
        r = DoRound()
        if r == 0:
            break
elif sys_mode == "a":
    sleep = input("enter amount of sleep between each attempt(second): ")
    DoRoundAutomatic(sleep)