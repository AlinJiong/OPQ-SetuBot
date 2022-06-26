from botoy import decorators
import requests
import json
from botoy import FriendMsg, GroupMsg, S, jconfig, logger
from botoy.decorators import equal_content, ignore_botself
from botoy.session import SessionHandler, ctx, session
import gc
from botoy import async_decorators as deco
import httpx

__doc__ = "知乎热搜"


# async def get_HotList(choice: str = 'zhihu'):
#     "获取知乎热搜"
#     url = "https://v2.alapi.cn/api/tophub/get"
#     payload = "token=nZJjbVKX1guoU4I4&type=zhihu"
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
#         'Content-Type': "application/x-www-form-urlencoded"
#     }

#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.post(url, data=payload, headers=headers, timeout=10)
#             text_to_dic = json.loads(response.text)
#             data = text_to_dic['data']['list']

#             content = "#实时知乎热搜#\n"

#             for i in range(0, 10):
#                 content += str(i)+'.' + data[i]['title'] + \
#                     '\n' + data[i]['link'] + '\n'

#             return content
#         except:
#             return None

async def get_HotList():
    url = 'https://tenapi.cn/zhihuresou/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': "application/x-www-form-urlencoded"
    }
    try:
        res = requests.get(url=url, headers=headers, timeout=10)
        text_to_dic = json.loads(res.text)

        data = text_to_dic['list']

        print(data)
        content = "#实时知乎热搜#\n"

        for i in range(0, 10):
            content += str(i)+'.' + str(data[i]['name']) + \
                '\n' + str(data[i]['url']) + '\n'
        return content
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
@deco.equal_content("知乎热搜")
async def receive_group_msg(_):
    zhihu = await get_HotList()
    if zhihu == None:
        await S.atext("网络响应超时，请稍后重试！")
    else:
        await S.atext(zhihu)
        del zhihu
        gc.collect()


@deco.ignore_botself
@deco.equal_content("知乎热搜")
async def receive_friend_msg(_):
    zhihu = await get_HotList()
    if zhihu == None:
        await S.atext("网络响应超时，请稍后重试！")
    else:
        await S.atext(zhihu)
        del zhihu
        gc.collect()
