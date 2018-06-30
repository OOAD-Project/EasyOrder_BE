import sqlalchemy as sa
from models.meta import meta

import random

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
    for i in range(64):
        s += str(random.randint(1,9))

    try:
        async with engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(payment.insert().values(id = s, payment_time = payment_object["payment_time"], payment_way = payment_object["payment_way"], payment_amount = payment_object["payment_amount"], reservation_id = payment_object["reservation_id"]))
            await trans.commit()
    except Exception as e:
        return e
    else:
        result = {}
        result["insert_state"] = True
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
