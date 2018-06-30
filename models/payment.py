import sqlalchemy as sa
from models.meta import meta

import pathlib
import sys
BASE_DIR = pathlib.Path(__file__).parent.parent
models_path = BASE_DIR / "models"
aiohttp_polls_path = BASE_DIR / "aiohttp_polls"
sys.path.append(str(models_path))
sys.path.append(str(aiohttp_polls_path))

import random
import sales
import datetime
from models.reservation import reservation


payment = sa.Table(
    "payment",
    meta,
    sa.Column("id", sa.String(64), primary_key = True),
    sa.Column("payment_time", sa.DateTime, nullable = False),
    sa.Column("payment_way", sa.String(50), nullable = False),
    sa.Column("payment_amount", sa.Float),
    sa.Column("reservation_id", sa.Integer, nullable = False)
)

async def insert(engine, payment_object):
    s=""
    is_find = False;
    for i in range(64):
        s += str(random.randint(1,9))
    
    print("payment_object", payment_object)

    # try:
    async with engine.acquire() as conn:
        trans = await conn.begin()
            #先判断reservation有没有payment
        print("reservation_id", payment_object["reservation_id"])
        res = await sales.sales_reservation.select(engine, id=int(payment_object["reservation_id"]))
        if (res != [] and res[0]["isPaid"] == False):
            is_find = True
            res = res[0]
            res["isPaid"] = True
            res["pay_datetime"] = datetime.datetime.now()
                #更新reservation
            await conn.execute(reservation.update().where(reservation.c.id == payment_object["reservation_id"]).values(isPaid = res["isPaid"], reserve_datetime = res["reserve_datetime"], table_num = res["table_num"], food_list = res["food_list"], total = res["total"], pay_datetime = res["pay_datetime"], isOutOfDate = res["isOutOfDate"]))
            #插入payment
            await conn.execute(payment.insert().values(id = s, payment_time = payment_object["payment_time"], payment_way = payment_object["payment_way"], payment_amount = payment_object["payment_amount"], reservation_id = payment_object["reservation_id"]))
        await trans.commit()
    # except Exception as e:
    #     return e
    # else:
    result = {}
    result["status"] = False
    result["payment_id"] = ""
    if is_find:
        result["status"] = True
        result["payment_id"] = s
    return result


async def delete(engine, payment_id):
    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(payment.delete().where(payment.c.id == payment_id))
            await trans.commit()
    except:
        return False
    else:
        return True


async def select(engine, payment_id = None, reservation_id = None, payment_time = None, payment_amount = None, payment_way = None):
    async with engine.acquire() as conn:
        trans = await conn.begin()
        select_object = payment.select()
        if payment_id:
            select_object = select_object.where(payment.c.id == payment_id)
        if reservation_id:
            select_object = select_object.where(payment.c.reservation_id == reservation_id)
        if payment_time:
            select_object = select_object.where(payment.c.payment_time <= payment_time)
        if payment_amount:
            select_object = select_object.where(payment.c.payment_amount >= payment_amount)
        if payment_way:
            select_object = select_object.where(payment.c.payment_way == payment_way)
        cursor = await conn.execute(select_object)
        records = await cursor.fetchall()
        await trans.commit()
        return [dict(r) for r in records]
