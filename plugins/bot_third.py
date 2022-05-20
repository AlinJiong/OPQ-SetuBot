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
from botoy import Action

__doc__ = "三次元"


@deco.ignore_botself
@deco.equal_content("三次元")
async def receive_group_msg(ctx: FriendMsg):
    action = Action(qq=jconfig.bot)
    action.sendGroupPic(ctx.FromUin, picUrl='http://api.wadg.pro/')


@deco.ignore_botself
@deco.equal_content("三次元")
async def receive_friend_msg(ctx: FriendMsg):
    action = Action(qq=jconfig.bot)
    action.sendFriendPic(ctx.FromUserId, picUrl='http://api.wadg.pro/')
