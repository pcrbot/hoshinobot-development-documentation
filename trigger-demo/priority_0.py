from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('priority-demo-0')
    
@sv.on_prefix('优先级0')
async def demo_fun_0(bot, ev:CQEvent):
    await bot.send(ev, '触发了on_prefixh呦~~~')

@sv.on_fullmatch('优先级0测试')
async def demo_fun_1(bot, ev:CQEvent):
    await bot.send(ev, '触发了on_fullmatch呦~~~')
