#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
複数ユーザーからのアクセスをシミュレーションするスクリプト

PlayScraperAPIに対して複数ユーザーからの同時アクセスをシミュレーションします。
各ユーザーは異なるURLにアクセスするか、同じURLに異なるセレクタでアクセスします。
"""

import asyncio
import argparse
import random
import time
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

from loguru import logger
from client.api import PlayScraperClient
from client.utils import load_json_file, setup_logger
from client.output import ResultHandler


# テスト用URLリスト（サンプル）
DEFAULT_URLS = [
    "https://codeium.com/windsurf",
    "https://github.com",
    "https://qiita.com",
    "https://zenn.dev",
    "https://news.ycombinator.com",
    "https://www.python.org",
    "https://fastapi.tiangolo.com",
    "https://playwright.dev",
    "https://docs.pydantic.dev",
]


async def simulate_user(
    user_id: str,
    client: PlayScraperClient,
    urls: List[str],
    selectors_file: Optional[str],
    save_output: bool,
    output_dir: str,
    random_delay: bool = True
) -> Dict[str, Any]:
    """
    1ユーザーのアクセスをシミュレートする

    Args:
        user_id: ユーザーID
        client: APIクライアント
        urls: アクセス対象のURLリスト
        selectors_file: セレクタファイルパス
        save_output: 出力を保存するかどうか
        output_dir: 出力ディレクトリ
        random_delay: ランダム遅延を入れるかどうか

    Returns:
        結果情報
    """
    # ランダム遅延（ユーザーのアクセスタイミングを分散させる）
    if random_delay:
        delay = random.uniform(0.1, 2.0)
        await asyncio.sleep(delay)
    
    # ランダムにURLを選択
    url = random.choice(urls)
    
    # セレクタの読み込み
    selectors = None
    if selectors_file:
        try:
            selectors = load_json_file(selectors_file)
        except Exception as e:
            logger.error(f"セレクタファイルの読み込みに失敗（ユーザー {user_id}）: {e}")
            return {"user_id": user_id, "status": "error", "message": str(e)}

    try:
        # API状態確認
        await client.check_status_async(user_id)
        
        # スクレイピングタスクの開始
        logger.info(f"スクレイピング開始（ユーザー {user_id}）: {url}")
        task = await client.start_scraping_async(
            url=url,
            selectors=selectors,
            save_html_file=save_output,
            html_output_dir=output_dir,
            user_id=user_id
        )
        task_id = task["task_id"]
        
        # タスクの完了を待機
        result = await client.wait_for_completion_async(
            task_id=task_id,
            user_id=user_id
        )
        
        # 結果処理
        handler = ResultHandler(output_dir=output_dir)
        handler.process_result(result)
        
        return {
            "user_id": user_id,
            "url": url,
            "task_id": task_id,
            "status": "completed",
            "elapsed": result.get("elapsed", 0)
        }
    
    except Exception as e:
        logger.error(f"エラー（ユーザー {user_id}）: {e}")
        return {
            "user_id": user_id,
            "url": url,
            "status": "error",
            "message": str(e)
        }


async def simulate_multiple_users(
    num_users: int,
    urls: List[str],
    api_url: str = "http://localhost:8001",
    selectors_file: Optional[str] = None,
    save_output: bool = False,
    output_dir: str = "output/html_files",
    concurrency: int = 5
) -> List[Dict[str, Any]]:
    """
    複数ユーザーのアクセスをシミュレートする

    Args:
        num_users: ユーザー数
        urls: アクセス対象のURLリスト
        api_url: APIのURL
        selectors_file: セレクタファイルパス
        save_output: 出力を保存するかどうか
        output_dir: 出力ディレクトリ
        concurrency: 同時実行数

    Returns:
        全ユーザーの結果リスト
    """
    start_time = time.time()
    logger.info(f"複数ユーザーシミュレーション開始（ユーザー数: {num_users}, 同時実行数: {concurrency}）")
    
    # クライアントの初期化
    client = PlayScraperClient(api_url)
    
    # 並行実行制限（セマフォ）
    semaphore = asyncio.Semaphore(concurrency)
    
    # ユーザーシミュレーション関数（セマフォで同時実行数を制限）
    async def simulate_user_with_semaphore(user_id: str) -> Dict[str, Any]:
        async with semaphore:
            return await simulate_user(
                user_id=user_id,
                client=client,
                urls=urls,
                selectors_file=selectors_file,
                save_output=save_output,
                output_dir=output_dir
            )
    
    # ユーザーIDのリストを作成
    user_ids = [f"user_{i+1}" for i in range(num_users)]
    
    # すべてのユーザーのタスクを作成
    tasks = [simulate_user_with_semaphore(user_id) for user_id in user_ids]
    
    # すべてのタスクを実行
    results = await asyncio.gather(*tasks)
    
    # セッションをクローズ
    await client.close_async_sessions()
    
    elapsed = time.time() - start_time
    logger.info(f"複数ユーザーシミュレーション完了（所要時間: {elapsed:.2f}秒）")
    
    # 結果の集計
    completed = sum(1 for r in results if r["status"] == "completed")
    errors = sum(1 for r in results if r["status"] == "error")
    avg_time = sum(r.get("elapsed", 0) for r in results if "elapsed" in r) / max(completed, 1)
    
    logger.info(f"集計: 成功 {completed}/{num_users}, エラー {errors}/{num_users}, 平均処理時間 {avg_time:.2f}秒")
    
    return results


async def main_async():
    """非同期メイン関数"""
    # 引数解析
    parser = argparse.ArgumentParser(description="複数ユーザーからのアクセスをシミュレーション")
    parser.add_argument("--users", type=int, default=10, help="シミュレーションするユーザー数")
    parser.add_argument("--api-url", default="http://localhost:8001", help="PlayScraperAPIのURL")
    parser.add_argument("--urls", help="カンマ区切りのURLリスト（指定しない場合はデフォルトURLが使用されます）")
    parser.add_argument("--url-file", help="URLリストを含むファイル（1行に1 URL）")
    parser.add_argument("--selectors", help="セレクタのJSONファイルパス")
    parser.add_argument("--concurrency", type=int, default=5, help="同時実行数")
    parser.add_argument("--save-output", action="store_true", help="HTML出力を保存する")
    parser.add_argument("--output-dir", default="output/html_files", help="HTML出力ディレクトリ")
    parser.add_argument("--results", default="simulation_results.json", help="シミュレーション結果を保存するファイル")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細なログを表示")
    
    args = parser.parse_args()
    
    # ロガー設定
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logger("simulation", log_level)
    
    # URLリストの準備
    urls = DEFAULT_URLS
    if args.urls:
        urls = args.urls.split(",")
    elif args.url_file:
        try:
            with open(args.url_file, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.error(f"URLファイルの読み込みに失敗: {e}")
            return 1
    
    logger.info(f"使用するURL数: {len(urls)}")
    if args.verbose:
        for i, url in enumerate(urls):
            logger.debug(f"URL {i+1}: {url}")
    
    # 出力ディレクトリの作成
    if args.save_output:
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    # シミュレーション実行
    results = await simulate_multiple_users(
        num_users=args.users,
        urls=urls,
        api_url=args.api_url,
        selectors_file=args.selectors,
        save_output=args.save_output,
        output_dir=args.output_dir,
        concurrency=args.concurrency
    )
    
    # 結果の保存
    if args.results:
        try:
            with open(args.results, "w", encoding="utf-8") as f:
                import json
                json.dump(results, f, ensure_ascii=False, indent=2)
            logger.success(f"シミュレーション結果を {args.results} に保存しました")
        except Exception as e:
            logger.error(f"結果の保存に失敗: {e}")
    
    return 0


def main():
    """メイン関数"""
    try:
        return asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.warning("ユーザーによる中断")
        return 130
    except Exception as e:
        logger.error(f"予期せぬエラー: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
