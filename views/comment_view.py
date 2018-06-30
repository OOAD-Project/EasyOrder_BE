# 评论视图

from aiohttp import web
import pathlib
import yaml
import sys
from aiojobs.aiohttp import atomic

# 加载模型和路由模块
BASE_DIR = pathlib.Path(__file__).parent.parent
models_path = BASE_DIR / "models"
aiohttp_polls_path = BASE_DIR / "aiohttp_polls"
sys.path.append(str(models_path))
sys.path.append(str(aiohttp_polls_path))

import comment
import aio_engine

# 获取所有评论
# 输入参数：request 用户请求
# 返回值：json 格式的所有评论
async def get_comments(request):
    engine = await aio_engine.init_engine()
    records = await comment.select(engine)
    if records == []:
        return web.json_response({})
    for r in records:
        r["comment_time"] = str(r["comment_time"])
    return web.json_response({"comments": records})

# 生成新的评论
# 输入参数：request 用户post请求
# 返回值：新评论生成状态
@atomic
async def create_comment(request):
    engine = await aio_engine.init_engine()
    data = await request.json()
    print(data["comment"][0]["food_id"])
    food_id = data["comment"][0]["food_id"]
    rating = data["comment"][0]["rating"]
    content = data["comment"][0]["content"]
    comment_object = {
        "food_id": food_id,
        "rating": rating,
        "content": content
    }
    # comment.insert(engine, comment_object)
    r = await comment.insert(engine, comment_object)
    print("r", r)
    return web.json_response({"status": r})
    
