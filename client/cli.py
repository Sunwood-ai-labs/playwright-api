"""
PlaywrightAPI クライアント CLI

PlaywrightAPIをコマンドラインから使用するためのインターフェース
"""

import argparse
import sys
import asyncio
from typing import Dict, Any, Optional, List

from loguru import logger
from .api import PlayScraperClient
from .utils import load_json_file
from .output import ResultHandler


async def async_main(args):
    """
    非同期メイン関数
    
    Args:
        args: コマンドライン引数
        
    Returns:
        終了コード
    """
    # クライアントの初期化
    client = PlayScraperClient(args.api_url)
    
    try:
        # APIの状態確認
        status = await client.check_status_async()
        logger.info(f"API状態: {status['status']} - {status['message']}")
        
        # セレクタの読み込み
        selectors = None
        if args.selectors:
            try:
                logger.info(f"セレクタファイル読み込み: {args.selectors}")
                selectors = load_json_file(args.selectors)
            except Exception as e:
                logger.error(f"セレクタファイルの読み込みに失敗: {e}")
                return 1
        
        # アクションの読み込み
        actions = None
        if args.actions:
            try:
                logger.info(f"アクションファイル読み込み: {args.actions}")
                actions = load_json_file(args.actions)
            except Exception as e:
                logger.error(f"アクションファイルの読み込みに失敗: {e}")
                return 1
        
        # 出力ハンドラの初期化
        result_handler = ResultHandler(
            output_dir=args.html_dir,
            result_file=args.output
        )
        
        # スクレイピングタスクの開始
        logger.info(f"スクレイピング開始: {args.url}")
        task = await client.start_scraping_async(
            args.url, 
            selectors, 
            actions, 
            save_html_file=args.save_output,
            html_output_dir=args.html_dir
        )
        task_id = task["task_id"]
        
        # タスクの完了を待機
        result = await client.wait_for_completion_async(task_id, args.interval, args.timeout)
        
        # 結果の処理
        result_handler.process_result(result)
        
        # HTMLとスクリーンショットの保存
        if args.save_output:
            result_handler.save_html_content(result)
            result_handler.save_screenshot(result)
        
        # クライアントのセッションをクローズ
        await client.close_async_sessions()
        
        return 0
    
    except Exception as e:
        logger.error(f"エラー: {e}")
        # クライアントのセッションをクローズ
        await client.close_async_sessions()
        return 1


def main():
    """
    メイン関数
    
    Returns:
        終了コード
    """
    parser = argparse.ArgumentParser(description="PlaywrightAPI クライアント")
    parser.add_argument("url", help="スクレイピング対象のURL")
    parser.add_argument("--api-url", default="http://localhost:8001", help="PlaywrightAPI のURL")
    parser.add_argument("--selectors", help="セレクタのJSONファイルパス")
    parser.add_argument("--actions", help="アクションのJSONファイルパス")
    parser.add_argument("--timeout", type=float, default=60.0, help="タイムアウト時間（秒）")
    parser.add_argument("--interval", type=float, default=1.0, help="ステータス確認の間隔（秒）")
    parser.add_argument("--output", default="output.json", help="結果を保存するJSONファイルパス")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細なログを表示")
    parser.add_argument("--save-output", action="store_true", help="HTMLとスクリーンショットをファイルとして保存する")
    parser.add_argument("--html-dir", default="output/html", help="HTMLファイルとスクリーンショットを保存するディレクトリ")
    parser.add_argument("--async-mode", action="store_true", help="非同期モードで実行")
    
    args = parser.parse_args()
    
    # 詳細ログの設定
    if args.verbose:
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")
    else:
        logger.remove()
        logger.add(sys.stdout, level="INFO")
    
    # 非同期モードで実行
    if args.async_mode:
        return asyncio.run(async_main(args))
    else:
        # クライアントの初期化
        client = PlayScraperClient(args.api_url)
        
        try:
            # APIの状態確認
            status = client.check_status()
            logger.info(f"API状態: {status['status']} - {status['message']}")
            
            # セレクタの読み込み
            selectors = None
            if args.selectors:
                try:
                    logger.info(f"セレクタファイル読み込み: {args.selectors}")
                    selectors = load_json_file(args.selectors)
                except Exception as e:
                    logger.error(f"セレクタファイルの読み込みに失敗: {e}")
                    return 1
            
            # アクションの読み込み
            actions = None
            if args.actions:
                try:
                    logger.info(f"アクションファイル読み込み: {args.actions}")
                    actions = load_json_file(args.actions)
                except Exception as e:
                    logger.error(f"アクションファイルの読み込みに失敗: {e}")
                    return 1
            
            # 出力ハンドラの初期化
            result_handler = ResultHandler(
                output_dir=args.html_dir,
                result_file=args.output
            )
            
            # スクレイピングタスクの開始
            logger.info(f"スクレイピング開始: {args.url}")
            task = client.start_scraping(
                args.url, 
                selectors, 
                actions, 
                save_html_file=args.save_output,
                html_output_dir=args.html_dir
            )
            task_id = task["task_id"]
            
            # タスクの完了を待機
            result = client.wait_for_completion(task_id, args.interval, args.timeout)
            
            # 結果の処理
            result_handler.process_result(result)
            
            # HTMLとスクリーンショットの保存
            if args.save_output:
                result_handler.save_html_content(result)
                result_handler.save_screenshot(result)
            
            return 0
        
        except Exception as e:
            logger.error(f"エラー: {e}")
            return 1


if __name__ == "__main__":
    sys.exit(main())
