from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nonebot-tuling',
    version='1.0.1',
    packages=find_packages(include=('nonebot_tuling', 'nonebot_tuling.*')),
    url='https://github.com/richardchien/nonebot-tuling',
    license='MIT License',
    author='Richard Chien',
    author_email='richardchienthebest@gmail.com',
    description='A NoneBot plugin that provides Tuling\'s chatting function',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['nonebot>=1.0.0', 'aiohttp~=3.5.1'],
)
