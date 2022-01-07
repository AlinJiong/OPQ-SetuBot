import datetime
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

__doc__ = "自动推送 微博热搜 早9点，晚7点"


def url_encode(url: str):
    "链接encode"
    return urllib.parse.quote(url, encoding="utf-8")


def long_to_short(url: str):
    "长链接转短链接"
    api_url = "http://api.suowo.cn/api.htm?url="

    origin_url = url_encode(url)
    key = "61d6c080aee1e862935dab34@9ee40add55f5e3eb3580deb02fa3658b"

    # 第二天 = today + 2
    date_after = datetime.date.today() + datetime.timedelta(days=1)
    # 格式转换

    expireDate = date_after.strftime("%Y-%m-%d")

    url = api_url + origin_url+'&key=' + \
        key+'&expireDate='+expireDate+'&domain=5'
    # print(url)
    response = requests.request("GET", url)

    if len(str(response.text)) == 0 or len(str(response.text)) > 40:
        return url

    return str(response.text)


def get_HotList(choice: str = 'weibo'):
    "获取微博热搜"
    url = "https://v2.alapi.cn/api/tophub/get"
    payload = "token=EFolx1cxAdqqSWqy&type=" + choice
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)

    text_to_dic = json.loads(response.text)
    data = text_to_dic['data']['list']

    content = "#实时微博热搜：\n"

    for i in range(0, 10):
        content += str(i)+'.' + data[i]['title'] + \
            '\n' + long_to_short(data[i]['link'])+'\n'
        time.sleep(3)

    action = Action(qq=jconfig.bot)
    action.sendGroupText(257069779, content)
    action.sendFriendText(jconfig.superAdmin, content)

    # del content
    # gc.collect()

    return content


# @decorators.ignore_botself
# @deco.equal_content("测试")
# async def receive_group_msg(_):
#     await S.atext("长链接转短链接中，请稍后！")
#     await S.atext(get_HotList())


# @deco.ignore_botself
# @deco.equal_content("测试")
# async def receive_friend_msg(_):
#     await S.atext("长链接转短链接中，请稍后！")
#     await S.atext(get_HotList())


job1 = scheduler.add_job(get_HotList, 'cron', hour=9, minute=5)

job2 = scheduler.add_job(get_HotList, 'cron', hour=19, minute=0)
