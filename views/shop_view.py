from aiohttp import web
import json

async def get_shop(request):
    print("========================");
    with open("/home/gzm/three/系统分析与设计/大作业/EasyOrder_BE/shop.json", 'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)
        return web.json_response(load_dict)
    return web.json_response({})
