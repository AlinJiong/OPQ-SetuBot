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


@deco.ignore_botself
@deco.from_these_groups(953219612, 815234602)
@deco.equal_content("看看腿")
async def receive_group_msg(ctx: GroupMsg):
    action = Action(qq=jconfig.bot)
    action.sendGroupPic(
        ctx.FromGroupId, picUrl='https://api.5s9s.com/product/api?&apikey=8715f1e155618c19e563cca1fae62f4e')


@deco.ignore_botself
@deco.equal_content("看看腿")
async def receive_friend_msg(ctx: FriendMsg):
    action = Action(qq=jconfig.bot)
    action.sendFriendPic(
        ctx.FromUin, picUrl='https://api.5s9s.com/product/api?&apikey=8715f1e155618c19e563cca1fae62f4e')
