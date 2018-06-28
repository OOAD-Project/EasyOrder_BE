# 订单 CRUD 操作

import sqlalchemy as sa
from models.meta import meta
import datetime

# reservation 订单的结构，通过 meta 注册器映射为数据库 reservation 表
reservation = sa.Table(
    "reservation",                                        # 表名
    meta,                                                 # 注册器
    sa.Column("isPaid", sa.Boolean, default = False),     # 订单是否已结账
    sa.Column("id", sa.Integer, primary_key = True),      # 订单编号
    sa.Column("reserve_datetime", sa.DateTime),           # 订单日期
    sa.Column("pay_datetime", sa.DateTime),               # 结账日期
    sa.Column("table_num", sa.Integer, nullable = False), # 订单对应的饭桌号
    sa.Column("food_list", sa.JSON),                      # 订单包含的菜品列表
    sa.Column("total", sa.Float),                         # 订单总价
    sa.Column("isOutOfDate",sa.Boolean, default = False)             # 订单是否过期
)

# 插入新的订单记录
# 输入参数：engine 连接数据库的引擎，reservation_object 要新增的订单
# 返回值：若插入成功则返回最新插入的订单的id
async def insert(engine, reservation_object):
    async with engine.acquire() as conn:
        trans = await conn.begin()
        if "pay_datetime" not in reservation_object:
        	await conn.execute(reservation.insert().values(isPaid = reservation_object["isPaid"], reserve_datetime = datetime.datetime.now(), table_num = reservation_object["table_num"], food_list = reservation_object["food_list"], total = reservation_object["total"], isOutOfDate = reservation_object["isOutOfDate"]))
        elif "pay_datetime" in reservation_object:
        	await conn.execute(reservation.insert().values(isPaid = reservation_object["isPaid"], reserve_datetime = datetime.datetime.now(), pay_datetime = reservation_object["pay_datetime"],
                                                           table_num = reservation_object["table_num"], food_list = reservation_object["food_list"], total = reservation_object["total"], isOutOfDate = reservation_object["isOutOfDate"]))
        cursor = await conn.execute("SELECT LAST_INSERT_ID() FROM reservation;")
        record = await cursor.fetchone()
        await trans.commit()
        return dict(record)

# 删除已有的订单记录
# 输入参数：engine 连接数据库的引擎，id 要删除订单的编号
# 返回值：若删除成功则返回true，删除失败则返回 false
async def delete(engine, id):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(reservation.delete().where(id == id))
            await trans.commit()
    except:
        return False
    else:
        return True

# 获取已有的订单记录
# 输入参数：engine 连接数据库的引擎，id 要获取的订单编号，reserve_datetime 订单创建日期，pay_datetime 订单结账日期，table_num 订单对应桌号
# 返回值：与各个参数对应的所有订单列表；如果不指定参数则返回 reservation 表的所有菜品列表
async def select(engine, id = None, reserve_datetime = None, pay_datetime = None, table_num = None):
    async with engine.acquire() as conn:
        trans = await conn.begin()
        select_object = reservation.select()
        if id:
            select_object = select_object.where(reservation.c.id == id)
        if reserve_datetime:
            select_object = select_object.where(reservation.c.reserve_datetime == reserve_datetime)
        if pay_datetime:
            select_object = select_object.where(reservation.c.pay_datetime == pay_datetime)
        if table_num:
            select_object = select_object.where(reservation.c.table_num == table_num)
        cursor = await conn.execute(select_object)
        records = await cursor.fetchall()
        await trans.commit()
        return [dict(r) for r in records]


#获取所有订单
async def select_all_reservation(engine):
    r = await select(engine)
    return r


# 获取所有已支付订单
# 输入参数 数据库连接 engine
# 返回所有已支付订单
async def select_paid_reservation(engine):
    async with engine.acquire() as conn:
        trans = await conn.begin()
        select_obj = reservation.select().where(reservation.c.isPaid == True)
        cursor = await conn.execute(select_obj)
        records = await cursor.fetchall()
        await trans.commit()
        return [dict(r) for r in records]





# 获取指定年月的所有订单
# 输入参数：engine 连接数据库的引擎，year 年，mon 月
# 返回值：对应年月的所有订单记录
async def select_count_by_month(engine, year, mon):
    async with engine.acquire() as conn:
        trans = await conn.begin()
        cursor = await conn.execute(reservation.select().where(sa.extract('year', reservation.c.reserve_datetime) == year).where(sa.extract("month", reservation.c.reserve_datetime) == mon))
        records = await cursor.fetchall()
        await trans.commit()
        return records

# 获取指定年月日的所有订单
# 输入参数：engine 连接数据库的引擎，year 年，mon 月 day 日
# 返回值：对应年月日的所有订单记录
async def select_count_by_day(engine, year, mon, day):
    async with engine.acquire() as conn:
        trans = await conn.begin()
        cursor = await conn.execute(reservation.select().where(sa.extract('year', reservation.c.reserve_datetime) == year).where(sa.extract("month", reservation.c.reserve_datetime) == mon)
                                    .where(sa.extract("day", reservation.c.reserve_datetime) == day))
        records = await cursor.fetchall()
        await trans.commit()
        return records

# 获取所有订单汇总信息
# 输入参数：engine 连接数据库的引擎
# 返回值：total_turnover 总销售额，total_reservation 总订单量，
#        total_payment 已结账订单的总额，reservation_payment_ratio 已结账订单占总订单份额
async def total_static_info(engine):
    async with engine.acquire() as conn:
        trans = await conn.begin()
        cursor = await conn.execute(reservation.select())
        records = await cursor.fetchall()
        await trans.commit()
        print("record", records)
        records = [dict(r) for r in records]
        total_turnover = 0
        total_reservation = 0
        total_payment = 0
        pay_count = 0
        for r in records:
            total_turnover += r["total"]
            total_reservation += 1
            if r["isPaid"]:
                total_payment += r["total"]
                pay_count += 1
        reservation_payment_ratio = float(pay_count) / float(total_reservation)
        return {
            "total_turnover": total_turnover,
            "total_reservation": total_reservation,
            "total_payment": total_payment,
            "reservation_payment_ratio": reservation_payment_ratio
        }




