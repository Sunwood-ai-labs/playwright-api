# 🎮 サポートされているアクション

PlaywrightAPIでは、スクレイピング前にページに対して様々なアクションを実行できます。これにより、ログイン、フォーム入力、ボタンクリックなどの複雑な操作を自動化できます。

## 🔍 利用可能なアクションタイプ

- `click`: 要素をクリック
- `type`: テキストを入力
- `wait_for_selector`: セレクタが表示されるのを待つ
- `wait_for_navigation`: ページ遷移を待つ
- `wait`: 指定秒数待機
- `select`: ドロップダウンから選択

## 📝 アクション定義の例

アクションは以下のような形式でJSON配列として定義します：

```json
[
  {
    "type": "click",
    "selector": ".login-button"
  },
  {
    "type": "type",
    "selector": "#username",
    "value": "testuser"
  },
  {
    "type": "type",
    "selector": "#password",
    "value": "password123"
  },
  {
    "type": "click",
    "selector": "button[type='submit']"
  },
  {
    "type": "wait_for_navigation",
    "options": {
      "waitUntil": "networkidle"
    }
  },
  {
    "type": "wait",
    "value": "2"
  }
]
```

## 🔍 各アクションタイプの詳細

### click

指定したセレクタの要素をクリックします。

```json
{
  "type": "click",
  "selector": ".button-class",
  "options": {
    "button": "left",
    "clickCount": 1,
    "delay": 100
  }
}
```

### type

指定したセレクタの要素にテキストを入力します。

```json
{
  "type": "type",
  "selector": "#search-input",
  "value": "検索キーワード",
  "options": {
    "delay": 50
  }
}
```

### wait_for_selector

指定したセレクタの要素が表示されるのを待ちます。

```json
{
  "type": "wait_for_selector",
  "selector": ".content-loaded",
  "options": {
    "state": "visible",
    "timeout": 30000
  }
}
```

### wait_for_navigation

ページ遷移が完了するのを待ちます。

```json
{
  "type": "wait_for_navigation",
  "options": {
    "waitUntil": "networkidle",
    "timeout": 30000
  }
}
```

### wait

指定した秒数だけ待機します。

```json
{
  "type": "wait",
  "value": "5"
}
```

### select

ドロップダウンメニューから選択肢を選びます。

```json
{
  "type": "select",
  "selector": "#dropdown",
  "value": "option2",
  "options": {
    "timeout": 5000
  }
}
```

## 📋 アクションの実行例

```python
from client import PlayScraperClient

client = PlayScraperClient()

# アクションを定義
actions = [
    {
        "type": "click",
        "selector": ".cookie-consent-button"
    },
    {
        "type": "type",
        "selector": "#search",
        "value": "スマートフォン"
    },
    {
        "type": "click",
        "selector": ".search-button"
    },
    {
        "type": "wait_for_navigation"
    }
]

# スクレイピングを実行
result = client.start_scraping(
    "https://example.com", 
    selectors={"products": ".product-item"}, 
    actions=actions
)

task_id = result["task_id"]
data = client.wait_for_completion(task_id)
print(data["result"]["data"])
```

## ⚠️ 注意点

- アクションはリクエストで指定した順序通りに実行されます
- タイムアウトはオプションで指定できますが、デフォルトでは30秒です
- 複雑なアクションの場合は、適切な待機時間や条件を設定することをお勧めします
