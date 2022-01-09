import datetime
import time
from botoy.action import Action

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
            return img


@deco.ignore_botself
@deco.equal_content("早报")
async def receive_group_msg(ctx: GroupMsg):
    Action(ctx.CurrentQQ).sendGroupPic(ctx.FromGroupId,
                                         content="#今日早报#", picBase64Buf=get_news())
    logger.info(f'向群：{ctx.FromGroupId} 发送早报')


@deco.ignore_botself
@deco.equal_content("早报")
async def receive_friend_msg(ctx: FriendMsg):
    Action(ctx.CurrentQQ).sendFriendPic(ctx.FromUin,
                                         content="#今日早报#", picBase64Buf=get_news())
    logger.info(f'向好友：{ctx.FromUin} 发送早报')
