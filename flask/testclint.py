import asyncio
import json
class Client:
    def __init__(self, host, port):
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
                data = await self.reader.read(100)
                if not data:
                    break
                message = data.decode()
                print("接收到服务器的消息:", message)
        except asyncio.CancelledError:
            pass

    async def send_message(self, message):
        self.writer.write(message.encode())
        await self.writer.drain()

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

async def main():
    client = Client('127.0.0.1', 12321)
    await client.connect()

    # 启动接收消息的协程
    receive_task = asyncio.create_task(client.receive_messages())

    # 发送消息给服务器
    tj = { "g_command": "get_department_report_txt", "department": 4 }
    #把tj 转换为 json
    
    tj = json.dumps(tj)
    #把json 转为字符串



    await client.send_message(tj)


    #await client.send_message("Hello, server!")

    try:
        # 保持事件循环运行
        cladd=0
        while True:
            await asyncio.sleep(1)
            cladd+=1
            if cladd >=3:
                pass
                #await client.send_message("Hello, server!"+str(cladd))
    except KeyboardInterrupt:
        # 捕获 Ctrl+C 以优雅地关闭连接
        pass

    # 取消接收消息的协程并关闭连接
    receive_task.cancel()
    await client.close()

asyncio.run(main())
