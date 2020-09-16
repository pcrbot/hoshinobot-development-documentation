from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('priority-demo-1')

@sv.on_keyword('优先级1')
async def demo_fun_0(bot, ev:CQEvent):
    await bot.send(ev, '触发了on_keyword呦~~~')


@sv.on_fullmatch('优先级1')
async def demo_fun_1(bot, ev:CQEvent):
    await bot.send(ev, '触发了on_fullmatch呦~~~')
