import openai
import pandas as pd
import numpy as np

from uiautomation import WindowControl,MenuControl
import uiautomation as automation

context = "你好"


openai.api_key = "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"


   







def ask(question, context):
    if context is None:
        prompt = question
    else:
        prompt = f"{context}\n{question}"
    response = openai.Completion.create(
        #engine="davinci",
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )
    if context is None:
        return response.choices[0].text.strip()
    else:
        return response.choices[0].text.replace(context, "").strip()





def chat(question, context=None):
    answer = ask(question, context=context)
    context = answer
    return answer


#如直接运行则执行下面的代码
if __name__ == "__main__":
    while True:
        #question = input("您的问题： ")
        #iask = "你们好"
        #answer = ask(iask, context=context)
        #context = answer
        answer = chat("你们好")
        
        print("CHATGPT的回答： ", answer)
        #退出
        
        break

