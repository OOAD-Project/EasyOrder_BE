# 用户评论 CRUD 操作

import sqlalchemy as sa
from models.meta import meta

# comment 用户评论的结构，通过 meta 注册器映射为数据库 comment 表
comment = sa.Table(
    "comment",                                                  # 表名
    meta,                                                       # 注册器
    sa.Column("id", sa.Integer, primary_key = True),            # 评论编号
    sa.Column("content", sa.String(50), nullable = False),      # 评论内容
    sa.Column("food_id", sa.Integer, sa.ForeignKey("food.id"))  # 评论对应的菜品编号
)

# 插入新的评论记录
# 输入参数：engine 连接数据库的引擎，comment_object 要新增的评论
# 返回值：若插入成功则返回 true，插入失败则返回 false
async def insert(engine, comment_object):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(comment.insert().values(id = comment_object["id"], content = comment_object["content"], food_id = comment_object["food_id"]))
            await trans.commit()
    except:
        return False
    else:
        return True

# 删除已有的评论记录
# 输入参数：engine 连接数据库的引擎，id 要删除的评论编号
# 返回值：若删除成功则返回 true，删除失败则返回 false
async def delete(engine, id):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(comment.delete().where(id == id))
            await trans.commit()
    except:
        return False
    else:
        return True

# 获取已有的评论记录
# 输入参数：engine 连接数据库的引擎，id 要获取的评论编号，food_id 要获取的评论对应的菜品编号
# 返回值：返回相应菜品的评论记录
async def select(engine, id = None, food_id = None):
    if not id and not food_id:
        return None
    async with engine.acquire() as conn:
        trans = await conn.begin()
        if id and food_id:
            cursor = await conn.execute(comment.select().where(id = id).where(food_id = food_id))
        elif not id and food_id:
            cursor = await conn.execute(comment.select().where(food_id = food_id))
        elif id and not food_id:
            cursor = await conn.execute(comment.select().where(id = id))
        records = cursor.fetchall()
        return [dict(r) for r in records]