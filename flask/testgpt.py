import requests

# ChatGPT API配置
GPT_API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = "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"

# 用于保存会话状态的全局字典
sessions = {}

def chat_with_gpt(user_id, user_message):
    if user_id not in sessions:
        sessions[user_id] = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    # 向ChatGPT API发送POST请求
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': sessions[user_id] + [{'role': 'user', 'content': user_message}]
    }

    response = requests.post(GPT_API_URL, json=payload, headers=headers)
    response_data = response.json()

    # 提取ChatGPT的回复
    chat_reply = response_data['choices'][0]['message']['content']

    sessions[user_id] = payload['messages'] + [{'role': 'assistant', 'content': chat_reply}]

    return chat_reply

if __name__ == '__main__':
    # 示例交互
    user_id = 'twobaozi_shouhou'
    user_message = '下面是售后记录的信息\
        1.南京蒋总售后群 客户反馈打印照片曝光 对接指导客户准备win系统的笔记本电脑调试打印机thp电压色彩颜色\
2吉林辽源崔总 客户反馈镜头被东西挡住 对接检查发现摄像头被戳掉 指导客户重新固定摄像头\
3.佳叽娃娃机供应商 娃娃机天车出现故障 指导更换微动 检查马达故障 需更换配件 让把有问题的天车寄回维修\
4.山东赵总大头贴售后群 客户反馈拍照背景不均匀 视频对接发现是现场灯光的原因 指导客户调调试机器补光灯灯光\
5.黑龙江张总售后群 客户反馈打印照片有白条 打印头上面沾了脏东西 指导客户清理打印头\
6.云南玉溪何晶晶售后 客户反馈色带有问题 我们把我们的色带给客户寄过去 让客户把有问题的色带返回给我们\
7.南京陈总互动相机 协助客户调试设备 上传相框\
8.浙江杨总 客户反馈打印机频繁卡纸 更换打印机\
9.广西陈总售后 客户反馈机器卡在加印页面退出不了 指导客户重启机器\
10.山西吕梁大头贴售后 客户返回购买耗材色带头发现破裂 客户要求更换一个色带\
11.吉林吉延李总售后 帮客户上传客户制作的相框 调整边框颜色\
12.21年山东临沂小鹿款大头贴售后群 客户设备到期 收取年费300'

    #reply = chat_with_gpt(user_id, user_message)
   # print(reply)
    #创建一个循环 每次等待用户输入
    while True:
        user_message = input('用户：')
        reply = chat_with_gpt(user_id, user_message)
        print('机器人：', reply)
        if user_message == '再见':
            break

