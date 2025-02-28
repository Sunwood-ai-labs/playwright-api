#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PlayScraperAPI 非同期クライアント例

非同期APIを使用したクライアント例です。
"""

import asyncio
from client import PlayScraperClient

async def main():
    """非同期メイン関数"""
    # クライアントの初期化
    client = PlayScraperClient("http://localhost:8001")
    
    # APIの状態確認
    status = await client.check_status_async()
    print(f"API状態: {status['status']} - {status['message']}")
    
    # スクレイピング実行
    url = "https://example.com"
    selectors = {
        "title": "h1",
        "description": "p"
    }
    
    # スクレイピングタスク開始
    print(f"スクレイピング開始: {url}")
    task = await client.start_scraping_async(url, selectors)
    task_id = task["task_id"]
    
    # タスク完了を待機
    result = await client.wait_for_completion_async(task_id)
    
    # 結果の出力
    print("\nスクレイピング結果:")
    print(f"URL: {result['result']['url']}")
    
    if result['result']['data']:
        print("抽出データ:")
        for key, value in result['result']['data'].items():
            print(f"  {key}: {value}")
    else:
        print("抽出データなし")
    
    # 非同期セッションをクローズ
    await client.close_async_sessions()
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))
