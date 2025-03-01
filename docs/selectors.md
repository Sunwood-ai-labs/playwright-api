# 🧩 拡張セレクタ機能

PlaywrightAPIは、より柔軟で強力なセレクタ定義をサポートしています。従来の単純な文字列セレクタに加えて、詳細なセレクタ定義オブジェクトを使用できます。

## 📝 基本的な使い方

```json
{
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
```

## 🔢 セレクタタイプ

- `css`: CSSセレクタ (デフォルト)
- `xpath`: XPathセレクタ
- `text`: テキスト内容によるセレクタ

## 🔄 変換処理

- `text`: テキスト内容を抽出 (デフォルト)
- `html`: HTML内容を抽出
- `attribute:name`: 指定した属性の値を抽出 (例: `attribute:href`, `attribute:src`)

## ⚙️ オプション設定

- `optional`: `true`の場合、要素が見つからなくてもエラーにならない
- `fallback`: 要素が見つからない場合のデフォルト値

## 🔗 複合セレクタ

複数のセレクタを組み合わせて論理演算を行う複合セレクタもサポートしています。

```json
{
  "has_login_form": {
    "operator": "or",
    "selectors": [
      "form.login",
      "input[type='password']",
      {
        "type": "css",
        "value": ".login-button"
      }
    ],
    "transform": "text",
    "optional": true,
    "fallback": "false"
  }
}
```

### 🔗 複合演算子

- `and`: すべてのセレクタが一致した場合のみ結果を返す
- `or`: いずれかのセレクタが一致した場合に結果を返す
- `not`: セレクタが一致しない場合に結果を返す
- `chain`: セレクタを順番に適用する（最初のセレクタから始めて、その結果に次のセレクタを適用）

## 📝 使用例

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

# HTMLファイルを保存する場合
result = client.start_scraping(
    "https://example.com", 
    selectors=selectors, 
    save_html_file=True, 
    html_output_dir="output/html_files"
)
task_id = result["task_id"]
data = client.wait_for_completion(task_id)
print(data["result"]["data"])

# HTMLファイルのパスを確認
if "html_file" in data["result"]:
    print(f"HTMLファイルが保存されました: {data['result']['html_file']}")
```

詳細な例は `examples/selectors.json` と `examples/compound_selectors.json` を参照してください。
