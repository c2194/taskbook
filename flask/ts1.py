import datetime
from flask import Flask, render_template, request, redirect, session,send_from_directory
import os
import flask
from flask_cors import CORS
import threading
import time
import mysqllib
import json

#给copilot用的数据
# work_tasks 表中有字段 `task_id``task_name``creation_time``creator``task_status``task_class``progree``participant``plan_time``task_readme`
# users 表中有字段 `user_id``username``chinese_name``department_id``password`

#获取本文件所在的目录
this_dir_path = os.path.dirname(os.path.realpath(__file__))
respath = this_dir_path + '\\res'
# 把 respath 转换成正斜杠
respath = respath.replace('\\', '/')
print(respath)

#db = mysqllib.MySQL(host='localhost', port=3306, user='root', password='root', db='task')
db = mysqllib.MySQL(host='localhost', port=3306, user='task', password='taskAa88888888', db='task')
db.connect()

app = Flask(__name__)
CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'your_secret_key'

this_dir_path = os.path.dirname(os.path.realpath(__file__))
# 登录状态检查装饰器
def login_required(view_func):
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return view_func(*args, **kwargs)
        else:
            return redirect('/login')
    return wrapper
@app.route('/version')
def show_flask_version():
    #返回flask 版本、
    return f'flask version: {flask.__version__}'


@app.route('/')
@login_required
def index():
    #return f'欢迎回来，{session["username"]}!'
    return redirect('/login')
    #return render_template('home.html')

@app.route('/res/<path:filename>')
def serve_file(filename):
    # 指定文件所在的目录
    directory = respath
    return send_from_directory(directory, filename)

@app.route('/home/<path:filename>')
def home_file(filename):
    # 指定文件所在的目录
    directory = respath
    return send_from_directory(directory, filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        #获取request.data 字典
        data = request.get_json()
        username = data['username']
        password = data['password']
        #产生sql语句通过username和password查询数据库，关联部门表
        sql = f"SELECT u.*,d.*,f.* FROM users u JOIN department_members dm ON u.user_id = dm.user_id JOIN departments d ON dm.department_id = d.department_id JOIN function_members fm ON u.user_id = fm.user_id JOIN functions f ON fm.function_id = f.function_id  WHERE username = '{username}' AND password = '{password}'"


        db.connect()
        result = db.read(sql)

        # TODO: 根据用户名和密码验证用户，进行登录逻辑
        # 这里只是示例代码，假设用户名和密码正确

        # 用户验证成功后，创建会话
        if len(result) == 0:
            
            session['username'] = ""
            session['chinese_name'] = ""
            session['department_name'] = ""
            session['department_id'] = 0
            session['user_id'] = 0
            session['functionarr'] = 0
            return {'code': 1, 'message': '用户名或密码错误'}
        else:

            functionarr = []
            for i in result:
                functionarr.append(i['function_name'])



            session['username'] = username
            session['chinese_name'] = result[0]['chinese_name']
            session['department_name'] = result[0]['department_name']
            session['department_id'] = result[0]['department_id']
            session['user_id'] = result[0]['user_id']
            session['functionarr'] = functionarr

            #返回json
            return {'code': 0, 'message': '登录成功','data':session}
    


    else:
        #获取当前目录

        directory = respath
        return send_from_directory(directory, "login2.html")
        #return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['username'] = ""
    session['chinese_name'] = ""
    session['department_name'] = ""
    session['department_id'] = 0
    session['user_id'] = 0
    session['functionarr'] = 0
    return {'code': 0, 'message': '退出成功'}
    return redirect('/')

#创建/html路由
@app.route('/html', methods=['GET', 'POST'] )
def html():
    if request.method == 'GET':
        act = request.args.get('act')
        return render_template(act)
        

def update_sub_progress(data):
    

            task_id = data['task_id']
            progress = data['progress']
            sub_task_id = data['sub_task_id']   
            set_state = data['set_state']
            p_readme = data['p_readme']
             #根据 sub_task_id 查询 sub_tasks 表

            if set_state == 1:
                if progress == "":
                    return {'code': 1, 'g_command':'set_sub_progress','message': 'fail'}
                    
                sql = 'UPDATE `sub_tasks` SET  `sub_ctrl_time` = NOW(),	 `completion_rate` = ' + str(data['progress']) + ' WHERE `sub_tasks`.`id` = ' + str(data['sub_task_id'])
                
            else:
                if data['set_state'] == 5:
                    data['set_state'] = 1

                sql = 'UPDATE `sub_tasks` SET  `sub_ctrl_time` = NOW(),	 `state` = ' + str(data['set_state']) + ', `completion_rate` = ' + str(data['progress']) + ' WHERE `sub_tasks`.`id` = ' + str(data['sub_task_id'])
                progress='0'
                  
            db.connect()
            result = db.write(sql)
            db.conn.close()

            #表的结构 `sub_progress`
            #CREATE TABLE `sub_progress` (
            #  `sup_id` int(11) NOT NULL,
            #  `sup_progress` int(11) NOT NULL COMMENT '进度',
            #  `sup_sub_id` int(2) NOT NULL COMMENT '操作id，进行了什么类型的操作',
            #  `sup_readame` text COLLATE utf8_unicode_ci NOT NULL COMMENT '说明',
            #  `sup_task_id` int(11) NOT NULL COMMENT 'task_id',
            #  `sup_time` datetime NOT NULL COMMENT '创建时间'
            #) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='sub 进度与设置记录';
            #ALTER TABLE `sub_progress` ADD `sup_create_user_id` INT(11) NOT NULL COMMENT '操作人id' AFTER `sup_time`;

            #sql 语句 向 sub_progress 表中插入数据
            sql = 'INSERT INTO `sub_progress` (`sup_id`, `sup_progress`, `sup_sub_id`, `sup_readame`, `sup_task_id`, `sup_time`,`sup_create_user_id`) VALUES (NULL,'
            sql = sql + str(progress) + ','
            sql = sql + str(set_state) + ','
            sql = sql + "'" + p_readme + "',"
            sql = sql + str(sub_task_id) + ','
            sql = sql + "NOW(),"+str(session['user_id'])+")"
            db.connect()
            result = db.write(sql)
            db.conn.close()
            return result


#路由 endpoint
@app.route('/endpoint', methods=['GET', 'POST'])
def endpoint():
    if request.method == 'POST':
        #获取request.data 字典
        
        #判断session中是否有user_id
        if 'user_id' not in session:
            pass
        else:
            user_id = session['user_id']
        
        #判断session中是否有chinese_name
        if 'chinese_name' not in session:
            pass
        else:
            chinese_name = session['chinese_name'] 
        data = request.get_json()
        get_command = data['g_command']
        if get_command == 'task_types':
            sql = 'SELECT * FROM task_types'
            db.connect()
            result = db.read(sql)
            db.conn.close()
            return {'code': 0, 'g_command':'task_types','message': 'success', 'data': result}
        if get_command == 'get_users':
            sql = 'SELECT * FROM users u JOIN department_members dm ON u.user_id = dm.user_id JOIN departments d ON dm.department_id = d.department_id'
            db.connect()
            result = db.read(sql)
            #db.conn.close()
            # result = [19: {'user_id': 18, 'username': 'user18', 'chinese_name': '用户18', 'department_id': 3, 'password': '', 'department_name': '工厂'}，
            # 19: {'user_id': 18, 'username': 'user18', 'chinese_name': '用户18', 'department_id': 3, 'password': '', 'department_name': '工厂'}]
            # 生成新的列表 用于前端显示 保留 user_id chinese_name department_name
            new_result = []
            for i in result:
                new_result.append({'value': i['user_id'], 'title':i['chinese_name'] +"-"+i['department_name']})
            return {'code': 0, 'g_command':'get_users','message': 'success', 'data': new_result}
        if get_command == 'get_me':
              return {'code': 0, 'g_command':'get_me','message': 'success', 'data': session["department_name"]+" "+ session["chinese_name"]}
        if get_command == 'push_task':
            #把字典转换成字符串
            #print(data["data"])
            #INSERT INTO `work_tasks` (`task_id`, `task_name`, `creation_time`, `creator`,
            #  `task_status`, `task_class`, `progree`, `participant`, `plan_time`, `task_readme`) VALUES (NULL, '名字', '2023-07-01 00:00:00', '2', '1', '2', '32', ' [{\'title\': \'技术部-用 户1\', \'value\': 1}, {\'title\': \'技术部-用户4\', \'value\': 4}, {\'title\': \'技术部-用户7\', \'value\': 7}, {\'title\': \'技术部-用户10\', \'value\': 10}, {\'title\': \'技术部-用户13\', \'value\': 13}, {\'title\': \'技术部-用户16\', \'value\': 16}, {\'title\': \'技术部-用户19\', \'value\': 19}, {\'title\': \'市场部-用户2\', \'value\': 2}, {\'title\': \'市场部-用户5\', \'value\': 5}, {\'title\': \'市场部-用户8\', \'value\': 8}, {\'title\': \'市场部-用户11\', \'value\': 11}, {\'title\': \'市场部-用户14\', \'value\': 14}, {\'title\': \'市场部-用户17\', \'value\': 17}, {\'title\': \'市场部-用户20\', \'value\': 20}, {\'title\': \'工厂-用户3\', \'value\': 3}, {\'title\': \'工厂-用户6\', \'value\': 6}, {\'title\': \'工厂-用户9\', \'value\': 9}, {\'title\': \'工厂-用户12\', \'value\': 12}, {\'title\': \'工厂-用户15\', \'value\': 15}, {\'title\': \'工厂-用户18\', \'value\': 18}]', '2023-07-12 00:00:00', '说明');
            
            task_name = data["data"]["task_name"]
            creator = session["user_id"]
            task_status = '1'
            task_class = data["data"]["rw"]
            progree = '0'
            participant = data["data"]["users"]
            plan_time = data["data"]["endtime"]
            task_readme = data["data"]["readme"]

            if data["data"]["rw"] == '3':
                progree = '100'
                task_status = '2'
            link_sub_id = int(data["link_sub_id"])
            if link_sub_id > 0:
                pass
                



            
            sql = "INSERT INTO `work_tasks` (`task_id`, `task_name`, `creation_time`, `creator`, `task_status`, `task_class`, `progree`, `participant`, `plan_time`, `task_readme`, `created_department`,`link_sub`) VALUES (NULL,"
            istr = data["data"]["task_name"]
            #把字符串中双引号前面加上反斜杠
            istr = istr.replace('"', '\\"')
            #istr = istr.replace('"', '\"')
            sql = sql + '"'+istr +'"'+","
            task_class = data["data"]["rw"]
            sql = sql + "NOW(),"+str(session["user_id"])+","+task_status+","+str(data["data"]["rw"])+","+progree+","
            istr = str(data["data"]["users"])
            user_list = istr
            #把字符串中双引号和单引号和\ 加上注解
            istr = istr.replace('"', '\\"')
            #istr = istr.replace("'", "\'")
            #istr = istr.replace("\\", "\\\\")
            sql = sql + '"'+istr +'"'+","
            # `plan_time`, `task_readme`
            sql = sql + '"'+data["data"]["endtime"] +'"'+","
            istr = data["data"]["readme"]
            #把字符串中双引号和单引号和\ 加上注解
            istr = istr.replace('"', '\\"')
           # istr = istr.replace("'", "\'")
            #istr = istr.replace("\\", "\\\\")
            sql = sql + '"'+istr +'",'+str(session["department_id"])+","+str(link_sub_id)+")"
            print(sql)
            db.connect()
            result = db.write(sql)
            #获取刚刚插入的数据的id
            sql = "SELECT LAST_INSERT_ID() as id"
            result = db.read(sql)
            upid = result[0]["id"]
            print(upid)

            #更新sub_tasks表中的link_task 字段的值为 upid 条件是 id = link_sub_id
            if link_sub_id > 0:
                sql = "UPDATE sub_tasks SET link_task = "+str(upid)+" WHERE id = "+str(link_sub_id)
                print(sql)

                result = db.write(sql)
                print(result)



            if task_class == '2' or task_class == '4':
                
                #创建一条sql语句，把上述信息插入到 sub_tasks 表中
                l='`id`,`task_id`,`sub_task_name`,`sub_task_description`,\
                 `end_time`,`created_at`,`create_user_id`,\
                    `next_user_id`,`next_sub_task_id`,`completion_rate`,\
                        `sub_user`,`state`,`sub_class`'
                sql = "INSERT INTO `sub_tasks` (`id`,`task_id`,`sub_task_name`,`sub_task_description`,`end_time`,`created_at`,`create_user_id`,`next_user_id`,`next_sub_task_id`,`completion_rate`,`sub_user`,`state`,`task_class`) VALUES "
                
                #abdd = "[{'title': '技术部-用户4', 'value': 4}, {'title': '技术部-用户7', 'value': 7}, {'title': '技术部-用户16', 'value': 16}, {'title': '市场部-万五', 'value': 2}]"
                #把字符串转换成字典
                user_list = eval(user_list)



                #遍历 user_list
                for i in user_list:


                    sql = sql + '(NULL,'+str(upid)+','+'"'+task_name+'"'+','+'"'+task_readme+'"'+','
                    sql = sql + '"'+plan_time+'"'+',NOW(),'+str(creator)+','
                    sql = sql + '0,0,0,'
                    sql = sql + str(i["value"])+',1,'+task_class+'),'
                
                #去除最后一个逗号
                sql = sql[:-1]
                print(sql)
                result = db.write(sql)
                db.conn.close()

                    





            if result == 0:
                return {'code': 1, 'g_command':'push_task','message': 'fail'}
            else:
                return {'code': 0, 'g_command':'push_task','message': 'success'}
        if get_command == 'get_tasks':

            myid = session["user_id"]
            #sql 语句 搜索 work_tasks表 关联 users ,条件是 creator = myid  ,task_status = 1   关联 users表的user_id 关联 work_tasks表的creator
            
            mydepartment	= session["department_id"]

            #获取部门名字
            sql = 'SELECT department_name,department_id FROM departments WHERE department_id = ' + str(data["department"])
            db.connect()
            result = db.read(sql)
            db.conn.close()
           

            if len(result) == 0:
                department_name = session["department_name"]
                department_id = session["department_id"]
                
            else:
                department_name = result[0]['department_name']
                department_id = result[0]['department_id']
           
            depstr = ""
            if data["department"]==0:
                depstr = ""
                #department_name="所有部门"
            else:
                depstr = " WHERE work_tasks.created_department = "+str(data["department"])
                
        



            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks INNER JOIN users ON work_tasks.creator = users.user_id'
            #给sql语句 增加条件  只返回 50条 `task_id` 倒排序
            sql = sql + depstr + ' ORDER BY `task_id` DESC LIMIT 50'

            

            db.connect()
            result = db.read(sql)
            db.conn.close()
            # result = [19: {'user_id': 18, 'username': 'user18', 'chinese_name': '用户18', 'department_id': 3, 'password': '', 'department_name': '工厂'}，
            # 19: {'user_id': 18, 'username': 'user18', 'chinese_name': '用户18', 'department_id': 3, 'password': '', 'department_name': '工厂'}]
            # 生成新的列表 用于前端显示 保留 user_id chinese_name department_name
            new_result = []
            for i in result:
                idate = i['creation_time']
                #把时间格式转换为带中文的 年月日
                idate = idate.strftime("%Y年%m月%d日")
                i['creation_time'] = idate

                new_result.append({'task_id': i['task_id'], 'task_name':i['task_name'], 'creation_time':i['creation_time'], 'chinese_name':i['chinese_name'],'progree': i['progree'],'task_class': i['task_class'],'task_status': i['task_status'],'plan_time': i['plan_time']})
            return { 'the_department_id':data["department"],'department_name':department_name,'department_id':department_id, 'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_tasks','message': 'success', 'data': new_result}            
        
        if get_command == 'get_run_tasks':
            myid = session["user_id"]
            #sql 语句 搜索 work_tasks表 关联 users ,条件是 creator = myid  ,task_status = 1   关联 users表的user_id 关联 work_tasks表的creator
            
            mydepartment	= session["department_id"]

            sql = 'SELECT department_name,department_id FROM departments WHERE department_id = ' + str(data["department"])
            db.connect()
            result = db.read(sql)
            db.conn.close()

            if len(result) == 0:
                department_name = session["department_name"]
                department_id = session["department_id"]
                
            else:
                department_name = result[0]['department_name']
                department_id = result[0]['department_id']
            





            #depstr = ""
            #if data["department"]==1:
            #    depstr = " AND work_tasks.created_department = "+str(mydepartment)
            #else:
            #    depstr = ""
        
            depstr = ""
            if data["department"]==0:
                depstr = ""
                department_name= session["department_name"]
            else:
                depstr = " AND work_tasks.created_department = "+str(data["department"])
                
        




            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks INNER JOIN users ON work_tasks.creator = users.user_id WHERE work_tasks.task_status = 1 '+ depstr
            #给sql语句 增加条件  只返回 50条 `task_id` 倒排序
            sql = sql + ' ORDER BY `task_id` DESC LIMIT 50'

            

            db.connect()
            result = db.read(sql)
            #db.conn.close()
            # result = [19: {'user_id': 18, 'username': 'user18', 'chinese_name': '用户18', 'department_id': 3, 'password': '', 'department_name': '工厂'}，
            # 19: {'user_id': 18, 'username': 'user18', 'chinese_name': '用户18', 'department_id': 3, 'password': '', 'department_name': '工厂'}]
            # 生成新的列表 用于前端显示 保留 user_id chinese_name department_name
            new_result = []
            for i in result:
                idate = i['creation_time']
                #把时间格式转换为带中文的 年月日
                idate = idate.strftime("%Y年%m月%d日")
                i['creation_time'] = idate

                new_result.append({'task_id': i['task_id'], 'task_name':i['task_name'], 'creation_time':i['creation_time'], 'chinese_name':i['chinese_name'],'progree': i['progree'],'task_class': i['task_class'],'task_status': i['task_status'],'plan_time': i['plan_time']})
            #return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_run_tasks','message': 'success', 'data': new_result}            
            return { 'the_department_id':data["department"], 'department_name':department_name,'department_id':department_id, 'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_run_tasks','message': 'success', 'data': new_result}            
       
        if get_command == 'get_task':
            #sql 语句 搜索 work_tasks表 关联 users ,条件是 task_id = data["task_id"]  关联 users表的user_id 关联 work_tasks表的creator
            #sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks INNER JOIN users ON work_tasks.creator = users.user_id WHERE task_id = ' + str(data["task_id"])
            sql = 'SELECT work_tasks.*, users.username, users.chinese_name FROM work_tasks INNER JOIN users ON work_tasks.creator = users.user_id WHERE task_id = ' + str(data["task_id"])
            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = result[0]

            new_result["creation_time"] = new_result["creation_time"].strftime("%m月%d日")
            new_result["plan_time"] = new_result["plan_time"].strftime("%m月%d日")

            arrstr = new_result["participant"]
            #去除字符串中的 [ 字符
            arrstr = arrstr.replace("'", '"')
            #去除字符串中的 ] 字符
            #arrstr = arrstr.replace(']', '')

            #nstr = "{'abc':[{'title': '技术部-用户1', 'value': 1}, {'title': '技术部-用户4', 'value': 4}, {'title': '技术部-用户7', 'value': 7}, {'title': '技术部-用户10', 'value': 10}, {'title': '技术部-用户13', 'value': 13}, {'title': '技术部-用户16', 'value': 16}, {'title': '技术部-用户19', 'value': 19}, {'title': '市场部-用户2', 'value': 2}, {'title': '市场部-用户5', 'value': 5}, {'title': '市场部-用户8', 'value': 8}, {'title': '市场部-用户11', 'value': 11}, {'title': '市场部-用户14', 'value': 14}, {'title': '市场部-用户17', 'value': 17}, {'title': '市场部-用户20', 'value': 20}, {'title': '工厂-用户3', 'value': 3}, {'title': '工厂-用户6', 'value': 6}, {'title': '工厂-用户9', 'value': 9}, {'title': '工厂-用户12', 'value': 12}, {'title': '工厂-用户15', 'value': 15}, {'title': '工厂-用户18', 'value': 18}]}"

            #把字符串nstr 转换成 对象

            #nstr = json.loads(nstr)


            arrstr = json.loads(arrstr)
            new_result["participant"] = arrstr
            new_result["task_readme"] = new_result["task_readme"].replace('\n', '<br>')
            new_result["task_readme"] = new_result["task_readme"].replace(' ', '&nbsp;')
            new_result["task_readme"] = new_result["task_readme"].replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
            new_result["chinese_name"] = new_result['chinese_name']


            


           #把new_result 转换为json
            #new_result = json.dumps(new_result)
            


                #new_result.append({'task_id': i['task_id'], 'task_name':i['task_name'], 'creation_time':i['creation_time'], 'chinese_name':i['chinese_name'],'progree': i['progree'],'task_class': i['task_class'],'task_status': i['task_status'],'plan_time': i['plan_time']})
            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_task','message': 'success', 'data': new_result}   
        if get_command == 'create_execuition': #更新主任务状态
            task_id = data['task_id']
            #获取task的状态
            sql = 'SELECT * FROM work_tasks WHERE task_id = ' + str(task_id)
            db.connect()
            result = db.read(sql)
            db.conn.close()
            task_status = result[0]['task_status']
            link_sub = result[0]['link_sub']


            

            
            #
            sql = 'INSERT INTO task_execution (task_id,sub_task_id,completion_rate,completion_description,execution_time,submitter,modify_by,state,type,state_up) VALUES ('
            sql = sql + str(data['task_id']) + ','
            sql = sql + str(data['sub_task_id']) + ','
            sql = sql + str(data['completion_rate']) + ','
            sql = sql + "'" + data['completion_description'] + "',"
            sql = sql + "NOW(),"
            sql = sql + str(session['user_id']) + ','
            sql = sql + str(session['user_id']) + ','
            sql = sql + str(data['state']) + ','
            sql = sql + str(data['type']) + ','
            sql = sql + str(task_status) + ')'
            
            db.connect()
            result = db.write(sql)
            db.conn.close()
            #更新work_task表中的progree字段
            sql = 'UPDATE work_tasks SET task_ctrl_time = NOW(), progree = ' + str(data['completion_rate']) + ',task_status='+data['state']+' WHERE task_id = ' + str(data['task_id'])
            db.connect()
            result = db.write(sql)
            db.conn.close()
            db.connect()
            if link_sub > 0:
                #data={}


                data['progress'] = str(data['completion_rate'])
                data['sub_task_id'] = link_sub   
                data['set_state'] = int(data['state'])
                data['p_readme'] = data['completion_description']

                result = update_sub_progress(data)


            if result == 0:
                return {'code': 1, 'g_command':'create_execuition','message': 'fail'}
            else:
                return {'code': 0, 'g_command':'create_execuition','message': 'success'}
        if get_command == 'get_execution':
            if data['type'] == 1:
                #创建sql语句 task_id = data['task_id'] ，execution_time 倒排序
                sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(data['task_id']) + ' ORDER BY execution_time DESC'
            else:
                sql = 'SELECT * FROM task_execution WHERE sub_task_id = ' + str(data['sub_task_id']) + ' ORDER BY execution_time DESC'

            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = []
            for i in result:
                i['execution_time'] = i['execution_time'].strftime("%m-%d")
                i['completion_description'] = i['completion_description'].replace('\n', '<br>')
                i['completion_rate'] = str(i['completion_rate'])
                i['state'] = str(i['state'])
                i['type'] = str(i['type'])
                new_result.append(i)
            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_execution','message': 'success', 'data': new_result}
        if get_command == 'create_discussions':
            sql = 'INSERT INTO discussions (sub_task_id,speaker_id,speak_time,work_tasks_id, type, text) VALUES ('
            sql = sql + str(data['sub_task_id']) + ','
            sql = sql + str(session['user_id']) + ','
            sql = sql + "NOW(),"
            sql = sql + str(data['task_id']) + ','
            sql = sql + str(data['type']) + ','
            sql = sql + "'" + data['text'] + "')"
            db.connect()
            result = db.write(sql)
            db.conn.close()
            if result == 0:
                return {'code': 1, 'g_command':'create_discussions','message': 'fail'}
            else:
                return {'code': 0, 'g_command':'create_discussions','message': 'success'}
        if get_command == 'get_discussions':
            #sql语句 work_tasks_id = data['task_id'] speak_time 倒排序 speaker_id关联user表的user_id
            #sql = 'SELECT discussions.*,user.chinese_name FROM discussions,user WHERE discussions.work_tasks_id = ' + str(data['task_id']) + ' AND discussions.speaker_id = user.user_id ORDER BY speak_time DESC'
            sql = 'SELECT discussions.*,users.chinese_name FROM discussions,users WHERE discussions.work_tasks_id = ' + str(data['task_id']) + ' AND discussions.speaker_id = users.user_id ORDER BY speak_time DESC'
            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = []
            for i in result:
                i['speak_time'] = i['speak_time'].strftime("%m-%d")
                i['text'] = i['text'].replace('\n', '<br>')
                i['type'] = str(i['type'])
                new_result.append(i)
            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_discussions','message': 'success', 'data': new_result}
        if get_command == 'create_sub_task':
            data = data['data']
            sql = 'INSERT INTO sub_tasks (task_id, sub_task_name,sub_task_description,end_time,\
                created_at,create_user_id,completion_rate,sub_user,state,task_class) VALUES ('
            sql = sql + str(data['task_id']) + ','
            sql = sql + "'" + data['sub_task_name'] + "',"
            sql = sql + "'" + data['sub_task_description'] + "',"
            sql = sql + "'" + data['end_time'] + "',"
            sql = sql + "NOW(),"
            sql = sql + str(session['user_id']) + ','
            sql = sql + '0 ,'
            sql = sql + str(data['sub_user']) + ','
            sql = sql + str(data['sub_state']) + ','
            sql =  sql + str(data['task_class']) + ")"
            db.connect()
            result = db.write(sql)
            db.conn.close()
            if result == 0:
                return {'code': 1, 'g_command':'create_sub_task','message': 'fail'}
            else:
                return {'code': 0, 'g_command':'create_sub_task','message': 'success'}
        if get_command == 'get_sub_task_list':
            #sql语句 task_id = data['task_id'] sub_user关联user表的user_id create_user_id关联user表的user_id
            sql = 'SELECT sub_tasks.*,users.chinese_name AS sub_user_name,users2.chinese_name AS create_user_name FROM sub_tasks,users,users AS users2 WHERE sub_tasks.task_id = ' + str(data['task_id']) + ' AND sub_tasks.sub_user = users.user_id AND sub_tasks.create_user_id = users2.user_id'
            #sql = 'SELECT * FROM sub_tasks WHERE task_id = ' + str(data['task_id'])
            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = []
            for i in result:
                i['end_time'] = i['end_time'].strftime("%m-%d")
                i['created_at'] = i['created_at'].strftime("%m-%d")
                i['state'] = str(i['state'])
                new_result.append(i)
            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_sub_task_list','message': 'success', 'data': new_result}
        if get_command == 'get_sub_task':

            #sql 语句 sub_task_id 作为条件 sub_user关联user表的user_id create_user_id关联user表的user_id
            sql = 'SELECT sub_tasks.*,users.chinese_name AS sub_user_name,users2.chinese_name AS create_user_name FROM sub_tasks,users,users AS users2 WHERE sub_tasks.id = ' + str(data['sub_task_id']) + ' AND sub_tasks.sub_user = users.user_id AND sub_tasks.create_user_id = users2.user_id'
            ###sql = 'SELECT * FROM sub_tasks WHERE id = ' + str(data['sub_task_id'])
            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = []
            #判读result是什么类型
            try:
                result[0]
            except:
                return {'user_id':user_id,'chinese_name':chinese_name,'code': 1, 'g_command':'get_sub_task','message': 'fail','data': new_result}
            
            if len(result) == 0:
                return {'user_id':user_id,'chinese_name':chinese_name,'code': 1, 'g_command':'get_sub_task','message': 'fail','data': new_result}
            else:
                for i in result:
                    i['end_time'] = i['end_time'].strftime("%m-%d")
                    i['created_at'] = i['created_at'].strftime("%m-%d")
                    i['state'] = str(i['state'])
                    new_result.append(i)
                #获取sub_progress 子任务状态表的相关数据，sup_time 倒排序 最多5条
                sql = 'SELECT * FROM sub_progress WHERE sup_task_id = ' + str(data['sub_task_id']) + ' ORDER BY sup_time DESC LIMIT 5'

                db.connect()
                result = db.read(sql)
                db.conn.close()
                sub_progress = []
                for i in result:
                    i['sup_time'] = i['sup_time'].strftime("%m-%d")
                    sub_progress.append(i)
                



                

                return {'sub_progress':sub_progress,'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_sub_task','message': 'success','data': new_result}
        if get_command == 'create_sub_step':
            data = data['data']
            sql = 'INSERT INTO `sub_task_step` (`id`, `completion_rate`, `step_name`, `step_readme`, `sub_tasks_id`) VALUES (NULL,0,'
            sql = sql + "'" + data['step_name'] + "',"
            sql = sql + "'" + data['step_readme'] + "',"
            sql = sql + str(data['sub_task_id']) + ')'
            db.connect()
            result = db.write(sql)
            db.conn.close()
            if result == 0:
                return {'code': 1, 'g_command':'create_sub_step','message': 'fail'}
            else:
                return {'code': 0, 'g_command':'create_sub_step','message': 'success'}
        if get_command == 'get_sub_step_list':
            sql = 'SELECT * FROM sub_task_step WHERE sub_tasks_id = ' + str(data['sub_task_id'])
            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = []
            for i in result:
                i['create_time'] = i['create_time'].strftime("%m-%d")
                i['step_readme'] =""
                i['step_progress']=[]
                new_result.append(i)
                # sql 语句 搜索 setp_progress表,条件是 step_id = i['id'] 返回最多返回2条数据
                sql = ' SELECT * FROM `setp_progress` WHERE `step_id` =' + str(i['id']) + ' ORDER BY sp_id DESC LIMIT 2'
               #1 ORDER BY sp_id DESC LIMIT 2
                db.connect()
                result2 = db.read(sql)
                db.conn.close()
                for j in result2:
                    j['sp_time'] = j['sp_time'].strftime("%m-%d")
                    i['step_progress'].append(j)
            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_sub_step_list','message': 'success', 'data': new_result}
        if get_command == 'get_sub_step':
            sql = 'SELECT * FROM sub_task_step WHERE id = ' + str(data['step_id'])
            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = []
            for i in result:
                i['create_time'] = i['create_time'].strftime("%m-%d")
                i['step_progress']=[]
                new_result.append(i)
                # sql 语句 搜索 setp_progress表,条件是 step_id = i['id'] 返回最多返回2条数据
                sql = ' SELECT * FROM `setp_progress` WHERE `step_id` =' + str(i['id']) + ' ORDER BY sp_id DESC'
               #1 ORDER BY sp_id DESC LIMIT 2
                db.connect()
                result2 = db.read(sql)
                db.conn.close()
                for j in result2:
                    j['sp_time'] = j['sp_time'].strftime("%m-%d")
                    i['step_progress'].append(j)
            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_sub_step','message': 'success', 'data': new_result}
        if get_command == 'create_sub_step_progress':
           
            sql = 'INSERT INTO `setp_progress` (`sp_id`, `step_id`, `progress`, `sp_text`) VALUES (NULL,'
            sql = sql + str(data['step_id']) + ','
            sql = sql + str(data['progress']) + ','
            sql = sql + "'" + data['sp_text'] + "')"
            step_id=data['step_id']
            progress = data['progress']


            db.connect()
            result = db.write(sql)
            db.conn.close()
            #把 sub_task_step 表的 completion_rate 更新
            #创建update 更新sql 语句
            sql = 'UPDATE `sub_task_step` SET `completion_rate` = ' + str(progress) + ' WHERE `sub_task_step`.`id` = ' + str(step_id)
            db.connect()
            result = db.write(sql)
            db.conn.close()
            

            if result == 0:
                return {'code': 1, 'g_command':'create_sub_step_progress','message': 'fail'}
            else:
                return {'code': 0, 'g_command':'create_sub_step_progress','message': 'success'}
        if get_command == 'set_sub_progress':#更新子任务状态
            result = update_sub_progress(data)

            if result == 0:
                return {'code': 1, 'g_command':'set_sub_progress','message': 'fail'}
            else:
                return {'code': 0, 'g_command':'set_sub_progress','message': 'success'}
        if get_command == 'get_my_sub_tasks':
            
            
            if (data['user_id'] == 0):
                myid = session["user_id"]
            else:
                myid = data['user_id']
            
            #sql 语句 搜索 sub_tasks表 关联 users ,条件是 sub_user = myid sub_str ,state = 1   关联 users表的user_id  create_user_id 关联 users 表的user_id
            #sql = 'SELECT * FROM sub_tasks,users WHERE sub_user = ' + str(myid) + ' AND sub_str = 1 AND sub_tasks.create_user_id = users.user_id'
            sql = 'SELECT work_tasks.task_status , work_tasks.task_name, sub_tasks.*,users.chinese_name AS sub_user_name,users2.chinese_name AS create_user_name FROM work_tasks, sub_tasks,users,users AS users2 WHERE sub_tasks.sub_user = users.user_id AND sub_tasks.create_user_id = users2.user_id AND sub_tasks.state IN (1,3) AND sub_tasks.task_id = work_tasks.task_id AND work_tasks.task_status  IN (1,3) AND \
                sub_tasks.sub_user ='+str(myid)
            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = []
            for i in result:
                i['end_time'] = i['end_time'].strftime("%m-%d")
                i['created_at'] = i['created_at'].strftime("%m-%d")
                i['state'] = str(i['state'])
                i['sub_task_description'] = ""
                chinese_name = i['sub_user_name']
                new_result.append(i)
            
            if len(result) == 0:
                #sql 搜索users 表 通过user_id = myid 返回 chinese_name
                sql = 'SELECT * FROM users WHERE user_id = ' + str(myid)
                db.connect()
                result = db.read(sql)
                db.conn.close()
                chinese_name = result[0]['chinese_name']
                myid = result[0]['user_id']
                renum = 0
            else:
                renum = 1



            return {'user_id':myid,'chinese_name':chinese_name,'code': 0, 'renum':renum,'g_command':'get_my_sub_tasks','message': 'success', 'data': new_result}
        if get_command == 'get_my_tasks':
            depstr = ""
            myid = session["user_id"]
            
            if (data['user_id'] == 0):
                myid = session["user_id"]
            else:
                myid = data['user_id']
            
            
            sql = 'SELECT work_tasks.*,users.chinese_name AS creator_name FROM work_tasks,users WHERE  task_status IN (1,3) AND  creator = ' + str(myid) + ' AND work_tasks.creator = users.user_id '+depstr+' ORDER BY task_id DESC' 

            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = []
            for i in result:
                i['plan_time'] = i['plan_time'].strftime("%m-%d")
                i['creation_time'] = i['creation_time'].strftime("%m-%d")
                i['task_readme'] = ""
                i['participant']= ""
                new_result.append(i)
            
            sql = 'SELECT work_tasks.*,users.chinese_name AS creator_name FROM work_tasks,users WHERE  task_status NOT IN (1,3) AND  creator = ' + str(myid) + ' AND work_tasks.creator = users.user_id ORDER BY task_ctrl_time DESC' 
            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result2 = []
            for i in result:
                i['plan_time'] = i['plan_time'].strftime("%m-%d")
                i['creation_time'] = i['creation_time'].strftime("%m-%d")
                i['task_readme'] = ""
                i['participant']= ""
                new_result2.append(i)

            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_my_tasks','message': 'success','data2':new_result2 ,'data': new_result}
        if get_command == 'set_sub_close':
            state = str(data['state'])

            sql = 'UPDATE `sub_tasks` SET `state` = '+state+' WHERE `sub_tasks`.`id` = ' + str(data['sub_task_id'])
            db.connect()
            result = db.write(sql)
            db.conn.close()
            if result == 0:
                return {'code': 1, 'g_command':'set_sub_step_close','message': 'fail'}
            else:
                return {'code': 0, 'g_command':'set_sub_step_close','message': 'success'}
        if get_command == 'login':
            username = data['username']
            password = data['password']
            #产生sql语句通过username和password查询数据库，关联部门表
            sql = f"SELECT u.*,d.*,f.* FROM users u JOIN department_members dm ON u.user_id = dm.user_id JOIN departments d ON dm.department_id = d.department_id JOIN function_members fm ON u.user_id = fm.user_id JOIN functions f ON fm.function_id = f.function_id  WHERE username = '{username}' AND password = '{password}'"
            db.connect()
            result = db.read(sql)
            #db.conn.close()

            if len(result) == 0:
                
                session['username'] = ""
                session['chinese_name'] = ""
                session['department_name'] = ""
                session['department_id'] = 0
                session['user_id'] = 0
                session['functionarr'] = 0
                return {'code': 1, 'g_command':'login','message': 'fail'}
            else:

                functionarr = []
                for i in result:
                    functionarr.append(i['function_name'])



                session['username'] = username
                session['chinese_name'] = result[0]['chinese_name']
                session['department_name'] = result[0]['department_name']
                session['department_id'] = result[0]['d.department_id']
                session['user_id'] = result[0]['user_id']
                session['functionarr'] = functionarr

                #返回json
                return {'code': 0, 'g_command':'login','message': 'success'}
        if get_command == 'get_my_history':
            myid =  session["user_id"]
            if (data['user_id'] == 0):
                myid = session["user_id"]
            else:
                myid = data['user_id']
            
            sql = 'SELECT work_tasks.task_status , work_tasks.task_name, sub_tasks.*,users.chinese_name AS sub_user_name,users2.chinese_name AS create_user_name FROM work_tasks, sub_tasks,users,users AS users2 WHERE sub_tasks.sub_user = users.user_id AND sub_tasks.create_user_id = users2.user_id  AND sub_tasks.task_id = work_tasks.task_id AND sub_tasks.sub_user ='+str(myid) + ' ORDER BY sub_ctrl_time DESC'
            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = []
            for i in result:
                i['end_time'] = i['end_time'].strftime("%m-%d")
                i['created_at'] = i['created_at'].strftime("%m-%d")
                i['state'] = str(i['state'])
                i['sub_task_description'] = ""
                new_result.append(i)
            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_my_history','message': 'success', 'data': new_result}
        if get_command == 'get_daily_report':  #日报的英文是 daily report        
            #sql work_tasks表中的 task_status = 1 和 task_class = 1 的数据 关联 users表的user_id 得到 chinese_name
            outstr = "<br> 今日工作报告 <br> 本报告以每天 23.50 分做出的为准<br>"
            #显示今天限时类工作
            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.task_status = 1 AND work_tasks.task_class IN(1,2,4) AND work_tasks.creator = users.user_id ORDER BY task_class ASC'
            
            db.connect()
            result = db.read(sql)
            new_result = []
            
            
            work_master_lazy = {}
            work_lazy = {}

            #获取当前的 年-月-日

            now_ymd = datetime.datetime.now().strftime("%Y-%m-%d")

            for i in result:
                st = i['creation_time'].strftime("%m-%d")
                en = i['plan_time'].strftime("%m-%d")
                work = ""
                if i['task_class'] == 1:
                    work= '限时类工作'
                elif i['task_class'] == 4:
                    work = '群体工作'
                elif i['task_class'] == 2:
                    work = '每日类工作'




                new_result.append(i)
                outstr =  outstr + work+':<b>' + i['task_name'] + '</b> 计划时间['+st+' 到 '+en+'] 创建人: '+i['chinese_name']+' \n'
                #sql 搜索 sub_tasks 表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.state = 1 AND sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                db.connect()
                result2 = db.read(sql)
                r2_len = len(result2)
                if i['task_class'] == 1:
                    outstr = outstr + '有' + str(r2_len) + '个需执行子任务,执行人更新状态如下:\n'
                elif i['task_class'] == 4:
                    outstr = outstr + '有' + str(r2_len) + '人参与他她们是:\n'
                elif i['task_class'] == 2:
                    outstr = outstr + '有' + str(r2_len) + '参与,大家的更新状态如下:\n'
                
                
                the_num = 0
                mstr = "["
                tstr =""
                for j in result2:
                    the_num = the_num + 1
                    ctrl_time =  j['sub_ctrl_time'].strftime("%Y-%m-%d")
                    td = ""
                    if ctrl_time == now_ymd:
                        #把j['completion_rate']转为字符串

                        td= j['completion_rate']
                        td = str(td)+'%'
                        
                    else:
                        td = '偷懒了!'
                        work_lazy[j['chinese_name']] = 1
                        
                    tstr = tstr + str(the_num) + '.'+j['sub_task_name']+' _ ['  + j['chinese_name'] + ' '+td+']<br> '
                    mstr = mstr + j['chinese_name'] + ' '
                mstr = mstr + "]"
                if i['task_class'] == 1 or i['task_class'] == 2:
                    outstr = outstr + tstr + ''
                elif i['task_class'] == 4:
                    outstr = outstr + mstr + ''


                #查询task_execution表中的数据，条件是 task_id = i['task_id'] ，execution_time 倒排序
                sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id']) + ' ORDER BY execution_time DESC'
                
                #sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id'])
                db.connect()
                result3 = db.read(sql)
                r3_len = len(result3)
                if r3_len == 0:
                    outstr = outstr + '工作负责人'+i['chinese_name']+'未提交执行报告!\n'
                    work_master_lazy[i['chinese_name']] = 1
                else:
                    outstr = outstr + '工作负责人'+i['chinese_name']+'对进度的总结是: 总进展'+str(result3[0]['completion_rate'])+'% '+result3[0]['completion_description']+'\n'

                outstr = outstr + '\n'
           
            #把ourstr 字符串中的换行符替换为 <br>
            outstr = outstr.replace('\n', '<br>')
            outstr2="<br>"
            #创建2个时间变量，一个是今天的开始时间 一个是今天的结束时间
            today_start = datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
            today_end = datetime.datetime.now().strftime("%Y-%m-%d") + " 23:59:59"
            #sql语句 搜索 task_execution 表中的数据，条件是 state =2 与 execution_time 在今天的开始时间与结束时间之间
            sql = 'SELECT users.chinese_name, task_execution.*,work_tasks.task_name FROM task_execution,work_tasks,users WHERE modify_by = users.user_id AND work_tasks.task_id = task_execution.task_id AND task_execution.state = 2 AND execution_time BETWEEN "' + today_start + '" AND "' + today_end + '"'

            db.connect()
            result = db.read(sql)
            db.conn.close()
            for i in result:
                if i['state'] != i['state_up'] and i['state'] == 2:
                    
                    #sql 搜索sub_tasks表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                    sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                    db.connect()
                    result2 = db.read(sql)
                    db.conn.close()
                    r2_len = len(result2)
                    inuser = {}
                    for j in result2:
                        inuser[j['chinese_name']] = 1
                    iustr =""
                    #遍历inuser ，取出key
                    for k in inuser:
                        iustr = iustr + k + " "




                    
                    outstr2 = outstr2 + '《'+i['task_name']+'》工作在今日完成！\n'
                    outstr2 = outstr2 + '全公司感谢【'+iustr+'】等的辛勤工作！\n'
                    outstr2 = outstr2 + '工作负责人'+i['chinese_name']+'对进度的总结是:<br>'+i['completion_description']+'\n'
                    continue

            outstr2 = outstr2.replace('\n', '<br>')
            outstr = outstr + outstr2

            #sql 搜索 work_tasks 表中的数据，条件是 task_status = 2 与 task_class = 3 与时间在今天的开始时间与结束时间之间 关联 users表的user_id 得到 chinese_name
            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.task_status = 2 AND work_tasks.task_class = 3 AND work_tasks.creator = users.user_id AND work_tasks.task_ctrl_time BETWEEN "' + today_start + '" AND "' + today_end + '"'
            db.connect()
            result = db.read(sql)
            db.conn.close()
            outstr2 = "<br> 今天的快报工作有:<br>"
            for i in result:
                outstr2 = outstr2 + ' ['+i['chinese_name']+']:'+i['task_name']+'\n'
            outstr2 = outstr2.replace('\n', '<br>')
            outstr = outstr + outstr2

            outstr2 = "<br><br>我们最亲爱的工作执行者:<br>"
            for i in work_lazy:
                outstr2 = outstr2 + i + " "
            outstr2 = outstr2 + "你们今天偷懒了吗？<br><br>"

            outstr2 = outstr2 + "我们最亲爱的工作负责人:<br>"
            for i in work_master_lazy:
                outstr2 = outstr2 + i + " "
            outstr2 = outstr2 + "你们今天偷懒了吗？<br>"
            outstr2 = outstr2.replace('\n', '<br>')
            outstr = outstr + outstr2


            




            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_daily_report','message': 'success', 'outstr':outstr }
        
        if get_command == 'get_department_report':  #部门日报
            
            department = data['department']
            #根据 department 获取部门名称
            sql = 'SELECT * FROM departments WHERE department_id = ' + str(department)
            db.connect()
            result = db.read(sql)
            db.conn.close()
            department_name = result[0]['department_name']
            now_ymd = datetime.datetime.now().strftime("%Y-%m-%d") # 当期时间
            today_start = datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
            today_end = datetime.datetime.now().strftime("%Y-%m-%d") + " 23:59:59"
            outstr=""

            #获取部门下的所有用户

            sql ='SELECT users.user_id ,users.chinese_name FROM users INNER JOIN department_members ON users.user_id = department_members.user_id WHERE checkin = 1 AND department_members.department_id = '+ str(department)
            db.connect()
            result = db.read(sql)
            db.conn.close()
            user_list = {}
            id_list ={}
            id_list_str =""
            for i in result:
                user_list[i['chinese_name']] = i['user_id']
                id_list[i['user_id']] = i['chinese_name']
                id_list_str =  id_list_str + str(i['user_id']) + ","
            #去掉 id_list_str 最后一个逗号
            id_list_str = id_list_str[:-1]
            print(id_list_str)
            print(user_list)

            #搜索task_execution submitter字段中有 id_list_str 的数据
            sql = 'SELECT task_execution.* FROM task_execution WHERE task_execution.submitter IN ('+id_list_str+') AND   DATE( task_execution.execution_time) = "'+ now_ymd+'"'
            db.connect()
            result = db.read(sql)
            db.conn.close()
            #print(result)

            for i in result:
                #判读id_list中是否有key 是  i['submitter'] 的 如果有则删除
                if i['submitter'] in id_list:
                    del id_list[i['submitter']]


            #搜索sub_progress表中 sup_create_user_id 字段中有 id_list_str 的数据
            sql = 'SELECT sub_progress.* FROM sub_progress WHERE sub_progress.sup_create_user_id IN ('+id_list_str+') AND   DATE( sub_progress.sup_time) = "'+ now_ymd+'"'

            db.connect()
            result = db.read(sql)
            db.conn.close()
            #print(result)

            for i in result:
                #判读id_list中是否有key 是  i['submitter'] 的 如果有则删除
                if i['sup_create_user_id'] in id_list:
                    del id_list[i['sup_create_user_id']]



                









            #创建变量  outstr 内容是   部门名称 +  当前时间 +  ”本报告以每天 23.50 分做出的为准"
            heart_outstr = "<br><b> "+  department_name+"</b>"+now_ymd +" "+"部门工作报告<br> 本报告以每天 23.50 分做出的为准<br>"





            #sql work_tasks表中的 task_status = 1 和 task_class = 1 的数据 关联 users表的user_id 得到 chinese_name
            #outstr = "<br> 部门工作报告 <br> 本报告以每天 23.50 分做出的为准<br>"
            #显示今天限时类工作
            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 1 AND work_tasks.task_class IN(1) AND work_tasks.creator = users.user_id ORDER BY task_class ASC'
            
            db.connect()
            result = db.read(sql)
            new_result = []
            
            
            work_master_lazy = {}
            work_lazy = {}

            #获取当前的 年-月-日


            outstr = outstr+"<br><span class = \"class-bt\">进行中限时类工作:</span><br><br>"
            for i in result:
                st = i['creation_time'].strftime("%m-%d")
                en = i['plan_time'].strftime("%m-%d")
                work = ""
                if i['task_class'] == 1:
                    work= '限时类工作'
                elif i['task_class'] == 4:
                    work = '群体工作'
                elif i['task_class'] == 2:
                    work = '每日类工作'




                new_result.append(i)
                outstr =  outstr +'<b>' + i['task_name'] + '</b>['+st+'>'+en+']['+str(i['progree'])+'%] '+i['chinese_name']+' \n'
                #sql 搜索 sub_tasks 表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.state = 1 AND sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                db.connect()
                result2 = db.read(sql)
                r2_len = len(result2)
                
                
                the_num = 0
                mstr = "["
                tstr =""
                for j in result2:
                    the_num = the_num + 1
                    ctrl_time =  j['sub_ctrl_time'].strftime("%Y-%m-%d")
                    td = ""
                    hu =""
                    hud = ""
                    if ctrl_time == now_ymd:
                        #把j['completion_rate']转为字符串

                        td= j['completion_rate']
                        td = str(td)+'%'
                        # 把进行过工作的都删除了，剩下的就是没工作的
                        #查看 user_list 字典中是否有 j['chinese_name'] 这个key
                        if j['chinese_name'] in user_list:
                            #有的话就删除了
                            del user_list[j['chinese_name']]

                        
                    else:
                        hu="<u>"
                        hud="</u>"
                        td = '偷懒了!'
                        work_lazy[j['chinese_name']] = 1
                        
                    tstr = tstr + "&nbsp&nbsp"+str(the_num) + '.'+j['sub_task_name']+' _ ['+hu  + j['chinese_name'] + ' '+td+hud+']<br> '
                    mstr = mstr + j['chinese_name'] + ' '
                mstr = mstr + "]"
                if i['task_class'] == 1 or i['task_class'] == 2:
                    outstr = outstr + tstr + '</li></h2>'
                elif i['task_class'] == 4:
                    outstr = outstr + mstr + '</li></h2>'
                


                #查询task_execution表中的数据，条件是 task_id = i['task_id'] ，execution_time 倒排序
                sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id']) + ' AND    DATE(execution_time) = "'+now_ymd+'"  ORDER BY execution_time DESC'
                
                #sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id'])
                db.connect()
                result3 = db.read(sql)
                r3_len = len(result3)
                if r3_len == 0:
                    outstr = outstr + '工作负责人<u>'+i['chinese_name']+'未提交执行报告!</u>\n'
                    work_master_lazy[i['chinese_name']] = 1
                else:
                    outstr = outstr + '本工作总责任人<b>'+i['chinese_name']+'</b>对进度的总结是: 总进展'+str(result3[0]['completion_rate'])+'% '+result3[0]['completion_description']+'\n'
                    if i['chinese_name'] in user_list:
                        #有的话就删除了
                        del user_list[i['chinese_name']]
                outstr = outstr +"<br>"
            
           
            #把ourstr 字符串中的换行符替换为 <br>
            outstr = outstr.replace('\n', '<br>')
            outstr = outstr+"</ol>"


            outstr = outstr+"<br><br><span class = \"class-bt\">每日类工作完成情况:</span><br><br>"

            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 1 AND work_tasks.task_class IN(2) AND work_tasks.creator = users.user_id ORDER BY task_class ASC'
            
            db.connect()
            result = db.read(sql)
            new_result = []
            
            
            work_master_lazy = {}
            work_lazy = {}

            for i in result:
                st = i['creation_time'].strftime("%m-%d")
                en = i['plan_time'].strftime("%m-%d")
                work = ""
                if i['task_class'] == 1:
                    work= '限时类工作'
                elif i['task_class'] == 4:
                    work = '群体工作'
                elif i['task_class'] == 2:
                    work = '每日类工作'




                new_result.append(i)
                outstr =  outstr +'<b>' + i['task_name'] + '</b>['+st+'>'+en+']['+str(i['progree'])+'%] '+i['chinese_name']+' \n'
                #sql 搜索 sub_tasks 表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.state = 1 AND sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                db.connect()
                result2 = db.read(sql)
                r2_len = len(result2)
                
                
                the_num = 0
                mstr = "["
                tstr =""
                for j in result2:
                    the_num = the_num + 1
                    ctrl_time =  j['sub_ctrl_time'].strftime("%Y-%m-%d")
                    td = ""
                    hu =""
                    hud = ""
                    if ctrl_time == now_ymd:
                        #把j['completion_rate']转为字符串

                        td= j['completion_rate']
                        td = str(td)+'%'
                        
                    else:
                        hu="<u>"
                        hud="</u>"
                        td = '偷懒了!'
                        work_lazy[j['chinese_name']] = 1
                        
                    tstr = tstr + "&nbsp&nbsp"+str(the_num) + '. ['+hu  + j['chinese_name'] + ' '+td+hud+']<br> '
                    mstr = mstr + j['chinese_name'] + ' '
                mstr = mstr + "]"
                if i['task_class'] == 1 or i['task_class'] == 2:
                    outstr = outstr + tstr + '</li></h2>'
                elif i['task_class'] == 4:
                    outstr = outstr + mstr + '</li></h2>'


                #查询task_execution表中的数据，条件是 task_id = i['task_id'] ，execution_time 倒排序
                sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id']) + ' AND    DATE(execution_time) = "'+now_ymd+'"  ORDER BY execution_time DESC'
                
                #sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id'])
                db.connect()
                result3 = db.read(sql)
                r3_len = len(result3)
                if r3_len == 0:
                    outstr = outstr + '工作负责人<u>'+i['chinese_name']+'未提交执行报告!</u>\n'
                    work_master_lazy[i['chinese_name']] = 1
                else:
                    outstr = outstr + '本工作总责任人<b>'+i['chinese_name']+'</b>对进度的总结是: 总进展'+str(result3[0]['completion_rate'])+'% '+result3[0]['completion_description']+'\n'

                
            
           
            #把ourstr 字符串中的换行符替换为 <br>
            outstr = outstr.replace('\n', '<br>')
            outstr = outstr+"</ol>"





            outstr = outstr+"<br><br><span class = \"class-bt\">群体类工作完成情况:</span><br><br>"

            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 1 AND work_tasks.task_class IN(4) AND work_tasks.creator = users.user_id ORDER BY task_class ASC'
            
            db.connect()
            result = db.read(sql)
            new_result = []
            
            
            work_master_lazy = {}
            work_lazy = {}

            for i in result:
                st = i['creation_time'].strftime("%m-%d")
                en = i['plan_time'].strftime("%m-%d")
                work = ""
                if i['task_class'] == 1:
                    work= '限时类工作'
                elif i['task_class'] == 4:
                    work = '群体工作'
                elif i['task_class'] == 2:
                    work = '每日类工作'




                new_result.append(i)
                outstr =  outstr +'<b>' + i['task_name'] + '</b>['+st+'>'+en+']['+str(i['progree'])+'%] '+i['chinese_name']+' \n'
                #sql 搜索 sub_tasks 表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.state = 1 AND sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                db.connect()
                result2 = db.read(sql)
                r2_len = len(result2)
                
                outstr = outstr + "执行人："
                the_num = 0
                mstr = "["
                tstr =""
                for j in result2:
                    the_num = the_num + 1
                    ctrl_time =  j['sub_ctrl_time'].strftime("%Y-%m-%d")
                    td = ""
                    hu =""
                    hud = ""
                    if ctrl_time == now_ymd:
                        #把j['completion_rate']转为字符串

                        td= j['completion_rate']
                        td = str(td)+'%'
                        
                    else:
                        hu="<u>"
                        hud="</u>"
                        td = '偷懒了!'
                        work_lazy[j['chinese_name']] = 1
                        
                    tstr = tstr + "&nbsp&nbsp"+str(the_num) + '. ['+hu  + j['chinese_name'] + ' '+td+hud+']<br> '
                    mstr = mstr + j['chinese_name'] + ' '
                mstr = mstr + "]"
                if i['task_class'] == 1 or i['task_class'] == 2:
                    outstr = outstr + tstr + '</li></h2>'
                elif i['task_class'] == 4:
                    outstr = outstr + mstr + '</li></h2>'


                #查询task_execution表中的数据，条件是 task_id = i['task_id'] ，execution_time 倒排序
                sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id']) + ' AND    DATE(execution_time) = "'+now_ymd+'"  ORDER BY execution_time DESC'
                
                #sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id'])
                db.connect()
                result3 = db.read(sql)
                r3_len = len(result3)
                if r3_len == 0:
                    outstr = outstr + '工作负责人<u>'+i['chinese_name']+'未提交执行报告!</u>\n'
                    work_master_lazy[i['chinese_name']] = 1
                else:
                    outstr = outstr + '本工作总责任人<b>'+i['chinese_name']+'</b>对进度的总结是: 总进展'+str(result3[0]['completion_rate'])+'% '+result3[0]['completion_description']+'\n'

                
            
           
            #把ourstr 字符串中的换行符替换为 <br>
            outstr = outstr.replace('\n', '<br>')
            outstr = outstr+"</ol>"




























            outstr = outstr+"<br><br><span class = \"class-bt\">今天完成的工作:</span><br>"
            outstr2 = ""
            sql = 'SELECT users.chinese_name, task_execution.*,work_tasks.task_name FROM task_execution,work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND modify_by = users.user_id AND work_tasks.task_id = task_execution.task_id AND task_execution.state = 2 AND execution_time BETWEEN "' + today_start + '" AND "' + today_end + '"'

            db.connect()
            result = db.read(sql)
            db.conn.close()
            for i in result:
                if i['state'] != i['state_up'] and i['state'] == 2:
                    
                    #sql 搜索sub_tasks表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                    sql = 'SELECT sub_tasks.*,users.chinese_name,users.user_id FROM sub_tasks,users WHERE sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                    db.connect()
                    result2 = db.read(sql)
                    db.conn.close()
                    r2_len = len(result2)
                    inuser = {}
                    for j in result2:
                        inuser[j['chinese_name']] = 1
                        if j['task_class'] == 4:
                            if j['user_id'] in id_list:
                                del id_list[j['user_id']]


                    iustr =""
                    #遍历inuser ，取出key
                    for k in inuser:
                        iustr = iustr + k + " "




                    
                    outstr2 = outstr2 + '<br><b>《'+i['task_name']+'》工作在今日完成！</b>\n'
                    outstr2 = outstr2 + '公司全体感谢【'+i['chinese_name']+' '+iustr+'】等的辛勤工作！\n'
                    if i["completion_description"] == "" :
                        outstr2 = outstr2 + '负责人'+i['chinese_name']+'不进行总结\n'
                    else:
                        outstr2 = outstr2 + '负责人'+i['chinese_name']+'今天说:<br>'+i['completion_description']+'\n'
                    continue

            outstr2 = outstr2.replace('\n', '<br>')
            outstr = outstr + outstr2


            #
            # 快报类
            #

            #sql 搜索 work_tasks 表中的数据，条件是 task_status = 2 与 task_class = 3 与时间在今天的开始时间与结束时间之间 关联 users表的user_id 得到 chinese_name
            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE  work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 2 AND work_tasks.task_class = 3 AND work_tasks.creator = users.user_id AND work_tasks.task_ctrl_time BETWEEN "' + today_start + '" AND "' + today_end + '"'
            db.connect()
            result = db.read(sql)
            db.conn.close()
            outstr = outstr+"<br><br><span class = \"class-bt\">今天的快报工作:</span><br><br>"
            outstr2 =""
            for i in result:
                outstr2 = outstr2 + ' <br>['+i['chinese_name']+']:<b>'+i['task_name']+'</b><br>'
                outstr2 = outstr2 + '&nbsp;&nbsp;'+i['task_readme']+"<br>"

            outstr2 = outstr2.replace('\n', '<br>&nbsp;&nbsp;')
            outstr = outstr + outstr2



            

            h2str = "<br>今日懒王："
            #遍历 id_list
            for i in id_list:
                h2str = h2str + id_list[i] + " "
            #h2str = h2str + "<br>今日懒仔："

            #遍历 work_master_lazy 获取 key
           # for i in work_master_lazy:
             #   h2str = h2str + i + " "

            h2str = h2str + "<br>今日懒蛋："

            #遍历 work_lazy 获取 key
            for i in work_lazy:
                h2str = h2str + i + " "
            h2str = h2str + "<br><br>"

            outstr = heart_outstr + h2str + outstr








            return {'code': 0, 'g_command':'get_daily_report','message': 'success', 'outstr':outstr }




        if get_command == 'get_department_report_txt':  #部门日报
            
            department = data['department']
            #根据 department 获取部门名称
            sql = 'SELECT * FROM departments WHERE department_id = ' + str(department)
            db.connect()
            result = db.read(sql)
            db.conn.close()
            department_name = result[0]['department_name']
            now_ymd = datetime.datetime.now().strftime("%Y-%m-%d") # 当期时间
            today_start = datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
            today_end = datetime.datetime.now().strftime("%Y-%m-%d") + " 23:59:59"
            outstr=""

            #获取部门下的所有用户

            sql ='SELECT users.user_id ,users.chinese_name FROM users INNER JOIN department_members ON users.user_id = department_members.user_id WHERE checkin = 1 AND department_members.department_id = '+ str(department)
            db.connect()
            result = db.read(sql)
            db.conn.close()
            user_list = {}
            id_list ={}
            id_list_str =""
            for i in result:
                user_list[i['chinese_name']] = i['user_id']
                id_list[i['user_id']] = i['chinese_name']
                id_list_str =  id_list_str + str(i['user_id']) + ","
            #去掉 id_list_str 最后一个逗号
            id_list_str = id_list_str[:-1]
            print(id_list_str)
            print(user_list)

            #搜索task_execution submitter字段中有 id_list_str 的数据
            sql = 'SELECT task_execution.* FROM task_execution WHERE task_execution.submitter IN ('+id_list_str+') AND   DATE( task_execution.execution_time) = "'+ now_ymd+'"'
            db.connect()
            result = db.read(sql)
            db.conn.close()
            #print(result)

            for i in result:
                #判读id_list中是否有key 是  i['submitter'] 的 如果有则删除
                if i['submitter'] in id_list:
                    del id_list[i['submitter']]


            #搜索sub_progress表中 sup_create_user_id 字段中有 id_list_str 的数据
            sql = 'SELECT sub_progress.* FROM sub_progress WHERE sub_progress.sup_create_user_id IN ('+id_list_str+') AND   DATE( sub_progress.sup_time) = "'+ now_ymd+'"'

            db.connect()
            result = db.read(sql)
            db.conn.close()
            #print(result)

            for i in result:
                #判读id_list中是否有key 是  i['submitter'] 的 如果有则删除
                if i['sup_create_user_id'] in id_list:
                    del id_list[i['sup_create_user_id']]



                









            #创建变量  outstr 内容是   部门名称 +  当前时间 +  ”本报告以每天 23.50 分做出的为准"
            heart_outstr = ""+  department_name+" "+now_ymd +" "+"部门工作报告\n 本报告以每天 23.50 分做出的为准\n"





            #sql work_tasks表中的 task_status = 1 和 task_class = 1 的数据 关联 users表的user_id 得到 chinese_name
            #outstr = "<br> 部门工作报告 <br> 本报告以每天 23.50 分做出的为准<br>"
            #显示今天限时类工作
            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 1 AND work_tasks.task_class IN(1) AND work_tasks.creator = users.user_id ORDER BY task_class ASC'
            
            db.connect()
            result = db.read(sql)
            new_result = []
            
            
            work_master_lazy = {}
            work_lazy = {}

            #获取当前的 年-月-日


            outstr = outstr+"\n进行中限时类工作:\n"
            for i in result:
                st = i['creation_time'].strftime("%m-%d")
                en = i['plan_time'].strftime("%m-%d")
                work = ""
                if i['task_class'] == 1:
                    work= '限时类工作'
                elif i['task_class'] == 4:
                    work = '群体工作'
                elif i['task_class'] == 2:
                    work = '每日类工作'




                new_result.append(i)
                outstr =  outstr +'' + i['task_name'] + '['+st+'>'+en+']['+str(i['progree'])+'%] '+i['chinese_name']+' \n'
                #sql 搜索 sub_tasks 表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.state = 1 AND sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                db.connect()
                result2 = db.read(sql)
                r2_len = len(result2)
                
                
                the_num = 0
                mstr = "["
                tstr =""
                for j in result2:
                    the_num = the_num + 1
                    ctrl_time =  j['sub_ctrl_time'].strftime("%Y-%m-%d")
                    td = ""
                    hu =""
                    hud = ""
                    if ctrl_time == now_ymd:
                        #把j['completion_rate']转为字符串

                        td= j['completion_rate']
                        td = str(td)+'%'
                        # 把进行过工作的都删除了，剩下的就是没工作的
                        #查看 user_list 字典中是否有 j['chinese_name'] 这个key
                        if j['chinese_name'] in user_list:
                            #有的话就删除了
                            del user_list[j['chinese_name']]

                        
                    else:
                        hu=""
                        hud=""
                        td = '偷懒了!'
                        work_lazy[j['chinese_name']] = 1
                        
                    tstr = tstr + "  "+str(the_num) + '.'+j['sub_task_name']+' _ ['+hu  + j['chinese_name'] + ' '+td+hud+']\n'
                    mstr = mstr + j['chinese_name'] + ' '
                mstr = mstr + "]"
                if i['task_class'] == 1 or i['task_class'] == 2:
                    outstr = outstr + tstr + ''
                elif i['task_class'] == 4:
                    outstr = outstr + mstr + ''
                


                #查询task_execution表中的数据，条件是 task_id = i['task_id'] ，execution_time 倒排序
                sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id']) + ' AND    DATE(execution_time) = "'+now_ymd+'"  ORDER BY execution_time DESC'
                
                #sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id'])
                db.connect()
                result3 = db.read(sql)
                r3_len = len(result3)
                if r3_len == 0:
                    outstr = outstr + '工作负责人'+i['chinese_name']+'未提交执行报告!\n'
                    work_master_lazy[i['chinese_name']] = 1
                else:
                    outstr = outstr + '本工作总责任人'+i['chinese_name']+'对进度的总结是: 总进展'+str(result3[0]['completion_rate'])+'% '+result3[0]['completion_description']+'\n'
                    if i['chinese_name'] in user_list:
                        #有的话就删除了
                        del user_list[i['chinese_name']]
                outstr = outstr +"\n"
            
           
            #把ourstr 字符串中的换行符替换为 <br>
            #outstr = outstr.replace('\n', '<br>')
            outstr = outstr+""


            outstr = outstr+"\n每日类工作完成情况:\n"

            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 1 AND work_tasks.task_class IN(2) AND work_tasks.creator = users.user_id ORDER BY task_class ASC'
            
            db.connect()
            result = db.read(sql)
            new_result = []
            
            
            work_master_lazy = {}
            work_lazy = {}

            for i in result:
                st = i['creation_time'].strftime("%m-%d")
                en = i['plan_time'].strftime("%m-%d")
                work = ""
                if i['task_class'] == 1:
                    work= '限时类工作'
                elif i['task_class'] == 4:
                    work = '群体工作'
                elif i['task_class'] == 2:
                    work = '每日类工作'




                new_result.append(i)
                outstr =  outstr +'' + i['task_name'] + '['+st+'>'+en+']['+str(i['progree'])+'%] '+i['chinese_name']+' \n'
                #sql 搜索 sub_tasks 表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.state = 1 AND sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                db.connect()
                result2 = db.read(sql)
                r2_len = len(result2)
                
                
                the_num = 0
                mstr = "["
                tstr =""
                for j in result2:
                    the_num = the_num + 1
                    ctrl_time =  j['sub_ctrl_time'].strftime("%Y-%m-%d")
                    td = ""
                    hu =""
                    hud = ""
                    if ctrl_time == now_ymd:
                        #把j['completion_rate']转为字符串

                        td= j['completion_rate']
                        td = str(td)+'%'
                        
                    else:
                        hu=""
                        hud=""
                        td = '偷懒了!'
                        work_lazy[j['chinese_name']] = 1
                        
                    tstr = tstr + "  "+str(the_num) + '. ['+hu  + j['chinese_name'] + ' '+td+hud+']\n'
                    mstr = mstr + j['chinese_name'] + ' '
                mstr = mstr + "]"
                if i['task_class'] == 1 or i['task_class'] == 2:
                    outstr = outstr + tstr + ''
                elif i['task_class'] == 4:
                    outstr = outstr + mstr + ''


                #查询task_execution表中的数据，条件是 task_id = i['task_id'] ，execution_time 倒排序
                sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id']) + ' AND    DATE(execution_time) = "'+now_ymd+'"  ORDER BY execution_time DESC'
                
                #sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id'])
                db.connect()
                result3 = db.read(sql)
                r3_len = len(result3)
                if r3_len == 0:
                    outstr = outstr + '工作负责人'+i['chinese_name']+'未提交执行报告!\n'
                    work_master_lazy[i['chinese_name']] = 1
                else:
                    outstr = outstr + '本工作总责任人'+i['chinese_name']+'对进度的总结是: 总进展'+str(result3[0]['completion_rate'])+'% '+result3[0]['completion_description']+'\n'

                
            
           
            #把ourstr 字符串中的换行符替换为 <br>
            #outstr = outstr.replace('\n', '<br>')
            #outstr = outstr+"</ol>"





            outstr = outstr+"\n\n群体类工作完成情况:\n"

            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 1 AND work_tasks.task_class IN(4) AND work_tasks.creator = users.user_id ORDER BY task_class ASC'
            
            db.connect()
            result = db.read(sql)
            new_result = []
            
            
            work_master_lazy = {}
            work_lazy = {}

            for i in result:
                st = i['creation_time'].strftime("%m-%d")
                en = i['plan_time'].strftime("%m-%d")
                work = ""
                if i['task_class'] == 1:
                    work= '限时类工作'
                elif i['task_class'] == 4:
                    work = '群体工作'
                elif i['task_class'] == 2:
                    work = '每日类工作'




                new_result.append(i)
                outstr =  outstr +'' + i['task_name'] + '['+st+'>'+en+']['+str(i['progree'])+'%] '+i['chinese_name']+' \n'
                #sql 搜索 sub_tasks 表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.state = 1 AND sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                db.connect()
                result2 = db.read(sql)
                r2_len = len(result2)
                
                outstr = outstr + "执行人："
                the_num = 0
                mstr = "["
                tstr =""
                for j in result2:
                    the_num = the_num + 1
                    ctrl_time =  j['sub_ctrl_time'].strftime("%Y-%m-%d")
                    td = ""
                    hu =""
                    hud = ""
                    if ctrl_time == now_ymd:
                        #把j['completion_rate']转为字符串

                        td= j['completion_rate']
                        td = str(td)+'%'
                        
                    else:
                        hu=""
                        hud=""
                        td = '偷懒了!'
                        work_lazy[j['chinese_name']] = 1
                        
                    tstr = tstr + "  "+str(the_num) + '. ['+hu  + j['chinese_name'] + ' '+td+hud+']\n'
                    mstr = mstr + j['chinese_name'] + ' '
                mstr = mstr + "]"
                if i['task_class'] == 1 or i['task_class'] == 2:
                    outstr = outstr + tstr + ''
                elif i['task_class'] == 4:
                    outstr = outstr + mstr + ''


                #查询task_execution表中的数据，条件是 task_id = i['task_id'] ，execution_time 倒排序
                sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id']) + ' AND    DATE(execution_time) = "'+now_ymd+'"  ORDER BY execution_time DESC'
                
                #sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id'])
                db.connect()
                result3 = db.read(sql)
                r3_len = len(result3)
                if r3_len == 0:
                    outstr = outstr + '工作负责人'+i['chinese_name']+'未提交执行报告!\n'
                    work_master_lazy[i['chinese_name']] = 1
                else:
                    outstr = outstr + '本工作总责任人'+i['chinese_name']+'对进度的总结是: 总进展'+str(result3[0]['completion_rate'])+'% '+result3[0]['completion_description']+'\n'

                
            
           
            #把ourstr 字符串中的换行符替换为 <br>
            #outstr = outstr.replace('\n', '<br>')
            #outstr = outstr+"</ol>"




























            outstr = outstr+"\n\n今天完成的工作:\n"
            outstr2 = ""
            sql = 'SELECT users.chinese_name, task_execution.*,work_tasks.task_name FROM task_execution,work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND modify_by = users.user_id AND work_tasks.task_id = task_execution.task_id AND task_execution.state = 2 AND execution_time BETWEEN "' + today_start + '" AND "' + today_end + '"'

            db.connect()
            result = db.read(sql)
            db.conn.close()
            for i in result:
                if i['state'] != i['state_up'] and i['state'] == 2:
                    
                    #sql 搜索sub_tasks表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                    sql = 'SELECT sub_tasks.*,users.chinese_name,users.user_id FROM sub_tasks,users WHERE sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                    db.connect()
                    result2 = db.read(sql)
                    db.conn.close()
                    r2_len = len(result2)
                    inuser = {}
                    for j in result2:
                        inuser[j['chinese_name']] = 1
                        if j['task_class'] == 4:
                            if j['user_id'] in id_list:
                                del id_list[j['user_id']]


                    iustr =""
                    #遍历inuser ，取出key
                    for k in inuser:
                        iustr = iustr + k + " "




                    
                    outstr2 = outstr2 + '\n《'+i['task_name']+'》工作在今日完成！\n'
                    outstr2 = outstr2 + '公司全体感谢【'+i['chinese_name']+' '+iustr+'】等的辛勤工作！\n'
                    if i["completion_description"] == "" :
                        outstr2 = outstr2 + '负责人'+i['chinese_name']+'不进行总结\n'
                    else:
                        outstr2 = outstr2 + '负责人'+i['chinese_name']+'今天说:<br>'+i['completion_description']+'\n'
                    continue

            #outstr2 = outstr2.replace('\n', '<br>')
            outstr = outstr + outstr2


            #
            # 快报类
            #

            #sql 搜索 work_tasks 表中的数据，条件是 task_status = 2 与 task_class = 3 与时间在今天的开始时间与结束时间之间 关联 users表的user_id 得到 chinese_name
            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE  work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 2 AND work_tasks.task_class = 3 AND work_tasks.creator = users.user_id AND work_tasks.task_ctrl_time BETWEEN "' + today_start + '" AND "' + today_end + '"'
            db.connect()
            result = db.read(sql)
            db.conn.close()
            outstr = outstr+"\n今天的快报工作:\n"
            outstr2 =""
            for i in result:
                outstr2 = outstr2 + '\n['+i['chinese_name']+']:'+i['task_name']+'\n'
                outstr2 = outstr2 + '  '+i['task_readme']+"\n"

            #outstr2 = outstr2.replace('\n', '<br>&nbsp;&nbsp;')
            outstr = outstr + outstr2



            

            h2str = "\n今日懒王："
            #遍历 id_list
            for i in id_list:
                h2str = h2str + id_list[i] + " "
            #h2str = h2str + "<br>今日懒仔："

            #遍历 work_master_lazy 获取 key
           # for i in work_master_lazy:
             #   h2str = h2str + i + " "

            h2str = h2str + "\n今日懒蛋："

            #遍历 work_lazy 获取 key
            for i in work_lazy:
                h2str = h2str + i + " "
            h2str = h2str + "\n\n"

            outstr = heart_outstr + h2str + outstr








            return {'code': 0, 'g_command':'get_daily_report','message': 'success', 'outstr':outstr }








        
        if get_command == 'get_department_report_easy':  #部门日报简略版本，生成用于推送的文本
            
            department = data['department']
            #根据 department 获取部门名称
            sql = 'SELECT * FROM departments WHERE department_id = ' + str(department)
            db.connect()
            result = db.read(sql)
            db.conn.close()
            department_name = result[0]['department_name']





            now_ymd = datetime.datetime.now().strftime("%Y-%m-%d") # 当期时间
            now_ymd_hms = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") # 当期时间
            today_start = datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
            today_end = datetime.datetime.now().strftime("%Y-%m-%d") + " 23:59:59"
            mstr =""


            #创建变量  outstr 内容是   部门名称 +  当前时间 +  ”本报告以每天 23.50 分做出的为准"
            outstr = ""+  department_name+"_"+now_ymd_hms +"_部门工作\n\n"





            #sql work_tasks表中的 task_status = 1 和 task_class = 1 的数据 关联 users表的user_id 得到 chinese_name
            #outstr = "<br> 部门工作报告 <br> 本报告以每天 23.50 分做出的为准<br>"
            #显示今天限时类工作
            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 1 AND work_tasks.task_class IN(1) AND work_tasks.creator = users.user_id ORDER BY task_class ASC'
            
            db.connect()
            result = db.read(sql)
            new_result = []
            
            
            work_master_lazy = {}
            work_lazy = {}

            #获取当前的 年-月-日


            outstr = outstr+"限时类工作:\n"
            for i in result:
                st = i['creation_time'].strftime("%m-%d")
                en = i['plan_time'].strftime("%m-%d")
                work = ""
                if i['task_class'] == 1:
                    work= '限时类工作'
                elif i['task_class'] == 4:
                    work = '群体工作'
                elif i['task_class'] == 2:
                    work = '每日类工作'




                new_result.append(i)
                outstr =  outstr +'' + i['task_name'] + ' '+i['chinese_name']+' \n'
                #sql 搜索 sub_tasks 表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.state = 1 AND sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                db.connect()
                result2 = db.read(sql)
                r2_len = len(result2)
                
                
                the_num = 0
                mstr = "["
                tstr =""
                for j in result2:
                    the_num = the_num + 1
                    ctrl_time =  j['sub_ctrl_time'].strftime("%Y-%m-%d")
                    td = ""
                    hu =""
                    hud = ""
                    if ctrl_time == now_ymd:
                        #把j['completion_rate']转为字符串

                        td= j['completion_rate']
                        td = str(td)+'%'
                        
                    else:
                        hu="<u>"
                        hud="</u>"
                        td = '偷懒了!'
                        work_lazy[j['chinese_name']] = 1
                        
                    tstr = tstr + "&nbsp&nbsp"+str(the_num) + '.'+j['sub_task_name']+' _ ['+ j['chinese_name'] + ']\n'
                    mstr = mstr + j['chinese_name'] + ' '
                mstr = mstr + "]\n"
                if i['task_class'] == 1 or i['task_class'] == 2:
                    outstr = outstr + tstr + ''
                elif i['task_class'] == 4:
                    outstr = outstr + mstr + ''
                


                #查询task_execution表中的数据，条件是 task_id = i['task_id'] ，execution_time 倒排序
                sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id']) + ' AND    DATE(execution_time) = "'+now_ymd+'"  ORDER BY execution_time DESC'
                
                #sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id'])
                db.connect()
                result3 = db.read(sql)
                r3_len = len(result3)
                if r3_len == 0:
                    
                    work_master_lazy[i['chinese_name']] = 1
                else:
                    pass
                outstr = outstr +"\n"
            
           
            #把ourstr 字符串中的换行符替换为 <br>



            outstr = outstr+"\n每日类工作:\n"

            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 1 AND work_tasks.task_class IN(2) AND work_tasks.creator = users.user_id ORDER BY task_class ASC'
            
            db.connect()
            result = db.read(sql)
            new_result = []
            
            
            work_master_lazy = {}
            work_lazy = {}

            for i in result:
                st = i['creation_time'].strftime("%m-%d")
                en = i['plan_time'].strftime("%m-%d")
                work = ""
                if i['task_class'] == 1:
                    work= '限时类工作'
                elif i['task_class'] == 4:
                    work = '群体工作'
                elif i['task_class'] == 2:
                    work = '每日类工作'




                new_result.append(i)
                outstr =  outstr +'' + i['task_name'] + ' '+i['chinese_name']+' \n'
                #sql 搜索 sub_tasks 表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.state = 1 AND sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                db.connect()
                result2 = db.read(sql)
                r2_len = len(result2)
                
                
                the_num = 0
                mstr = "["
                tstr =""
                for j in result2:
                    the_num = the_num + 1
                    ctrl_time =  j['sub_ctrl_time'].strftime("%Y-%m-%d")
                    td = ""
                    hu =""
                    hud = ""
                    if ctrl_time == now_ymd:
                        #把j['completion_rate']转为字符串

                        td= j['completion_rate']
                        td = str(td)+'%'
                        
                    else:
                        hu="<u>"
                        hud="</u>"
                        td = '偷懒了!'
                        work_lazy[j['chinese_name']] = 1
                        
                    tstr = tstr + "&nbsp&nbsp"+str(the_num) + '. ['+hu  + j['chinese_name'] 
                    mstr = mstr + j['chinese_name'] + ' '
                mstr = mstr + "]"


                #查询task_execution表中的数据，条件是 task_id = i['task_id'] ，execution_time 倒排序
                sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id']) + ' AND    DATE(execution_time) = "'+now_ymd+'"  ORDER BY execution_time DESC'
                
                #sql = 'SELECT * FROM task_execution WHERE task_id = ' + str(i['task_id'])
                db.connect()
                result3 = db.read(sql)
                r3_len = len(result3)
                if r3_len == 0:
                    work_master_lazy[i['chinese_name']] = 1
                else:
                    pass

                
            
           
            #把ourstr 字符串中的换行符替换为 <br>


            outstr = outstr+"\n群体类工作:\n\n"

            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks,users WHERE work_tasks.created_department = '+str( department)+' AND work_tasks.task_status = 1 AND work_tasks.task_class IN(4) AND work_tasks.creator = users.user_id ORDER BY task_class ASC'
            
            db.connect()
            result = db.read(sql)
            new_result = []
            
            
            work_master_lazy = {}
            work_lazy = {}

            for i in result:
                st = i['creation_time'].strftime("%m-%d")
                en = i['plan_time'].strftime("%m-%d")
                work = ""
                if i['task_class'] == 1:
                    work= '限时类工作'
                elif i['task_class'] == 4:
                    work = '群体工作'
                elif i['task_class'] == 2:
                    work = '每日类工作'




                new_result.append(i)
                outstr =  outstr +'' + i['task_name'] + ' '+i['chinese_name']+' \n'
                #sql 搜索 sub_tasks 表中的数据，条件是 task_id = i['task_id'] sub_user 关联 users表的user_id 得到 chinese_name
                sql = 'SELECT sub_tasks.*,users.chinese_name FROM sub_tasks,users WHERE sub_tasks.state = 1 AND sub_tasks.task_id = ' + str(i['task_id']) + ' AND sub_tasks.sub_user = users.user_id'
                db.connect()
                result2 = db.read(sql)
                r2_len = len(result2)
                
                outstr = outstr + "执行人："
                the_num = 0
                mstr = "["
                tstr =""
                for j in result2:
                    the_num = the_num + 1
                    ctrl_time =  j['sub_ctrl_time'].strftime("%Y-%m-%d")
                    td = ""
                    hu =""
                    hud = ""
                    if ctrl_time == now_ymd:
                        #把j['completion_rate']转为字符串

                        td= j['completion_rate']
                        td = str(td)+'%'
                        
                    else:
                        hu="<u>"
                        hud="</u>"
                        td = '偷懒了!'
                        work_lazy[j['chinese_name']] = 1
                        
                    tstr = tstr + "&nbsp&nbsp"+str(the_num) + '. [' + j['chinese_name']
                    mstr = mstr + j['chinese_name'] + ' '
                mstr = mstr + "]"
            outstr = outstr + mstr + "\n"

           
            #把ourstr 字符串中的换行符替换为 <br>
            outstr = outstr.replace('&nbsp', ' ')
            #outstr = outstr.replace('\n', '<br>')

            print(outstr)


            return {'code': 0, 'g_command':'get_daily_report_easy','message': 'success', 'outstr':outstr }




        if get_command == "get_departments_user":
            sql = "SELECT * FROM departments"
            db.connect()
            result = db.read(sql)
            
            new_result = []
            for i in result:
                new_result.append(i)
                new_result[-1]['users'] = []
                sql = "SELECT users.user_id ,users.chinese_name FROM users INNER JOIN department_members ON users.user_id = department_members.user_id WHERE department_members.department_id = " + str(i['department_id'])
                db.connect()
                result2 = db.read(sql)
                db.conn.close()
                for j in result2:
                    new_result[-1]['users'].append(j)

            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_departments_user','message': 'success', 'data': new_result }

        if get_command == "get_departments":#返回部门列表
            sql = "SELECT * FROM departments"
            db.connect()
            result = db.read(sql)
            db.conn.close()
            return {'user_id':user_id,'chinese_name':chinese_name,'code': 0, 'g_command':'get_departments','message': 'success', 'data': result }
        



if __name__ == '__main__':
    #port 12345 所有ip 都可以访问
    app.run(debug=True, port=12345, host='0.0.0.0' )
    #完成度 的 英文单词是 progress 参与者的英文单词是 participant 计划时间 的英文单词是 plan_time