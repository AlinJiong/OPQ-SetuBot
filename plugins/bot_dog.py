import datetime
import time

import cpuinfo
import psutil
from botoy import S
from botoy import async_decorators as deco
from botoy import logger

__doc__ = "发送 舔狗日记 查看"

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

    def get_news():
        url = "https://v2.alapi.cn/api/dog"
        payload = "token=EFolx1cxAdqqSWqy&format=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, data=payload, headers=headers)
        text_to_dic = json.loads(response.text)
        content = text_to_dic['data']['content']
        return content


@deco.ignore_botself
@deco.in_content("舔狗日记")
async def receive_group_msg(_):
    await S.atext(SearchNews.get_news())


@deco.ignore_botself
@deco.in_content("舔狗日记")
async def receive_friend_msg(_):
    await S.atext(SearchNews.get_news())
