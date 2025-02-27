from playwright.async_api import async_playwright, Page, Browser, Playwright
import asyncio
import logging
import base64
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class PlaywrightScraper:
    """Playwrightを使用したスクレイピングクラス"""
    
    def __init__(self):
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
    
    async def initialize(self):
        """Playwrightとブラウザを初期化する"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,  # ヘッドレスモードで実行
        )
        logger.info("Playwrightとブラウザが初期化されました")
    
    async def close(self):
        """ブラウザとPlaywrightを終了する"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("ブラウザとPlaywrightを終了しました")
    
    async def execute_actions(self, page: Page, actions: List[Dict[str, Any]]):
        """定義されたアクションをページ上で実行する"""
        if not actions:
            return
        
        for action in actions:
            action_type = action.get("type")
            selector = action.get("selector")
            value = action.get("value")
            options = action.get("options", {})
            
            try:
                if action_type == "click" and selector:
                    await page.click(selector, **options)
                    logger.info(f"クリックアクション実行: {selector}")
                
                elif action_type == "type" and selector and value:
                    await page.fill(selector, value, **options)
                    logger.info(f"入力アクション実行: {selector}, 値: {value}")
                
                elif action_type == "wait_for_selector" and selector:
                    await page.wait_for_selector(selector, **options)
                    logger.info(f"セレクタ待機アクション実行: {selector}")
                
                elif action_type == "wait_for_navigation":
                    await page.wait_for_navigation(**options)
                    logger.info("ナビゲーション待機アクション実行")
                
                elif action_type == "wait":
                    await asyncio.sleep(float(value) if value else 1.0)
                    logger.info(f"待機アクション実行: {value if value else 1.0}秒")
                
                elif action_type == "select" and selector and value:
                    await page.select_option(selector, value, **options)
                    logger.info(f"選択アクション実行: {selector}, 値: {value}")
                
                else:
                    logger.warning(f"未対応のアクションタイプ: {action_type}")
            
            except Exception as e:
                logger.error(f"アクション実行エラー {action_type}: {str(e)}")
                raise
    
    async def extract_data(self, page: Page, selectors: Dict[str, str]) -> Dict[str, Any]:
        """指定されたセレクタを使用してページからデータを抽出する"""
        result = {}
        
        if not selectors:
            return result
        
        for key, selector in selectors.items():
            try:
                if selector.startswith("//"):  # XPathセレクタ
                    elements = await page.xpath(selector)
                    if elements:
                        result[key] = await elements[0].inner_text()
                else:  # CSSセレクタ
                    element = await page.query_selector(selector)
                    if element:
                        result[key] = await element.inner_text()
            except Exception as e:
                logger.error(f"データ抽出エラー {key}: {str(e)}")
                result[key] = None
        
        return result
    
    async def scrape(
        self, 
        url: str, 
        selectors: Optional[Dict[str, str]] = None, 
        actions: Optional[List[Dict[str, Any]]] = None,
        take_screenshot: bool = True,
        get_html: bool = True
    ) -> Dict[str, Any]:
        """指定されたURLをスクレイピングし、データを抽出する"""
        if not self.browser:
            await self.initialize()
        
        context = await self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        try:
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle")
            logger.info(f"ページにアクセスしました: {url}")
            
            # アクションの実行
            if actions:
                await self.execute_actions(page, actions)
            
            # データの抽出
            data = await self.extract_data(page, selectors or {})
            
            result = {
                "url": url,
                "data": data
            }
            
            # スクリーンショットの取得
            if take_screenshot:
                screenshot = await page.screenshot(type="jpeg", quality=80)
                result["screenshot"] = base64.b64encode(screenshot).decode("utf-8")
            
            # HTMLの取得
            if get_html:
                result["html"] = await page.content()
            
            return result
        
        except Exception as e:
            logger.error(f"スクレイピングエラー: {str(e)}")
            raise
        
        finally:
            await context.close()
