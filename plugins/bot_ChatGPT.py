# -*- coding:UTF-8 -*-
# ChatGPTBot
# Author:AlinJiong
# Time: 2022/12/22 16:45

from botoy.parser import group as gp
from botoy import Botoy, GroupMsg
from botoy import GroupMsg, Action, S, Botoy
from botoy import decorators as deco
from botoy.collection import MsgTypes
from botoy.decorators import these_msgtypes, from_these_groups
from botoy.contrib import plugin_receiver
import ast
import requests
from urllib import parse
import json
import threading
import time

MyBotName = '@' + '摸鱼提醒小助手' + ' '  # 在这里输入你的Bot的昵称
locka = threading.Lock()


@plugin_receiver.group
@deco.ignore_botself
@from_these_groups(953219612, 773933325)  # 这里填入监听的群聊
@these_msgtypes(MsgTypes.AtMsg)
def main(ctx=GroupMsg):
    if MyBotName in ctx.Content.strip():
        MsgPre = ast.literal_eval(ctx.Content)
        Msg = MsgPre.get('Content')
        if Msg.find(MyBotName) == 0:
            qa = Msg.replace(MyBotName, '')
            print(qa)
            try:
                locka.acquire()
                print('获得锁')
                if len(qa) > 2:  # 这里是为了防止有人简单回复你好浪费API免费额度，如果有需要可以自行修改最短长度
                    res = requests.get(
                        url='http://chat.h2ai.cn/api/trilateral/openAi/completions?prompt=' +
                            qa+'&openaiId=123910453021889130720167012221015126174233152702504',
                        timeout=30)
                    if res.status_code != 200:
                        S.bind(ctx).text("调用超时，请重试！", 'utf-8')
                    else:
                        txt = json.loads(res.text)
                        try:
                            ans = txt['data']['choices'][0]['text'].replace(
                                '<br/>', ' ')
                            S.bind(ctx).text(ans, 'utf-8')
                        except:
                            pass
                else:
                    S.bind(ctx).text("已禁止简单问题", 'utf-8')
                    Action(ctx.CurrentQQ).shutUserUp(
                        groupID=ctx.FromGroupId,
                        userid=ctx.FromUserId,
                        ShutTime=1
                    )
            finally:
                time.sleep(10)
                print('释放锁')
                locka.release()
