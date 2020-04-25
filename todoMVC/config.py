class DefaultConfig(object):
    DEBUG = None
    # 链接数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:!QAZ2wsx@localhost/todoMVC"
    # 动态追踪修改数据库，关闭警告信息
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProConfig(DefaultConfig):
    DEBUG = False

class DevConfig(DefaultConfig):
    DEBUG = True


config_dict = {
    "dev":DevConfig,
    "pro":ProConfig,
}
