import asyncio
import json
from typing import List, Optional, Union, Iterable

import aiohttp
from aiocqhttp.message import Message, escape
from nonebot import get_bot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
from nonebot.helpers import context_id, render_expression
from nonebot.log import logger
from nonebot.session import BaseSession

__all__ = []

assert get_bot(), 'NoneBot is not initialized yet'

bot = get_bot()
api_keys = getattr(bot.config, 'TULING_API_KEY', None)
assert api_keys, 'TULING_API_KEY must be set in configurations'
if not isinstance(api_keys, Iterable) or isinstance(api_keys, str):
    api_keys = [api_keys]

EXPR_I_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)
expr_dont_understand = getattr(bot.config, 'TULING_EXPR_I_DONT_UNDERSTAND',
                               EXPR_I_DONT_UNDERSTAND)


@on_command('_tuling')
async def _(session: CommandSession):
    message = session.get('message')

    tmp_msg = Message(message)
    text = tmp_msg.extract_plain_text()
    images = [s.data['url'] for s in tmp_msg
              if s.type == 'image' and 'url' in s.data]

    # call tuling api
    replies = await call_tuling_api(session, text, images)
    logger.debug(f'Got tuling\'s replies: {replies}')

    if replies:
        for reply in replies:
            await session.send(escape(reply))
            await asyncio.sleep(0.8)
    else:
        await session.send(render_expression(expr_dont_understand))


@on_natural_language
async def _(session: NLPSession):
    return NLPResult(60.0, '_tuling', {'message': session.msg})


async def call_tuling_api(
        session: BaseSession,
        text: Optional[str],
        image: Optional[Union[List[str], str]]) -> List[str]:
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    for api_key in api_keys:
        payload = {
            'reqType': 0,
            'perception': {},
            'userInfo': {
                'apiKey': api_key,
                'userId': context_id(session.ctx, use_hash=True)
            }
        }

        group_unique_id = context_id(session.ctx, mode='group', use_hash=True)
        if group_unique_id:
            payload['userInfo']['groupId'] = group_unique_id

        if image and not isinstance(image, str):
            image = image[0]

        if text:
            payload['perception']['inputText'] = {'text': text}
            payload['reqType'] = 0
        elif image:
            payload['perception']['inputImage'] = {'url': image}
            payload['reqType'] = 1
        else:
            return []

        try:
            resp_payload = None
            async with aiohttp.ClientSession() as sess:
                async with sess.post(url, json=payload) as resp:
                    if resp.status == 200:
                        resp_payload = json.loads(await resp.text())

            if resp_payload['intent']['code'] == 4003:  # 当日请求超限
                continue
            if resp_payload['results']:
                return_list = []
                for result in resp_payload['results']:
                    res_type = result.get('resultType')
                    if res_type in ('text', 'url'):
                        return_list.append(result['values'][res_type])
                return return_list
        except (aiohttp.ClientError, TypeError, KeyError):
            pass
    return []
