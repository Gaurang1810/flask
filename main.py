from flask import Flask,make_response, jsonify,render_template,url_for,request
import os
import psycopg2
from queryFunction import *
import json
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
    return render_template("Login.html")

@app.route('/home',methods=['GET', 'POST'])
def isUser():
    if request.method=="POST":
        print("###############in Route function########################")
        data = request.form.get("userid")
        # loginID=data["userid"]
        print(data)
        return "test"
    elif request.method=="GET":
        data = request.args
        print(data)
        ##check from data that is this user exist or not, and return true false accordinglly
        global loginID
        loginID=data["userid"]
        global loginRole
        loginRole=data["role"]
        print(loginID + " " + loginRole)
        userData = {"role":data["role"],"id":data["userid"]}
        return render_template(data["role"]  + "/index.html",userData = userData)

@app.route('/student/updetemyinfo',methods=['GET', 'POST'])
def student_updateMyInfo():
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

# route for student -> viewAcademicMarkStudent
@app.route('/student/viewacademicmarks')
def student_viewacademicmarks():
    return render_template("Student/view/viewAcademicMarks.html",id = request.args["id"])


@app.route('/student/getacademicmarks')
def student_getAcademicMarks():
    print("loginID " +loginID )
    studentAcademicMarks = viewAcademicMarkStudent(loginID)
    print(studentAcademicMarks)
    return studentAcademicMarks

# route for student -> viewNonAcademicMarkStudent
@app.route('/student/viewnonacademicmarks')
def student_viewNonAcademicMarks():
    # studentNonAcademicMarks = viewNonAcademicMarkStudent(request.args["id"])
    # print(studentNonAcademicMarks)
    return render_template("Student/view/viewNonAcademicMarks.html",id = request.args["id"])

@app.route('/student/getnonacademicmarks')
def student_getNonAcademicMarks():
    studentNonAcademicMarks = viewNonAcademicMarkStudent(loginID)
    return studentNonAcademicMarks

#route for student -> view top five students
@app.route('/student/viewtopfivestudents')
def student_viewTopFiveStudents():
    return render_template("Student/view/viewTopFiveStudents.html",id = request.args["id"])

@app.route('/student/gettopfivestudents')
def student_getTopFiveStudents():
    topFiveStudents = viewTopFiveStudentsStudent(loginID)
    return topFiveStudents


if __name__ == '__main__':
    app.run(debug=False, port=os.getenv("PORT", default=5000))