# 💻 コマンドラインからの使用

PlayScraperAPIクライアントはコマンドラインからも使用できます。

## 🔍 基本的な使用方法

```bash
# 基本的な使用方法
python client.py https://example.com

# HTMLファイルを保存する場合
python client.py https://example.com --save-output --html-dir output/html_files

# セレクタとアクションを指定する場合
python client.py https://example.com --selectors examples/selectors.json --actions examples/actions.json

# 詳細なログを表示する場合
python client.py https://example.com -v
```

## 🛠️ コマンドラインオプション

| オプション | 説明 |
|------------|------|
| `url` | スクレイピング対象のURL（必須） |
| `--api-url` | PlayScraperAPIのURL（デフォルト: http://localhost:8001） |
| `--selectors` | セレクタのJSONファイルパス |
| `--actions` | アクションのJSONファイルパス |
| `--timeout` | タイムアウト時間（秒）（デフォルト: 60.0） |
| `--interval` | ステータス確認の間隔（秒）（デフォルト: 1.0） |
| `--output` | 結果を保存するJSONファイルパス（デフォルト: output.json） |
| `--verbose`, `-v` | 詳細なログを表示 |
| `--save-output` | HTMLとスクリーンショットをファイルとして保存する |
| `--html-dir` | HTMLファイルとスクリーンショットを保存するディレクトリ（デフォルト: output/html） |

## 📝 HTMLファイルの保存について

PlayScraperAPIでは、HTMLファイルを保存する方法が2つあります：

1. **🖥️ サーバー側での保存**：
   - APIリクエスト時に `save_html_file: true` を指定すると、サーバー側でHTMLファイルが保存されます。
   - 保存先ディレクトリは `html_output_dir` パラメータで指定できます（デフォルト: "output/html"）。

2. **💻 クライアント側での保存**：
   - クライアントコマンドで `--save-output` オプションを指定すると、クライアント側でHTMLファイルが保存されます。
   - 保存先ディレクトリは `--html-dir` オプションで指定できます（デフォルト: "output/html"）。
   - この方法では、スクリーンショットも同じディレクトリに保存されます。

どちらの方法でも、ファイル名はURLから自動的に生成されます。例えば、`https://example.com/page` というURLの場合、`example_com_page.html` というファイル名になります。
