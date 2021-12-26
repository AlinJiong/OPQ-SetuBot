import re

from botoy import GroupMsg, S
from botoy import async_decorators as deco
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
from botoy import Action

import requests
import re


__doc__ = "检测到python关键字，给主人发消息"


@deco.ignore_botself
@deco.in_content("ython")
async def receive_group_msg(ctx: GroupMsg):
    info = ctx.Content
    action = Action(qq=461505108)

    action.sendFriendText(2311366525, info)
    logger.info("发送python相关信息成功！")
    del action
