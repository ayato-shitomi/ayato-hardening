

# シナリオ

1分毎にサーバーにチェックが入り以下の項目がすべてクリアであればポイントが10ポイント加算される

- 80番ポートにてWEBサーバーが稼働している

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