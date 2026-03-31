from flask import Flask, render_template, request
from datetime import datetime
import random 

app = Flask(__name__)

# 1. 首頁
@app.route("/")
def index():
    link = "<h1>歡迎進入黃婉凌的網站首頁</h1>"
    link += "<a href=/mis>課程</a><hr>"
    link += "<a href=/today>今天日期</a><hr>"
    link += "<a href=/about>關於黃婉凌</a><hr>"
    link += "<a href=/welcome?u=婉凌&dep=靜宜資管>GET傳值</a><hr>"
    link += "<a href=/account>POST傳值(帳號密碼)</a><hr>"
    link += "<a href=/math>數學運算</a><hr>"
    link += "<a href=/cup>擲茭</a><hr>"
    return link

# 2. 課程頁面
@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1><a href=/>回到網站首頁</a>"

# 3. 今天日期 (需配合 templates/today.html)
@app.route("/today")
def today():
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    date_str = year + "年" + month + "月"+ day + "日"
    return render_template("today.html", datetime = date_str)

# 4. 關於頁面 (需配合 templates/about.html)
@app.route("/about")
def about(): 
    return render_template("about.html") 

# 5. GET 傳值示範 (需配合 templates/welcome.html)
@app.route("/welcome", methods=["GET"])
def welcome():
    x = request.values.get("u")
    y = request.values.get("dep")
    return render_template("welcome.html", name = x, dep = y)

# 6. POST 帳號密碼 (需配合 templates/account.html)
@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

# 7. 數學運算 (需配合 templates/math.html 與 math_result.html)
@app.route("/math", methods=["GET", "POST"])
def math():
    if request.method == "POST":
        try:
            x = float(request.form.get("x"))
            y = float(request.form.get("y"))
            opt = request.form.get("opt")
            if opt == "+": res = x + y
            elif opt == "-": res = x - y
            elif opt == "*": res = x * y
            elif opt == "/": res = x / y if y != 0 else "除數不能為0"
            else: res = "錯誤"
            return render_template("math_result.html", x=x, y=y, opt=opt, res=res)
        except:
            return "請輸入正確數字！<a href='/math'>返回</a>"
    return render_template("math.html")

# 8. 擲茭功能 (原本寫在 run 之後，現在移到前面了)
@app.route('/cup', methods=["GET"])
def cup():
    action = request.values.get("action")
    result = None
    
    if action == 'toss':
        # 0 代表陽面，1 代表陰面
        x1 = random.randint(0, 1)
        x2 = random.randint(0, 1)
        
        # 判斷結果文字
        if x1 != x2:
            msg = "聖筊：表示神明允許、同意，或行事會順利。"
        elif x1 == 0:
            msg = "笑筊：表示神明一笑、不解，或者考慮中，行事狀況不明。"
        else:
            msg = "陰筊：表示神明否定、憤怒，或者不宜行事。"
            
        result = {
            "cup1": "/static/" + str(x1) + ".jpg",
            "cup2": "/static/" + str(x2) + ".jpg",
            "message": msg
        }
        
    return render_template('cup.html', result=result)

# 9. 啟動伺服器 (必須放在所有路由定義的最下面)
if __name__ == "__main__":
    app.run(debug=True)