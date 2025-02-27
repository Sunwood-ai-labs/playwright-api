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