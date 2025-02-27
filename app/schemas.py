from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, List, Optional, Any, Union


class ScrapingAction(BaseModel):
    """スクレイピング中に実行するアクション"""
    type: str = Field(..., description="アクションタイプ (click, type, wait, etc.)")
    selector: Optional[str] = Field(None, description="アクション対象の要素セレクタ")
    value: Optional[str] = Field(None, description="アクションの値（typeアクションの入力テキストなど）")
    options: Optional[Dict[str, Any]] = Field(None, description="アクションのオプション")


class ScrapingRequest(BaseModel):
    """スクレイピングリクエスト"""
    url: HttpUrl = Field(..., description="スクレイピング対象のURL")
    selectors: Optional[Dict[str, str]] = Field(None, description="抽出するデータのセレクタマップ")
    actions: Optional[List[ScrapingAction]] = Field(None, description="スクレイピング前に実行するアクション")
    options: Optional[Dict[str, Any]] = Field(None, description="スクレイピングオプション")


class ScrapingResponse(BaseModel):
    """スクレイピング結果"""
    url: str = Field(..., description="スクレイピングしたURL")
    data: Dict[str, Any] = Field(..., description="抽出されたデータ")
    screenshot: Optional[str] = Field(None, description="スクリーンショット（Base64エンコード）")
    html: Optional[str] = Field(None, description="取得したHTMLコンテンツ")


class ScraperStatus(BaseModel):
    """スクレイピングタスクのステータス"""
    task_id: str
    status: str = Field(..., description="タスクステータス (pending, running, completed, failed)")
    result: Optional[ScrapingResponse] = Field(None, description="完了した場合のスクレイピング結果")
    error: Optional[str] = Field(None, description="エラーが発生した場合のエラーメッセージ")
