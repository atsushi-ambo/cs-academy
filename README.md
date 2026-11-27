# CS Academy

Python の Lists を、短いステップと復習で学ぶ macOS 向けローカルアプリです。P0 では、サンプル教材の Read、Predict、Try it、Parsons、Fix、Code の21ステップをブラウザで進められます。レッスンの参照シートと端末ハンズオンの手順は Today の「教材を読む」から開けます。

## 起動

Python 3.13 を使うための uv と、起動済みの Docker Engine（Docker Desktop や OrbStack）が必要です。ランナーは Mac 内の Unix ソケットへ接続します。セットアップで uv が Python 3.13 の環境を選び、`uv.lock` の PyYAML をインストールします。
テストを実行する場合は Node.js 22 以上も用意します。

```sh
make setup
make runner-image
make run
```

ターミナルに `CS Academy is ready at http://127.0.0.1:4350` と出たら、その URL を開きます。初回起動時に `data/`（0700）と学習用 SQLite が作られます。終了はターミナルで Ctrl+C を押します。

## 学習

- **Today** に Lists の進捗、累計 XP、Daily quest、今日の復習数とストリークが出ます。15分モードでは、今日の復習または学習のクエストを1つ表示します。
- **Play** の **Run** はコードに「標準入力」の内容を渡します。**Run tests** はサーバーが選んだテストで判定します。コード課題の失敗回数と合格 XP は Run tests で更新されます。ヒントを開くと合格時の XP が減り、模範解答は合格後か Run tests で3回失敗した後に開きます。
- **Review Arena** は FSRS-5 による出題日にカードを表示します。1日最大10問を5分の目安で進めます。間違えたカードはラウンド終盤にもう一度出ます。正解は Good、不正解は Again で記録し、Play でヒントを使った正解は一段階ずつ下げます。
- **Placement** は Lists の四択4問と専用のコード課題1問です。四択3問以上とコード課題の合格でスキップを選べます。スキップした場合は未登録の四択を1日2枚ずつ追加します。復習で不正解になると Today に Lists が再表示されます。

Docker またはイメージが起動できない場合は、結果欄に理由が表示されます。Docker Engine が起動していることを確認し、イメージがない場合は `make runner-image` を実行します。起動失敗では、テスト失敗回数や XP は変わりません。コード実行は10秒で打ち切り、出力は stdout と stderr にそれぞれ16 KiBまで保持します。

## バックアップと復元

「バックアップ」画面で作成済みのバックアップを確認し、選んで復元できます。既存の学習データがある場合、復元前にその状態も別のバックアップとして保存します。

CLI でも同じ操作ができます。既定の保存先は `~/cs-academy-backups` です。変更する場合は、リポジトリ外に 0700 のディレクトリを用意し、`CS_ACADEMY_BACKUP_DIR` をサーバーと CLI に同じ値で指定します。

```sh
make backup
make restore BACKUP=20261127T190000-0123456789ab
```

1. `make backup` が表示した日付付きフォルダの名前を控えます。その中の `academy.sqlite3` が SQLite のオンラインバックアップです。
2. `BACKUP=` に復元するフォルダ名を指定します。別の Mac では、日付付きフォルダごとバックアップディレクトリへ移してから復元します。
3. `Restored ...` が出たら、Today と Review Arena を開き、学習進捗と復習数を確認します。

P0 の永続データは SQLite にあります。エディタの未提出の下書きはブラウザのタブ内に保存されます。

## 検証

`make test` と `make test-web` の実行前に、`node --version` で Node.js 22 以上を確認します。CI は Node.js 22 を使います。

| コマンド | 成功の目安 |
| --- | --- |
| `make lint` | Ruff と教材検証が成功する |
| `make test` | Web、教材、FSRS、XP、配置テスト、バックアップと復元、HTTP と Docker のテストが成功する |
| `make test-web` | Web のテストが成功する |
| `make test-docker` | Docker の起動、隔離、出力上限、実コードの合否と Lists の TCP e2e が成功する |
| `make audit` | `uv.lock` から抽出した依存を pip-audit が検査する |

Docker に接続できない場合、通常のテストは Docker の項目をスキップします。Docker に接続できてイメージが見つからない場合は失敗します。TCP の待ち受けが制限される環境では、通常テストの TCP 項目がスキップされます。CI では Docker と TCP の確認が必須です。週次・手動の監査では Python 依存とランナーイメージを検査します。
