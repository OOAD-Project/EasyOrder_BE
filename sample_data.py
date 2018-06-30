from models import food
from models import tag
from models import comment
from models import reservation
from models import keeper
from aiohttp_polls.aio_engine import init_engine
import asyncio

async def insert_sample_data():
    engine = await init_engine()
    tag_object = {"description": "粉面", "picture": "this is a tag picture"}
    tag_object1 = {"description": "饮品", "picture": "this is a tag picture"}
    food_object = {
        "name": "牛杂汤粉面",
        "imageUrl": "https://i8.meishichina.com/attachment/recipe/2014/07/18/20140718114832312460803.jpg?x-oss-process=style/p800",
        "price": 15,
        "description": "this is a pork",
        "rate": "0.8",
        "remain": "100",
        "tag_id": 1
    }
    food_object1 = {
        "name": "素粉面",
        "imageUrl": "https://www.jucanw.com/UploadFiles/2013-05/admin/2013051715282196795.jpg",
        "price": 12,
        "description": "this is a fish",
        "rate": "0.4",
        "remain": "10",
        "tag_id": 1
    }

    r_object = {
        "isPaid": True,
        "table_num": 12,
        "food_list": {"牛杂汤粉面": 3, "素粉面": 2},
        "total": 69,
        "isOutOfDate": False
    }
    keeper_object = {
        "name": "root",
        "psw": "Gzm20125"
    }
    comment_object1 = {
        "food_id": 1,
        "rating": 4,
        "content": "oh, so delicious!"
    }
    comment_object2 = {
        "food_id": 1,
        "rating": 5,
        "content": "oh, so tasty!"
    }
    comment_object3 = {
        "food_id": 2,
        "rating": 3,
        "content": "oh, so lovely!"
    }
    comment_object4 = {
        "food_id": 2,
        "rating": 4,
        "content": "oh, so cute!"
    }

    r = await tag.insert(engine, tag_object)
    print("tag r", r)
    r = await tag.insert(engine, tag_object1)
    print("tag r", r)
    r = await food.insert(engine, food_object)
    print("food r", r)
    r = await food.insert(engine, food_object1)
    print("food r", r)
    r = await reservation.insert(engine, r_object)
    print("reservation r", r)
    r = await keeper.insert(engine, keeper_object)
    print("keeper r", r)
    r = await comment.insert(engine, comment_object1)
    print("comment r", r)
    r = await comment.insert(engine, comment_object2)
    print("comment r", r)
    r = await comment.insert(engine, comment_object3)
    print("comment r", r)
    r = await comment.insert(engine, comment_object4)
    print("comment r", r)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(insert_sample_data())
