# from todoMVC import app models.py文件中不能导入app
# 这里我们先将sqlalchemy实例化，在启动文件中进行调用init_app()方法进行数据库连接
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config_dict


db = SQLAlchemy()


# 定义模型类
class TodoList(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(32))
    isEdited = db.Column(db.BOOLEAN,default=False)
    isSelected = db.Column(db.BOOLEAN,default=False)

    def __str__(self):
        return f"{self.value}"

if __name__ == '__main__':
    from todoMVC import app
    with app.app_context():
        db.drop_all()
        db.create_all()