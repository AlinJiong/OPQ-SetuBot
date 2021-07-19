from botoy import FriendMsg, GroupMsg, S
from botoy import decorators as deco
from loguru import logger
from .setu import Setu
from .model import GetSetuConfig
import re

setuPattern = '来(.*?)[点丶、个份张幅](.*?)的?(|[rR]18)[色瑟涩䔼😍🐍][图圖🤮]'
__doc__ = """色图姬"""


def check_and_processing(ctx: [GroupMsg, FriendMsg]) -> GetSetuConfig:
    send = S.bind(ctx)
    info = ctx._match
    config = GetSetuConfig()
    digitalConversionDict = {'一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                             '十': 10}
    if info[1] != '':
        if info[1] in digitalConversionDict.keys():
            config.toGetNum = int(digitalConversionDict[info[1]])
        else:
            if info[1].isdigit():
                config.toGetNum = int(info[1])
            else:
                send.text('能不能用阿拉伯数字?')
                # logger.info('非数字')
                return
    else:  # 未指定数量,默认1
        config.toGetNum = 1
    config.tags = [i for i in list(set(re.split(r'[,， ]', info[2]))) if i != '']
    if info[3] != '':  # r18关键字
        config.level = 1
    return config


@deco.on_regexp(setuPattern)
@deco.ignore_botself
@deco.queued_up
def receive_group_msg(ctx: GroupMsg):
    if config := check_and_processing(ctx):
        Setu(ctx, config).main()


@deco.on_regexp(setuPattern)
@deco.ignore_botself
@deco.queued_up
def receive_friend_msg(ctx: FriendMsg):
    if config := check_and_processing(ctx):
        Setu(ctx, config).main()
