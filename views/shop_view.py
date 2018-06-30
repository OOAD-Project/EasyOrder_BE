from aiohttp import web
import json

async def get_shop(request):
    with open("/var/www/aio_ooad/shop.json", 'r') as load_f:
    #with open("./shop.json", 'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)
        return web.json_response(load_dict)
    return web.json_response({})
