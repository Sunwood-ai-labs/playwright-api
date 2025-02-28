#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements_client.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="playscraper-api-client",
    version="1.0.0",
    author="Maki",
    author_email="sunwood.ai.labs@gmail.com",
    description="PlayScraperAPIのクライアントライブラリ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sunwood-ai-labs/playwright-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "playscraper-api=client:main",
        ],
    },
)
