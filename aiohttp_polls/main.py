# 构建全局 web Application 对象，连接路由和session

from aiohttp import web
from aiohttp_polls import routes
from aiohttp_polls import session_encrypt
# from aiohttp_polls import session_redis

# app 全局 web Application 对象，控制整个后台的响应和数据传送
app = web.Application()                           # 初始化 web Application 对象
app = routes.setup_routes(app)                    # 添加路由
app = session_encrypt.setup_session_support(app)  # 初始化 session
# app = session_redis.setup_session_support(app)