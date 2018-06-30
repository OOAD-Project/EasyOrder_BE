# 支付视图

from aiohttp import web
import pathlib
import yaml
import sys


BASE_DIR = pathlib.Path(__file__).parent.parent
models_path = BASE_DIR / "models"
aiohttp_polls_path = BASE_DIR / "aiohttp_polls"
sys.path.append(str(models_path))
sys.path.append(str(aiohttp_polls_path))

import payment
import aio_engine
from aiohttp_session import get_session

async def get_payment(request):
    id = int(request.match_info['reservation_id'])
    engine = await aio_engine.init_engine()
    record = await payment.select(engine, None, id)
    if record == []:
        return web.json_response({})
    record = record[0]
    record["payment_time"] = str(record["payment_time"])
    record["reservation_id"] = str(record["reservation_id"])
    return web.json_response(record)


async def create_payment(request):
    engine = await aio_engine.init_engine()
    data = await request.post()
    r = await payment.insert(engine, data)
    result = {}
    print("r", r)
    result["status"] = r["status"]
    result["payment_id"] = r["payment_id"]
    return web.json_response(result)
