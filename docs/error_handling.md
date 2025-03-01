# 🚨 エラーハンドリング

PlaywrightAPIは、スクレイピング中に発生したエラーを詳細に記録し、結果に含めることができます。これにより、どのセレクタが問題を引き起こしたのかを特定しやすくなります。

## 📝 エラー情報の構造

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

## 🔢 エラータイプ

- `error`: 重大なエラーで、要素が見つからないか処理に失敗した場合
- `warning`: 軽度の警告で、オプショナルな要素が見つからないか、フォールバック値が使用された場合

## 📝 エラーメッセージの例

- `要素が見つかりませんでした`: 指定されたセレクタに一致する要素がページ内に存在しない
- `変換処理エラー`: 要素は見つかったが、指定された変換処理（text, html, attributeなど）の適用に失敗した
- `セレクタ検索エラー`: セレクタの構文が無効であるか、検索処理中にエラーが発生した
- `データ抽出エラー`: その他の一般的なエラー

## 📝 エラーハンドリングの例

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
