import datetime
import time
from tkinter.messagebox import NO
from botoy.action import Action

import psutil
from botoy import S
from botoy import async_decorators as deco
from botoy import logger
from sympy import im

__doc__ = "早报"

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
    url = 'http://dwz.2xb.cn/zaob'
    content = requests.get(url)
    text_to_dic = json.loads(content.text)
    img_url = text_to_dic['imageUrl']
    if text_to_dic['code'] != 200:
        return None
    return img_url


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
                                           content="#今日早报#", picUrl=img)
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
            ctx.FromUin, content="#今日早报#", picUrl=img)
    del img
    gc.collect()
