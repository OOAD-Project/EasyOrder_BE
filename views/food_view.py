# 菜品视图

from aiohttp import web
import pathlib
import yaml
import sys

# 加载模型和路由模块
BASE_DIR = pathlib.Path(__file__).parent.parent
models_path = BASE_DIR / "models"
aiohttp_polls_path = BASE_DIR / "aiohttp_polls"
sys.path.append(str(models_path))
sys.path.append(str(aiohttp_polls_path))

import sales
import aio_engine
import tag

# 获取指定编号的菜品信息
# 输入参数：request 用户请求
# 返回值：json 格式的单个菜品信息
async def get_food(request):
    id = int(request.match_info['id'])
    engine = await aio_engine.init_engine()
    record = await sales.sales_food.select(engine, food_id = id)
    if record == []:
        return web.json_response({})
    record = record[0]
    sales_permonth = await sales.sales_permonth(engine, id = id)
    record["salesPerMonth"] = sales_permonth

    tag_id = record.pop("tag_id");
    r = await tag.select(engine, tag_id)
    record["category"] = r[0]["description"]
    record["id"] = str(record["id"])

    return web.json_response(record)

# 获取所有的菜品信息
# 输入参数：request 用户请求
# 返回值：json 格式的所有菜品信息
async def get_all_food(request):
    engine = await aio_engine.init_engine()
    records = await sales.sales_food.select(engine)
    if records == []:
        return web.json_response({})
    for r in records:
        id = r["id"]
        sales_permonth = await sales.sales_permonth(engine, id = id)
        r["salesPerMonth"] = sales_permonth
        r["id"] = str(r["id"])
        tag_id = r.pop("tag_id");
        t = await tag.select(engine, tag_id)
        r["category"] = t[0]["description"]

    return web.json_response(records)
