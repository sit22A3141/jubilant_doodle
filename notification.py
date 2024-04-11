# こちらは色んな媒体にプログラム終了時などに簡単にメッセージを送るためのモジュールです。
# 必ず一読してから使用してください。

#以下の1,2のどちらかの方法でインポートし、利用出来ます(1を推奨)
# どちらの場合においても最初に下のLIEN,SLACK,DISCODEのうち使う予定の物の設定を完了させてください

# 1.githubを用いる場合
"""
まずgithubにこのpython fileをprivate(*)の設定でアップロードしてください。(*:keyの漏洩を防ぐため)
緑色のCodeボタンを押してLocalのタブのHTTPSを選択し、「!git clone https://github.com/***/notification.git」のような文章をコピーしてください。

実際に使う際は下記のように記述することで利用できるようになります(importの後に記述するのはLINE, DISCORD, SLACKのうち使いたい物のみで大丈夫です)
---------------------------program--------------------------
!git clone https://github.com/***/notification.git
from notification.notification import LINE, DISCORD, SLACK
---------------------------program--------------------------
"""

# 2.google driveを用いる場合
"""
まず、このファイルをgoogle driveにMy_Moduleというフォルダを作り、そこにこのファイルを格納してください。
その後、google colabなどで以下のプログラムをコピペすることでインストールできます。
----------------program---------------
# GoogleDriveのマウント
from google.colab import drive
drive.mount('/content/drive')
# notificationのそれぞれのクラスをインポート
from drive.MyDrive.My_Module.notification import LINE, DISCORD, SLACK
----------------program---------------
"""

# 使う際は次のように記述します。
"""
LINEに送る為のコマンド
LINE()

Slackに送る為のコマンド
SLACK()

Discordに送る為のコマンド
DISCORD()

デフォルトだとそれぞれの__init__内に記述した文章を送信します
google colabなどで使用する際、LINE()などの引数であるtext=を指定して文章を書くとその文章を送ることができます
さらに、files=に画像の名前を指定すると画像も送れます(SLACKのみ対応していません)
(google colab内の変数などを送りたいとき、任意の文章を送信したいときに使用を想定)
"""

# コマンド使用例
"""
LINE() ----> AIのプログラムが終了しました。 (デフォルト文)が送信される
LINE(text="hello world !") ----> hello world ! (指定した文のみ)が送信される
LINE(file="test.png") ----> AIのプログラムが終了しました。 + test.png (デフォルト文+指定した画像)が送信される
LINE(text="hello world !", file="test.png") ----> hello world ! + test.png (指定した文+指定した画像)が送信される
LINE(text="", file="test.png") ----> 何も送信されない
LINE(text=" ", file="test.png") ----> 画像のみ送信

LINE(f"loss:{loss}")  このように書くことで変数の値を送ることも可能です

文を改行したいときは\nを用いることで実現できます
"""

# Lineに送信する関数
def LINE(text = None, file = None):
    # self.TOKENに自分のline-notifyのトークンを入力　**必須です**
    # TOKENの取得はこちらからできます。→　https://notify-bot.line.me/ja/
    TOKEN = ""
    
    # self.api_urlは何も変更しないでください
    api_url = 'https://notify-api.line.me/api/notify'
    
    # self.send_contentsにデフォルト文の設定
    send_contents = "AIのプログラムが終了しました。"
    
    # requestsで送るために辞書化
    TOKEN_dic = {'Authorization': 'Bearer' + ' ' + TOKEN}
    send_dic = {'message': send_contents}

    if text is not None:
        send_contents = text
        send_dic = {'message': send_contents}
    try:
        if file is None:
            requests.post(api_url, headers=TOKEN_dic, data=send_dic)
        else:
            requests.post(api_url, headers=TOKEN_dic, data=send_dic, files = {"imageFile": open(file, "rb")})
    except:
        import requests
        if file is None:
            requests.post(api_url, headers=TOKEN_dic, data=send_dic)
        else:
            requests.post(api_url, headers=TOKEN_dic, data=send_dic, files = {"imageFile": open(file, "rb")})
    print("LINEにメッセージを送信しました。")

# Slackに送信する関数
def SLACK(text = None):
    # self.webhook_urlに送りたい場所のwebhook urlを入力
    # urlの取得はこちらからできます。→　https://slack.com/services/new/incoming-webhook
    webhook_url = "https://hooks.slack.com/services/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"
    
    # self.textに送りたい文章を入力
    content = "AIのプログラムが終了しました。"
    
    # requestsで送るために辞書化
    text_dic = {"text":content}

    if text is not None:
        content = text
        text_dic = {"text":content}
    try:
        requests.post(webhook_url, data = json.dumps(text_dic))
    except:
        import requests, json
        requests.post(webhook_url, data = json.dumps(text_dic))
    print("SLACKにメッセージを送信しました。")

# Discordに送信する関数
def DISCORD(text = None, files = None):
    # self.webhook_urlに送りたい場所のwebhook urlを入力
    # urlの取得はこちらを参照してください。→　https://qiita.com/otuhs_d/items/41f018ec3762db93a740
    # 現在webhookは送りたいテキストチャンネルの設定内の連携サービスの中で設定ができます。
    webhook_url = ""
    
    # self.contntに送りたい文章を入力
    content = "AIのプログラムが終了しました。"
    
    # requestsで送るために辞書化
    content_dic = {"content": content}
    headers = {"Content-Type": "application/json"}

    if text is not None:
        content = text
        content_dic = {"content": content}
    elif files is not None:
        with open(files, "rb") as f:
            file_bin = f.read()
            file = {"favicon":(files,file_bin),}
    try:
        if files is None:
            requests.post(webhook_url, json.dumps(content_dic), headers = headers)
            print("Discordにメッセージを送信しました。")
        else:
            requests.post(webhook_url, files = file)
            print("Discordにメッセージと画像を送信しました。")
    except:
        import requests, json
        if files is None:
            requests.post(webhook_url, json.dumps(content_dic), headers = headers)
            print("Discordにメッセージを送信しました。")
        else:
            requests.post(webhook_url, files = file)
            print("Discordにメッセージと画像を送信しました。")