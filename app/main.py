from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from typing import Dict, List, Optional, Any

from .schemas import ScrapingRequest, ScrapingResponse, ScraperStatus
from .scraper import PlaywrightScraper

app = FastAPI(
    title="PlayScraperAPI",
    description="Playwright を使用したウェブスクレイピング API",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# スクレイパーインスタンス
scraper = PlaywrightScraper()
scraping_tasks: Dict[str, Dict[str, Any]] = {}


@app.on_event("startup")
async def startup_event():
    await scraper.initialize()
    logger.info("Playwrightスクレイパーが初期化されました")


@app.on_event("shutdown")
async def shutdown_event():
    await scraper.close()
    logger.info("Playwrightスクレイパーが終了しました")


async def scrape_task(task_id: str, request: ScrapingRequest):
    """バックグラウンドでスクレイピングを実行するタスク"""
    try:
        scraping_tasks[task_id]["status"] = "running"
        result = await scraper.scrape(str(request.url), request.selectors, request.actions)
        scraping_tasks[task_id]["status"] = "completed"
        scraping_tasks[task_id]["result"] = result
    except Exception as e:
        logger.error(f"スクレイピングエラー: {str(e)}")
        scraping_tasks[task_id]["status"] = "failed"
        scraping_tasks[task_id]["error"] = str(e)


@app.post("/scrape", response_model=Dict[str, str])
async def scrape(request: ScrapingRequest, background_tasks: BackgroundTasks):
    """スクレイピングタスクを開始する"""
    task_id = f"task_{len(scraping_tasks) + 1}"
    
    # request.dictの代わりにモデルを手動で辞書に変換し、URLを文字列に変換
    request_dict = {
        "url": str(request.url),
        "selectors": request.selectors,
        "actions": [action.dict() for action in request.actions] if request.actions else None,
        "options": request.options
    }
    
    scraping_tasks[task_id] = {"status": "pending", "request": request_dict}
    
    background_tasks.add_task(scrape_task, task_id, request)
    
    return {"task_id": task_id, "status": "pending"}


@app.get("/status/{task_id}", response_model=ScraperStatus)
async def get_status(task_id: str):
    """スクレイピングタスクのステータスを取得する"""
    if task_id not in scraping_tasks:
        raise HTTPException(status_code=404, detail="タスクが見つかりません")
    
    task_info = scraping_tasks[task_id]
    response = {
        "task_id": task_id,
        "status": task_info["status"],
    }
    
    if "result" in task_info:
        response["result"] = task_info["result"]
    if "error" in task_info:
        response["error"] = task_info["error"]
    
    return response


@app.get("/", response_model=Dict[str, str])
async def root():
    """APIのルートエンドポイント"""
    return {"status": "online", "message": "PlayScraperAPI が実行中です"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
