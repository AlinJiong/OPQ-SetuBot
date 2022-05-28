from random import random
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
import random


__doc__ = "二次元"

setuPattern = "二[次刺][元猿]"

api_list = ["https://api.ixiaowai.cn/api/api.php",
            "https://www.dmoe.cc/random.php"]


@deco.ignore_botself
@deco.on_regexp(setuPattern)
async def receive_group_msg(ctx: GroupMsg):
    action = Action(qq=jconfig.bot)
    action.sendGroupPic(
        ctx.FromGroupId, picUrl=api_list[random.randint(0, len(api_list)-1)])


@deco.ignore_botself
@deco.on_regexp(setuPattern)
async def receive_friend_msg(ctx: FriendMsg):
    action = Action(qq=jconfig.bot)
    action.sendFriendPic(
        ctx.FromUin, picUrl='https://www.dmoe.cc/random.php')
