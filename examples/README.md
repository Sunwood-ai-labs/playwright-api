# PlayScraperAPI クライアント使用例

このディレクトリには、PlayScraperAPIクライアントの使用例が含まれています。

## ファイル構成

- `selectors.json` - スクレイピングで抽出するデータのセレクタ定義
- `actions.json` - スクレイピング前に実行するアクションの定義
- `package_client.py` - インストールしたパッケージを使用した例（同期・非同期）

## 使用例

### 基本的な使用方法

```bash
# 基本的なスクレイピング（セレクタとアクションなし）
python playscraper_api_cli.py https://example.com

# セレクタを指定してスクレイピング
python playscraper_api_cli.py https://example.com --selectors examples/selectors.json

# アクションを指定してスクレイピング
python playscraper_api_cli.py https://example.com --actions examples/actions.json

# セレクタとアクションの両方を指定
python playscraper_api_cli.py https://example.com --selectors examples/selectors.json --actions examples/actions.json

# 結果をJSONファイルに保存
python playscraper_api_cli.py https://example.com --output result.json

# HTMLとスクリーンショットを自動的に保存
python playscraper_api_cli.py https://example.com --save-output

# タイムアウトと確認間隔を指定
python playscraper_api_cli.py https://example.com --timeout 120 --interval 2
```

### カスタムAPIエンドポイントの指定

```bash
# カスタムAPIエンドポイントを指定
python playscraper_api_cli.py https://example.com --api-url http://custom-api-server:8000
```

### パッケージを使用した例

パッケージをインストールした後に使用できる `package_client.py` の例も用意されています：

```bash
# パッケージを使用した例を実行
python examples/package_client.py
```

この例では、同期クライアントと非同期クライアントの両方の使用方法を示しています。
インストールされた `playscraper-api-client` パッケージを使用して、実際のウェブサイトからデータを抽出し、結果をJSONファイルに保存します。

注意：インストール方法によってインポート文が異なります：
```python
# 通常のインストール時（pip install playscraper-api-client）
from playscraper_api_client import PlayScraperClient

# 開発モードでのインストール時（pip install -e .）- 現在の実装
from client import PlayScraperClient
```

## 出力ファイル

`--save-output`オプションを使用すると、以下のファイルが`output`ディレクトリに保存されます：

- `{ドメイン}_{パス}.html` - スクレイピングしたページのHTML
- `{ドメイン}_{パス}.png` - スクレイピングしたページのスクリーンショット

例えば、`https://example.com/page`をスクレイピングした場合：
- `output/example_com_page.html`
- `output/example_com_page.png`

## セレクタの例

```json
{
  "title": "h1",
  "description": "meta[name='description']",
  "links": "a.nav-link",
  "main_content": ".main-content p"
}
```

## アクションの例

```json
[
  {
    "type": "wait",
    "value": "2"
  },
  {
    "type": "click",
    "selector": ".accept-cookies"
  },
  {
    "type": "wait",
    "value": "1"
  }
]
