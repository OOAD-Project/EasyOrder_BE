# 评论视图

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