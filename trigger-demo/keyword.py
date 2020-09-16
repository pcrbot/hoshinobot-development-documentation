from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('keyword-demo')

@sv.on_keyword('色图')
async def demo_fun_0(bot, ev:CQEvent):
    await bot.send(ev, '发点色图。--鲁迅')

@sv.on_keyword(('憨批', '憨憨'), only_to_me=True)
async def demo_fun_1(bot, ev:CQEvent):
    await bot.send(ev, '别骂辣别骂辣')

@sv.on_keyword('鏡華', normalize=False)
async def demo_fun_2(bot, ev:CQEvent):
    # 仅当繁体或日文汉字时触发
    await bot.send(ev, '叫我？')

@sv.on_keyword('小倉唯')
async def demo_fun_3(bot, ev:CQEvent):
    # 日本汉字、简体字、繁体字均触发
    await bot.send(ev, '叫我干嘛~')
