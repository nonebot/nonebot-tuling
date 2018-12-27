# nonebot-tuling

[![License](https://img.shields.io/github/license/richardchien/nonebot-tuling.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/nonebot-tuling.svg)](https://pypi.python.org/pypi/nonebot-tuling)

## 安装

```bash
pip install nonebot-tuling
```

## 配置

```python
from nonebot.default_config import *

TULING_API_KEY = '你的图灵机器人 API KEY'
```

## 使用

```python
import nonebot

from demo import config

nonebot.init(config)

if __name__ == '__main__':
    nonebot.load_plugin('nonebot_tuling')
    nonebot.run()
```
