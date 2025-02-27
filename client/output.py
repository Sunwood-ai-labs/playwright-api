"""
PlayScraperAPI クライアント 出力処理モジュール

スクレイピング結果の出力処理を行うユーティリティを提供します。
"""

import os
import base64
from typing import Dict, Any, Optional

from loguru import logger
from .utils import url_to_filename, save_html_to_file, save_screenshot_to_file, save_json_file


class ResultHandler:
    """スクレイピング結果ハンドラクラス"""
    
    def __init__(self, output_dir: str = "output/html", result_file: str = "output.json"):
        """
        初期化
        
        Args:
            output_dir: 出力ディレクトリ
            result_file: 結果JSONファイル
        """
        self.output_dir = output_dir
        self.result_file = result_file
    
    def process_result(self, task_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        タスク結果を処理する
        
        Args:
            task_result: タスク結果
            
        Returns:
            処理結果の情報
        """
        if "result" not in task_result:
            logger.warning("処理する結果がありません")
            return task_result
        
        result = task_result["result"]
        url = result.get("url", "")
        data = result.get("data", {})
        
        logger.info(f"スクレイピング結果を処理中: {url}")
        
        # 結果の概要を表示
        logger.info("URL: " + url)
        
        if data:
            logger.info("抽出データ:")
            for key, value in data.items():
                logger.info(f"  {key}: {value}")
        else:
            logger.warning("抽出データなし（セレクタが指定されていないか、一致するデータがありません）")
        
        # エラー情報を表示
        if "errors" in result:
            logger.warning("エラー情報:")
            for key, error in result["errors"].items():
                logger.warning(f"  {key}: {error['message']} ({error['type']})")
        
        # 結果をJSONとして保存
        if self.result_file:
            save_json_file(task_result, self.result_file)
            logger.success(f"結果を {self.result_file} に保存しました")
        
        return task_result
    
    def save_html_content(self, task_result: Dict[str, Any]) -> Optional[str]:
        """
        HTML内容をファイルとして保存
        
        Args:
            task_result: タスク結果
            
        Returns:
            保存されたHTMLファイルのパス（保存しなかった場合はNone）
        """
        if "result" not in task_result or "html" not in task_result["result"]:
            return None
        
        result = task_result["result"]
        url = result.get("url", "")
        html_content = result.get("html", "")
        
        if not html_content:
            return None
        
        # URLからファイル名を生成
        filename = url_to_filename(url, ".html")
        
        # HTMLをファイルに保存
        filepath = save_html_to_file(html_content, self.output_dir, filename)
        logger.success(f"HTMLをファイルに保存しました: {filepath}")
        
        return filepath
    
    def save_screenshot(self, task_result: Dict[str, Any]) -> Optional[str]:
        """
        スクリーンショットをファイルとして保存
        
        Args:
            task_result: タスク結果
            
        Returns:
            保存されたスクリーンショットファイルのパス（保存しなかった場合はNone）
        """
        if "result" not in task_result or "screenshot" not in task_result["result"]:
            return None
        
        result = task_result["result"]
        url = result.get("url", "")
        screenshot_base64 = result.get("screenshot", "")
        
        if not screenshot_base64:
            return None
        
        # URLからファイル名を生成
        filename = url_to_filename(url, ".png")
        
        # スクリーンショットをファイルに保存
        filepath = save_screenshot_to_file(screenshot_base64, self.output_dir, filename)
        logger.success(f"スクリーンショットを保存しました: {filepath}")
        
        return filepath
