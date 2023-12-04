
# 概要

40分のハードニングイベントを作ってみた

# ルール

- 

# シナリオ

## ベーススコア

1分毎にサーバーにチェックが入り以下の項目がすべてクリアであればポイントが10ポイント加算される

- 80番ポートにてWEBサーバーが稼働している

## アディショナルスコア

攻撃を防ぐごとに以下のポイントが加算される

|時間|イベント|内容|ポイント|
|:--|:--|:--|:--|
|0min|スタート|||
|10min|ユーザーへのブルートフォース|不正なユーザーが作成される<br>WEBサーバーが停止する|+50<br>+50|
|20min|vsftpdへの攻撃|RCEにより不正なShellがアップロードされる<br>Shellにより不正なファイルがアップロードされる|+50<br>+100|
|25min|クレデンシャル情報の流出|クレデンシャル情報が流出する<br>devユーザーが不正な通信を始める|+50<br>+100|
|30min|WEBアプリへの攻撃|サイト内容が改ざんされる<br>サーバーが停止する|+100<br>+100|
|40min|終了|||

## 競技終了時のポイント

|スコア部類|内容|ポイント|
|:--|:--|:--|
|ベーススコア|すべてのリクエストが通った|400ポイント|
|アディショナルスコア|すべての攻撃を防いだ|600ポイント|
|**合計**||**1000ポイント**|

# レッドチームメモ

## ユーザーへのブルートフォース

デフォルトのユーザーへの攻撃を行う

- root: root
- user1: user1
- user6: user6
- user11: pass

侵入された場合

- `sg`ユーザーが作成される
- `systemctl stop http-flask.service`でWEBサーバーが停止する

## vsftpdの脆弱性を利用した攻撃

vsftpdの脆弱性を利用した攻撃を行う

- RCEにより侵入される

侵入された場合

- `sudo useradd test`により`test`ユーザーが作られる

## クレデンシャル情報の流出

WEBサーバーよりクレデンシャル情報が流出する

- `:8080/README.md`にリクエストが来る
- クレデンシャル情報が流出する

侵入された場合

- `dev`ユーザーが侵害される（`dev`/`devpass123`）
- 不正なファイルが`/var/www/html/hacked`作成される

## WEBアプリへの攻撃

SSTIでWEBアプリへの攻撃を行う

- WEBサーバーに攻撃が来る
- SSTIでUFWのルールが追加される

```
{{request.application.__globals__.__builtins__.__import__('os').popen('whoami').read()}}
```

```
{{request.application.__globals__.__builtins__.__import__(%27os%27).popen(%27systemctl%20stop%20http-flask.service%27).read()}}
```

# todo 

- すべてのシステムでuser.shを実行する
- vsftpdの脆弱性を発生させる

