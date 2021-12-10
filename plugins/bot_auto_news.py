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

__doc__ = "自动发送早报"


class SearchNews:

    def get_news():
        url = "https://v2.alapi.cn/api/zaobao"
        payload = "token=EFolx1cxAdqqSWqy&format=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, data=payload, headers=headers)
        text_to_dic = json.loads(response.text)
        img_url = text_to_dic['data']['image']

        content = httpx.get(img_url).content
        with BytesIO() as bf:
            image = Image.open(BytesIO(content))
            if image.format == 'WEBP':
                image.save(bf, format="JPEG")
                img = base64.b64encode(bf.getvalue()).decode()
                action = Action(qq=461505108)
                return action.sendFriendPic(2311366525, content="早报", picBase64Buf=img)


job1 = scheduler.add_job(
    SearchNews.get_news, 'interval', hours=9, minutes=0)

# job2 = scheduler.add_job(lambda: print("我一分钟出现一次"), 'interval', minutes=1)
