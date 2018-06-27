# 菜品 CRUD 操作

import sqlalchemy as sa
from models.meta import meta

# food 菜品的结构，通过 meta 注册器映射为数据库 food 表
food = sa.Table(
    "food",                                                                     # 表名/结构名
    meta,                                                                       # 注册器   
    sa.Column("id", sa.Integer, primary_key = True),                            # 菜品编号
    sa.Column("name", sa.String(50), unique = True, nullable = False),          # 菜名
    sa.Column("picture", sa.String(200)),                                       # 菜品图片
    sa.Column("price", sa.Integer, nullable = False),                           # 菜品价格
    sa.Column("description", sa.String(50)),                                    # 菜品描述
    sa.Column("rating", sa.Float),                                              # 菜品评价
    sa.Column("amount", sa.Integer, nullable = False),                          # 菜品库存
    sa.Column("likes", sa.Integer, default = 0),                                # 菜品点赞
    sa.Column("tag_id", sa.Integer, sa.ForeignKey("tag.id"), nullable = False)  # 菜品所属种类编号
)

# 插入新的菜品记录
# 输入参数：engine 连接数据库的引擎，food_object 要新增的菜品
# 返回值：若插入成功则返回 true，插入失败则返回异常
async def insert(engine, food_object):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(food.insert().values(name = food_object["name"], picture = food_object["picture"], price = food_object["price"], description = food_object["description"], rating = food_object["rating"], amount = food_object["amount"], likes = 0, tag_id = food_object["tag_id"]))
            await trans.commit()
    except Exception as e:
        return e
    else:
        return True

# 删除已有菜品记录
# 输入参数：engine 连接数据库的引擎，food_id 要删除的菜品编号
# 返回值：若删除成功则返回 true，删除失败则返回 false
async def delete(engine, food_id):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(food.delete().where(food.c.id == food_id))
            await trans.commit()
    except:
        return False
    else:
        return True

# 获取已有菜品记录
# 输入参数：engine 连接数据库的引擎，food_name 菜品名，food_id 菜品编号，likes 菜品点赞数
# 返回值：与 food_name 和 food_id 对应的点赞数 >= likes 的所有菜品列表；如果不指定参数则返回 food 表的所有菜品列表
async def select(engine, food_name = None, food_id = None, likes = None):
    async with engine.acquire() as conn:
        trans = await conn.begin()
        select_object = food.select()
        if food_name:
            select_object = select_object.where(food.c.name == food_name)
        if food_id:
            select_object = select_object.where(food.c.id == food_id)
        if likes:
            select_object = select_object.where(food.c.likes >= likes)
        cursor = await conn.execute(select_object)
        records = await cursor.fetchall()
        await trans.commit()
        return [dict(r) for r in records]

# 相应菜品的点赞数 +1
# 输入参数：engine 连接数据库的引擎，id 菜品编号
# 返回值：更新成功返回 true，更新失败则返回 false
async def like(engine, id):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(food.update().where(food.c.id == id).values(likes = food.c.likes + 1))
            await trans.commit()
    except:
        return False
    else:
        return True





