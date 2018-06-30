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
    tag_object2 = {"description": "美颜素粥", "picture": "this is a tag picture"}
    tag_object3 = {"description": "精美小吃", "picture": "this is a tag picture"}

    food_object = {
        "name": "牛杂汤粉面",
        "imageUrl": "https://i8.meishichina.com/attachment/recipe/2014/07/18/20140718114832312460803.jpg?x-oss-process=style/p800",
        "price": 15,
        "description": "beef noodles",
        "rate": "0.8",
        "remain": "100",
        "tag_id": 1
    }
    food_object1 = {
        "name": "素粉面",
        "imageUrl": "https://www.jucanw.com/UploadFiles/2013-05/admin/2013051715282196795.jpg",
        "price": 12,
        "description": "ordinary noodles",
        "rate": "0.4",
        "remain": "10",
        "tag_id": 1
    }
    food_object2 = {
        "name": "冰冻橙汁",
        "imageUrl": "https://gss0.bdstatic.com/-4o3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike92%2C5%2C5%2C92%2C30/sign=f5c5d8dfa0014c080d3620f76b12696d/2e2eb9389b504fc2c983e573ecdde71191ef6de3.jpg",
        "price": 8,
        "description": "orange juice",
        "rate": "0.4",
        "remain": "10",
        "tag_id": 2
    }
    food_object3 = {
        "name": "冰镇可乐",
        "imageUrl": "http://p0.ifengimg.com/pmop/2017/1220/7DDBA45DDA9A9A5D12A7A860D5AACEBD0A4DB733_size41_w562_h654.jpeg",
        "price": 8,
        "description": "cola",
        "rate": "0.4",
        "remain": "10",
        "tag_id": 2
    }
    food_object4 = {
        "name": "海鲜砂锅粥",
        "imageUrl": "http://pic7.huitu.com/res/20130219/148918_20130219110853979392_1.jpg",
        "price": 12,
        "description": "pot porrige",
        "rate": "0.4",
        "remain": "10",
        "tag_id": 3
    }
    food_object5 = {
        "name": "皮蛋瘦肉粥",
        "imageUrl": "http://img2.imgtn.bdimg.com/it/u=2229490176,1502774060&fm=27&gp=0.jpg",
        "price": 10,
        "description": "pidan porrige",
        "rate": "0.4",
        "remain": "10",
        "tag_id": 3
    }
    food_object6 = {
        "name": "极品黄金糕",
        "imageUrl": "http://img1.imgtn.bdimg.com/it/u=2957551126,1609655971&fm=27&gp=0.jpg",
        "price": 8,
        "description": "golden cake",
        "rate": "0.4",
        "remain": "10",
        "tag_id": 4
    }
    food_object7 = {
        "name": "精美鱼蛋",
        "imageUrl": "http://imgsrc.baidu.com/image/c0%3Dpixel_huitu%2C0%2C0%2C294%2C40/sign=062f903d9c0a304e462fa8bab8b0c2ea/0ff41bd5ad6eddc4aaea50c232dbb6fd526633fe.jpg",
        "price": 6,
        "description": "fish egg",
        "rate": "0.4",
        "remain": "10",
        "tag_id": 4
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
    r = await tag.insert(engine, tag_object2)
    print("tag r", r)
    r = await tag.insert(engine, tag_object3)
    print("tag r", r)

    r = await food.insert(engine, food_object)
    print("food r", r)
    r = await food.insert(engine, food_object1)
    print("food r", r)
    r = await food.insert(engine, food_object2)
    print("food r", r)
    r = await food.insert(engine, food_object3)
    print("food r", r)
    r = await food.insert(engine, food_object4)
    print("food r", r)
    r = await food.insert(engine, food_object5)
    print("food r", r)
    r = await food.insert(engine, food_object6)
    print("food r", r)
    r = await food.insert(engine, food_object7)
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
