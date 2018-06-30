# 菜品种类/标签 CRUD 操作

import sqlalchemy as sa
from models.meta import meta
import asyncio

# tag 菜品种类/标签的结构，通过 meta 注册器映射为数据库 tag 表
tag = sa.Table(
    "tag",                                            # 表名
    meta,                                             # 注册器
    sa.Column("id", sa.Integer, primary_key = True),  # 种类编号
    sa.Column("description", sa.String(50)),          # 种类描述
    sa.Column("picture", sa.String(50))               # 种类图片
)

# 插入新的菜品种类记录
# 输入参数：engine 连接数据库的引擎，tag_object 要新增的菜品种类
# 返回值：若插入成功则返回 true，插入失败则返回 false
async def insert(engine, tag_object):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(tag.insert().values(description = tag_object["description"], picture = tag_object["picture"]))
            await trans.commit()
    except:
        return False
    else:
        return True

# 删除已有的菜品种类记录
# 输入参数：engine 连接数据库的引擎，tag_id 要删除的菜品种类编号
# 返回值：若插入成功则返回 true，插入失败则返回 false
async def delete(engine, tag_id):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(tag.delete().where(tag.c.id == tag_id))
            await trans.commit()
    except:
        return False
    else:
        return True

# 获取已有的菜品种类记录
# 输入参数：engine 连接数据库的引擎，tag_id 要获取的菜品种类编号
# 返回值：对应编号的菜品种类记录
async def select(engine, tag_id):
    if not tag_id:
        return None
    async with engine.acquire() as conn:
        trans = await conn.begin()
        cursor = await conn.execute(tag.select().where(tag.c.id == tag_id))
        records = await cursor.fetchall()
        await trans.commit()
        return [dict(r) for r in records]



if __name__ == "__main__":
	pass
