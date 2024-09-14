
# 概要

40分のハードニングイベントを作ってみた

# 起動

```bash
# やられサーバーの起動
docker-compose up -d

# スコアボードの起動
python3 ./white-team/score.py

# スコアBOTの起動
python3 ./red-team/check.py
# 攻撃BOTの起動
python3 ./red-team/main.py
```

## ポートの解放

```
# IPアドレス1 (192.168.1.100) から許可
sudo ufw allow proto tcp from 192.168.1.100 to any port 11021:18021
sudo ufw allow proto tcp from 192.168.1.100 to any port 11022:18022
sudo ufw allow proto tcp from 192.168.1.100 to any port 11080:18080
sudo ufw allow proto tcp from 192.168.1.100 to any port 11081:18081
sudo ufw allow proto tcp from 192.168.1.100 to any port 11062:18062
```

# テクニック

```bash
# WEBアプリケーションの起動
python3 /var/www/html/webapp/app.py &>/dev/null &
```

## 堅牢MAX

```bash
for i in {1..11}; do userdel -r user$i; done
userdel dev && userdel ubuntu && echo "root:toor" | chpasswd
pkill -f "/usr/local/sbin/vsftpd /etc/vsftpd.conf"
rm -rf /var/www/html/webapp/README.md && rm -rf /var/www/html/webapp/webapp/README.md && rm -rf /var/www/html/README.md
sed -i 's/<h1>Welcome {}, your browser infomation<\/h1>/<h1>Welcome, your browser infomation<\/h1>/' /var/www/html/webapp/app.py
pkill -f "python3 /var/www/html/webapp/app.py" && python3 /var/www/html/webapp/app.py &>/dev/null &
```

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
|20min|vsftpdへの攻撃|RCEにより侵入される<br>testユーザーが作られる|+50<br>+100|
|25min|クレデンシャル情報の流出|クレデンシャル情報が流出する<br>devユーザーが不正なファイルを作る|+50<br>+100|
|30min|WEBアプリへの攻撃|WEBサーバーに攻撃が来る<br>サーバーが停止する|+100<br>+100|
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
- WEBサーバーが停止する

## vsftpdの脆弱性を利用した攻撃

vsftpdの脆弱性を利用した攻撃を行う

- RCEにより侵入される

侵入された場合

- `useradd test`により`test`ユーザーが作られる

## クレデンシャル情報の流出

WEBサーバーよりクレデンシャル情報が流出する

- `:1x081/README.md`にリクエストが来る
- クレデンシャル情報が流出する

## WEBアプリへの攻撃

SSTIでWEBアプリへの攻撃を行う

- WEBサーバーに攻撃が来る
- サーバーが停止する

1回目のリクエスト

```
/app?name={{request.application.__globals__.__builtins__.__import__("os").popen("whoami").read()}}
```

```
/app?name={{request.application.__globals__.__builtins__.__import__("os").popen("pkill -f 'python3 /var/www/html/webapp/app.py'").read()}}
```


