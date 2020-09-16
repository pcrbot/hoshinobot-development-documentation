# 消息触发器

本文介绍的是封装在`hoshino.Service`中的触发器类型，如果您要查看nonebot原生的触发器，可以前往nonebot的[官方文档](https://docs.nonebot.dev/)进行查阅，本文中可能会给出一些简单的介绍，但不会作出详细说明。HoshinoBot 的触发器是通用的程序入口，通过内部维护的前缀树实现高效率的消息预处理。

本教程附带示范代码，如果想要尝试，请将本项目中的`trigger-demo`目录拷贝至到`hoshino/modules/`目录下，并在`hoshino/config/__bot__.py`的`MODULES_ON`中仿照格式添加`'trigger-demo'`。

## 触发流程

HoshinoBot对消息的触发方法在文件`msghandler.py`中使用nonebot自带的装饰器`@message_preprocessor`来预处理，当接收到消息后，会按照顺序进行如下的步骤：

1. 检查是否是群聊消息，如果否则过滤
2. 检查是否是指令，如果否则过滤，如果是则输出日志显示指令已被触发
3. 检查消息接受条件是否符合，即是否是仅对自己发送
4. 检查权限是否允许
5. 调用对应方法

因此，当您在控制台看到日志显示指令被触发，而实际并未响应时，应当依照此顺序检查错误的环节。

## 优先级

**注意本条目内容由测试而来，优先级排序实际上只是优先级数值只用于相互对比（越大优先级越高），并无可量化的含义。**

**本条目仅用来排查错误，请勿利用本条目特性来开发**。

使用已`on_*`开头的装饰器来添加命令，如果有一条消息有多个匹配指令，会按照优先级来触发。同一优先级会先按照命令匹配程度来触发，如果命令匹配程度一致，则按照命令注册的先后顺序（即在代码中的先后顺序）触发。

相同优先级的示例代码——`priority_0.py`

```python
from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('priority-demo-0')
    
@sv.on_prefix('优先级0')
async def demo_fun_0(bot, ev:CQEvent):
    await bot.send(ev, '触发了on_prefixh呦~~~')

@sv.on_fullmatch('优先级0测试')
async def demo_fun_1(bot, ev:CQEvent):
    await bot.send(ev, '触发了on_fullmatch呦~~~')

```

当发送指令【优先级测试】时，由于触发器`on_fullmatch`和`on_prefix`优先级相同，但是`on_fullmatch`匹配度更高，因此会优先触发`on_fullmatch`，即便调换两个函数的顺序，也会触发`on_fullmatch`。

如果将全字匹配的条件改为“优先级”三个字，则会按照导入的先后顺序触发。



不同优先级的示例代码——`priority_1.py`

```python
from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('priority-demo-1')

@sv.on_keyword('优先级1')
async def demo_fun_0(bot, ev:CQEvent):
    await bot.send(ev, '触发了on_keyword呦~~~')


@sv.on_fullmatch('优先级1')
async def demo_fun_1(bot, ev:CQEvent):
    await bot.send(ev, '触发了on_fullmatch呦~~~')

```

由于`on_fullmatch`的优先级高于`on_keyword`，因此虽然关键词触发的方法更靠前，但是此时只会触发`on_fullmatch`。

推荐您在选择触发器时，先选择低优先级的触发器来完成（如果可以满足需求），以免与其他插件的指令产生冲突，当您确定要使用`on_prefix`触发器时，您的触发关键词应当注意规避现有插件的指令、群聊经常出现的词、其他插件可能会用到的词。

## 触发器与函数方法

*消息触发器*封装于[服务层](./service.md)中，使用服务提供的`on_*`装饰器作为入口，后跟方法，一个触发器只能对应一个函数方法，但是一个函数方法可以有多个触发器作为入口。

多匹配的实例代码——`mulmatch.py`

```python
from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('mulmatch-demo')

@sv.on_prefix('之后')
@sv.on_suffix('之前')
async def demo_fun_0(bot, ev:CQEvent):
    msg = ev.message.extract_plain_text()
    await bot.send(ev, f'提取到了的文本内容是：\n{msg}')

```
在群聊中发送”XXX是谁“或”谁是XXX“，均会触发相关函数。此种情况仍受到优先级约束。


## HoshinoBot触发器种类

以下触发器均为`Service`类中封装的方法。由于原生HoshinoBot 过滤了群聊以外的消息，因此本页所示触发器均为群聊消息有效，如果需私聊指令，可以考虑：

1. 使用nonebot原生触发器`on_command`
2. 修改`msghandler.py`，使得其不过滤非群聊消息

### 全字匹配

装饰器：`on_fullmatch`

优先级：999

触发条件：当接收到的消息与触发词完全相同时触发。

原型：

```python
def on_fullmatch(self, word, only_to_me=False) -> Callable:
    #...
```

参数与缺省值：

1. `word`，全字匹配的条件，可以使用元组配置多个。
2. `only_to_me`，指令是否需要@机器人，缺省值为False，即不@也可触发。

用法示例——`fullmatch.py`

```python
from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('fullmatch-demo')

@sv.on_fullmatch('你好')
async def demo_fun_0(bot, ev:CQEvent):
    await bot.send(ev, '你好！')
    
@sv.on_fullmatch(('老婆', '老公'), only_to_me=True)
async def demo_fun_1(bot, ev):
    await bot.send(ev, '???')

```


### 前缀触发器

装饰器：`on_prefix`

优先级：999
触发条件：当接收到的消息以触发词开头时触发。当使用`CQEvent.message.extract_plain_text()`提取消息内容时将不会包含前缀关键词。

原型：

```python
def on_prefix(self, prefix, only_to_me=False) -> Callable:
    # ...
```

参数与缺省值：

1. `prefix`，前缀触发的关键词，可以使用元组或列表配置多个（使用列表时最终也会转换为元组）。
2. `only_to_me`，指令是否需要@机器人，缺省值为False，即不@也可触发。

用法示例——`prefix.py`

```python
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

```

### 后缀触发器

装饰器：`on_suffix`

优先级：22

触发条件：于`on_prefix`类似，当接收到的消息以触发词结尾时触发。使用`CQEvent.message.extract_plain_text()`提取消息内容时将不会包含后缀关键词。

原型：

```python
def on_suffix(self, suffix, only_to_me=False) -> Callable:
    # ...
```

参数与缺省值：

1. `suffix`，后缀触发的关键词，可以使用元组或列表配置多个（使用列表时最终也会转换为元组）。
2. `only_to_me`，指令是否需要@机器人，缺省值为False，即不@也可触发。

示例代码——`suffix.py`

```python
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

```

### 关键词触发器

装饰器：`on_keyword`

优先级：21
触发条件：当接受到的消息包含该命令时，即触发。

原型：

```python
def on_keyword(self, keywords, only_to_me=False, normalize=True) -> Callable:
    # ...
```

参数与缺省值：

1. `keywords`，触发的关键词，可以元组配置多个

2. `only_to_me`，指令是否需要@机器人，缺省值为False，即不@也可触发。

3. `normalize`，是否进行归一化处理，缺省值为True。如果处理，则会规范化Unicode字符、字母转换为小写、繁体转换为简体，详细方法可查看`trigger.py`中的`normalize_str()`函数。

   **仅此触发器包含normalize，HoshinoBot于2020年8月10日之后已支持自动[繁简转换](https://github.com/Ice-Cirno/HoshinoBot/commit/d91756408762f971b7f0491ffa06f78b7450cbc4)，其他触发器添加的简体指令可以直接用繁体触发**

用法示例——`keyword.py`

```python
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

```

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
