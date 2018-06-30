from aiohttp import web
import json

async def get_shop(request):
    print("========================");
<<<<<<< HEAD
<<<<<<< HEAD
    with open("/var/www/aio_ooad/shop.json", 'r') as load_f:
=======
    with open("/home/gzm/three/系统分析与设计/大作业/EasyOrder_BE/shop.json", 'r') as load_f:
>>>>>>> 9138b7fbe995cec2c7a867adcf5b8ca68cf1e7ff
=======
    with open("./shop.json", 'r') as load_f:
>>>>>>> 47732bb9f12743d1b45ed4a6c848d116ba92edc0
        load_dict = json.load(load_f)
        print(load_dict)
        return web.json_response(load_dict)
    return web.json_response({})
