#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PlayScraperAPI クライアント

PlayScraperAPIを簡単に利用するためのクライアントスクリプト
"""

import argparse
import json
import time
import sys
from typing import Dict, Any, Optional, List

import requests
from pprint import pprint
from loguru import logger

# ロガーの設定
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    level="INFO"
)


class PlayScraperClient:
    """PlayScraperAPIクライアントクラス"""

    def __init__(self, base_url: str = "http://localhost:8001"):
        """
        クライアントの初期化
        
        Args:
            base_url: APIのベースURL
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def check_status(self) -> Dict[str, Any]:
        """
        APIの状態を確認
        
        Returns:
            APIの状態情報
        """
        logger.info(f"APIの状態を確認中: {self.base_url}")
        response = self.session.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()
    
    def start_scraping(
        self,
        url: str,
        selectors: Optional[Dict[str, str]] = None,
        actions: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Dict[str, Any]] = None,
        save_html_file: bool = False
    ) -> Dict[str, Any]:
        """
        スクレイピングタスクを開始
        
        Args:
            url: スクレイピング対象のURL
            selectors: 抽出するデータのセレクタマップ
            actions: スクレイピング前に実行するアクション
            options: スクレイピングオプション
            save_html_file: HTMLをファイルとして保存するかどうか
            
        Returns:
            タスクID情報
        """
        logger.info(f"スクレイピングリクエスト準備: {url}")
        
        payload = {
            "url": url,
            "save_html_file": save_html_file
        }
        
        if selectors:
            logger.debug(f"セレクタ: {selectors}")
            payload["selectors"] = selectors
        if actions:
            logger.debug(f"アクション: {len(actions)}個")
            payload["actions"] = actions
        if options:
            logger.debug(f"オプション: {options}")
            payload["options"] = options
        
        logger.info("スクレイピングリクエスト送信中...")
        logger.debug(f"リクエストペイロード: {payload}")
        response = self.session.post(
            f"{self.base_url}/scrape",
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        logger.success(f"タスク作成成功: {result['task_id']}")
        return result
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        タスクのステータスを取得
        
        Args:
            task_id: タスクID
            
        Returns:
            タスクのステータス情報
        """
        logger.debug(f"タスクステータス確認: {task_id}")
        response = self.session.get(f"{self.base_url}/status/{task_id}")
        response.raise_for_status()
        return response.json()
    
    def wait_for_completion(self, task_id: str, interval: float = 1.0, timeout: float = 60.0) -> Dict[str, Any]:
        """
        タスクの完了を待機
        
        Args:
            task_id: タスクID
            interval: ステータス確認の間隔（秒）
            timeout: タイムアウト時間（秒）
            
        Returns:
            完了したタスクの結果
            
        Raises:
            TimeoutError: タイムアウト時間を超えた場合
            RuntimeError: タスクが失敗した場合
        """
        start_time = time.time()
        logger.info(f"タスク {task_id} の完了を待機中...")
        
        progress_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        progress_idx = 0
        
        while True:
            if time.time() - start_time > timeout:
                logger.error(f"タイムアウト: {timeout}秒経過")
                raise TimeoutError(f"タスク {task_id} がタイムアウトしました")
            
            status = self.get_task_status(task_id)
            status_text = status["status"]
            
            # 進捗表示
            progress_idx = (progress_idx + 1) % len(progress_chars)
            elapsed = time.time() - start_time
            sys.stdout.write(f"\r{progress_chars[progress_idx]} 状態: {status_text} ({elapsed:.1f}秒経過)")
            sys.stdout.flush()
            
            if status_text == "completed":
                sys.stdout.write("\n")
                logger.success(f"タスク完了: {elapsed:.1f}秒")
                return status
            elif status_text == "failed":
                sys.stdout.write("\n")
                error_msg = status.get("error", "不明なエラー")
                logger.error(f"タスク失敗: {error_msg}")
                raise RuntimeError(f"タスク {task_id} が失敗しました: {error_msg}")
            
            time.sleep(interval)


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="PlayScraperAPI クライアント")
    parser.add_argument("url", help="スクレイピング対象のURL")
    parser.add_argument("--api-url", default="http://localhost:8001", help="PlayScraperAPI のURL")
    parser.add_argument("--selectors", help="セレクタのJSONファイルパス")
    parser.add_argument("--actions", help="アクションのJSONファイルパス")
    parser.add_argument("--timeout", type=float, default=60.0, help="タイムアウト時間（秒）")
    parser.add_argument("--interval", type=float, default=1.0, help="ステータス確認の間隔（秒）")
    parser.add_argument("--output", default="output.json", help="結果を保存するJSONファイルパス")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細なログを表示")
    parser.add_argument("--save-output", action="store_true", help="HTMLとスクリーンショットをファイルとして保存する")
    
    args = parser.parse_args()
    
    # 詳細ログの設定
    if args.verbose:
        logger.remove()
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
            level="DEBUG"
        )
    
    # セレクタの読み込み
    selectors = None
    if args.selectors:
        try:
            logger.info(f"セレクタファイル読み込み: {args.selectors}")
            with open(args.selectors, 'r', encoding='utf-8') as f:
                selectors = json.load(f)
        except Exception as e:
            logger.error(f"セレクタファイルの読み込みに失敗: {e}")
            return 1
    
    # アクションの読み込み
    actions = None
    if args.actions:
        try:
            logger.info(f"アクションファイル読み込み: {args.actions}")
            with open(args.actions, 'r', encoding='utf-8') as f:
                actions = json.load(f)
        except Exception as e:
            logger.error(f"アクションファイルの読み込みに失敗: {e}")
            return 1
    
    # クライアントの初期化
    client = PlayScraperClient(args.api_url)
    
    try:
        # APIの状態確認
        status = client.check_status()
        logger.info(f"API状態: {status['status']} - {status['message']}")
        
        # スクレイピングタスクの開始
        logger.info(f"スクレイピング開始: {args.url}")
        task = client.start_scraping(args.url, selectors, actions, save_html_file=args.save_output)
        task_id = task["task_id"]
        
        # タスクの完了を待機
        result = client.wait_for_completion(task_id, args.interval, args.timeout)
        
        # 結果の表示
        if "result" in result:
            logger.info("スクレイピング結果:")
            logger.info(f"URL: {result['result']['url']}")
            
            if result['result']['data']:
                logger.info("抽出データ:")
                for key, value in result['result']['data'].items():
                    logger.info(f"  {key}: {value}")
            else:
                logger.warning("抽出データなし（セレクタが指定されていないか、一致するデータがありません）")
            
            # HTMLファイルが保存された場合
            if "html_file" in result["result"]:
                logger.success(f"HTMLファイルを保存しました: {result['result']['html_file']}")
            
            # スクリーンショットの保存
            if "screenshot" in result["result"] and args.save_output:
                import os
                import base64
                from urllib.parse import urlparse
                
                # URLからファイル名を生成
                parsed_url = urlparse(args.url)
                domain = parsed_url.netloc.replace(".", "_")
                path = parsed_url.path.replace("/", "_")
                if path == "":
                    path = "_index"
                filename = f"{domain}{path}.png"
                
                # outputディレクトリがなければ作成
                os.makedirs("output", exist_ok=True)
                filepath = os.path.join("output", filename)
                
                # Base64エンコードされたスクリーンショットをデコードしてファイルに保存
                screenshot_data = base64.b64decode(result["result"]["screenshot"])
                with open(filepath, "wb") as f:
                    f.write(screenshot_data)
                
                logger.success(f"スクリーンショットを保存しました: {filepath}")
            elif "screenshot" in result["result"]:
                logger.info("スクリーンショット: [base64エンコードデータ]")
            
            # HTMLコンテンツの情報
            if "html" in result["result"]:
                logger.info("HTML: [HTMLコンテンツ]")
            
            # 結果の保存
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                logger.success(f"結果を {args.output} に保存しました")
        
        return 0
    
    except Exception as e:
        logger.error(f"エラー: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
