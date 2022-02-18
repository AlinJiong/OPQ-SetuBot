from botoy import decorators
import requests
import json
from botoy import FriendMsg, GroupMsg, S, jconfig, logger
from botoy.decorators import equal_content, ignore_botself
from botoy.session import SessionHandler, ctx, session
import gc
from botoy import async_decorators as deco
import httpx

__doc__ = "发送 土味情话 获取"


async def get_Tuwei():
    url = "https://v2.alapi.cn/api/qinghua"
    payload = "token=1jfSWghgtebOjpQi&format=json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': "application/x-www-form-urlencoded"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=payload, headers=headers, timeout=10)
            text_to_dic = json.loads(response.text)

            return text_to_dic['data']['content']
        except:
            return None


# 对话式发送
# search_handler1 = SessionHandler(
#     ignore_botself,
#     equal_content("知乎热搜"),
#     single_user=True,
#     expiration=1 * 30,
# ).receive_group_msg().receive_friend_msg()


# @search_handler1.handle
# def _():
#     data, content = get_HotList("zhihu")
#     session.send_text(content+"30s内回复数字查看对应知乎热搜！")

#     while True:
#         word = session.pop("word", wait=True, timeout=30)

#         if str(word).isdigit():
#             session.send_text(data[int(word)]['link'])
#         else:
#             del data, content
#             gc.collect()
#             logger.info('查询知乎热搜结束')
#             search_handler1.finish()


@deco.ignore_botself
@deco.equal_content("土味情话")
async def receive_group_msg(_):
    zhihu = await get_Tuwei()
    if zhihu == None:
        await S.atext("网络响应超时，请稍后重试！")
    else:
        await S.atext(zhihu)
        del zhihu
        gc.collect()


@deco.ignore_botself
@deco.equal_content("土味情话")
async def receive_friend_msg(_):
    zhihu = await get_Tuwei()
    if zhihu == None:
        await S.atext("网络响应超时，请稍后重试！")
    else:
        await S.atext(zhihu)
        del zhihu
        gc.collect()
