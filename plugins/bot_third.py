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

__doc__ = "三次元"

# api V1：http://api.wadg.pro/
# api V2: https://api.ityun.tech/api/getPic?token=e2d74a2b83b549248421dedd7e293e13
# api V3: https://api.uomg.com/api/rand.img3?format=images
# api v4: https://api.5s9s.com/product/api?&apikey=61334714823020445e3cbc82aa5c5b26
# api v5: http://api.btstu.cn/sjbz/?lx=meizi


@deco.ignore_botself
@deco.from_these_groups(953219612, 815234602)
@deco.equal_content("三次元")
async def receive_group_msg(ctx: GroupMsg):
    action = Action(qq=jconfig.bot)
    action.sendGroupPic(
        ctx.FromGroupId, picUrl='http://api.btstu.cn/sjbz/?lx=meizi')


@deco.ignore_botself
@deco.equal_content("三次元")
async def receive_friend_msg(ctx: FriendMsg):
    action = Action(qq=jconfig.bot)
    action.sendFriendPic(
        ctx.FromUin, picUrl='http://api.btstu.cn/sjbz/?lx=meizi')
