# 用户评论 CRUD 操作

import sqlalchemy as sa
from models.meta import meta
from models import food
import datetime

comment_food = food

# comment 用户评论的结构，通过 meta 注册器映射为数据库 comment 表
comment = sa.Table(
    "comment",                                                  # 表名
    meta,                                                       # 注册器
    sa.Column("id", sa.Integer, primary_key = True),            # 评论编号
    sa.Column("food_id", sa.Integer, sa.ForeignKey("food.id")), # 评论对应的菜品编号
    sa.Column("rating", sa.Float),                              # 菜品评价
    sa.Column("content", sa.String(50), nullable = False),      # 评论内容
    sa.Column("comment_time", sa.DateTime)                      # 评论的日期
)

# 插入新的评论记录
# 输入参数：engine 连接数据库的引擎，comment_object 要新增的评论
# 返回值：若插入成功则返回 true，插入失败则返回 false
async def insert(engine, comment_object):
    # try:
    async with engine.acquire() as conn:
        trans = await conn.begin()
        await conn.execute(comment.insert().values(content = comment_object["content"], food_id = comment_object["food_id"], rating = comment_object["rating"], comment_time = datetime.datetime.now()))
        await trans.commit()
    # except Exception as e:
    #     return e
    # else:
    #     return True

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
# 输入参数：engine 连接数据库的引擎，id 要获取的评论编号，food_id 要获取的评论对应的菜品编号；如果不指定参数则返回 comment 表的所有评论列表
# 返回值：返回相应菜品的评论记录
async def select(engine, id = None, food_id = None):
    async with engine.acquire() as conn:
        trans = await conn.begin()
        if not id and not food_id:
            cursor = await conn.execute(comment.select())
            comment_records = await cursor.fetchall()
            cursor = await conn.execute(food.food.select())
            food_records = await cursor.fetchall() 
        if id and food_id:
            cursor = await conn.execute(comment.select().where(id = id).where(food_id = food_id))
            comment_records = await cursor.fetchall()
            cursor = await conn.execute(food.food.select().where(food.food.c.id == food_id))
            food_records = await cursor.fetchall()
        elif not id and food_id:
            cursor = await conn.execute(comment.select().where(food_id = food_id))
            comment_records = await cursor.fetchall()
            cursor = await conn.execute(food.food.select().where(food.food.c.id == food_id))
            food_records = await cursor.fetchall()
        elif id and not food_id:
            cursor = await conn.execute(comment.select().where(id = id))
            comment_records = await cursor.fetchall()
            cursor = await conn.execute(food.food.select().where(food.food.c.id == comment_result[0]["food_id"]))
            food_records = await cursor.fetchall()
        await trans.commit()
        comment_result = [dict(r) for r in comment_records]
        food_result = [dict(r) for r in food_records]

        for c_rst in comment_result:
            for f_rst in food_result:
                if c_rst["food_id"] == f_rst["id"]:
                    c_rst["id"] = str(c_rst["id"])
                    c_rst["food_id"] = str(c_rst["food_id"])
                    c_rst["food_name"] = f_rst["name"]
        
        return comment_result
