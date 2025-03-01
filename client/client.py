#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PlaywrightAPI クライアント互換モジュール

このモジュールは旧client.pyとの互換性を提供します。
新しい実装ではclient.api.PlayScraperClientの使用を推奨します。
"""

from .api import PlayScraperClient
from .cli import main

# 互換性のためにここでもクライアントクラスをエクスポート
__all__ = ["PlayScraperClient", "main"]
