import datetime
import time

import cpuinfo
import psutil
from botoy import S
from botoy import async_decorators as deco
from botoy import logger

__doc__ = "发送 早报 查看新闻"

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


class SearchNews:
    def __init__(self):
        self.msg = '早报'

    async def get_news(self):
        url = "https://v2.alapi.cn/api/zaobao"
        payload = "token=EFolx1cxAdqqSWqy&format=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, data=payload, headers=headers)
        img_url = response.text['image'].replace('\\', '')

        content = httpx.get(img_url).content
        with BytesIO() as bf:
            image = Image.open(content)
            if image.format == 'WEBP':
                image.save(bf, format="JPEG")
                img = base64.b64encode(bf.getvalue()).decode()
                return img
                # await self.send.aimage(img, msg="早报", type=self.send.TYPE_BASE64)


@deco.ignore_botself
@deco.equal_content("早报")
async def receive_group_msg(_):
    await S.aimage(SearchNews.get_news(), msg="早报", type=S.TYPE_BASE64)


@deco.ignore_botself
@deco.equal_content("早报")
async def receive_friend_msg(_):
    await S.aimage(SearchNews.get_news(), msg="早报", type=S.TYPE_BASE64)
