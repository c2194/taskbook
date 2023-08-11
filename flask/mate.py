this_to_book = ["查询","告诉我","今天","获取","抓取"]

dp = [["技术部",1],["开发部",1],["业务部",3],["市场部",3],["直播",2],
      ["职能",5],["办公室",5],["门店",6],["生产",4],["售货",4],["工厂",4],["所有",99]]
tc= [["计划","get_department_report_easy"],
     ["完成","get_department_report_txt"],
     ["工作","get_department_report_txt"]]


inputstr = "告诉我今天技术部工作计划"

def get_mate(inputstr):
    mate_state = 0

    for i in this_to_book:
        if i in inputstr:
            mate_state = 1
            break
    dp_id =0
    if mate_state == 1:
        for i in dp:
            if i[0] in inputstr:
                mate_state = 2
                dp_id = i[1]
                break
    tc_command = {}
    
    if mate_state == 2:
        for i in tc:
            if i[0] in inputstr:
                mate_state = 3
                tc_command["g_command"]=i[1]
                tc_command["department"]=dp_id
                break
    if mate_state == 3:
        return [tc_command]
    else:
        return False
    