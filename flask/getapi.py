from typing import Any
import requests
import json
import threading
import time
import asyncio



class get_api: #这

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

    def send_request(self,json_str):

        #json_str = json.dumps(json_str) #这句话的意思是：  把字典转换成字符串

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
            self.t_call_back(result,json_str,1,self.writer)
        else:
            #print("请求失败，状态码：", response.status_code)
            self.t_call_back(response.status_code,json_str,0,self.writer)
        

    def __init__(self):
        #self.t_call_back = callback
        self.api_list=[]
        self.this_api =""
        #创建一个定时，每0.3秒执行一次 time_task 
        child_thread = threading.Thread(target=self.threading_loop)
        child_thread.daemon = True
        child_thread.start()



 
    def add_get_api(self,command_json,writer,t_call_back):
        self.t_call_back = t_call_back
        self.writer = writer
        self.api_list.append(command_json)
        print(self.api_list)
        return 1


class Server:
    def __init__(self, host, port,get):
        self.get = get
        self.host = host
        self.port = port
        self.server = None
        self.clients = {}  # 保存客户端链接对象的字典

    def call_back(self,result,json_obj,state,writer):

        #判断result 是否是字典
        if isinstance(result,dict):



            outstr = result["outstr"]
            #把字符串outstr 中的 \n 换成 {Shift}{Enter}
            outstr = outstr.replace("\n","{Shift}{Enter}")
            writer.write(outstr.encode())
            writer.drain() #这一句的意思是：强制刷新缓冲区，把数据发送出去


    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print("新客户端连接:", addr)

        self.clients[addr] = (reader, writer)  # 将客户端链接对象保存到字典中

        try:
            while True:
                data = await reader.read(100)
                if not data:
                    break
                message = data.decode()
                print("接收到来自 {} 的数据: {}".format(addr, message))

                message2 = message+""



                self.get.add_get_api(message2,writer,self.call_back)

                # 假设在这里进行一些处理，并将响应发送回客户端
                #response = "正在从服务器获取。。!"
                #print("发送响应给客户端: {}".format(response))
                #writer.write(response.encode())
                #await writer.drain()

        except asyncio.CancelledError:
            pass
        finally:
            print("客户端断开连接:", addr)
            del self.clients[addr]  # 客户端断开连接时，从字典中删除该连接对象

            writer.close()
            await writer.wait_closed()

    async def start(self):
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port)
        print("服务器已启动")

        async with self.server:
            await self.server.serve_forever()

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print("服务器已关闭")
def call_back(result,json_obj,state):
    outstr = result["outstr"]
    #把字符串outstr 中的 \n 换成 {Shift}{Enter}
    outstr = outstr.replace("\n","{Shift}{Enter}")
async def main():


    get = get_api()




    server = Server('127.0.0.1', 12321,get)
    await server.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass

    await server.stop()

asyncio.run(main())
