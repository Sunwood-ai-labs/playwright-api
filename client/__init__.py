"""
PlayScraperAPI クライアントパッケージ

このパッケージはPlayScraperAPIを簡単に利用するためのクライアントライブラリを提供します。
"""

from .api import PlayScraperClient
from .cli import main as cli_main

__version__ = "1.0.0"

# コマンドライン実行用のエントリーポイント
def main():
    """コマンドラインエントリーポイント"""
    import sys
    sys.exit(cli_main())

# クライアントをトップレベルで直接インポートできるようにする
__all__ = ["PlayScraperClient", "main", "cli_main"]
