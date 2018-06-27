# 管理员 CRUD 操作

import sqlalchemy as sa
from models.meta import meta
from passlib.hash import pbkdf2_sha256

# keeper 管理员的结构，通过 meta 注册器映射为数据库 keeper 表
keeper = sa.Table(
    "keeper",                                                       # 表名
    meta,                                                           # 注册器
    sa.Column("id", sa.Integer, primary_key=True),                  # 管理员id
    sa.Column("name", sa.String(50), nullable=False, unique=True),  # 管理员姓名
    sa.Column("psw_hash", sa.String(200), nullable=False)           # 管理员密码哈希值
)

# 插入新的管理员记录
# 输入参数：engine 连接数据库的引擎，keeper_object 要新增的管理员
# 返回值：若插入成功则返回 true，插入失败则返回异常
async def insert(engine, keeper_object):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            psw_hash = pbkdf2_sha256.hash(keeper_object["psw"])
            await conn.execute(keeper.insert().values(name=keeper_object["name"], psw_hash=psw_hash))
            await trans.commit()
    except Exception as e:
        return e
    else:
        return True

# 删除已有的管理员记录
# 输入参数：engine 连接数据库的引擎，id 要删除的管理员编号
# 返回值：若删除成功则返回 true，删除失败则返回false
async def delete(engine, id):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(keeper.delete().where(keeper.c.id == id))
            await trans.commit()
    except:
        return False
    else:
        return True

# 获取已有的管理员记录
# 输入参数：engine 连接数据库的引擎，id 要获取的管理员编号，name 要获取的管理员名字
# 返回值：与 id 和 name 对应所有管理员列表；如果不指定参数则返回 keeper 表的所有管理员列表
async def select(engine, id = None, name = None):
    async with engine.acquire() as conn:
        trans = await conn.begin()
        select_object = keeper.select()
        if id:
            select_object = select_object.where(keeper.c.id == id)
        if name:
            select_object == select_object.where(keeper.c.name == name)
        cursor = await conn.execute(select_object)
        records = await cursor.fetchall()
        await trans.commit()
        return [dict(r) for r in records]

# 验证管理员的用户名与密码是否正确
# 输入参数：engine 连接数据库的引擎，name 管理员用户名，psw 管理员登陆密码
# 返回值：用户名和密码均正确返回 true，否则返回 false
async def verify(engine, name = None, psw = None):
    if not name or not psw:
        return False
    # try:
    async with engine.acquire() as conn:
        trans = await conn.begin()
        cursor = await conn.execute(keeper.select().where(keeper.c.name == name))
        record = await cursor.fetchone()
        # print("record", record)
        await trans.commit()
        if not record:
            return False
        psw_hash = dict(record)["psw_hash"]
        return pbkdf2_sha256.verify(psw, psw_hash)
    # except:
    #     return None
    # else:
    #     return result
