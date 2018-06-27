import aiomysql.sa 
from aiohttp_polls.setting import config
import asyncio

config = config["mysql"]
async def init_engine():
    engine = await aiomysql.sa.create_engine(user = config["user"], db = config["database"], host = config["host"], password = config["password"])
    return engine
#engine = await init_engine()

def get_read_engine():
    engine = asyncio.get_event_loop().run_until_complete(init_engine())
    return engine

read_engine = get_read_engine()

