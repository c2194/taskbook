from typing import Any
import requests
import json
import threading
import time




class get_api:

    url = "http://111.230.23.33:12345/endpoint"
    #url = "http://localhost:12345/endpoint"

    api_list=[]
    this_api =""
    get_state = 0 #是否正在执行获取功能
    t_call_back = None

    def threading_loop(self):
        while True:
            if self.get_state == 0:
                 if len(self.api_list) != 0:
                    #取出api_list中的第一个元素
                    self.get_state=1
                    self.this_api = self.api_list[0]
                    self.api_list.pop(0)
                    #发送请求
                    self.send_request(self.this_api)
                        
            else:
                time.sleep(0.3)
                pass

    def send_request(self,ijson):

        json_str = json.dumps(ijson)

        # 设置请求头
        headers = {
            "Content-Type": "application/json"
        }

        # 设置要发送请求的URL
        url = self.url
        # 发送POST请求并获取响应
        response = requests.post(url, data=json_str, headers=headers)

        self.get_state = 0
        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应的JSON数据
            result = response.json()
            #print("响应结果：", result)
            self.t_call_back(result,json_str,1)
        else:
            #print("请求失败，状态码：", response.status_code)
            self.t_call_back(response.status_code,json_str,0)
        

    def __init__(self,callback):
        self.t_call_back = callback
        self.api_list=[]
        self.this_api =""
        #创建一个定时，每0.3秒执行一次 time_task 
        child_thread = threading.Thread(target=self.threading_loop)
        child_thread.daemon = True
        child_thread.start()



 
    def add_get_api(self,command_json):
        self.api_list.append(command_json)
        print(self.api_list)
        return 1
