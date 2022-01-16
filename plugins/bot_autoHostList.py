import datetime
from email import header
from random import random
from socket import herror
import time
from botoy import action, decorators
from botoy.schedule import scheduler
import requests
import json
from botoy import FriendMsg, GroupMsg, S, jconfig, logger
from botoy.decorators import equal_content, ignore_botself
from botoy.session import SessionHandler, ctx, session
import gc
import urllib.parse
from botoy import async_decorators as deco
from botoy import Action
import random
import httpx
from botoy.contrib import sync_run

__doc__ = "自动推送 微博热搜 早9点，晚7点"


def url_encode(url: str):
    "链接encode"
    return urllib.parse.quote(url, encoding="utf-8")


async def long_to_short(url: str):
    "长链接转短链接"
    api_url = "http://api.suowo.cn/api.htm?url="

    encode_url = url_encode(url)
    key = "61d6c080aee1e862935dab34@9ee40add55f5e3eb3580deb02fa3658b"

    # 第二天 = today + 2
    date_after = datetime.date.today() + datetime.timedelta(days=1)
    # 格式转换

    expireDate = date_after.strftime("%Y-%m-%d")

    final_url = api_url+encode_url+'&key=' + \
        key+'&expireDate='+expireDate+'&domain=5'

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    # }

    t = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
         'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko']

    headers = {}
    headers['User-Agent'] = t[random.randint(0, len(t)-1)]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(final_url, headers=headers, timeout=10)
            return str(response.text)
        except:
            logger.info("长链接转短链接异常！")
            return url

    #     if len(str(response.text)) == 0 or len(str(response.text)) > 40:
    #         return url

    # return str(response.text)


async def get_HotList(choice: str = 'weibo'):
    "获取微博热搜"
    url = "https://v2.alapi.cn/api/tophub/get"
    payload = "token=EFolx1cxAdqqSWqy&type=" + choice
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
               'Content-Type': "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=payload, headers=headers, timeout=10)
            text_to_dic = json.loads(response.text)
            data = text_to_dic['data']['list']
            # logger.info(data[0]['link'])

            content = "#实时微博热搜#\n"

            for i in range(0, 10):
                link = await long_to_short(data[i]['link'])
                logger.info(link)
                content += str(i)+'.' + data[i]['title'] + \
                    '\n' + link + '\n'
                time.sleep(random.randint(5, 8))

            action = Action(qq=jconfig.bot)
            action.sendGroupText(257069779, content)
            time.sleep(5)
            action.sendGroupText(331620093, content)
            time.sleep(3)
            action.sendFriendText(jconfig.superAdmin, content)

            del content, action
            gc.collect()
        except:
            logger.info('自动获取微博热搜失败！')
            return None

    # return content


# @decorators.ignore_botself
# @deco.equal_content("测试")
# async def receive_group_msg(_):
#     await S.atext("长链接转短链接中，请稍后！")
#     await S.atext(get_HotList())


# @deco.ignore_botself
# @deco.equal_content("测试")
# async def receive_friend_msg(_):
#     HotList = await get_HotList()
#     await S.atext(HotList)


def func1():
    sync_run(get_HotList())


job1 = scheduler.add_job(func1, 'cron', hour=9, minute=5)

job2 = scheduler.add_job(func1, 'cron', hour=19, minute=0)
