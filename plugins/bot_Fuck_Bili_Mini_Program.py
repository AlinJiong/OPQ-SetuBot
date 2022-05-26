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

import requests
import re
from io import BytesIO
from PIL import Image, ImageFilter

__doc__ = """B站小程序转成链接(auto)"""


@deco.ignore_botself
@deco.these_msgtypes("XmlMsg")
async def receive_group_msg(ctx: GroupMsg):
    if info := re.findall(r"(https://b23\.tv/\w*)", ctx.Content):
        try:
            img_url = re.findall(r'http://pub.*?\\', ctx.Content)[0].replace('\\', '')
            content = requests.request("get", img_url).content
            with BytesIO() as bf:
                image = Image.open(BytesIO(content))
                image.save(bf, format="JPEG")
                img = base64.b64encode(bf.getvalue()).decode()

            await S.bind(ctx).aimage(
                img,
                info[0],
                type=S.TYPE_BASE64,
            )
            #await S.bind(ctx).atext(info[0])
        except:
            pass
