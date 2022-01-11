import os
import random
import re
import time

from botoy import Action, GroupMsg, jconfig
from botoy.decorators import from_botself, in_content
from botoy import async_decorators as deco

__doc__ = "根据 关键字 踢出群聊"
patten = "(.*lunwen.*|.*论文.*|.*论wen.*|.*lun文.*)"


@deco.ignore_botself
@deco.on_regexp(patten)
async def receive_group_msg(ctx: GroupMsg):
    
    Action(ctx.CurrentQQ).revokeGroupMsg(
        group=ctx.FromGroupId,
        msgSeq=ctx.MsgSeq,
        msgRandom=ctx.MsgRandom,
    )
    Action(ctx.CurrentQQ).driveUserAway(ctx.FromGroupId, ctx.FromUserId)
