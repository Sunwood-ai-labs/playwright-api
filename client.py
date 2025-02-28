#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PlayScraperAPI クライアント（レガシー）

このファイルは後方互換性のために維持されています。
新しい実装では `from client import PlayScraperClient` を使用してください。
"""

# 新しいクライアントパッケージをインポート
from client import PlayScraperClient, main

if __name__ == "__main__":
    import sys
    sys.exit(main())
