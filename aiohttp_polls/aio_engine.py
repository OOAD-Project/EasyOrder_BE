import aiomysql.sa 
from aiohttp_polls.setting import config
import asyncio

# 获取配置文件的数据库信息
config = config["mysql"]

# 异步连接数据库
# 返回值：engine 连接上数据库的引擎
async def init_engine():
    engine = await aiomysql.sa.create_engine(user = config["user"], db = config["database"], host = config["host"], password = config["password"], charset = "gbk")
    return engine
#engine = await init_engine()

# 把所有读操作集中到一个read_engine上
# 返回值：read_engine 读操作引擎
def get_read_engine():
    engine = asyncio.get_event_loop().run_until_complete(init_engine())
    return engine

read_engine = get_read_engine()