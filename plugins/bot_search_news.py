import datetime
import time
from tkinter.messagebox import NO
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
import gc


async def get_news():
    url = "https://v2.alapi.cn/api/zaobao"
    payload = "token=1jfSWghgtebOjpQi&format=json"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
               'Content-Type': "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=payload, headers=headers, timeout=10)
            text_to_dic = json.loads(response.text)
            img_url = text_to_dic['data']['image']
        except:
            logger.info("早报api获取失败！")
            return None

        try:
            new_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }

            content = await client.get(img_url, headers=new_headers, timeout=10)
            content = content.content
            with BytesIO() as bf:
                image = Image.open(BytesIO(content))
                if image.format == 'WEBP':
                    image.save(bf, format="JPEG")
                    img = base64.b64encode(bf.getvalue()).decode()
                    logger.info("获取早报成功！")
                    return img
        except:
            logger.info("早报api转图片失败！")
            return None

# @deco.ignore_botself
# @deco.equal_content("早报")
# async def receive_group_msg(ctx: GroupMsg):
#     await S.bind(ctx).aimage(get_news(), text='#今日早报#', type=S.TYPE_BASE64)
#     # Action(ctx.CurrentQQ).sendGroupPic(ctx.FromGroupId,
#     #                                    content="#今日早报#", picBase64Buf=get_news())
#     logger.info(f'向群：{ctx.FromGroupId} 发送早报')


# @deco.ignore_botself
# @deco.equal_content("早报")
# async def receive_friend_msg(ctx: FriendMsg):
#     # Action(ctx.CurrentQQ).sendFriendPic(ctx.FromUin,
#     #                                     content="#今日早报#", picBase64Buf=get_news())
#     await S.bind(ctx).aimage(get_news(), text='#今日早报#', type=S.TYPE_BASE64)
#     logger.info(f'向好友：{ctx.FromUin} 发送早报')


@deco.ignore_botself
@deco.equal_content("早报")
async def receive_group_msg(ctx: GroupMsg):
    img = await get_news()
    if img == None:
        Action(ctx.CurrentQQ).sendGroupText(
            ctx.FromGroupId, content="网络响应超时，请稍后重试！")
    else:
        Action(ctx.CurrentQQ).sendGroupPic(ctx.FromGroupId,
                                           content="#今日早报#", picBase64Buf=img)
    del img
    gc.collect()


@deco.ignore_botself
@deco.equal_content("早报")
async def receive_friend_msg(ctx: FriendMsg):
    img = await get_news()
    if img == None:
        Action(ctx.CurrentQQ).sendFriendText(
            ctx.FromUin, content="网络响应超时，请稍后重试！")
    else:
        Action(ctx.CurrentQQ).sendFriendPic(
            ctx.FromUin, content="#今日早报#", picBase64Buf=img)
    del img
    gc.collect()
