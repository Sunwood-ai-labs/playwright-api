<div align="center">
  
![Image](https://github.com/user-attachments/assets/044e65b8-5d87-4b00-ba53-f59292cfcf8c)

# 🎭 PlaywrightAPI

</div>

## 🌟 概要

PlaywrightとPythonを使用したウェブスクレイピングAPIサーバー。Docker Composeで簡単に構築・デプロイが可能です。

## ✨ 主な機能

- 🔍 Playwrightを使用した高度なブラウザ自動化でのスクレイピング
- ⚡ 非同期処理によるスケーラブルなAPI設計
- 🖱️ 様々なウェブインタラクション（クリック、タイプ、待機など）のサポート
- 📸 スクリーンショット取得機能
- 📄 HTML全体の取得機能
- 🔄 バックグラウンドタスク処理と状態管理
- 🧩 拡張性の高いセレクタシステム

## 🔧 必要条件

- Docker
- Docker Compose

## 📦 プロジェクト構成

プロジェクトは以下のコンポーネントで構成されています：

- `app/` - APIサーバーとスクレイピングエンジン
- `client/` - Pythonクライアントライブラリ ([詳細はこちら](client/README.md))
- `examples/` - 使用例とサンプルコード
- `assets/` - プロジェクトで使用される静的リソース
- `docs/` - 詳細なドキュメント

## 🚀 クイックスタート

### 🐳 サーバーの起動

```bash
# リポジトリのクローン
git clone https://github.com/Sunwood-ai-labs/playwright-api.git
cd playwright-api

# Docker Composeでサーバーを起動
docker-compose up -d

# ブラウザでAPI確認
# http://localhost:8001/docs にアクセス
```

### 🐍 クライアントライブラリの使用

```bash
# クライアントライブラリのインストール
pip install -e .

# クライアントのインポート
from client import PlayScraperClient

# 使用例
client = PlayScraperClient("http://localhost:8001")
status = client.check_status()
print(f"API状態: {status['status']}")
```

詳細な使用方法は[クライアント README](client/README.md)を参照するか、`examples/`ディレクトリのサンプルコードをご覧ください。

## 📚 詳細ドキュメント

プロジェクトの詳細な情報は以下のドキュメントを参照してください：

- [📡 API エンドポイント](docs/api_endpoints.md) - 利用可能なAPIエンドポイントの詳細説明
- [🧩 拡張セレクタ機能](docs/selectors.md) - 高度なセレクタシステムの使用方法
- [🚨 エラーハンドリング](docs/error_handling.md) - エラー処理とトラブルシューティング
- [🎮 サポートされているアクション](docs/actions.md) - ページ操作アクションの詳細
- [💻 コマンドラインからの使用](docs/command_line.md) - CLIツールの使用方法

## 🤝 貢献方法

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m '✨ feat: 素晴らしい機能を追加'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📜 ライセンス

MIT
