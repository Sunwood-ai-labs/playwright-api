#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PlaywrightAPI 簡易クライアント例

新しいクライアントパッケージを使用した簡単な例です。
"""

from client import PlayScraperClient

def main():
    """メイン関数"""
    # クライアントの初期化
    client = PlayScraperClient("http://localhost:8001")
    
    # APIの状態確認
    status = client.check_status()
    print(f"API状態: {status['status']} - {status['message']}")
    
    # スクレイピング実行
    url = "https://example.com"
    selectors = {
        "title": "h1",
        "description": "p"
    }
    
    # スクレイピングタスク開始
    print(f"スクレイピング開始: {url}")
    task = client.start_scraping(url, selectors)
    task_id = task["task_id"]
    
    # タスク完了を待機
    result = client.wait_for_completion(task_id)
    
    # 結果の出力
    print("\nスクレイピング結果:")
    print(f"URL: {result['result']['url']}")
    
    if result['result']['data']:
        print("抽出データ:")
        for key, value in result['result']['data'].items():
            print(f"  {key}: {value}")
    else:
        print("抽出データなし")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
