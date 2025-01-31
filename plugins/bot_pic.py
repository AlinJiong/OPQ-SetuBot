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

__doc__ = "壁纸（横屏）"


@deco.ignore_botself
@deco.equal_content("壁纸")
async def receive_group_msg(ctx: GroupMsg):
    action = Action(qq=jconfig.bot)
    action.sendGroupPic(
        ctx.FromGroupId, picUrl='https://iw233.cn/api.php?sort=pc')


@deco.ignore_botself
@deco.equal_content("壁纸")
async def receive_friend_msg(ctx: FriendMsg):
    action = Action(qq=jconfig.bot)
    action.sendFriendPic(
        ctx.FromUin, picUrl='https://iw233.cn/api.php?sort=pc')
