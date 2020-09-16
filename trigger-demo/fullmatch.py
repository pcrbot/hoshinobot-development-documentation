from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('fullmatch-demo')

@sv.on_fullmatch('你好')
async def demo_fun_0(bot, ev:CQEvent):
    await bot.send(ev, '你好！')
    
@sv.on_fullmatch(('老婆', '老公'), only_to_me=True)
async def demo_fun_1(bot, ev):
    await bot.send(ev, '???')
