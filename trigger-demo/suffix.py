from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('suffix-demo')

@sv.on_suffix('前面')
async def demo_fun_0(bot, ev:CQEvent):
    msg = ev.message.extract_plain_text()
    await bot.send(ev, f'suffix提取到了的文本内容是：\n{msg}')

@sv.on_suffix(('之前', '以前'), only_to_me=True)
async def demo_fun_1(bot, ev:CQEvent):
    msg = ev.message.extract_plain_text()
    await bot.send(ev, f'suffix提取到了的文本内容是：\n{msg}')
