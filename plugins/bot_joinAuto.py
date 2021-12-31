from botoy import logger
import base64
import io
import random
import time
from threading import Lock
from typing import Tuple

from botoy import Action, EventMsg, GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, these_msgtypes
from botoy.parser import event as ep
from PIL import Image, ImageDraw, ImageFont

__doc__ = "加群申请自动同意"


def receive_events(ctx: EventMsg):
    join_request = ep.group_adminsysnotify(ctx)
    if join_request is None:
        return
    else:
        try:
            logger.info("有人申请入群同意！")
            Action(ctx.CurrentQQ).groupJoinAuth(join_request.Seq,
                                                join_request.GroupId, join_request.Who, True)
        except:
            pass
