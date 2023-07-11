import datetime
from flask import Flask, render_template, request, redirect, session,send_from_directory
import os
import flask
from flask_cors import CORS
import threading
import time
import mysqllib
import json


db = mysqllib.MySQL(host='localhost', port=3306, user='root', password='root', db='task')
db.connect()

app = Flask(__name__)
CORS(app)
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
    return render_template('home.html')

@app.route('/res/<path:filename>')
def serve_file(filename):
    # 指定文件所在的目录
    directory = 'E:/work/task/res'
    return send_from_directory(directory, filename)

@app.route('/home/<path:filename>')
def home_file(filename):
    # 指定文件所在的目录
    directory = 'E:/work/task/res'
    return send_from_directory(directory, filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        #获取request.data 字典
        data = request.get_json()
        username = data['username']
        password = data['password']
        #产生sql语句通过username和password查询数据库，关联部门表
        sql = f"SELECT users.*, departments.department_name FROM users INNER JOIN departments ON users.department_id = departments.department_id WHERE username = '{username}' AND password = '{password}'"


        db.connect()
        result = db.read(sql)

        # TODO: 根据用户名和密码验证用户，进行登录逻辑
        # 这里只是示例代码，假设用户名和密码正确

        # 用户验证成功后，创建会话
        if len(result) == 0:
            return {'code': 1, 'message': '用户名或密码错误'}
        else:
            session['username'] = username
            session['chinese_name'] = result[0]['chinese_name']
            session['department_name'] = result[0]['department_name']
            session['department_id'] = result[0]['department_id']
            session['user_id'] = result[0]['user_id']

            #返回json
            return {'code': 0, 'message': '登录成功'}
    


    else:
        #获取当前目录


        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

#创建/html路由
@app.route('/html', methods=['GET', 'POST'] )
def html():
    if request.method == 'GET':
        act = request.args.get('act')
        return render_template(act)
        

    

#路由 endpoint
@app.route('/endpoint', methods=['GET', 'POST'])
def endpoint():
    if request.method == 'POST':
        #获取request.data 字典
        data = request.get_json()
        get_command = data['g_command']
        if get_command == 'task_types':
            sql = 'SELECT * FROM task_types'
            db.connect()
            result = db.read(sql)
            db.conn.close()
            return {'code': 0, 'g_command':'task_types','message': 'success', 'data': result}
        if get_command == 'get_users':
            sql = 'SELECT users.*, departments.department_name FROM users INNER JOIN departments ON users.department_id = departments.department_id'
            db.connect()
            result = db.read(sql)
            #db.conn.close()
            # result = [19: {'user_id': 18, 'username': 'user18', 'chinese_name': '用户18', 'department_id': 3, 'password': '', 'department_name': '工厂'}，
            # 19: {'user_id': 18, 'username': 'user18', 'chinese_name': '用户18', 'department_id': 3, 'password': '', 'department_name': '工厂'}]
            # 生成新的列表 用于前端显示 保留 user_id chinese_name department_name
            new_result = []
            for i in result:
                new_result.append({'value': i['user_id'], 'title':i['department_name'] +"-"+i['chinese_name']})
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
            task_status = 1
            task_class = data["data"]["rw"]
            progree = 0
            participant = data["data"]["users"]
            plan_time = data["data"]["endtime"]
            task_readme = data["data"]["readme"]


            
            sql = "INSERT INTO `work_tasks` (`task_id`, `task_name`, `creation_time`, `creator`, `task_status`, `task_class`, `progree`, `participant`, `plan_time`, `task_readme`) VALUES (NULL,"
            istr = data["data"]["task_name"]
            #把字符串中双引号前面加上反斜杠
            istr = istr.replace('"', '\\"')
            #istr = istr.replace('"', '\"')
            sql = sql + '"'+istr +'"'+","
            task_class = data["data"]["rw"]
            sql = sql + "NOW(),"+str(session["user_id"])+",1,"+str(data["data"]["rw"])+",0,"
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
            sql = sql + '"'+istr +'"'+")"
            print(sql)
            db.connect()
            result = db.write(sql)
            #获取刚刚插入的数据的id
            sql = "SELECT LAST_INSERT_ID() as id"
            result = db.read(sql)
            upid = result[0]["id"]
            print(upid)


            if task_class == '2':
                
                #创建一条sql语句，把上述信息插入到 sub_tasks 表中
                l='`id`,`task_id`,`sub_task_name`,`sub_task_description`,\
                 `end_time`,`created_at`,`create_user_id`,\
                    `next_user_id`,`next_sub_task_id`,`completion_rate`,\
                        `sub_user`,`state`,`sub_class`'
                sql = "INSERT INTO `sub_tasks` (`id`,`task_id`,`sub_task_name`,`sub_task_description`,`end_time`,`created_at`,`create_user_id`,`next_user_id`,`next_sub_task_id`,`completion_rate`,`sub_user`,`state`,`sub_class`) VALUES "
                
                #abdd = "[{'title': '技术部-用户4', 'value': 4}, {'title': '技术部-用户7', 'value': 7}, {'title': '技术部-用户16', 'value': 16}, {'title': '市场部-万五', 'value': 2}]"
                #把字符串转换成字典
                user_list = eval(user_list)



                #遍历 user_list
                for i in user_list:


                    sql = sql + '(NULL,'+str(upid)+','+'"'+task_name+'"'+','+'"'+task_readme+'"'+','
                    sql = sql + '"'+plan_time+'"'+',NOW(),'+str(creator)+','
                    sql = sql + '0,0,0,'
                    sql = sql + str(i["value"])+',1,2),'
                
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
            sql = 'SELECT work_tasks.*,users.chinese_name FROM work_tasks INNER JOIN users ON work_tasks.creator = users.user_id '
            #给sql语句 增加条件  只返回 50条 `task_id` 倒排序
            sql = sql + 'ORDER BY `task_id` DESC LIMIT 50'

            

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
            return {'code': 0, 'g_command':'get_tasks','message': 'success', 'data': new_result}            
        if get_command == 'get_task':
            sql = 'SELECT * FROM work_tasks WHERE task_id = ' + str(data["task_id"])
            db.connect()
            result = db.read(sql)
            db.conn.close()
            new_result = result[0]

            new_result["creation_time"] = new_result["creation_time"].strftime("%Y年%m月%d日")
            new_result["plan_time"] = new_result["plan_time"].strftime("%Y年%m月%d日")

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
            new_result["chinese_name"] = session['chinese_name']


            


           #把new_result 转换为json
            #new_result = json.dumps(new_result)
            


                #new_result.append({'task_id': i['task_id'], 'task_name':i['task_name'], 'creation_time':i['creation_time'], 'chinese_name':i['chinese_name'],'progree': i['progree'],'task_class': i['task_class'],'task_status': i['task_status'],'plan_time': i['plan_time']})
            return {'code': 0, 'g_command':'get_task','message': 'success', 'data': new_result}   
        if get_command == 'create_execuition':
            sql = 'INSERT INTO task_execution (task_id, sub_task_id	, completion_rate, completion_description,\
                 execution_time	,submitter	,modify_by	,state,type ) VALUES ('
            sql = sql + str(data['task_id']) + ','
            sql = sql + str(data['sub_task_id']) + ','
            sql = sql + str(data['completion_rate']) + ','
            sql = sql + "'" + data['completion_description'] + "',"
            sql = sql + "NOW(),"
            sql = sql + str(session['user_id']) + ','
            sql = sql + str(session['user_id']) + ','
            sql = sql + str(data['state']) + ','
            sql = sql + str(data['type']) + ')'
            
            db.connect()
            result = db.write(sql)
            db.conn.close()
            #更新work_task表中的progree字段
            sql = 'UPDATE work_tasks SET progree = ' + str(data['completion_rate']) + ' WHERE task_id = ' + str(data['task_id'])
            db.connect()
            result = db.write(sql)
            db.conn.close()
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
            return {'code': 0, 'g_command':'get_execution','message': 'success', 'data': new_result}
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
            return {'code': 0, 'g_command':'get_discussions','message': 'success', 'data': new_result}
        if get_command == 'create_sub_task':
            data = data['data']
            sql = 'INSERT INTO sub_tasks (task_id, sub_task_name,sub_task_description,end_time,\
                created_at,create_user_id,completion_rate,sub_user,state) VALUES ('
            sql = sql + str(data['task_id']) + ','
            sql = sql + "'" + data['sub_task_name'] + "',"
            sql = sql + "'" + data['sub_task_description'] + "',"
            sql = sql + "'" + data['end_time'] + "',"
            sql = sql + "NOW(),"
            sql = sql + str(session['user_id']) + ','
            sql = sql + '0 ,'
            sql = sql + str(data['sub_user']) + ','
            sql = sql + "1)"
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
            return {'code': 0, 'g_command':'get_sub_task_list','message': 'success', 'data': new_result}
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
                return {'code': 1, 'g_command':'get_sub_task','message': 'fail','data': new_result}
            
            if len(result) == 0:
                return {'code': 1, 'g_command':'get_sub_task','message': 'fail','data': new_result}
            else:
                for i in result:
                    i['end_time'] = i['end_time'].strftime("%m-%d")
                    i['created_at'] = i['created_at'].strftime("%m-%d")
                    i['state'] = str(i['state'])
                    new_result.append(i)

                

                return {'code': 0, 'g_command':'get_sub_task','message': 'success', 'data': new_result}
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
            return {'code': 0, 'g_command':'get_sub_step_list','message': 'success', 'data': new_result}
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
            return {'code': 0, 'g_command':'get_sub_step','message': 'success', 'data': new_result}
        if get_command == 'create_sub_step_progress':
           
            sql = 'INSERT INTO `setp_progress` (`sp_id`, `step_id`, `progress`, `sp_text`) VALUES (NULL,'
            sql = sql + str(data['step_id']) + ','
            sql = sql + str(data['progress']) + ','
            sql = sql + "'" + data['sp_text'] + "')"

            db.connect()
            result = db.write(sql)
            db.conn.close()
            if result == 0:
                return {'code': 1, 'g_command':'create_sub_step_progress','message': 'fail'}
            else:
                return {'code': 0, 'g_command':'create_sub_step_progress','message': 'success'}
        if get_command == 'set_sub_progress':
            sql = 'UPDATE `sub_tasks` SET `completion_rate` = ' + str(data['progress']) + ' WHERE `sub_tasks`.`id` = ' + str(data['sub_task_id'])
            db.connect()
            result = db.write(sql)
            db.conn.close()
            if result == 0:
                return {'code': 1, 'g_command':'set_sub_progress','message': 'fail'}
            else:
                return {'code': 0, 'g_command':'set_sub_progress','message': 'success'}
        if get_command == 'get_my_sub_tasks':
            myid = session["user_id"]
            #sql 语句 搜索 sub_tasks表 关联 users ,条件是 sub_user = myid sub_str ,state = 1   关联 users表的user_id  create_user_id 关联 users 表的user_id
            #sql = 'SELECT * FROM sub_tasks,users WHERE sub_user = ' + str(myid) + ' AND sub_str = 1 AND sub_tasks.create_user_id = users.user_id'
            sql = 'SELECT sub_tasks.*,users.chinese_name AS sub_user_name,users2.chinese_name AS create_user_name FROM sub_tasks,users,users AS users2 WHERE sub_tasks.sub_user =' + str(myid) + ' AND sub_tasks.sub_user = users.user_id AND sub_tasks.create_user_id = users2.user_id'
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
            return {'code': 0, 'g_command':'get_my_sub_tasks','message': 'success', 'data': new_result}


if __name__ == '__main__':
    #port 12345 所有ip 都可以访问
    app.run(debug=True, port=12345, host='0.0.0.0' )
    #完成度 的 英文单词是 progress 参与者的英文单词是 participant 计划时间 的英文单词是 plan_time