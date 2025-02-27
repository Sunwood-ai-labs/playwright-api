# PlayScraperAPI クライアント使用例

このディレクトリには、PlayScraperAPIクライアントの使用例が含まれています。

## ファイル構成

- `selectors.json` - スクレイピングで抽出するデータのセレクタ定義
- `actions.json` - スクレイピング前に実行するアクションの定義

## 使用例

### 基本的な使用方法

```bash
# 基本的なスクレイピング（セレクタとアクションなし）
python client.py https://example.com

# セレクタを指定してスクレイピング
python client.py https://example.com --selectors examples/selectors.json

# アクションを指定してスクレイピング
python client.py https://example.com --actions examples/actions.json

# セレクタとアクションの両方を指定
python client.py https://example.com --selectors examples/selectors.json --actions examples/actions.json

# 結果をJSONファイルに保存
python client.py https://example.com --output result.json

# HTMLとスクリーンショットを自動的に保存
python client.py https://example.com --save-output

# タイムアウトと確認間隔を指定
python client.py https://example.com --timeout 120 --interval 2
```

### カスタムAPIエンドポイントの指定

```bash
# カスタムAPIエンドポイントを指定
python client.py https://example.com --api-url http://custom-api-server:8000
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
```
