from flask import Flask,make_response, jsonify,render_template,url_for,request,send_from_directory,redirect
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

# @app.route('/static/<path:path>')
# def send_report(path):
#     return send_from_directory('Templates/static', path)

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
        answerObtained = isValidUser(loginID,loginRole)
        if(answerObtained==True):
            userData = {"role":data["role"],"id":data["userid"]}
            return render_template(data["role"]  + "/index.html",userData = userData)
        else:
            return redirect("/")

@app.route('/student/updatestudentinfo',methods=['GET', 'POST'])
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
        return render_template("Student/view/updateStudentInfo.html" , id = request.args["id"])

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

# route for student-> view profile
@app.route('/student/viewprofile')
def student_viewProfile():
    return render_template("Student/view/viewProfile.html",id=request.args["id"] )

@app.route('/student/getprofile')
def student_getProfile():
    studentProfile = getStudentProfile(loginID)
    return studentProfile
# route for faculty -> view profile 
@app.route('/teacher/viewprofile')
def teacher_viewProfile():
    return render_template("Teacher/view/viewProfile.html",id=request.args["id"])

@app.route('/teacher/getprofile')
def teacher_getProfile():
    teacherProfile = getTeacherProfile(loginID)
    return teacherProfile

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

# route for teacher -> update my info
@app.route('/teacher/updateteacherinfo',methods=['GET', 'POST'])
def teacher_updateMyInfo():
    if request.method=="POST":
        print("###############in Route function########################")
        fname = request.form.get("firstName")
        mname = request.form.get("middleName")
        lname = request.form.get("lastName")
        address = request.form.get("Address")
        fphonenumber = request.form.get("PhoneNumber")
        fmail = request.form.get("Email")
        loginID = request.form.get("uid")
        print(loginID + " " +fname + " " +mname+ " " +lname)
        updateTeacher(loginID,fname,mname,lname,fphonenumber,fmail,address)
        userData = {"role":"Teacher","id":loginID}
        return render_template("Teacher/index.html", userData = userData)

    elif request.method=="GET":
        print(request.args)
        return render_template("Teacher/view/updateTeacherInfo.html" , id = request.args["id"])

# route for teacher -> update studentyt marks
@app.route('/teacher/updatestudentacademicmark',methods=['GET', 'POST'])
def teacher_updateStudentAcademicMarks():
    if request.method=="POST":
        print("###############in Route function########################")
        sid = request.form.get("studentID")
        cid = request.form.get("subjectID")
        exam = request.form.get("examMarks")
        practical = request.form.get("practicalMarks")
        project = request.form.get("projectMarks")
        quizzes = request.form.get("quizzesMarks")
        attendence = request.form.get("attendenceMarks")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        ansObtained = updateStudentAcademicMarks(loginID,sid,cid,exam,practical,project,quizzes,attendence)
        if ansObtained == True:
            userData = {"role":"Teacher","id":loginID}
            return render_template("Teacher/index.html", userData = userData)
        else:
            return render_template("Teacher/view/updateStudentAcademicMarks.html", id = loginID)

    elif request.method=="GET":
        print(request.args)
        return render_template("Teacher/view/updateStudentAcademicMarks.html" , id = request.args["id"])


# route for teacher -> update student's nonacademic marks
@app.route('/teacher/updatestudentnonacademicmark',methods=['GET','POST'])
def teacher_updateStudentNonAcademicMarks():
    if request.method=="POST":
        print("###############in Route function########################")
        sid = request.form.get("studentID")
        # cid = request.form.get("subjectID")
        sports = request.form.get("sportsMarks")
        technical = request.form.get("technicalMarks")
        art = request.form.get("artMarks")
        cultural = request.form.get("culturalMarks")
        other = request.form.get("otherMarks")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        updateStudentNonAcademicMarks(sid,sports,technical,art,cultural,other)
        
        userData = {"role":"Teacher","id":loginID}
        return render_template("Teacher/index.html", userData = userData)
        

    elif request.method=="GET":
        print(request.args)
        return render_template("Teacher/view/updateStudentNonAcademicMarks.html" , id = request.args["id"])

#route Teacher->view top five students
@app.route('/teacher/viewtopfivestudents',methods=['GET','POST'])
def teacher_viewTopFiveStudents():
    if request.method=="POST":
        print("###############in Route function########################")
        sid = request.form.get("studentID")
        # cid = request.form.get("subjectID")
        sBatch = request.form.get("studentBatch")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        global student_Batch
        student_Batch = sBatch
        ansObtained =isBatchExist(sBatch)
        if(ansObtained == True):
            userData = {"role":"Teacher","id":loginID}
            return render_template("Teacher/view/getTopFiveStudent.html", userData = userData)
        else:
            return render_template("Teacher/view/viewTopFiveStudents.html" , id = loginID)

    elif request.method=="GET":
        print(request.args)
        return render_template("Teacher/view/viewTopFiveStudents.html" , id = request.args["id"])

@app.route('/teacher/gettopfivestudents')
def teacher_getTopFiveStudents():
    topFiveStudents = getTopFiveStudentsStudent(student_Batch)
    return topFiveStudents
# route for ta->update student marks
@app.route('/ta/updetestudentacademicmarks',methods=['GET','POST'])
def ta_updatestudentacademicmarks():
    if request.method=="POST":
        sid = request.form.get("studentID")
        cid = request.form.get("subjectID")
        exam = request.form.get("examMarks")
        practical = request.form.get("practicalMarks")
        project = request.form.get("projectMarks")
        quizzes = request.form.get("quizzesMarks")
        attendence = request.form.get("attendenceMarks")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        ansObtained = updateStudentAcademicMarksTA(loginID,sid,cid,exam,practical,project,quizzes,attendence)
        if ansObtained == True:
            userData = {"role":"TA","id":loginID}
            return render_template("TA/index.html", userData = userData)
        else:
            return render_template("TA/view/updateStudentAcademicMarks.html", id = loginID)
        

    elif request.method=="GET":
        print(request.args)
        return render_template("TA/view/updateStudentAcademicMarks.html" , id = request.args["id"])

# admin->insertStudent
@app.route('/admin/insertnewstudent',methods=['GET','POST'])
def admin_insertstudent():
    if request.method=="POST":
        print("###############in Route function########################")
        sid = request.form.get("studentID")
        fname = request.form.get("firstName")
        mname = request.form.get("middleName")
        lname = request.form.get("lastName")
        sbatch = request.form.get("Batch")
        sphonenumber = request.form.get("PhoneNumber")
        smail = request.form.get("Email")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        answerObtained = insertStudent(sid,fname,mname,lname,sbatch,sphonenumber,smail)
        if answerObtained == True:
            userData = {"role":"Admin","id":loginID}
            return render_template("Admin/index.html", userData = userData)
        else:
            return render_template("Admin/view/InsertNewStudent.html",id=loginID)

    elif request.method=="GET":
        print(request.args)
        return render_template("Admin/view/InsertNewStudent.html" , id = request.args["id"])

@app.route('/admin/insertnewfaculty',methods=['GET','POST'])
def admin_insertFaculty():
    if request.method=="POST":
        print("###############in Route function########################")
        fid = request.form.get("facultyID")
        fname = request.form.get("firstName")
        mname = request.form.get("middleName")
        lname = request.form.get("lastName")
        address = request.form.get("Address")
        fphonenumber = request.form.get("PhoneNumber")
        fmail = request.form.get("Email")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        answerObtained = insertTeacher(fid,fname,mname,lname,fphonenumber,fmail,address)
        if answerObtained == True:
            userData = {"role":"Admin","id":loginID}
            return render_template("Admin/index.html", userData = userData)
        else:
            return render_template("Admin/view/InsertNewFaculty.html" , id = loginID)

    elif request.method=="GET":
        print(request.args)
        return render_template("Admin/view/InsertNewFaculty.html" , id = request.args["id"])

# admin-> insert course
@app.route('/admin/insertnewcourse',methods=['GET','POST'])
def admin_insertCourse():
    if request.method=="POST":
        print("###############in Route function########################")
        cid = request.form.get("courseID")
        cname = request.form.get("courseName")
        fid = request.form.get("facultyID")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        answerObtained = insertCourse(cid,cname,fid)
        if answerObtained == True:
            userData = {"role":"Admin","id":loginID}
            return render_template("Admin/index.html", userData = userData)
        else:
            return render_template("Admin/view/InsertNewCourse.html" , id = loginID)

    elif request.method=="GET":
        print(request.args)
        return render_template("Admin/view/InsertNewCourse.html" , id = request.args["id"])

# admin -> insert takes 
@app.route('/admin/insertnewtakes',methods=['GET','POST'])
def admin_insertTakes():
    if request.method=="POST":
        print("###############in Route function########################")
        sid = request.form.get("studentID")
        cid = request.form.get("courseID")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        answerObtained = insertTakes(sid,cid)
        if answerObtained == True:
            userData = {"role":"Admin","id":loginID}
            return render_template("Admin/index.html", userData = userData)
        else:
            return render_template("Admin/view/InsertNewTakes.html" , id = loginID)

    elif request.method=="GET":
        print(request.args)
        return render_template("Admin/view/InsertNewTakes.html" , id = request.args["id"])

# admin->delete student
@app.route('/admin/deletestudent',methods=['GET','POST'])
def admin_deleteStudent():
    if request.method=="POST":
        print("###############in Route function########################")
        sid = request.form.get("studentID")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        answerObtained = deleteStudent(sid)
        if answerObtained == True:
            userData = {"role":"Admin","id":loginID}
            return render_template("Admin/index.html", userData = userData)
        else:
            return render_template("Admin/view/DeleteStudent.html" , id = loginID)

    elif request.method=="GET":
        print(request.args)
        return render_template("Admin/view/DeleteStudent.html" , id = request.args["id"])

# admin ->delete faculty
@app.route('/admin/deletefaculty',methods=['GET','POST'])
def admin_deleteFaculty():
    if request.method=="POST":
        print("###############in Route function########################")
        fid = request.form.get("facultyID")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        answerObtained = deleteFaculty(fid)
        if answerObtained == True:
            userData = {"role":"Admin","id":loginID}
            return render_template("Admin/index.html", userData = userData)
        else:
            return render_template("Admin/view/DeleteFaculty.html" , id = loginID)

    elif request.method=="GET":
        print(request.args)
        return render_template("Admin/view/DeleteFaculty.html" , id = request.args["id"])

# admin->delete Course
@app.route('/admin/deletecourse',methods=['GET','POST'])
def admin_deleteCourse():
    if request.method=="POST":
        print("###############in Route function########################")
        cid = request.form.get("courseID")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        answerObtained = deleteCourse(cid)
        if answerObtained == True:
            userData = {"role":"Admin","id":loginID}
            return render_template("Admin/index.html", userData = userData)
        else:
            return render_template("Admin/view/DeleteCourse.html" , id = loginID)

    elif request.method=="GET":
        print(request.args)
        return render_template("Admin/view/DeleteCourse.html" , id = request.args["id"])
# admin->delete student takes 
@app.route('/admin/deletetakes',methods=['GET','POST'])
def admin_deleteTakes():
    if request.method=="POST":
        print("###############in Route function########################")
        sid = request.form.get("studentID")
        cid = request.form.get("courseID")
        loginID = request.form.get("uid")
        # print(loginID + " " +fname + " " +mname+ " " +lname)
        answerObtained = deleteTakes(sid,cid)
        if answerObtained == True:
            userData = {"role":"Admin","id":loginID}
            return render_template("Admin/index.html", userData = userData)
        else:
            return render_template("Admin/view/DeleteTakes.html" , id = loginID)

    elif request.method=="GET":
        print(request.args)
        return render_template("Admin/view/DeleteTakes.html" , id = request.args["id"])


if __name__ == '__main__':
    app.run(debug=False, port=os.getenv("PORT", default=5000))