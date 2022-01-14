import requests
import json
from botoy import FriendMsg, GroupMsg, S, jconfig, logger
from botoy.decorators import equal_content, ignore_botself
from botoy.session import SessionHandler, ctx, session
import gc
import httpx
from botoy.contrib import sync_run

__doc__ = "发送 微博热搜 获取信息"


async def get_HotList(choice: str = 'weibo'):
    "获取微博热搜"
    url = "https://v2.alapi.cn/api/tophub/get"
    payload = "token=EFolx1cxAdqqSWqy&type=" + choice
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': "application/x-www-form-urlencoded"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=payload, headers=headers, timeout=10)

            text_to_dic = json.loads(response.text)
            data = text_to_dic['data']['list']

            content = "#实时微博热搜#\n"

            for i in range(0, 10):
                content += str(i)+'.' + data[i]['title']+'\n'

            return data, content
        except:
            logger.info('获取微博热搜请求超时！')
            return None, None


search_handler = SessionHandler(
    ignore_botself,
    equal_content("微博热搜"),
    single_user=True,
    expiration=1 * 30,
).receive_group_msg().receive_friend_msg()


@search_handler.handle
def WbHostList():
    data, content = sync_run(get_HotList())
    if content == None:
        session.send_text("网络响应超时，请稍后重试！")
        search_handler.finish()

    session.send_text(content+"30s内回复数字查看对应微博热搜！")

    while True:
        word = session.pop("word", wait=True, timeout=30)

        if str(word).isdigit():
            session.send_text(data[int(word)]['link'])
        else:
            del data, content
            gc.collect()
            logger.info('查询微博热搜结束')
            search_handler.finish()
