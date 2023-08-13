
import datetime
import threading
import time
from uiautomation import WindowControl,MenuControl
import uiautomation as automation

import mate

import asyncio
import json

g_message=[0,""]


run_list =[]
#写一个方法 把参数[小时，分，秒]转换为秒
def run_time(hour,minute,second):
    return hour*3600+minute*60+second

#把要执行得时间点和要执行的方法放到一个列表中
run_list.append([run_time(10,8,0),{"g_command":"get_department_report_easy","department":3},1,"【预执行命令测试】哆儿，今天10.08获取市场部工作计划"])
run_list.append([run_time(10,27,0),{"g_command":"get_department_report_easy","department":2},1,"【预执行命令测试】哆儿，今天10.18获取直播部工作计划"])
run_list.append([run_time(10,28,0),{"g_command":"get_department_report_easy","department":4},1,"【预执行命令测试】哆儿，今天10.28获取生产售货部工作计划"])
run_list.append([run_time(10,38,0),{"g_command":"get_department_report_easy","department":1},1,"【预执行命令测试】哆儿，今天10.38获取技术货部工作计划"])
run_list.append([run_time(10,58,0),{"g_command":"get_department_report_easy","department":5},1,"【预执行命令测试】哆儿，今天10.58获取办公室工作计划"])
#创建一个定时器方法，该方法每1秒执行一次
def alarm_clock():

    #判断当前时间是否是 0:0:0

    now = datetime.datetime.now()
    if  now.hour == 0 and now.minute == 0 and now.second == 0:
        #把run_list中的所有元素的第三个元素设置为1
        for i in run_list:
            i[2]=1

    #遍历 run_list
    for i in run_list:
        if i[2]==1:
            #格式化当天的年月日
            ttime = time.strftime("%Y-%m-%d", time.localtime())+" 00:00:00"
            #把当天的年月日转换为时间戳
            ttime2 = time.mktime(time.strptime(ttime, "%Y-%m-%d %H:%M:%S"))
            gettime = ttime2+i[0] #当天的时间戳+run_list中的时间点
            nowtime = int(time.time()) #现在的时间错
            if nowtime == gettime: #
                i[2]=0              #每天只返回一次
                return i[1]
    return False
                

class Client:
    global g_message

    def clock(self):
        global g_message


    def __init__(self, host, port,call_back):
        self.call_back = call_back
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
      
    async def connect(self):
        
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print("已连接到服务器")

    async def receive_messages(self):
        
        try:
            while True:

                
                data = await self.reader.read(100000)
                if not data:
                    break
                message = data.decode()
                #把message 字符串中 <br> 换成 空格
                message = message.replace("<br>","{Shift}{Enter}")
                message2 = {}
                message2["outstr"] = message
                self.call_back(message2,None,None)
                print("接收到服务器的消息:", message)

        except asyncio.CancelledError:
            pass

    async def send_message(self, message):
        self.writer.write(message.encode())
        await self.writer.drain()

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()



wx = WindowControl( Name='实验群')
print(wx)
#切换到窗口
wx.SwitchToThisWindow()
context = None
lodmess = []
bot_name = "机器人-小哆"
bot_name = "机器人-小哆"

def get_message(chobj): #信息的单词是 
    ilist = chobj.GetFirstChildControl().GetChildren()
    if len(ilist) ==0:
        return [0]
    else:
     return [chobj.GetFirstChildControl().GetChildren()[0].Name,chobj.Name]
def send_wx_message(outstr):
    wx.EditControl(Name="输入").SendKeys(outstr)
    wx.ButtonControl(Name="发送(S)").Click()
def call_back(result,json_obj,state):
    outstr = result["outstr"]
    #把字符串outstr 中的 \n 换成 {Shift}{Enter}
    outstr = outstr.replace("\n","{Shift}{Enter}")
    #检查字符串长度
    lenstr = len(outstr)
    #如果字符串长度大于3000 每次3000 多次发送
    if lenstr > 3000:
        #计算需要发送的次数
        send_times = lenstr//3000
        #计算最后一次发送的长度
        send_last = lenstr%3000
        #计算需要发送的次数
        for i in range(send_times):
            #计算开始位置
            start = i*3000
            #计算结束位置
            end = start+3000
            #发送消息
            send_wx_message(outstr[start:end])
        #发送最后一次消息
        send_wx_message(outstr[-send_last:])
    else:
        #发送消息
        send_wx_message(outstr)

context = "你好"
iClient = None
def run_wx():
    global iClient
    global g_message
    while True:

        try:
                last_msg = wx.ListControl(Name = "消息").GetChildren()


                sendName = get_message(last_msg[-1])[0]
                sendMsg = get_message(last_msg[-1])[1]
                #查找 sendMsg 是否在开头包含 @+bot_name 字符串
                if sendMsg.startswith("@"+bot_name):
                    print("bot_name")
                    #过滤掉@+bot_name
                    sendMsg = sendMsg.replace("@"+bot_name,"")
                    #查看 lodmess 是否有 sendMsg
                    if sendMsg in lodmess:
                        print("已经回复过了")
                        continue  #如果有，则跳过
                    else:
                        lodmess.append(sendMsg)
                        #看 lodmess 的长度是否大于 10 ,如果大于，则删除第一个
                        if len(lodmess) > 10:
                            lodmess.pop(0)
                            



                    #如果是，则调用gpt
                    #获取回复
                    reply = "亲爱的"+sendName+"。。。"
                    #回复消息
                    wx.EditControl(Name="输入").SendKeys(reply)
                    wx.ButtonControl(Name="发送(S)").Click()
                    print("回复成功")
                    #sendMsg = '\u2005你们好'
                    #过了掉\u2005
                    sendMsg = sendMsg.replace('\u2005','') 

                    
                    tcommand = mate.get_mate(sendMsg)

                    if tcommand != False:
                        #get_api.add_get_api(tcommand[0])
                        if g_message[0] == 0:
                            g_message[0] = 1
                            g_message[1] = json.dumps(tcommand[0])
                        pass
                    else:
                        #getchat = chat(sendMsg,context)
                        #wx.EditControl(Name="输入").SendKeys(getchat)
                        wx.EditControl(Name="输入").SendKeys("今天墙太高，翻的超时了！")
                        wx.ButtonControl(Name="发送(S)").Click()





                pass
        except:
            pass

#以非阻塞的方式运行 run_wx
child_thread = threading.Thread(target=run_wx)
child_thread.daemon = True
child_thread.start()

async def main():
    client = Client('127.0.0.1', 12321,call_back)
    global iClient
    iClient = client
    global g_message
    
    await client.connect()
    
    # 启动接收消息的协程
    receive_task = asyncio.create_task(client.receive_messages())

    # 发送消息给服务器
    tj = { "g_command": "get_department_report_txt", "department": 4 }
    #把tj 转换为 json
    
    tj = json.dumps(tj)

    try:
        # 保持事件循环运行
        cladd=0
        while True:
            await asyncio.sleep(0.5)




            
            
            tcommand = alarm_clock()
            if tcommand != False:
                #get_api.add_get_api(tcommand[0])
                if g_message[0] == 0:
                    g_message[0] = 1
                    g_message[1] = json.dumps(tcommand)
                pass




            if g_message[0] == 1:
                await client.send_message(g_message[1])
                g_message[0] = 0
                g_message[1] = ""

    except KeyboardInterrupt:
        # 捕获 Ctrl+C 以优雅地关闭连接
        pass

    # 取消接收消息的协程并关闭连接
    receive_task.cancel()
    await client.close()

asyncio.run(main())
