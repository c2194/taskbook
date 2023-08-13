import datetime
import threading
import time
from typing import Any
import requests
import json
import getapi
import mate



run_list =[]
#写一个方法 把参数[小时，分，秒]转换为秒
def run_time(hour,minute,second):
    return hour*3600+minute*60+second

#把要执行得时间点和要执行的方法放到一个列表中
run_list.append([run_time(10,8,0),{"g_command":"get_department_report_easy","department":3},1,"【预执行命令测试】哆儿，今天10.08获取市场部工作计划"])
run_list.append([run_time(10,18,0),{"g_command":"get_department_report_easy","department":2},1,"【预执行命令测试】哆儿，今天10.18获取直播部工作计划"])
run_list.append([run_time(10,28,0),{"g_command":"get_department_report_easy","department":4},1,"【预执行命令测试】哆儿，今天10.28获取生产售货部工作计划"])
run_list.append([run_time(10,38,0),{"g_command":"get_department_report_easy","department":1},1,"【预执行命令测试】哆儿，今天10.38获取技术货部工作计划"])
run_list.append([run_time(10,58,0),{"g_command":"get_department_report_easy","department":5},1,"【预执行命令测试】哆儿，今天10.58获取办公室工作计划"])








def call_back(result,json_obj,state):
    

    
    print(result)
    pass



get_api = getapi.get_api(call_back)
#时间戳开始时间是 1970-01-01 08:00:00

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
                i[2]=0
                  
                

                
                get_api.add_get_api(i[1])
    
    
        
    threading.Timer(0.5, alarm_clock).start()



#每1秒执行 一次alarm_clock方法
threading.Timer(1, alarm_clock).start()



tcommand = mate.get_mate("告诉我今天技术部工作计划")

if tcommand != False:
    get_api.add_get_api(tcommand[0])





#get_api.add_get_api({"g_command":"get_department_report_easy","department":4})
#get_api.add_get_api({"g_command":"get_department_report_easy","department":3})
#get_api.add_get_api({"g_command":"get_department_report_easy","department":2})
#get_api.add_get_api({"g_command":"get_department_report_easy","department":1})

while 1:
    pass