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
import re
import requests
import random


__doc__ = "妹子图"


async def get_img_url():
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
        'Cookie': '_gid=GA1.2.290905563.1658156949; _ga=GA1.2.1357810641.1658156947; _ga_JJBVYW78Q1=GS1.1.1658156947.1.1.1658158762.0',
    }

    random_id = str(random.randint(1, 7179))
    url = f'https://mm.tvv.tw/archives/{random_id}.html'
    logger.info(url)
    res = requests.get(url=url, headers=headers, timeout=10)

    if res.status_code == 200:
        pattern = r'https?://img.gh-proxy.com/.*?.jpg'
        img_list = re.findall(pattern, res.text)
        img_list = list(set(img_list))
        logger.info(img_list)
        if len(img_list) >= 6:
            return img_list[:5]
        else:
            return img_list
    else:
        logger.info('请求mm图失败！')
        return None


@deco.ignore_botself
@deco.from_these_groups(953219612, 815234602)
@deco.equal_content("妹子图")
async def receive_group_msg(ctx: GroupMsg):
    action = Action(qq=jconfig.bot)
    img_list = await get_img_url()
    if img_list:
        action.sendGroupMultiPic(ctx.FromGroupId, *img_list)
