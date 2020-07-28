# HoshinoBot(v2) 插件开发指南（社区版）

[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot) 是一款 QQ 群应答机器人框架，在 [nonebot](https://github.com/richardchien/nonebot) 框架的基础上进一步提供了更优秀的封装，大大方便了开发者和使用者。

本文档为社区文档，是对官方文档的做出一些更方便初学者阅读的说明。

## 部署 HoshinoBot

编写中……

## 快速上手

HoshinoBot 部署完成后，我们可以在 `hoshino/modules` 目录下创建一个新的文件夹，作为功能模块

```shell
cd hoshino/modules
mkdir my_module
```

在这个模块下，创建一个新的插件文件

```shell
cd my_module
vi hello.py
```

编写一点内容

```python
from hoshino import Service

sv = Service('hello')

@sv.on_fullmatch('你好')
async def hello(bot, ev):
    await bot.send(ev, '你好，世界！')
```

然后编辑 `HoshinoBot/config/__bot__.py` 来启用这个新的模块

```python
# 前略
MODULES_ON = {
    # 前略
    'my_module',  # 添加新的功能模块名称到这里
}
```

现在，重新启动 hoshino，对机器人说一声 `你好` 吧！

## 插件结构介绍

编写中……

## 高级功能

HoshinoBot 封装了很多高级用法，使得编写插件非常简单

触发器：多种消息触发方式

服务层：分群、分权限的管理插件

资源管理：轻松管理图片、语言资源，简单地合成图片并发送

编写中……

## 学习资料

编写中……
