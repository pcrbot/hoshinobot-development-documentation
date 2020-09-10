# 消息触发器

本文介绍的是封装在`hoshino.Service`中的触发器类型，如果您要查看nonebot原生的触发器，可以前往nonebot的[官方文档](https://docs.nonebot.dev/)进行查阅，本文中可能会给出一些简单的介绍，但不会作出详细说明。HoshinoBot 的触发器是通用的程序入口，通过内部维护的前缀树实现高效率的消息预处理。

## 触发流程

HoshinoBot对消息的触发方法在文件`msghandler.py`中使用nonebot自带的装饰器`@message_preprocessor`来实现，当接受到消息后，会按照顺序进行如下的检查：

1. 检查是否是群聊消息，如果否则过滤
2. 检查是否是指令，如果否则过滤，如果是则输出日志显示指令已被触发
3. 检查消息接受条件是否符合，即是否是仅对自己发送
4. 检查权限是否允许
5. 调用对应方法

综上所述，当您在控制台看到日志显示指令被触发时而出现异常时，应当依照此顺序检查错误的环节。

## 优先级

**注意本条目内容由测试而来，优先级数值只用于相互对比（越大优先级越高），并无可量化的含义。**

**推荐您仅使用本条目来排查错误，而非利用本条目特性来开发**。

使用已`on_*`开头的装饰器来添加命令，如果有一条消息有多个匹配指令，会按照优先级来触发。如果有同一优先级，则会按照命令注册的先后顺序（即在代码中的先后顺序）触发。

相同优先级的实例代码：

```python
from hoshino import Service

sv = Service('demo-service')

sv.on_fullmatch('优先级测试')
async def demo_fullmatch(bot, ev):
    await bot.send(ev, '触发了on_fullmatch呦~~~')
    
sv.on_prefix('优先级')
async def demo_prefix(bot, ev):
    await bot.send(ev, '触发了on_prefixh呦~~~')

```

由于触发器`on_fullmatch`和`on_prefix`优先级相同，因此会优先触发`on_fullmatch`，如果调换两个函数的顺序，则会触发`on_prefix`。当两个冲突指令不在同一个文件时，依然遵循此原则，会按照包导入的顺序来触发。



不同优先级的实例代码：

```python
from hoshino import Service

sv = Service('demo-service')

sv.on_keyword('优先级')
async def demo_keyword(bot, ev):
    await bot.send(ev, '触发了on_keyword呦~~~')


sv.on_fullmatch('优先级测试')
async def demo_fullmatch(bot, ev):
    await bot.send(ev, '触发了on_fullmatch呦~~~')

```

由于`on_fullmatch`的优先级高于`on_keyword`，因此虽然关键词触发的方法更靠前，但是此时只会触发`on_fullmatch`。

推荐您在选择触发器时，先选择低优先级的触发器来完成（如果可以满足需求），以免与其他插件的指令产生冲突，当您确定要使用`on_prefix`触发器时，您的触发关键词应当注意规避现有插件的指令、群聊经常出现的词、其他插件可能会用到的词。

## 触发器与函数方法

*消息触发器*封装于[服务层](./service.md)中，使用服务提供的`on_*`装饰器作为入口，后跟方法，一个触发器只能对应一个函数方法，但是一个函数方法可以由多个触发器触发，例如：

```python
import Service

sv = Service('demo-service')

@sv.on_prefix('谁是')
@sv.on_suffix('是谁')
async def whois(bot, ev):
    await bot.send(ev, '你问的谁啊？我不知道啦~~')

```
在群聊中发送”XXX是谁“或”谁是XXX“，均会触发相关函数。此种情况仍受到优先级约束。


## HoshinoBot触发器种类

由于原生HoshinoBot 过滤了所有群消息，因此本页所实触发器均为群聊消息有效，如果需私聊指令，可以考虑：

1. 使用nonebot原生触发器`on_command`
2. 修改`msghandler.py`，使得其不过滤私聊消息

### 全字匹配

装饰器：`on_fullmatch()`

优先级：999

触发条件：当接收到的消息与触发词完全相同时触发。

原型：封装于服务层中，

```python
def on_fullmatch(self, word, only_to_me=False) -> Callable:
    #...
```

参数与缺省值：

1. `word`，全字匹配的条件，可以使用元组配置多个。
2. `only_to_me`，指令是否需要@机器人，缺省值为False，即不@也可触发。

用法实例1：

```python
from hoshino import Service

sv = Service('demo-service')

sv.on_fullmatch('你好')
async def demo_fun(bot, ev):
    await bot.send(ev, '你好！')
    
```

用法示例2：

```python
from hoshino import Service

sv = Service('demo-service')

sv.on_fullmatch(('你好','你坏'),only_to_me=True)
async def demo_fun(bot, ev):
    await bot.send(ev, '???')

```

### 前缀/后缀触发器

`on_prefix`, `on_suffix`

当接收到的消息以触发词开头/结尾时触发。这类触发器会截取前缀词/后缀词，提取消息体时不包含触发词。

### 关键词触发器

`on_keyword`

当接收到的消息包含触发词时触发。

### 正则表达式触发器

`on_rex`

效率极低不推荐使用，当接收到的消息符合正则表达式时触发。

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
