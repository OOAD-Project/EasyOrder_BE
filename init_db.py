# 初始化数据库

from models.meta import meta
from models.tag import tag
from models.food import food
from models.comment import comment
from models.reservation import reservation
from models.keeper import keeper
from models.payment import payment
from aiohttp_polls.setting import config
import sqlalchemy as sa
import mysql.connector

config = config["mysql"]
URI = "mysql+{connector}://{user}:{password}@{host}:{port}/{database}"
URI = URI.format(
    connector = config["init_connector"],
    user = config["user"],
    password = config["password"],
    host = config["host"],
    port = config["port"],
    database = config["database"]
)



#init_database函数用于flask运行之前同步初始化数据库，app的连接引擎是异步的，由aiomysql.ra提供连接
def init_database():
    try:
        raw_conn = mysql.connector.connect(user = config["user"], password = config["password"])
        raw_cursor = raw_conn.cursor()
        raw_cursor.execute("show databases;")
        r = raw_cursor.fetchall()
        print(r)
        if ("restaurant",) not in r:
            raw_cursor.execute("create database restaurant DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci;")
            engine = sa.create_engine(URI)
            if not engine.dialect.has_table(engine, table_name="tag") and not engine.dialect.has_table(engine, table_name="food") and not engine.dialect.has_table(engine, table_name="comment") and not engine.dialect.has_table(engine, table_name="reservation") and not engine.dialect.has_table(engine, table_name="keeper") and not engine.dialect.has_table(engine, table_name="payment"):
                meta.create_all(bind=engine, tables=[tag, food, comment, reservation, keeper, payment])
    except:
        return False
    else:
        return True


if __name__ == "__main__":
    # print(init_database())
    init_database()
