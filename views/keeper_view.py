from aiohttp import web
import pathlib
import sys
import datetime
from aiohttp_session import get_session
# from aiohttp_session.cookie_storage import EncryptedCookieStorage

BASE_DIR = pathlib.Path(__file__).parent.parent
models_path = BASE_DIR / "models"
aiohttp_polls_path = BASE_DIR / "aiohttp_polls"
sys.path.append(str(models_path))
sys.path.append(str(aiohttp_polls_path))

import keeper
import sales
import aio_engine

# json format
# {
#     "name": "gzm",
#     "psw": "Gzm20125"
# }

engine = aio_engine.read_engine



async def login(request):
    data = await request.json()
    print("data", data)
    if "name" not in data or "psw" not in data:
        return web.json_response({
            "status": False
        })
    name = data["name"]
    psw = data["psw"]
    verify = await keeper.verify(engine, name = name, psw = psw)
    if verify:
        session = await get_session(request)
        session["ooad"] = name
        session["login"] = psw
        session["time"] = str(datetime.datetime.now())
        return web.json_response({
            "status": True
        })
    return web.json_response({
        "status": False
    })



async def need_cookies_page(request):
    session = await get_session(request)
    if "ooad" not in session or "login" not in session or "time" not in session:
        return web.json_response({
            "status": False
        })
    name = session["ooad"]
    psw = session["login"]
    verifyLogin = await keeper.verify(engine, name = name, psw = psw)
    if verifyLogin:
        return web.json_response({
            "status": True
        })
    return web.json_response({
        "status": False
    })


async def verify_login(engine, session):
    if "ooad" not in session or "login" not in session or "time" not in session:
        return False
    name = session["ooad"]
    psw = session["login"]
    r = await keeper.verify(engine, name = name, psw = psw)
    # print("verify r", r)
    if r:
        return True
    return False

async def reservation_count_by_month(request):
    session = await get_session(request)
    r = await verify_login(engine, session)
    print("r", r)
    if not r:
        return web.json_response({
            "info": "you have not login!"
        })
    result_l = []
    now_time = datetime.datetime.now()
    for i in range(1, 13):
        if (i + now_time.month < 13):
            year = now_time.year - 1
        else :
            year = now_time.year
        month = (now_time.month + i - 1) % 12 + 1

        if month <= 9:
            year_mon = str(year) + "-0" + str(month)
        else:
            year_mon = str(year) + "-" + str(month)
        num = await sales.sales_reservation.select_count_by_month(engine, year, str(month))
        num = len(num)
        result_l.append({
            "x": year_mon,
            "y": num
        })
    return web.json_response(result_l)


async def reservation_count_by_day(request):
    session = await get_session(request)
    r = await verify_login(engine, session)
    print("r", r)
    if not r:
        return web.json_response({
            "info": "you have not login!"
        })
    result_l = []
    now_time = datetime.datetime.now()

    #统计最近30天的数据
    for i in range(1, 31):
        tmp_time = now_time - datetime.timedelta(days = i)
        y = str(tmp_time.year)
        m = "0" + str(tmp_time.month) if tmp_time.month < 10  else str(tmp_time.month)
        d = "0" + str(tmp_time.day) if tmp_time.day < 10  else str(tmp_time.day)   
        num = await sales.sales_reservation.select_count_by_day(engine, y, m, d)
        num = len(num)

        result_l.append({
            "x": y + "-" + m + "-" + d,
            "y": num
        })
        #顺序问题？
        #print(result_l)
        result_l.reverse()
    return web.json_response(result_l)




async def reservation_count_by_week(request):
    session = await get_session(request)
    r = await verify_login(engine, session)
    print("r", r)
    if not r:
        return web.json_response({
            "info": "you have not login!"
        })
    result_l = []
    now_time = datetime.datetime.now()
    #统计最近10周的数据
    for i in range(1, 11):
        start_time = now_time - datetime.timedelta(days = 7 * i)
        end_time = start_time + datetime.timedelta(days = 7)
        sum = 0
        for j in range(7):
            tmp_time = start_time + datetime.timedelta(days = j + 1)
            y = str(tmp_time.year)
            m = "0" + str(tmp_time.month) if tmp_time.month < 10  else str(tmp_time.month)
            d = "0" + str(tmp_time.day) if tmp_time.day < 10  else str(tmp_time.day)
            num = await sales.sales_reservation.select_count_by_day(engine, y, m, d)
            sum = sum + len(num)

        result_l.append({
            "x": str(start_time.date()) + "~" + str(end_time.date()),
            "y": sum
        })
        #顺序问题？
        #print(result_l)
        result_l.reverse()
    return web.json_response(result_l)






async def reservation_quantity_piedata(request):
    session = await get_session(request)
    r = await verify_login(engine, session)
    if not r:
        return web.json_response({
            "info": "you have not login!"
        })
    r = await sales.reservation_quantity_piedata(engine)
    return web.json_response(r)




async def total_static_info(request):
    session = await get_session(request)
    r = await verify_login(engine, session)
    if not r:
        return web.json_response({
            "info": "you have not login!"
        })
    r = await sales.sales_reservation.total_static_info(engine)
    return web.json_response(r)


async def transaction_count_by_month(request):
    session = await get_session(request)
    r = await verify_login(engine, session)
    if not r:
        return web.json_response({
            "info": "you have not login!"
        })
    r_list = []
    n = datetime.datetime.now()
    year = n.year
    for i in range(1, 13):
        if i <= 9:
            year_mon = str(year) + "-0" + str(i)
        else:
            year_mon = str(year) + "-" + str(i)
        all_r_in_that_mon = await sales.sales_reservation.select_count_by_month(engine, year, i)
        transation_in_that_mon = 0
        for r in all_r_in_that_mon:
            transation_in_that_mon += r["total"]
        r_list.append({
            "x": year_mon,
            "y": transation_in_that_mon
        })
    return web.json_response(r_list)


async def turnover_piedata(request):
    session = await get_session(request)
    r = await verify_login(engine, session)
    if not r:
        return web.json_response({
            "info": "you have not login!"
        })
    r_list = await sales.turnover_piedata(engine)
    return web.json_response(r_list)



