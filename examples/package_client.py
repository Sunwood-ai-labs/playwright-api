#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PlayScraperAPI パッケージを使用したサンプルスクリプト

このサンプルは、インストールしたplayscraper-api-clientパッケージを使用して
スクレイピングを行う方法を示しています。
"""

import json
import asyncio
import sys
from loguru import logger

# パッケージからのインポート
# -e オプションでインストールした場合は直接clientからインポートします
from client import PlayScraperClient

# ロガーの設定
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    level="INFO"
)


async def simple_async_example():
    """
    非同期クライアントを使用した簡単な例
    """
    # クライアントの初期化
    client = PlayScraperClient(base_url="http://localhost:8001")
    
    try:
        # APIステータスの確認
        status = await client.check_status_async()
        logger.info(f"API状態: {status['status']} - {status['message']}")
        
        # セレクタの定義
        selectors = {
            "title": "h1",
            "description": {
                "type": "css",
                "value": "meta[name='description']",
                "transform": "attribute:content",
                "optional": True
            },
            "links": {
                "type": "css",
                "value": "a",
                "transform": "attribute:href",
                "optional": True,
                "multiple": True,
                "limit": 5  # 最初の5つのリンクのみを取得
            }
        }
        
        # スクレイピングの実行
        result = await client.start_scraping_async(
            url="https://docs.pydantic.dev",
            selectors=selectors,
            save_html_file=True,
            html_output_dir="output/html_files"
        )
        
        # タスクIDの取得
        task_id = result["task_id"]
        logger.info(f"タスクID: {task_id}")
        
        # タスクの完了を待機
        data = await client.wait_for_completion_async(task_id)
        
        # 結果の表示
        logger.info("\n===== スクレイピング結果 =====")
        logger.info(f"URL: {data['result']['url']}")
        logger.info("\n--- 抽出データ ---")
        for key, value in data['result']['data'].items():
            logger.info(f"{key}: {value}")
        
        # HTMLファイルが保存された場合
        if "html_file" in data["result"]:
            logger.success(f"\nHTMLファイルが保存されました: {data['result']['html_file']}")
        
        # 結果をJSONファイルに保存
        with open("package_example_result.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.success("\n結果をpackage_example_result.jsonに保存しました")

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
    finally:
        # 必ず非同期セッションをクローズする
        await client.close_async_sessions()


def sync_example():
    """
    同期クライアントを使用した簡単な例
    """
    # クライアントの初期化
    client = PlayScraperClient(base_url="http://localhost:8001")
    
    # APIステータスの確認
    status = client.check_status()
    logger.info(f"API状態: {status['status']} - {status['message']}")
    
    # アクションの定義（必ずdict形式で定義する）
    actions = [
        {
            "type": "wait_for_selector",
            "selector": "body",
            "timeout": 5000  # 5秒待機
        },
        {
            "type": "click",
            "selector": "a[href='/docs/intro']"  # ドキュメントリンクをクリック
        }
    ]
    
    # セレクタの定義
    selectors = {
        "title": "h1",
        "content": {
            "type": "css",
            "value": "main .container",
            "transform": "text",
            "optional": True
        }
    }
    
    # スクレイピングの実行
    try:
        result = client.start_scraping(
            url="https://playwright.dev",
            selectors=selectors,
            actions=actions
        )
        
        # タスクIDの取得
        task_id = result["task_id"]
        logger.info(f"タスクID: {task_id}")
        
        # タスクの完了を待機
        data = client.wait_for_completion(task_id)
        
        # 結果の表示
        logger.info("\n===== スクレイピング結果 =====")
        logger.info(f"URL: {data['result']['url']}")
        logger.info("\n--- 抽出データ ---")
        for key, value in data['result']['data'].items():
            logger.info(f"{key}: {value}")
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")


# 同期的に実行する - 同期例と非同期例を別々に実行する
if __name__ == "__main__":
    # 非同期例を実行（単独で実行）
    logger.info("=== 非同期クライアント例 ===")
    asyncio.run(simple_async_example())
    
    # 同期例を実行
    logger.info("\n\n=== 同期クライアント例 ===")
    sync_example()
