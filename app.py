from crypt import methods
from distutils.log import debug
from unicodedata import name
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/search_race')
def search_race():
    return render_template('search_race.html')

@app.route('/results', methods=['GET','POST'])
def results():
    if request.method == 'POST':
        try:
            where = request.form.get('where')
            when = request.form.get("when")
            when = when.replace("-","/")
            number = request.form.get('number')
            sql = f"SELECT horse_pred FROM keiba WHERE day = '{when}' and place = '{where}' and race_num = {number}"
            users = 'yuzzebkekzwcou'     # DBにアクセスするユーザー名(適宜変更)
            dbnames = 'd77ip9uahjv90s'   # 接続するデータベース名(適宜変更)
            passwords = '981e62df5355aa7a7274b6939261583311d61eb03883dccc7447992bcc0a0e28' # DBにアクセスするユーザーのパスワード(適宜変更)
            host = "ec2-3-220-207-90.compute-1.amazonaws.com"      # DBが稼働しているホスト名(適宜変更)
            port = 5432
            conn = psycopg2.connect("user=" + users +" dbname=" + dbnames +" password=" + passwords, host=host, port=port)
            cur = conn.cursor()
            cur.execute(sql)
            for row in cur:
                pred_text_li = row[0].split("\n")
            conn.commit()
            cur.close()
            conn.close()
            return render_template('results.html',pred_text_li=pred_text_li)
        except:
            error_text = '該当日にレースがない、又はレースデータが登録されていません'
            return render_template('search_race.html',error_text = error_text)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)