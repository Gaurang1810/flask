from flask import Flask, jsonify,render_template,url_for,request
import os
import psycopg2
from queryFunction import *
conn = psycopg2.connect(database="railway",
                        host="containers-us-west-112.railway.app",
                        user="postgres",
                        password="lDW5AjH9jkxkfV6ASm2a",
                        port="6494")

cursor = conn.cursor()
app = Flask(__name__)

loginID=""
loginRole=""
@app.route('/')
def index():
    cursor.execute("SELECT * FROM student")
    print(cursor.fetchone())
    return render_template("Login.html")

@app.route('/home',methods=['GET', 'POST'])
def isUser():
    if request.method=="POST":
        print("###############in Route function########################")
        data = request.form.get("userid")
        print(data)
        return "test"
    elif request.method=="GET":
        data = request.args
        print(data)
        ##check from data that is this user exist or not, and return true false accordinglly
        ## data["userid"], data["password"]
        # return "GET"
        global loginID
        global loginRole
        loginID=data["userid"]
        loginRole=data["role"]
        print(loginID + " " + loginRole)
        userData = {"role":data["role"],"id":data["userid"]}
        return render_template(data["role"]  + "/index.html",userData = userData)

@app.route('/student/updetemyinfo',methods=['GET', 'POST'])
def updateMyInfo():
    if request.method=="POST":
        print("###############in Route function########################")
        fname = request.form.get("firstName")
        mname = request.form.get("middleName")
        lname = request.form.get("lastName")
        sbatch = request.form.get("Batch")
        sphonenumber = request.form.get("PhoneNumber")
        smail = request.form.get("Email")
        loginID = request.form.get("uid")
        print(loginID + " " +fname + " " +mname+ " " +lname)
        updateStudent(loginID,fname,mname,lname,sbatch,sphonenumber,smail)
        userData = {"role":"Student","id":loginID}
        return render_template("Student/index.html", userData = userData)

    elif request.method=="GET":
        print(request.args)
        return render_template("Student/view/updateMyinfo.html" , id = request.args["id"])


if __name__ == '__main__':
    app.run(debug=False, port=os.getenv("PORT", default=5000))