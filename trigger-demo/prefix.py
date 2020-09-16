from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('prefix-demo')

@sv.on_prefix('内容提取')
async def demo_fun_0(bot, ev:CQEvent):
    msg = ev.message.extract_plain_text()
    await bot.send(ev, f'prefix提取到了的文本内容是：\n{msg}')

@sv.on_prefix(['提取', '试试提取'], only_to_me=True)
async def demo_fun_1(bot, ev:CQEvent):
    msg = ev.message.extract_plain_text()
    await bot.send(ev, f'prefix提取到了的文本内容是：\n{msg}')
