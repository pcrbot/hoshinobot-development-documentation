# 定时任务

这是一个简易的演示，其使用可以有多种扩展。
当然如果你已经熟练掌握了APScheduler那么你并不需要这个文档

## 定时发送
```
sv = Service('hello')

@sv.scheduled_job('cron', minute='*/1')
async def hello():
    await sv.broadcast('hello,world','hello')
broadcast需要的参数是 消息'hello,world' 可选参数是 标签'hello'、发送间隔 不小于等于0的任意数，单位是秒 
```
这样一个简单的定时发送任务便完成了，在启动你的机器人之后将会每分钟都发送一次hello,world。
更加详细的定时任务可以了解APScheduler。
- [中文](https://www.jianshu.com/p/4f5305e220f0) 翻译文档
- [官方](https://apscheduler.readthedocs.io/en/latest/) 文档

## 进阶
```
def hello():
    print('hello,world')

@sv.scheduled_job('cron', hour='12')
async def test():
    hello()
```

这样可以用于执行hoshino外部的任务也可以用于执行内部任务，任凭发挥。
