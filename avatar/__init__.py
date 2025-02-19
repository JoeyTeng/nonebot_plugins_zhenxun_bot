import re
from typing import Type

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message, PrivateMessageEvent
from nonebot.matcher import Matcher
from nonebot.params import ArgStr, CommandArg
from nonebot.typing import T_State
from services.log import logger

from .data_source import get_image

__zx_plugin_name__ = "头像相关表情生成"
__plugin_usage__ = """
usage：
    摸/搓/撕/丢/爬/亲/贴/精神支柱 {qq/@user/自己/图片}

    参数解释:
        qq: qq号
        @user: @某个人
        自己: 生成自己的图片
        图片: 自定义图片（不是方形会被非等比缩放）
""".strip()
__plugin_des__ = "生成各种表情"
__plugin_cmd__ = [
    "摸",
    "搓",
    "撕",
    "丢",
    "爬",
    "亲",
    "亲我",
    "贴",
    "贴我",
    "精神支柱",
]
__plugin_version__ = 0.2
__plugin_author__ = ["梦璃雨落", "AkashiCoin"]
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": [
        "头像相关表情生成",
        "头像表情",
        "头像",
        "摸",
        "搓",
        "撕",
        "丢",
        "爬",
        "亲",
        "亲我",
        "贴",
        "贴我",
        "精神支柱",
    ],
}


petpet = on_command("摸", aliases={"rua"}, priority=5, block=True)
cuo = on_command("搓", priority=5, block=True)
tear = on_command("撕", priority=5, block=True)
throw = on_command("丢", priority=5, block=True)
crawl = on_command("爬", priority=4, block=True)
kiss = on_command("亲", priority=5, block=True)
kiss_me = on_command("亲我", priority=4, block=True)
rub = on_command("贴", priority=5, block=True)
rub_me = on_command("贴我", priority=4, block=True)
support = on_command("精神支柱", priority=5, block=True)


async def handle(
    matcher: Type[Matcher],
    event: Event,
    command: str,
    type: str,
    reverse: bool = False,
    arg: Message = CommandArg(),
):
    msg = event.get_message()
    msg_text = arg.extract_plain_text().strip()
    self_id = event.user_id
    user_id = ""

    for msg_seg in msg:
        if msg_seg.type == "at":
            user_id = msg_seg.data["qq"]
            break

    if not user_id:
        msg_content = re.sub(command, "", msg_text).strip()
        if msg_content.isdigit():
            user_id = msg_content
        elif msg_content == "自己":
            user_id = event.user_id

    img_url = ""
    if not user_id:
        for msg_seg in msg:
            if msg_seg.type == "image":
                img_url = msg_seg.data["url"]
                break

    image = None
    if user_id:
        image = await get_image(type, self_id, user_id=user_id, reverse=reverse)
    elif img_url:
        image = await get_image(type, self_id, img_url=img_url, reverse=reverse)
    else:
        matcher.block = False
        await matcher.finish()

    matcher.block = True
    if image:
        await matcher.send(message=image)
        logger.info(
            f"USER {event.user_id} GROUP {event.group_id if not isinstance(event, PrivateMessageEvent) else ''} "
            f"感觉这张图太好好看了，于是恶搞了一下了"
        )
        await matcher.finish()
    else:
        await matcher.finish(message="出错了，请稍后再试")


@petpet.handle()
async def _(
    bot: Bot,
    event: Event,
    state: T_State,
    arg: Message = CommandArg(),
):
    await handle(petpet, event, "摸", "petpet", arg=arg)


@cuo.handle()
async def _(
    bot: Bot,
    event: Event,
    state: T_State,
    arg: Message = CommandArg(),
):
    await handle(cuo, event, "搓", "cuo", arg=arg)


@tear.handle()
async def _(
    bot: Bot,
    event: Event,
    state: T_State,
    arg: Message = CommandArg(),
):
    await handle(tear, event, "撕", "tear", arg=arg)


@throw.handle()
async def _(
    bot: Bot,
    event: Event,
    state: T_State,
    arg: Message = CommandArg(),
):
    await handle(throw, event, "丢", "throw", arg=arg)


@crawl.handle()
async def _(
    bot: Bot,
    event: Event,
    state: T_State,
    arg: Message = CommandArg(),
):
    await handle(crawl, event, "爬", "crawl", arg=arg)


@kiss.handle()
async def _(
    bot: Bot,
    event: Event,
    state: T_State,
    arg: Message = CommandArg(),
):
    await handle(kiss, event, "亲", "kiss", arg=arg)


@kiss_me.handle()
async def _(
    bot: Bot,
    event: Event,
    state: T_State,
    arg: Message = CommandArg(),
):
    await handle(kiss, event, "亲我", "kiss", reverse=True, arg=arg)


@rub.handle()
async def _(
    bot: Bot,
    event: Event,
    state: T_State,
    arg: Message = CommandArg(),
):
    await handle(rub, event, "贴", "rub", arg=arg)


@rub_me.handle()
async def _(
    bot: Bot,
    event: Event,
    state: T_State,
    arg: Message = CommandArg(),
):
    await handle(rub, event, "贴我", "rub", reverse=True, arg=arg)


@support.handle()
async def _(
    bot: Bot,
    event: Event,
    state: T_State,
    arg: Message = CommandArg(),
):
    await handle(support, event, "精神支柱", "support", arg=arg)
