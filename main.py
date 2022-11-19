from flask import Flask, jsonify,render_template,url_for,request
import os
import psycopg2
conn = psycopg2.connect(database="railway",
                        host="containers-us-west-112.railway.app",
                        user="postgres",
                        password="lDW5AjH9jkxkfV6ASm2a",
                        port="6494")

cursor = conn.cursor()
app = Flask(__name__)
@app.route('/')
def index():
    cursor.execute("SELECT * FROM student")
    print(cursor.fetchone())
    return render_template("login.html")

@app.route('/isUser',methods=['GET', 'POST'])
def isUser():
    if request.method=="POST":
        print("###############in Route function########################")
        data = request.form.get("userid")
        print(data)
        return "test"
    elif request.method=="GET":
        data = request.args
        ##check from data that is this user exist or not, and return true false accordinglly
        ## data["userid"], data["password"]
        return "GET"

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))