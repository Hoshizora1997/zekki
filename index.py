from bottle import route, run, request, static_file, url, get, post, response, error, abort, redirect, os, \
    TEMPLATE_PATH, jinja2_template as template
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as dt
import uuid

# index.pyが設置されているディレクトリの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# テンプレートファイルを設置するディレクトリのパスを指定
TEMPLATE_PATH.append(BASE_DIR + "/views")

# テンプレートファイル群及びユーザーデータ群へのパス
@route('/css/<filename>')
def css_dir(filename):
    """ set css dir """
    return static_file(filename, root="./static/css")


@route('/js/<filename>')
def js_dir(filename):
    """ set js dir """
    return static_file(filename, root="./static/js")


@route('/img/<filename:path>')
def img_dir(filename):
    """ set img file """
    return static_file(filename, root="./static/img")


@route("/data/<usr_img_filepath:path>")
def usr_img(usr_img_filepath):
    return static_file(usr_img_filepath, root="./data/")

#トップページの表示
@get('/')
def top():
    return template('top')

#フォームの処理および画像処理
@post('/')
def main():
    # フォームから情報を受けとり
    name = request.forms.get('name')
    getupdate = request.forms.get('getupdate')
    getuptime = request.forms.get('getuptime')
    schdate = request.forms.get('schdate')
    schtime = request.forms.get('schtime')
    schdetail = request.forms.get('schdetail')
    reason = request.forms.get('reason')

    # 時刻情報を文字列からdatetimeへ変換
    getupdatetime = dt.strptime(getupdate+" "+getuptime+":00", '%Y-%m-%d %H:%M:%S')
    schdatetime = dt.strptime(schdate+" "+schtime+":00", '%Y-%m-%d %H:%M:%S')

    # 現在時刻を取得
    nowtime = dt.now().strftime('%Y年%m月%d日')

    # 超過時間を計算
    overtime = getupdatetime - schdatetime

    # ================画像合成=================

    # テンプレートの画像を読み込み
    tempImg = Image.open('./temp.png','r')
    tempImgDraw = ImageDraw.Draw(tempImg)

    # フォントの読み込み
    font = ImageFont.truetype('./ipaexm.ttf', 40)
    font2 = ImageFont.truetype('./ipaexm.ttf', 60)

    # 文字情報の合成
    tempImgDraw.text((950, 985), name, font=font, fill='#000')
    tempImgDraw.text((950, 1160), getupdatetime.strftime('%Y年%m月%d日　%H時%M分'), font=font, fill='#000')
    tempImgDraw.text((950, 1350), schdatetime.strftime('%Y年%m月%d日　%H時%M分'), font=font, fill='#000')
    tempImgDraw.text((950, 1400), str(overtime.days)+'日'+str(int(overtime.seconds/3600))+'時間'+str(int(overtime.seconds/60)-int(overtime.seconds/3600)*60)+'分', font=font, fill='#000')
    tempImgDraw.text((950, 1620), schdetail, font=font, fill='#000')
    tempImgDraw.text((950, 2150), reason, font=font, fill='#000')
    tempImgDraw.text((320, 2700), nowtime, font=font2, fill='#000')

    # 保存するファイル名を生成（uuid4を用いたランダム生成）
    filename = str(uuid.uuid4()).replace('-', '') + '.jpg'

    # 保存
    tempImg.save('./data/'+filename, 'JPEG', quality=100, optimize=True)

    # 生成された画像を返す
    return redirect('./data/'+filename)








if __name__ == "__main__":
    # localhost:8080 で公開するように実行
    run(host="localhost", port=10000, debug=True, reloader=True)