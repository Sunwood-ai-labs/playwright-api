"""
PlaywrightAPI クライアント

PlaywrightAPIを簡単に利用するためのクライアント実装
"""

import json
import time
from typing import Dict, Any, Optional, List, Union

import aiohttp
import requests
import asyncio

from loguru import logger


class PlayScraperClient:
    """PlaywrightAPIクライアントクラス"""

    def __init__(self, base_url: str = "http://localhost:8001"):
        """
        クライアントの初期化
        
        Args:
            base_url: APIのベースURL
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self._asyncio_sessions = {}  # 非同期セッションを保持する辞書（ユーザーIDをキーにする）
    
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
    
    async def check_status_async(self, user_id: str = "default") -> Dict[str, Any]:
        """
        APIの状態を非同期で確認
        
        Args:
            user_id: ユーザーID（セッション管理用）
            
        Returns:
            APIの状態情報
        """
        logger.info(f"APIの状態を非同期で確認中: {self.base_url} (ユーザー: {user_id})")
        session = await self._get_async_session(user_id)
        async with session.get(f"{self.base_url}/") as response:
            response.raise_for_status()
            return await response.json()
    
    def start_scraping(
        self,
        url: str,
        selectors: Optional[Dict[str, Any]] = None,
        actions: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Dict[str, Any]] = None,
        save_html_file: bool = False,
        html_output_dir: str = "output/html"
    ) -> Dict[str, Any]:
        """
        スクレイピングタスクを開始
        
        Args:
            url: スクレイピング対象のURL
            selectors: 抽出するデータのセレクタマップ（文字列または拡張セレクタ定義）
            actions: スクレイピング前に実行するアクション
            options: スクレイピングオプション
            save_html_file: HTMLをファイルとして保存するかどうか
            html_output_dir: HTMLファイルを保存するディレクトリ
            
        Returns:
            タスクID情報
        """
        logger.info(f"スクレイピングリクエスト準備: {url}")
        
        payload = {
            "url": url,
            "save_html_file": save_html_file,
            "html_output_dir": html_output_dir
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
    
    async def start_scraping_async(
        self,
        url: str,
        selectors: Optional[Dict[str, Any]] = None,
        actions: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Dict[str, Any]] = None,
        save_html_file: bool = False,
        html_output_dir: str = "output/html",
        user_id: str = "default"
    ) -> Dict[str, Any]:
        """
        スクレイピングタスクを非同期で開始
        
        Args:
            url: スクレイピング対象のURL
            selectors: 抽出するデータのセレクタマップ（文字列または拡張セレクタ定義）
            actions: スクレイピング前に実行するアクション
            options: スクレイピングオプション
            save_html_file: HTMLをファイルとして保存するかどうか
            html_output_dir: HTMLファイルを保存するディレクトリ
            user_id: ユーザーID（セッション管理用）
            
        Returns:
            タスクID情報
        """
        logger.info(f"非同期スクレイピングリクエスト準備: {url} (ユーザー: {user_id})")
        
        payload = {
            "url": url,
            "save_html_file": save_html_file,
            "html_output_dir": html_output_dir
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
        
        logger.info(f"非同期スクレイピングリクエスト送信中... (ユーザー: {user_id})")
        logger.debug(f"リクエストペイロード: {payload}")
        
        session = await self._get_async_session(user_id)
        async with session.post(
            f"{self.base_url}/scrape",
            json=payload
        ) as response:
            response.raise_for_status()
            result = await response.json()
            logger.success(f"タスク作成成功: {result['task_id']} (ユーザー: {user_id})")
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
    
    async def get_task_status_async(self, task_id: str, user_id: str = "default") -> Dict[str, Any]:
        """
        タスクのステータスを非同期で取得
        
        Args:
            task_id: タスクID
            user_id: ユーザーID（セッション管理用）
            
        Returns:
            タスクのステータス情報
        """
        logger.debug(f"非同期タスクステータス確認: {task_id} (ユーザー: {user_id})")
        session = await self._get_async_session(user_id)
        async with session.get(f"{self.base_url}/status/{task_id}") as response:
            response.raise_for_status()
            return await response.json()
    
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
            print(f"\r{progress_chars[progress_idx]} 状態: {status_text} ({elapsed:.1f}秒経過)", end="", flush=True)
            
            if status_text == "completed":
                print("\n")
                logger.success(f"タスク完了: {elapsed:.1f}秒")
                return status
            elif status_text == "failed":
                print("\n")
                error_msg = status.get("error", "不明なエラー")
                logger.error(f"タスク失敗: {error_msg}")
                raise RuntimeError(f"タスク {task_id} が失敗しました: {error_msg}")
            
            time.sleep(interval)
    
    async def wait_for_completion_async(
        self, 
        task_id: str, 
        interval: float = 1.0, 
        timeout: float = 60.0,
        user_id: str = "default"
    ) -> Dict[str, Any]:
        """
        タスクの完了を非同期で待機
        
        Args:
            task_id: タスクID
            interval: ステータス確認の間隔（秒）
            timeout: タイムアウト時間（秒）
            user_id: ユーザーID（セッション管理用）
            
        Returns:
            完了したタスクの結果
            
        Raises:
            TimeoutError: タイムアウト時間を超えた場合
            RuntimeError: タスクが失敗した場合
        """
        start_time = time.time()
        logger.info(f"非同期タスク {task_id} の完了を待機中... (ユーザー: {user_id})")
        
        while True:
            if time.time() - start_time > timeout:
                logger.error(f"タイムアウト: {timeout}秒経過")
                raise TimeoutError(f"タスク {task_id} がタイムアウトしました")
            
            status = await self.get_task_status_async(task_id, user_id)
            status_text = status["status"]
            
            elapsed = time.time() - start_time
            logger.debug(f"タスク状態: {status_text} ({elapsed:.1f}秒経過)")
            
            if status_text == "completed":
                logger.success(f"タスク完了: {elapsed:.1f}秒")
                return status
            elif status_text == "failed":
                error_msg = status.get("error", "不明なエラー")
                logger.error(f"タスク失敗: {error_msg}")
                raise RuntimeError(f"タスク {task_id} が失敗しました: {error_msg}")
            
            await asyncio.sleep(interval)
    
    async def _get_async_session(self, user_id: str) -> aiohttp.ClientSession:
        """
        ユーザーごとの非同期セッションを取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            aiohttp.ClientSession: ユーザー専用のセッション
        """
        if user_id not in self._asyncio_sessions or self._asyncio_sessions[user_id].closed:
            logger.debug(f"新しい非同期セッションを作成: ユーザー {user_id}")
            self._asyncio_sessions[user_id] = aiohttp.ClientSession()
        return self._asyncio_sessions[user_id]
    
    async def close_async_sessions(self):
        """
        全ての非同期セッションを閉じる
        """
        for user_id, session in self._asyncio_sessions.items():
            if not session.closed:
                logger.debug(f"非同期セッションを閉じる: ユーザー {user_id}")
                await session.close()
        self._asyncio_sessions = {}
