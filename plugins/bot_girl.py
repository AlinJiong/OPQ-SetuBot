# import datetime
# import time

# import cpuinfo
# import psutil
# from botoy import S
# from botoy import async_decorators as deco
# from botoy import logger

# __doc__ = "发送 妹子图 查看"

# import base64
# import json
# from io import BytesIO
# from pathlib import Path

# import httpx
# from PIL import Image, ImageFilter
# from botoy import FriendMsg, GroupMsg, S, jconfig, logger
# from botoy.parser import friend as fp
# from botoy.parser import group as gp
# from httpx_socks import AsyncProxyTransport
# import requests


# class SearchNews:

#     def get_news():
#         url = "http://api.nmb.show/xiaojiejie1.php"
#         content = requests.request("get", url).content
#         with BytesIO() as bf:
#             image = Image.open(BytesIO(content))
#             image.save(bf, format="JPEG")
#             img = base64.b64encode(bf.getvalue()).decode()
#             print(img)


# @deco.ignore_botself
# @deco.in_content("妹子图")
# async def receive_group_msg(_):
#     await S.aimage(SearchNews.get_news(),  type=S.TYPE_BASE64)


# @deco.ignore_botself
# @deco.in_content("妹子图")
# async def receive_friend_msg(_):
#     await S.aimage(SearchNews.get_news(),  type=S.TYPE_BASE64)
