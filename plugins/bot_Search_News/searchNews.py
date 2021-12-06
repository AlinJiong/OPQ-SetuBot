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


if proxies_socks := jconfig.proxies_socks:
    transport = AsyncProxyTransport.from_url(proxies_socks)
    proxies = None
else:
    transport = None
    proxies = jconfig.proxies_http

client_options = dict(proxies=proxies, transport=transport, timeout=20)


class SearchNews:
    def __init__(self, ctx):
        self.ctx = ctx
        self.send = S.bind(ctx)

    async def get_news(self):

        url = "https://v2.alapi.cn/api/zaobao"
        payload = "token=EFolx1cxAdqqSWqy&format=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, data=payload, headers=headers)
        img_url = response.text['image'].replace('\\', '')

        content = httpx.get(img_url).content
        with BytesIO() as bf:
            image = Image.open(content)
            if image.format == 'WEBP':
                image.save(bf, format="JPEG")
                img = base64.b64encode(bf.getvalue()).decode()
                await self.send.aimage(img, msg="早报", type=self.send.TYPE_BASE64)
