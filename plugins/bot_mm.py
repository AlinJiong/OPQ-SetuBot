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
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Cookie': 'SINAGLOBAL=619039809697.5059.1651107987513; UOR=,,www.baidu.com; _s_tentry=-; Apache=8730444394095.282.1656088091569; ULV=1656088091626:6:1:1:8730444394095.282.1656088091569:1653289701033; SSOLoginState=1656088105; SUB=_2A25PsZZ5DeRhGeBJ4lIQ9SvPyTqIHXVtXToxrDV8PUJbkNANLVTckW1NRiUdliZ2ex-vWrC51qNA7uvdGrUgg5lr; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFpz-VROc7-vMd2xUpqQbR45NHD95QcS0.7eK-fe0zcWs4DqcjMi--fiK.fiKyWi--fiK.0iKnRi--fiK.0iKLsqBtt'
    }

    random_id = str(random.randint(1, 7179))
    url = f'https://mm.tvv.tw/archives/{random_id}.html'
    res = requests.get(url=url,
                       headers=headers, timeout=10)

    if res.status_code == 200:
        pattern = r'https://img.gh-proxy.com/.*?.jpg'
        img_list = re.findall(pattern, res.text)
        if len(img_list) >= 7:
            return img_list[1:6]
        else:
            return img_list[1:]
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
