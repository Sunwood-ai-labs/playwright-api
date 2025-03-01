# 🎭 PlaywrightAPI クライアント

<p align="center">
  <img src="../assets/header.svg" alt="PlaywrightAPI Client" width="800">
</p>

## 🌟 概要

PlaywrightAPIを簡単に利用するためのクライアントライブラリです。このパッケージを使用することで、PlaywrightとPythonを使用したウェブスクレイピングAPIサーバーと簡単に連携できます。

## 🚀 インストール

```bash
# リポジトリからインストール
git clone https://github.com/Sunwood-ai-labs/playwright-api.git
cd playwright-api
pip install -e .

# または直接インストール (将来的にPyPIに公開される場合)
pip install playscraper-api-client
```

## 📋 特徴

- 🔄 同期・非同期APIのサポート
- 🛠️ シンプルで直感的なインターフェース
- 📊 豊富なセレクタオプション
- 🖼️ スクリーンショットと結果の自動保存
- 🧩 拡張性の高い設計

## 📋 使用方法

パッケージをインポートする際の注意点：
```python
# 通常のインストール時（pip install playscraper-api-client）
from playscraper_api_client import PlayScraperClient

# 開発モードでのインストール時（pip install -e .）
from client import PlayScraperClient
```

## 💻 使用例

### 基本的な使い方

```python
from playscraper_api_client import PlayScraperClient

# クライアントの初期化
client = PlayScraperClient("http://localhost:8001")

# APIの状態確認
status = client.check_status()
print(f"API状態: {status['status']} - {status['message']}")

# スクレイピング実行
url = "https://example.com"
selectors = {
    "title": "h1",
    "description": "p"
}

# スクレイピングタスク開始
task = client.start_scraping(url, selectors)
task_id = task["task_id"]

# タスク完了を待機
result = client.wait_for_completion(task_id)

# 結果の出力
print(f"タイトル: {result['result']['data']['title']}")
print(f"説明: {result['result']['data']['description']}")
```

### 非同期APIの使用

```python
import asyncio
from playscraper_api_client import PlayScraperClient

async def main():
    # クライアントの初期化
    client = PlayScraperClient("http://localhost:8001")
    
    # APIの状態確認（非同期）
    status = await client.check_status_async()
    
    # スクレイピングタスク開始（非同期）
    task = await client.start_scraping_async(
        "https://example.com", 
        {"title": "h1", "description": "p"}
    )
    
    # タスク完了を待機（非同期）
    result = await client.wait_for_completion_async(task["task_id"])
    
    # セッションのクローズ
    await client.close_async_sessions()
    
    return result

# 非同期メイン関数の実行
result = asyncio.run(main())
```

### コマンドライン使用

```bash
# 基本的な使用方法
python -m client https://example.com

# セレクタとアクションファイルを指定
python -m client https://example.com --selectors examples/selectors.json --actions examples/actions.json

# 結果の保存と詳細ログの出力
python -m client https://example.com --save-output --verbose
```

## 📦 モジュール構成

- `api.py` - APIクライアントの中核機能
- `cli.py` - コマンドラインインターフェース
- `output.py` - 結果処理ユーティリティ
- `session.py` - セッション管理
- `utils.py` - 汎用ユーティリティ関数

## 🔧 詳細設定

```python
# 詳細なセレクタ設定の例
selectors = {
    "title": "h1",  # 単純なセレクタ
    "meta_description": {  # 拡張セレクタ
        "type": "css",
        "value": "meta[name='description']",
        "transform": "attribute:content",
        "optional": True
    },
    "has_login": {  # 複合セレクタ
        "operator": "or",
        "selectors": [
            "form.login",
            "input[type='password']"
        ],
        "optional": True,
        "fallback": "false"
    }
}

# スクレイピング前のアクション定義の例
actions = [
    {
        "type": "click",
        "selector": ".cookie-accept"
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

# 結果の保存
client.start_scraping(
    "https://example.com",
    selectors=selectors,
    actions=actions,
    save_html_file=True,
    html_output_dir="output/html"
)
```

## 📚 詳細ドキュメント

より詳細な使い方については、[メインのREADME](../README.md)や`examples`ディレクトリのサンプルコードを参照してください。

## 🤝 貢献

バグ報告や機能リクエストは[GitHub Issues](https://github.com/Sunwood-ai-labs/playwright-api/issues)にお願いします。プルリクエストも歓迎します！

## 📜 ライセンス

MIT
