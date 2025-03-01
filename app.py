from selenium import webdriver
from openai import OpenAI
import requests, time, json, os

def Initialize():
    with open("config.json") as file:
        data = json.load(file)
    return data["Model-Name"], data["System-Role-Text"], data["System-Role-Image"], os.environ.get("OPENAI_API_KEY"), webdriver.Chrome(), OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def DetectTextData():
    try:
        answers = [webdriver.Chrome().find_element("css selector", f"[data-functional-selector='question-choice-text-{i}']") for i in range(4)]
        question = webdriver.Chrome().find_element("css selector", "[data-functional-selector='block-title']")
        return answers, question
    except:
        return None, None

def AI_PromptGenerator(answers, question):
    return "[Q: '" + question.text + "']" + "".join(f"[A{i}: '{a.text if a else 'None'}']" for i, a in enumerate(answers))

def GetAiResponseText(answers, question):
    return client.chat.completions.create(model=model, messages=[
        {"role": "system", "content": sys_role_text},
        {"role": "user", "content": AI_PromptGenerator(answers, question)}
    ]).choices[0].message

def GetAiResponseImage():
    response = requests.post("https://api.openai.com/v1/chat/completions", headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {api_key}"
    }, json={
        "model": model, "messages": [{
            "role": "user", "content": [
                {"type": "text", "text": sys_role_image},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{webdriver.Chrome().get_screenshot_as_base64()}"}}
            ]
        }], "max_tokens": 300
    })
    return response.json()["choices"][0]["message"]["content"]

def EnterGame():
    os.system("clear")
    mode = input("URL => [M]anual [P]in [S]kip: ").lower()
    if mode == "m":
        webdriver.Chrome().get(input("Enter the URL: "))
    elif mode == "p":
        driver = webdriver.Chrome()
        driver.get("https://kahoot.it")
        driver.find_element("id", "game-input").send_keys(input("Enter Gamecode: "))
        driver.find_element("id", "game-input").submit()
        while "PIN" in driver.title: pass
        driver.find_element("id", "nickname").send_keys(input("Enter Nickname: "))
        driver.find_element("id", "nickname").submit()

def DoRound():
    mode = input("[T]ext or [I]mage mode (0 to exit): ").lower()
    if mode in ("t", "i"):
        answers, question = DetectTextData()
        response = GetAiResponseText(answers, question) if mode == "t" else GetAiResponseImage()
        print("choosing", response)
        answers[int(response)].click()
    return mode != "0"

def DoRoundAutomatic(sleep):
    while True:
        time.sleep(int(sleep))
        try:
            answers, question = DetectTextData()
            response = GetAiResponseImage()
            print("choosing", response)
            answers[int(response)].click()
        except:
            pass

model, sys_role_text, sys_role_image, api_key, driver, client = Initialize()
EnterGame()
if input("[M]anual or [A]utomatic answering: ").lower() == "m":
    while DoRound(): pass
else:
    DoRoundAutomatic(input("Enter sleep time (seconds): "))
