"""
PlayScraperAPI クライアント セッション管理モジュール

複数ユーザーのセッションを管理するためのモジュールです。
"""

import os
import uuid
import time
import json
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor

from loguru import logger


class SessionManager:
    """セッション管理クラス"""
    
    def __init__(self, max_sessions: int = 10, session_timeout: int = 3600):
        """
        セッションマネージャの初期化
        
        Args:
            max_sessions: 最大セッション数
            session_timeout: セッションタイムアウト（秒）
        """
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.max_sessions = max_sessions
        self.session_timeout = session_timeout
        self.executor = ThreadPoolExecutor(max_workers=max_sessions)
    
    def create_session(self, user_identifier: Optional[str] = None) -> str:
        """
        新しいセッションを作成
        
        Args:
            user_identifier: ユーザー識別子（オプション）
            
        Returns:
            セッションID
        """
        # 古いセッションをクリーンアップ
        self._cleanup_expired_sessions()
        
        # セッション数が上限に達しているか確認
        if len(self.sessions) >= self.max_sessions:
            logger.warning(f"セッション数が上限（{self.max_sessions}）に達しています。最も古いセッションを削除します。")
            oldest_session_id = min(self.sessions, key=lambda s: self.sessions[s]["created_at"])
            self.delete_session(oldest_session_id)
        
        # 新しいセッションIDを生成
        session_id = str(uuid.uuid4())
        
        # セッション情報を作成
        self.sessions[session_id] = {
            "id": session_id,
            "user_identifier": user_identifier,
            "created_at": time.time(),
            "last_accessed": time.time(),
            "tasks": {}
        }
        
        logger.info(f"セッション作成: {session_id}" + (f" (ユーザー: {user_identifier})" if user_identifier else ""))
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        セッションを取得
        
        Args:
            session_id: セッションID
            
        Returns:
            セッション情報（存在しない場合はNone）
        """
        session = self.sessions.get(session_id)
        if session:
            # 最終アクセス時刻を更新
            session["last_accessed"] = time.time()
            return session
        return None
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """
        セッション情報を更新
        
        Args:
            session_id: セッションID
            data: 更新データ
            
        Returns:
            更新成功かどうか
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        # データをマージ
        for key, value in data.items():
            if key not in ["id", "created_at"]:
                session[key] = value
        
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """
        セッションを削除
        
        Args:
            session_id: セッションID
            
        Returns:
            削除成功かどうか
        """
        if session_id in self.sessions:
            user_identifier = self.sessions[session_id].get("user_identifier")
            del self.sessions[session_id]
            logger.info(f"セッション削除: {session_id}" + (f" (ユーザー: {user_identifier})" if user_identifier else ""))
            return True
        return False
    
    def add_task(self, session_id: str, task_id: str, task_info: Dict[str, Any]) -> bool:
        """
        セッションにタスクを追加
        
        Args:
            session_id: セッションID
            task_id: タスクID
            task_info: タスク情報
            
        Returns:
            追加成功かどうか
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        session["tasks"][task_id] = task_info
        logger.info(f"タスク追加: {task_id} to セッション {session_id}")
        return True
    
    def get_task(self, session_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        """
        セッションからタスクを取得
        
        Args:
            session_id: セッションID
            task_id: タスクID
            
        Returns:
            タスク情報（存在しない場合はNone）
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        return session["tasks"].get(task_id)
    
    def update_task(self, session_id: str, task_id: str, task_info: Dict[str, Any]) -> bool:
        """
        セッション内のタスク情報を更新
        
        Args:
            session_id: セッションID
            task_id: タスクID
            task_info: タスク情報
            
        Returns:
            更新成功かどうか
        """
        session = self.get_session(session_id)
        if not session or task_id not in session["tasks"]:
            return False
        
        # タスク情報をマージ
        for key, value in task_info.items():
            session["tasks"][task_id][key] = value
        
        return True
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """
        全セッションのリストを取得
        
        Returns:
            セッションリスト
        """
        return [{
            "id": session_id,
            "user_identifier": session["user_identifier"],
            "created_at": session["created_at"],
            "last_accessed": session["last_accessed"],
            "task_count": len(session["tasks"])
        } for session_id, session in self.sessions.items()]
    
    def _cleanup_expired_sessions(self) -> int:
        """
        期限切れのセッションをクリーンアップ
        
        Returns:
            削除されたセッション数
        """
        current_time = time.time()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if current_time - session["last_accessed"] > self.session_timeout
        ]
        
        for session_id in expired_sessions:
            self.delete_session(session_id)
        
        if expired_sessions:
            logger.info(f"{len(expired_sessions)}個の期限切れセッションを削除しました")
        
        return len(expired_sessions)
