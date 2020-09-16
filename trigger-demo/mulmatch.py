from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('mulmatch-demo')

@sv.on_prefix('之后')
@sv.on_suffix('之前')
async def demo_fun(bot, ev:CQEvent):
    msg = ev.message.extract_plain_text()
    await bot.send(ev, f'提取到了的文本内容是：\n{msg}')
