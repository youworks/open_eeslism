from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, sys
import subprocess
import tempfile
import shutil
from subprocess import PIPE

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
EESLISM_PATH = 'eeslism'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/', methods=['POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            with tempfile.TemporaryDirectory() as tempdirname:
                # 入力ファイルの保存
                file.save(os.path.join(tempdirname, 'sample.txt'))
                # 関連データのコピー
                wd_dir = os.path.join(tempdirname, "wd")
                os.mkdir(wd_dir)
                data_dir = os.path.join(os.path.dirname(__file__), "resource")
                shutil.copy(
                    os.path.join(data_dir, "wd", "6_Tokyo2010_watanabe.has"),
                    os.path.join(wd_dir, "6_Tokyo2010_watanabe.has")
                )
                shutil.copy(
                    os.path.join(data_dir, "dayweek.efl"),
                    os.path.join(tempdirname, "dayweek.efl")
                )
                shutil.copy(
                    os.path.join(data_dir, "supw.efl"),
                    os.path.join(tempdirname, "supw.efl")
                )
                shutil.copy(
                    os.path.join(data_dir, "wbmlist.efl"),
                    os.path.join(tempdirname, "wbmlist.efl")
                )

                # 実行
                proc = subprocess.Popen([EESLISM_PATH, "sample.txt", "-nstop", "-delay"], cwd=tempdirname, stdout=PIPE, stderr=PIPE, text=True)
                buf = []

                while True:
                    # バッファから1行読み込む.
                    line = proc.stdout.readline()
                    buf.append(line)
                    sys.stdout.write(line)

                    # バッファが空 + プロセス終了.
                    if not line and proc.poll() is not None:
                        break

                # 画面出量
                output_str = ''.join(buf)

                # 結果読み出し用関数
                def readall(fname):
                    with open(os.path.join(tempdirname, 'sample{}'.format(fname)), mode="r") as fp:
                        txt = fp.read()
                        fp.close()
                    return txt

                # 建物シミュレーション結果
                rm = readall('_rm.es')

                # 月・時刻集計値
                mt = readall('_mt.es')

            return rm

    return 'FAIL'

if __name__ == '__main__':
    app.run(debug=False)

