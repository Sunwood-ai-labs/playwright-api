# PlayScraperAPI

<p align="center">
  <img src="app/assets/header.svg" alt="PlayScraperAPI" width="800">
</p>

## 🌟 概要

PlaywrightとPythonを使用したウェブスクレイピングAPIサーバー。Docker Composeで簡単に構築・デプロイが可能です。

## ✨ 機能

- 🔍 Playwrightを使用した高度なブラウザ自動化でのスクレイピング
- ⚡ 非同期処理によるスケーラブルなAPI設計
- 🖱️ 様々なウェブインタラクション（クリック、タイプ、待機など）のサポート
- 📸 スクリーンショット取得機能
- 📄 HTML全体の取得機能
- 🔄 バックグラウンドタスク処理と状態管理

## 🔧 必要条件

- Docker
- Docker Compose

## 🚀 セットアップと実行

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/playscraperapi.git
cd playscraperapi

# Docker Composeでビルドして起動
docker-compose up -d

# ログの確認
docker-compose logs -f
```

サーバーは http://localhost:8000 で実行されます。

## 📡 API エンドポイント

### GET /

APIステータスの確認

**レスポンス例:**

```json
{
  "status": "online",
  "message": "PlayScraperAPI が実行中です"
}
```

### POST /scrape

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
  ]
}
```

**レスポンス例:**

```json
{
  "task_id": "task_1",
  "status": "pending"
}
```

### GET /status/{task_id}

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

## 🔍 拡張セレクタ機能

PlayScraperAPIは、より柔軟で強力なセレクタ定義をサポートしています。従来の単純な文字列セレクタに加えて、詳細なセレクタ定義オブジェクトを使用できます。

### 基本的な使い方

```json
{
  "title": "h1",                        // 従来の単純なCSSセレクタ
  "description": {                      // 拡張セレクタ定義
    "type": "css",                      // セレクタタイプ (css, xpath, text)
    "value": "meta[name='description']", // セレクタの値
    "transform": "attribute:content",   // 変換処理
    "optional": true,                   // 省略可能かどうか
    "fallback": "説明がありません"       // 見つからない場合のデフォルト値
  }
}
```

### セレクタタイプ

- `css`: CSSセレクタ (デフォルト)
- `xpath`: XPathセレクタ
- `text`: テキスト内容によるセレクタ

### 変換処理

- `text`: テキスト内容を抽出 (デフォルト)
- `html`: HTML内容を抽出
- `attribute:name`: 指定した属性の値を抽出 (例: `attribute:href`, `attribute:src`)

### オプション設定

- `optional`: `true`の場合、要素が見つからなくてもエラーにならない
- `fallback`: 要素が見つからない場合のデフォルト値

### 使用例

```python
from client import PlayScraperClient

client = PlayScraperClient()

# 拡張セレクタを使用したスクレイピング
selectors = {
    "title": {
        "type": "css",
        "value": "h1",
        "transform": "text"
    },
    "meta_description": {
        "type": "css",
        "value": "meta[name='description']",
        "transform": "attribute:content",
        "optional": true
    },
    "author": {
        "type": "xpath",
        "value": "//div[@class='author-info']/span",
        "fallback": "不明な著者"
    }
}

result = client.start_scraping("https://example.com", selectors=selectors)
task_id = result["task_id"]
data = client.wait_for_completion(task_id)
print(data["result"]["data"])
```

詳細な例は `examples/selectors.json` を参照してください。

## 🎮 サポートされているアクション

- `click`: 要素をクリック
- `type`: テキストを入力
- `wait_for_selector`: セレクタが表示されるのを待つ
- `wait_for_navigation`: ページ遷移を待つ
- `wait`: 指定秒数待機
- `select`: ドロップダウンから選択

## 🤝 貢献方法

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m '✨ feat: 素晴らしい機能を追加'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📜 ライセンス

MIT