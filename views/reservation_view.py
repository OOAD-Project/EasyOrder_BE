# 订单视图

from aiohttp import web
import pathlib
# import yaml
import sys
from aiojobs.aiohttp import atomic
from aiohttp_session import get_session
# import ast

# 加载模型和路由模块
BASE_DIR = pathlib.Path(__file__).parent.parent
models_path = BASE_DIR / "models"
aiohttp_polls_path = BASE_DIR / "aiohttp_polls"
sys.path.append(str(models_path))
sys.path.append(str(aiohttp_polls_path))

import sales
import aio_engine


"""
获取订单信息
输入参数：request 用户请求
返回值：
返回格式
{
    "id": "1080",
    "create_time": 1526203134762,
    "table": "8",
    "list": [
        {
            "id": "1",
            "name": "牛杂汤粉面",
            "count": 2,
            "price": 17
        }
    ],
    "total": 34,
    "isPaid": true
}
"""

async def get_order(request):
    id = int(request.match_info['id'])
    res = await get_order_by_reservation_id(id)
    return web.json_response(res)

async def get_order_by_reservation_id(id):
    engine = await aio_engine.init_engine()
    print("id", id)
    record = await sales.sales_reservation.select(engine, id = id)
    print("record", record)
    if record == []:
        return {}
    record = record[0]
    #类型为dict 例如{"pork": 1, "fish": 2}
    food_list = record["food_list"]
    new_food_list = []
    food_name_list = list(food_list.keys())
    for name in food_name_list:
        print("name", name)
        f = await sales.sales_food.select(engine, food_name = name)
        print("f", f)
        f = f[0]
        new_food_list.append({"id": f["id"], "name": name, "count": food_list[name], "price": f["price"]})
    record["food_list"] = new_food_list
    record["reserve_datetime"] = str(record["reserve_datetime"])
    record["pay_datetime"] = str(record["pay_datetime"])
    return record

#通过session来验证是否之前有过订单记录
async def get_order_by_table(request):
    #利用session中的reservation号来查找
    session = await get_session(request)
    if "reservation_id" not in session:
        return web.json_response({})
    else :
        res = await get_order_by_reservation_id(session["reservation_id"])
        print(res)
        if (res["isOutOfDate"]) :
            return web.json_response({})
        else:
            return web.json_response(res)

"""
返回值
{
    "id": "1080",
    "create_time": 1526203134762,
    "table": "8",
    "list": [
        {
            "id": "1",
            "name": "牛杂汤粉面",
            "count": 2,
            "price": 17
        }
    ],
    "total": 34,
    "isPaid": true
}
表单格式
interface IOrderItem {
    id: string;
    name: string;
    count: number;
    price: number;
}
"""

"""
        "isPaid": True,
        "table_num": 12,
        "food_list": {"pork": 13, "fish": 2},
        "total": 34,
        "isOutOfDate": False
"""
# 生成新的订单
# 输入参数：request 用户请求
# 返回值：新订单生成状态
@atomic
async def create_order(request):
    #利用session记录reservation_id
    session = await get_session(request)
    engine = await aio_engine.init_engine()
    data = await request.json()
    #print("data", data)
    table_num = data["table"]
    food_list = data["list"]
    new_food_list = {}
    total = 0
    for f in food_list:
        total += f["count"] * f["price"]
        new_food_list[f["name"]] = f["count"]
        #new_food_list.append({f["name"]: f["count"]})
    reservation_object = {
        "isPaid": False,
        "table_num": table_num,
        "food_list": new_food_list,
        "total": total,
        "isOutOfDate": False
    }
    r = await sales.sales_reservation.insert(engine, reservation_object)
    print(r)
    session["reservation_id"] = r["LAST_INSERT_ID()"]
    return web.json_response({"reservation_id": r["LAST_INSERT_ID()"]})


