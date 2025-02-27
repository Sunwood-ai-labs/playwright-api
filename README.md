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

### 複合セレクタ

複数のセレクタを組み合わせて論理演算を行う複合セレクタもサポートしています。

```json
{
  "has_login_form": {                   // 複合セレクタ定義
    "operator": "or",                   // 論理演算子 (and, or, not, chain)
    "selectors": [                      // セレクタのリスト
      "form.login",                     // 単純な文字列セレクタ
      "input[type='password']",
      {                                 // 拡張セレクタ定義も使用可能
        "type": "css",
        "value": ".login-button"
      }
    ],
    "transform": "text",                // 変換処理
    "optional": true,                   // 省略可能かどうか
    "fallback": "false"                 // 見つからない場合のデフォルト値
  }
}
```

#### 複合演算子

- `and`: すべてのセレクタが一致した場合のみ結果を返す
- `or`: いずれかのセレクタが一致した場合に結果を返す
- `not`: セレクタが一致しない場合に結果を返す
- `chain`: セレクタを順番に適用する（最初のセレクタから始めて、その結果に次のセレクタを適用）

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
    "is_article_page": {
        "operator": "and",
        "selectors": [
            "article",
            ".content",
            ".published-date"
        ],
        "optional": true,
        "fallback": "false"
    }
}

result = client.start_scraping("https://example.com", selectors=selectors)
task_id = result["task_id"]
data = client.wait_for_completion(task_id)
print(data["result"]["data"])
```

詳細な例は `examples/selectors.json` と `examples/compound_selectors.json` を参照してください。

## 🚨 エラーハンドリング

PlayScraperAPIは、スクレイピング中に発生したエラーを詳細に記録し、結果に含めることができます。これにより、どのセレクタが問題を引き起こしたのかを特定しやすくなります。

### エラー情報の構造

```json
{
  "url": "https://example.com",
  "data": {
    "title": "Example Domain",
    "description": null,
    "price": "¥1,980"
  },
  "errors": {
    "description": {
      "type": "error",
      "message": "要素が見つかりませんでした",
      "selector": {
        "type": "css",
        "value": "meta[name='description']",
        "transform": "attribute:content"
      }
    }
  }
}
```

### エラータイプ

- `error`: 重大なエラーで、要素が見つからないか処理に失敗した場合
- `warning`: 軽度の警告で、オプショナルな要素が見つからないか、フォールバック値が使用された場合

### エラーメッセージの例

- `要素が見つかりませんでした`: 指定されたセレクタに一致する要素がページ内に存在しない
- `変換処理エラー`: 要素は見つかったが、指定された変換処理（text, html, attributeなど）の適用に失敗した
- `セレクタ検索エラー`: セレクタの構文が無効であるか、検索処理中にエラーが発生した
- `データ抽出エラー`: その他の一般的なエラー

### エラーハンドリングの例

```python
from client import PlayScraperClient

client = PlayScraperClient()

# スクレイピングを実行
result = client.start_scraping("https://example.com", selectors={
    "title": "h1",
    "description": {
        "type": "css",
        "value": "meta[name='description']",
        "transform": "attribute:content"
    }
})

task_id = result["task_id"]
data = client.wait_for_completion(task_id)

# エラーの確認と処理
if "errors" in data["result"]:
    for key, error in data["result"]["errors"].items():
        print(f"エラー ({key}): {error['message']}")
        print(f"セレクタ: {error['selector']}")
        print(f"タイプ: {error['type']}")
        print("---")

# データの処理
print("抽出されたデータ:")
for key, value in data["result"]["data"].items():
    print(f"{key}: {value}")
```

オプショナルなセレクタやフォールバック値を使用することで、エラーが発生してもスクレイピングを続行し、可能な限りデータを抽出することができます。

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