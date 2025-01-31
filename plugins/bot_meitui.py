from urllib import response
from botoy import logger
from botoy import S
from botoy import decorators
import requests
import json
from botoy import FriendMsg, GroupMsg, S, jconfig, logger
from botoy.decorators import equal_content, ignore_botself
from botoy.session import SessionHandler, ctx, session
import gc
from botoy import async_decorators as deco
import httpx
from botoy import Action, AsyncAction

__doc__ = "看看腿"

# api
# V1: http://yuqingapi.xyz/api/tu.php
# v2: http://121.40.95.21/api/tu.php


async def getPicUrl():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    response = requests.get(url='http://121.40.95.21/api/tu.php',
                            headers=headers, timeout=10)
    if response.status_code != 200:
        logger.info('获取美腿图片异常')
        return None

    else:
        '''坑爹玩意，找了一下午'''
        return response.text.replace('\n', '')


@deco.ignore_botself
@deco.from_these_groups(953219612, 815234602)
@deco.equal_content("看看腿")
async def receive_group_msg(ctx: GroupMsg):
    action = Action(qq=jconfig.bot)
    pic = await getPicUrl()
    if pic:
        action.sendGroupPic(
            ctx.FromGroupId, picUrl=pic)


@deco.ignore_botself
@deco.equal_content("看看腿")
async def receive_friend_msg(ctx: FriendMsg):
    action = Action(qq=jconfig.bot)
    pic = await getPicUrl()
    if pic:
        action.sendFriendPic(
            ctx.FromUin, picUrl=pic)
