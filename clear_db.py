# 清空并重置数据库

from models.meta import meta
from models.tag import tag
from models.food import food
from models.comment import comment
from models.reservation import reservation
from models.keeper import keeper
from aiohttp_polls.setting import config
import sqlalchemy as sa
import mysql.connector

config = config["mysql"]

def drop_db():
    try:
        conn = mysql.connector.connect(user = config["user"], password = config["password"])
        cursor = conn.cursor()
        cursor.execute("show databases;")
        r = cursor.fetchall()
        # print("r", r)
        if ("restaurant",) in r:
            URI = "mysql+{connector}://{user}:{password}@{host}:{port}/{database}"
            URI = URI.format(
                connector=config["init_connector"],
                user=config["user"],
                password=config["password"],
                host=config["host"],
                port=config["port"],
                database=config["database"]
            )
            engine = sa.create_engine(URI)
            meta.drop_all(bind=engine)

            cursor.execute("drop database restaurant;")
        cursor.close()
        conn.close()
    except Exception as e:
        return e
    else:
        return True

if __name__ == "__main__":
    print(drop_db())
    # drop_db()




