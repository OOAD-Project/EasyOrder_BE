# 安装 session
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

# 安装 session
# 输入参数：app web Application 对象
# 返回值：app 已经安装了 session 的 web Application 对象
def setup_session_support(app):
    setup(app, EncryptedCookieStorage(b'Thirty  two  length  bytes  key.'))
    return app