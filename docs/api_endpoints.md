# 📡 API エンドポイント

PlayScraperAPIが提供する主要なエンドポイントと使用方法について説明します。

## 🔍 GET /

APIステータスの確認

**レスポンス例:**

```json
{
  "status": "online",
  "message": "PlayScraperAPI が実行中です"
}
```

## 🔍 POST /scrape

スクレイピングリクエストを送信

**リクエスト例:**

```json
{
  "url": "https://example.com",
  "selectors": {
    "title": "h1",
    "description": ".description",
    "price": "#price"
  },
  "actions": [
    {
      "type": "click",
      "selector": ".button-class"
    },
    {
      "type": "type",
      "selector": "#search-input",
      "value": "検索キーワード"
    },
    {
      "type": "wait",
      "value": "2"
    }
  ],
  "save_html_file": true,
  "html_output_dir": "output/html"
}
```

**レスポンス例:**

```json
{
  "task_id": "task_1",
  "status": "pending"
}
```

## 🔍 GET /status/{task_id}

タスクのステータスと結果の確認

**レスポンス例:**

```json
{
  "task_id": "task_1",
  "status": "completed",
  "result": {
    "url": "https://example.com",
    "data": {
      "title": "ページタイトル",
      "description": "ページの説明文",
      "price": "¥1,000"
    },
    "screenshot": "base64エンコードされた画像...",
    "html": "<!DOCTYPE html>..."
  }
}
```
