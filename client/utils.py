"""
PlayScraperAPI クライアント ユーティリティ関数

PlayScraperAPIクライアントで使用されるユーティリティ関数を提供します。
"""

import os
import sys
import json
from typing import Dict, Any, Optional, Union
from urllib.parse import urlparse
from loguru import logger

# ロガーのデフォルト設定をクリア
logger.remove()

def setup_logger(name: str, log_level: str = "INFO"):
    """
    ロガーを設定する
    
    Args:
        name: ロガー名（loguruではあまり使用しないが互換性のために残す）
        log_level: ログレベル
        
    Returns:
        設定されたロガーインスタンス
    """
    # 既存のハンドラをクリア
    logger.remove()
    
    # ログレベルの設定
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
    
    # コンソールへの出力を設定
    if log_level == "DEBUG":
        logger.add(sys.stdout, format=log_format, level="DEBUG")
    else:
        logger.add(sys.stdout, format=log_format, level="INFO")
    
    # 互換性のためにロガーを返す
    return logger


def url_to_filename(url: str, extension: str = ".html") -> str:
    """
    URLからファイル名を生成する
    
    Args:
        url: URL
        extension: ファイル拡張子（デフォルト: .html）
        
    Returns:
        ファイル名
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace(".", "_")
    path = parsed_url.path.replace("/", "_")
    if path == "":
        path = "_index"
    return f"{domain}{path}{extension}"


def save_html_to_file(
    html_content: str, 
    output_dir: str, 
    filename: str
) -> str:
    """
    HTMLコンテンツをファイルに保存する
    
    Args:
        html_content: HTMLコンテンツ
        output_dir: 出力ディレクトリ
        filename: ファイル名
        
    Returns:
        保存されたファイルのパス
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return filepath


def save_screenshot_to_file(
    screenshot_base64: str, 
    output_dir: str, 
    filename: str
) -> str:
    """
    Base64エンコードされたスクリーンショットをファイルに保存する
    
    Args:
        screenshot_base64: Base64エンコードされたスクリーンショット
        output_dir: 出力ディレクトリ
        filename: ファイル名
        
    Returns:
        保存されたファイルのパス
    """
    import base64
    
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    # Base64エンコードされたスクリーンショットをデコードしてファイルに保存
    screenshot_data = base64.b64decode(screenshot_base64)
    with open(filepath, "wb") as f:
        f.write(screenshot_data)
    
    return filepath


def load_json_file(filepath: str) -> Dict[str, Any]:
    """
    JSONファイルを読み込む
    
    Args:
        filepath: ファイルパス
        
    Returns:
        JSONデータ
        
    Raises:
        FileNotFoundError: ファイルが見つからない場合
        json.JSONDecodeError: JSONの解析に失敗した場合
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data: Dict[str, Any], filepath: str) -> None:
    """
    JSONファイルを保存する
    
    Args:
        data: 保存するデータ
        filepath: ファイルパス
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
