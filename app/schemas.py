from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, List, Optional, Any, Union


class ScrapingAction(BaseModel):
    """スクレイピング中に実行するアクション"""
    type: str = Field(..., description="アクションタイプ (click, type, wait, etc.)")
    selector: Optional[str] = Field(None, description="アクション対象の要素セレクタ")
    value: Optional[str] = Field(None, description="アクションの値（typeアクションの入力テキストなど）")
    options: Optional[Dict[str, Any]] = Field(None, description="アクションのオプション")


class SelectorDefinition(BaseModel):
    """セレクタ定義"""
    type: str = Field("css", description="セレクタタイプ (css, xpath, text, etc.)")
    value: str = Field(..., description="セレクタの値")
    optional: Optional[bool] = Field(False, description="このセレクタが省略可能かどうか")
    fallback: Optional[str] = Field(None, description="セレクタが見つからない場合のデフォルト値")
    transform: Optional[str] = Field(None, description="抽出後の変換処理 (text, html, attribute:name など)")


class ScrapingRequest(BaseModel):
    """スクレイピングリクエスト"""
    url: HttpUrl = Field(..., description="スクレイピング対象のURL")
    selectors: Optional[Dict[str, Union[str, SelectorDefinition]]] = Field(None, description="抽出するデータのセレクタマップ（文字列またはセレクタ定義オブジェクト）")
    actions: Optional[List[ScrapingAction]] = Field(None, description="スクレイピング前に実行するアクション")
    options: Optional[Dict[str, Any]] = Field(None, description="スクレイピングオプション")
    save_html_file: Optional[bool] = Field(False, description="HTMLをファイルとして保存するかどうか")


class ScrapingResponse(BaseModel):
    """スクレイピング結果"""
    url: str = Field(..., description="スクレイピングしたURL")
    data: Dict[str, Any] = Field(..., description="抽出されたデータ")
    screenshot: Optional[str] = Field(None, description="スクリーンショット（Base64エンコード）")
    html: Optional[str] = Field(None, description="取得したHTMLコンテンツ")
    html_file: Optional[str] = Field(None, description="保存されたHTMLファイルのパス")


class ScraperStatus(BaseModel):
    """スクレイピングタスクのステータス"""
    task_id: str
    status: str = Field(..., description="タスクステータス (pending, running, completed, failed)")
    result: Optional[ScrapingResponse] = Field(None, description="完了した場合のスクレイピング結果")
    error: Optional[str] = Field(None, description="エラーが発生した場合のエラーメッセージ")
