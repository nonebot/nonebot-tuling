import nonebot

from demo import config

nonebot.init(config)

if __name__ == '__main__':
    nonebot.load_plugin('nonebot_tuling')
    nonebot.run()
