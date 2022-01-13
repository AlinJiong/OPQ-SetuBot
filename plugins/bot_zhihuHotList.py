from botoy import decorators
import requests
import json
from botoy import FriendMsg, GroupMsg, S, jconfig, logger
from botoy.decorators import equal_content, ignore_botself
from botoy.session import SessionHandler, ctx, session
import gc
from botoy import async_decorators as deco
import httpx

__doc__ = "发送 知乎热搜 获取热搜信息"


async def get_HotList(choice: str = 'zhihu'):
    "获取知乎热搜"
    url = "https://v2.alapi.cn/api/tophub/get"
    payload = "token=EFolx1cxAdqqSWqy&type=" + choice
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload, headers=headers)
        text_to_dic = json.loads(response.text)
        data = text_to_dic['data']['list']

        content = "#实时知乎热搜#\n"

        for i in range(0, 10):
            content += str(i)+'.' + data[i]['title'] + \
                '\n' + data[i]['link'] + '\n'

        return content


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
    zhihu = get_HotList()
    await S.atext(zhihu)
    del zhihu
    gc.collect()


@deco.ignore_botself
@deco.equal_content("知乎热搜")
async def receive_friend_msg(_):
    zhihu = get_HotList()
    await S.atext(zhihu)
    del zhihu
    gc.collect()
