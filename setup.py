# encoding: utf-8
'''
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/6/12 1:39 下午
@desc:
'''

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="feishu-sdk",
    version="1.0.0",
    author="liyao",
    author_email="liyao2598330@126.com",
    description="a Feishu Third-party libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liyao2598330/feishu-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
