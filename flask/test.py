import pandas as pd

wechatWindow.SetFocus()
messages = wechatWindow.ListControl(Name='消息')
result = []
time = pd.NA
for message in messages.GetChildren():
    content = message.Name
    if content in ["查看更多消息", "以下为新消息"]:
        continue
    details = message.GetChildren()[0].GetChildren()
    if len(details) == 0:
        time = content
        continue
    nickname, detail, me = details
    name = nickname.Name
    if me.Name:
        name = me.Name

    link_all = pd.NA
    if not (content == "[图片]" or content.startswith("[语音]")):
        details = detail.GetChildren()
        if len(details) == 0:
            continue
        detail = details[-1].GetChildren()[0].GetChildren()[0].GetChildren()[0]
        details = detail.GetChildren()

        if len(details) != 0:
            link_title = details[0].Name
            link_content = details[1].Name
            content += f"{link_title}\n{link_content}"
#     print(time, name, content)
    result.append((time, name, content.strip()))
df = pd.DataFrame(result, columns=["时间", "昵称", "内容"])
df
