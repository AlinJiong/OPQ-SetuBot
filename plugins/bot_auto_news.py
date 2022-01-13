from botoy.schedule import async_scheduler
from botoy.schedule import scheduler
import datetime
import time
import psutil
from botoy import S
from botoy import async_decorators as deco
from botoy import logger
from botoy.config import Config

import base64
import json
from io import BytesIO
from pathlib import Path

import httpx
from PIL import Image, ImageFilter
from botoy import FriendMsg, GroupMsg, S, jconfig, logger
from botoy.parser import friend as fp
from botoy.parser import group as gp
from httpx_socks import AsyncProxyTransport
import requests

from botoy import Action
from botoy import AsyncAction
from botoy.contrib import sync_run


import gc

__doc__ = "自动发送早报"


async def get_news():
    url = "https://v2.alapi.cn/api/zaobao"
    payload = "token=EFolx1cxAdqqSWqy&format=json"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload, headers=headers)
        text_to_dic = json.loads(response.text)
        img_url = text_to_dic['data']['image']
        content = await client.get(img_url)
        content = content.content
        with BytesIO() as bf:
            image = Image.open(BytesIO(content))
            if image.format == 'WEBP':
                image.save(bf, format="JPEG")
                img = base64.b64encode(bf.getvalue()).decode()
                logger.info("获取早报成功！")
                return img


async def send_news():
    img = await get_news()
    action = Action(qq=jconfig.bot)
    groups_tmp = action.getGroupList()
    groups = []
    for group in groups_tmp:
        groups.append(group['GroupId'])

    try:
        for group in groups:
            try:
                action.sendGroupPic(group, content="#今日早报#", picBase64Buf=img)
                time.sleep(3)
                logger.info("发送"+str(group)+"早报成功！")
            except:
                pass

        action.sendFriendPic(jconfig.superAdmin,
                             content="#今日早报#", picBase64Buf=img)

        logger.info("发送早报成功！")
    except:
        logger.info("发送早报失败！")

    del img, groups_tmp, groups, action
    gc.collect()


async def send_news_to_one():
    img = await get_news()
    try:
        Action(qq=jconfig.bot).sendFriendPic(2382194151, content="#今日早报#", picBase64Buf=img)
        logger.info("发送7点早报成功！")
    except:
        pass
    del img
    gc.collect()


def fun1():
    sync_run(send_news())


def fun2():
    sync_run(send_news_to_one())


job1 = scheduler.add_job(fun1, 'cron', hour=9, minute=0)

job2 = scheduler.add_job(fun2, 'cron', hour=7, minute=0)

# 西科 544830164
# ac 257069779
# 西昌 554262929
# 测试 953219612
# job1 = scheduler.add_job(get_news, 'interval', minutes=1)

# if not flag:
#     action = Action(qq=461505108)
#     img = get_news()
#     # action.sendGroupPic(544830164, content="#今日早报#", picBase64Buf=img)
#     # action.sendGroupPic(257069779, content="#今日早报#", picBase64Buf=img)
#     # action.sendGroupPic(953219612, content="#今日早报#", picBase64Buf=img)
#     action.sendFriendPic(2311366525, content="#今日早报#", picBase64Buf=img)
#     del action

# job2 = scheduler.add_job(lambda: print("我一分钟出现一次"), 'interval', minutes=1)
