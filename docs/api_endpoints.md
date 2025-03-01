<div align="center">
  
![Image](https://github.com/user-attachments/assets/9bd05ea0-20d6-49c6-aea0-65c6e69500a7)

# 📡 API エンドポイント

PlaywrightAPIが提供する主要なエンドポイントと使用方法について説明します。

</div>

## 🔍 GET /

APIステータスの確認

**レスポンス例:**

```json
{
  "status": "online",
  "message": "PlaywrightAPI が実行中です"
}
```

**cURLリクエスト例:**

```bash
curl -X GET "http://localhost:8001/"
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

**cURLリクエスト例:**

```bash
curl -X POST "http://localhost:8001/scrape" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
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

**cURLリクエスト例:**

```bash
curl -X GET "http://localhost:8001/status/task_1"
```

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

## 🧩 高度なスクレイピング例

より複雑なセレクタとアクションを使用したスクレイピング例：

**cURLリクエスト例:**

```bash
curl -X POST "http://localhost:8001/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/products",
    "selectors": {
      "product_titles": {
        "type": "css",
        "value": ".product-item h2",
        "transform": "text"
      },
      "product_prices": {
        "type": "css",
        "value": ".product-item .price",
        "transform": "text",
        "optional": true,
        "fallback": "価格未設定"
      },
      "product_images": {
        "type": "css", 
        "value": ".product-item img", 
        "transform": "attribute:src"
      },
      "available": {
        "operator": "not",
        "selectors": [".sold-out"],
        "transform": "text"
      }
    },
    "actions": [
      {
        "type": "wait_for_selector",
        "selector": ".product-list",
        "options": {
          "timeout": 10000
        }
      },
      {
        "type": "click",
        "selector": ".load-more-button"
      },
      {
        "type": "wait",
        "value": "2"
      }
    ],
    "save_html_file": true
  }'
```
