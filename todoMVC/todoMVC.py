from flask import Flask, json, request
from config import config_dict
from models import db, TodoList

app = Flask(__name__)
app.config.from_object(config_dict["pro"])
# cors跨域解决方案
from flask_cors import CORS
CORS(app)
# 给db对象加载到app中
db.init_app(app)


@app.route("/", methods=["GET"])
def getTodoList():
    """
    获取所有列表方法
    """
    if request.method != "GET":
        return json.dumps({"status": 401, "msg": "request method error"})

    todolist = []
    try:
        todos = TodoList.query.all()
    except Exception as e:
        return json.dumps({"status": 402, "msg": "数据获取失败"})
    for todo in todos:
        todolist.append({
            "value": todo.value,
            "isEdited": todo.isEdited,
            "isSelected": todo.isSelected,
        })
    return json.dumps({"status": 200, "todolist": todolist})

@app.route("/addTodoObj/", methods=["POST"])
def addTodoObj():
    """
    添加todo对象方法
    """
    if request.method != "POST":
        return json.dumps({"status": 401, "msg": "request method error"})

    data = json.loads(request.get_data(as_text=True))

    value = data.get("value")
    isEdited = data.get("isEdited")
    isSelected = data.get("isSelected")

    if not all([value]):
        return json.dumps({"status": 402, "msg": "参数缺失"})

    try:
        count = db.session.query(TodoList).filter_by(value=value).count()
    except Exception as e:
        return json.dumps({"status": 402, "msg": "查重操作发生异常"})
    if count > 0:
        return json.dumps({"status": 402, "msg": "已存在事件 请重新添加"})

    try:
        todoObj = TodoList(value=value, isEdited=isEdited,isSelected=isSelected)
    except Exception as e:
        return json.dumps({"status": 402, "msg": "添加操作发生异常"})
    
    db.session.add_all([todoObj])
    db.session.commit()

    return json.dumps({"status": 200, "msg": "ok"})

@app.route("/delTodoObj/", methods=["POST"])
def delTodoObj():
    if request.method != "POST":
        return json.dumps({"status": 401, "msg": "request method error"})

    data = json.loads(request.get_data(as_text=True))

    value = data.get("value")

    if not value:
        return json.dumps({"status": 402, "msg": "参数缺失"})

    try:
        todoObj = db.session.query(TodoList).filter_by(value=value).first()
    except Exception as e:
        return json.dumps({"status": 402, "msg": "删除操作发生异常"})
    
    db.session.delete(todoObj)
    db.session.commit()


    return json.dumps({"status": 200, "msg": "ok"})

@app.route("/uploadTodolist/",methods=["POST"])
def uploadTodolist():
    if request.method != "POST":
        return json.dumps({"status": 401, "msg": "request method error"})

    data = json.loads(request.get_data(as_text=True))

    todolist = data.get("todolist")
    if not todolist and todolist !=[] :
        return json.dumps({"status": 402, "msg": "参数缺失"})

    try:
        db.drop_all()
        db.create_all()
    except Exception as e:
        return json.dumps({"status": 402, "msg": "去除旧数据失败"})

    if todolist == []:
        return json.dumps({"status": 200, "msg": "ok"})

    for todo in todolist:
        try:
            todoObj = TodoList(value=todo.get("value"), isEdited=todo.get("isEdited"),isSelected=todo.get("isSelected"))
        except Exception as e:
            return json.dumps({"status": 402, "msg": "添加新数据操作发生异常"})

        db.session.add_all([todoObj])
        db.session.commit()
    

    return json.dumps({"status": 200, "msg": "ok"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)
