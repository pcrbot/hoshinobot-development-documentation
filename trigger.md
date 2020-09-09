# 消息触发器

HoshinoBot 的*触发器*是通用的程序入口，通过内部维护的前缀树实现高效率的消息预处理。

*消息触发器*封装于[服务层](./service.md)中，使用服务提供的`on_*`装饰器作为入口。

*触发器*的第一个参数可以是字符串或字符串数组/元组，Hoshino 可以自动判断参数类型，无需担心类型错误

## 触发器种类

### 完全匹配触发器

`on_fullmatch`

当接收到的消息于触发词完全相同时触发。

```python
@sv.on_fullmatch(('你好', 'hello'), only_to_me=True)
async def hello(bot, ev: CQEvent):
    await bot.send(ev, '你好，请问我能怎么帮助你')
    return
```

### 前缀/后缀触发器

`on_prefix`, `on_suffix`

当接收到的消息以触发词开头/结尾时触发。这类触发器会截取前缀词/后缀词。在使用 `extract_plain_text` 提取消息体时，结果将不会包含触发词。

```python
@sv.on_suffix('是谁')
@sv.on_prefix('谁是')
async def hello(bot, ev: CQEvent):
    name = ev.message.extract_plain_text()
    await bot.send(ev, f'正在查询{name}的信息')
    # 后略
```

### 关键词触发器

`on_keyword`

当接收到的消息包含触发词时触发。

```python
@sv.on_keyword('granbluefantasy.jp')
async def qks_keyword(bot, ev: CQEvent):
    await bot.send(ev, '满世界都是骑空士的陷阱', at_sender=True)
    return
```

### 正则表达式触发器

`on_rex`

效率极低不推荐使用，当接收到的消息符合正则表达式时触发。

```python
@sv.on_rex(r'来[份点张][色瑟涩]图')
async def sleep(bot, ev: CQEvent):
    await bot.send(ev, '没有！', at_sender=True)
    return
```

### 其他 nonebot 原生触发器

`on_message` 捕获所有消息，不推荐使用；  
`on_command` 以第一个单词作为触发词，不符合中文习惯，不推荐使用；  
`on_natural_language` 效率极低不推荐使用。

具体使用方法与 nonebot 相同，此处不再赘述。

## 触发器参数

`only_to_me` 参数类型 `bool`，只有当 bot 被使用 `@` 提及时才会触发，默认值 `False`

## 消息处理

具体使用方法与 nonebot 相同。

<!-- 详细说明以后再写，咕咕咕 -->
