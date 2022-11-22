import psycopg2
import json

conn = psycopg2.connect(database="railway",
                        host="containers-us-west-112.railway.app",
                        user="postgres",
                        password="lDW5AjH9jkxkfV6ASm2a",
                        port="6494")

cursor = conn.cursor()


def test(tablename, columnname, compareValue):
    cursor.execute("select "+columnname+" from "+tablename +
                   " where "+columnname+"="+compareValue+"")
    data = cursor.fetchone()
    # print(data)
    return data == None


# print(test("student","studentid","2020001"))
# #insertion in student
def insertStudent(sid, fname, mname, lname, sbatch, sphonenumber, smail):
    if (test("student", "studentid", sid)):
        cursor.execute("insert into student values("+sid+", '"+fname+"', '"+mname+"', '"+lname+"', "+sbatch+", '"+sphonenumber+"', '"+smail+"') ")
        conn.commit()
        return True
    else:
        return False
#insertion in faculty
def insertTeacher(fid, fname, lname, mname, fphonenumber, fmail, faddress):
    if (test("faculty", "facultyid", fid)):
        cursor.execute("insert into faculty values("+fid+", '"+fname+"', '"+mname+"', '"+lname+"','"+faddress+"', '"+fmail+"', '"+fphonenumber+"') ")
        conn.commit()
        return True
    else:
        return False

#insertion in course
def insertCourse(cid, cname, fid):
    if (test("course", "subjectid", cid)):
        if(test("faculty", "facultyID", fid) == False):
            cursor.execute("insert into course values("+cid+", '"+cname+"', "+fid+" )")
            conn.commit()
            return True
        else:
            return False
    else:
        return False

#insertion in takes
def insertTakes(sid, cid):
    if(test("student","studentid",sid) == False):
        if(test("course","subjectid",cid) == False):
            cursor.execute("select * from takes where studentid = "+sid+" and subjectid = "+cid+" ")
            data = cursor.fetchone()
            if(data == None):
                cursor.execute("insert into takes values("+sid+","+cid+") ")
                conn.commit()
                return True
            else:
                return False
        else:
            return False
    else:
        return False

    # cursor.execute("insert into takes values (?,?)", (sid, cid))
def deleteStudent(sid):
    if(test("student","studentid",sid) == False):
        cursor.execute("delete from student where studentid = "+sid+"")
        conn.commit()
        return True
    else:
        return False


# deleting faculty
def deleteFaculty(fid):
    if(test("faculty","facultyid",fid) == False):
        cursor.execute("Delete from faculty where facultyid = "+fid+"")
        conn.commit()
        return True
    else:
        return False

# deleting course
def deleteCourse(cid):
    if(test("course","subjectid",cid) == False):
        cursor.execute("Delete from course where subjectid ="+cid+" ")
        conn.commit()
        return True
    else:
        return False

# deleting takes
def deleteTakes(sid,cid):
    cursor.execute("select * from takes where studentid = "+sid+" and subjectid="+cid+"")
    data = cursor.fetchone()
    if(data == None):
        return False
    else:
        cursor.execute("Delete from takes where studentid = "+sid+" and subjectid="+cid+" ")
        conn.commit()
        return True
# updation in student table
# assuming that the studentid is not going to be update.
# But his/her firstname,lastname,middlename,phonenumber,email, batch can be updated!


def updateStudent(sid, fname, mname, lname, sbatch, sphonenumber, smail):
    cursor.execute("update student set firstname = '"+fname+"', middlename = '"+mname+"', lastname='"+lname+"', studentbatch = " +
                   sbatch+", studentphonenumber = '"+sphonenumber+"', studentemail = '"+smail+"' where studentid = "+sid+" ")
    conn.commit()

# updation in faculty table
# assuming that the facultyid is not going to be update.
# But his/her firstname,lastname,middlename,phonenumber,email, address can be updated!




#insertion in takes




# student -> view academic marks


def viewAcademicMarkStudent(sid):
    cursor.execute("select studentid, subjectid, subjectname, exam, practical,project, quizzes, attendence,totalscore from academicactivity natural join course where studentid = "+sid+" ")
    row_headers = [x[0]
                   for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    json_return =  json.dumps(json_data)
    return json_return

# student -> view non-academic marks

def getStudentProfile(sid):
    cursor.execute("select * from student where studentid = "+sid+"")
    row_headers = [x[0]
                   for x in cursor.description]
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    json_return =  json.dumps(json_data)
    return json_return

def getTeacherProfile(fid):
    cursor.execute("select * from faculty where facultyid = "+fid+"")
    row_headers = [x[0]
                   for x in cursor.description]
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    json_return =  json.dumps(json_data)
    return json_return

def viewNonAcademicMarkStudent(sid):
    cursor.execute(
        "select * from nonacademicactivity where studentid = "+sid+" ")
    row_headers = [x[0]
                   for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    json_return =  json.dumps(json_data)
    return json_return

# student -> view top five students
def viewTopFiveStudentsStudent(sid):
    cursor.execute(
        "select studentid, firstname, lastname, studentbatch,academicperformance,nonacademicperformance,finalperformance from student natural join performance where studentbatch in (select studentbatch from student where studentid = "+sid+") order by finalperformance desc limit 5 "
    )
    row_headers = [x[0]
                   for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    json_return =  json.dumps(json_data)
    return json_return

# teacher-> update my info
def updateTeacher(fid, fname, lname, mname, fphonenumber, fmail, faddress):
    cursor.execute("update faculty set firstname = '"+fname+"', middlename = '"+mname+"', lastname='"+lname+"', facultyaddress = '" +faddress+"', facultyphonenumber = '"+fphonenumber+"', facultyemail = '"+fmail+"' where facultyid = "+fid+" ")
    conn.commit()


# teacher ->update student academic marks
def updateStudentAcademicMarks(fid,sid,cid,examMarks,practicalMarks,projectMarks,quizzesMarks,attendenceMarks):
    cursor.execute("select * from course where subjectid = "+cid+" and facultyid = "+fid+" ")
    data = cursor.fetchone()
    print(data)
    if data != None:
        cursor.execute("update academicactivity set exam = "+examMarks+", practical= "+practicalMarks+",project = "+projectMarks+",quizzes = "+quizzesMarks+",attendence = "+attendenceMarks+" where studentid = "+sid+" and subjectid="+cid+" ")
        conn.commit()
        return True
    else:
        return False

# teacher-> update student non academic marks
def updateStudentNonAcademicMarks(sid,sportsMarks,technicalMarks,artMarks,culturalMarks,otherMarks):
    cursor.execute("update nonacademicactivity set techinical="+technicalMarks+",art="+artMarks+",cultural="+culturalMarks+",sport="+sportsMarks+",other="+otherMarks+" where studentid="+sid+"  ")
    conn.commit()

# TA -> update student academic marks
def updateStudentAcademicMarksTA(loginID,sid,cid,examMarks,practicalMarks,projectMarks,quizzesMarks,attendenceMarks):
    cursor.execute("select * from TA where subjectid="+cid+" and studentid="+loginID+" ")
    data = cursor.fetchone()
    # print(data)
    if data != None:
        cursor.execute("select * from takes where studentid = "+sid+" and subjectid = "+cid+" ")
        data1 = cursor.fetchone()
        if(data1!= None):
            cursor.execute("update academicactivity set exam = "+examMarks+", practical= "+practicalMarks+",project = "+projectMarks+",quizzes = "+quizzesMarks+",attendence = "+attendenceMarks+" where studentid = "+sid+" and subjectid="+cid+" ")
            conn.commit()
            return True
        else:
            return False
    else:
        return False


def isValidUser(loginID,loginRole):
    if loginRole == "Student":
        if(test("student","studentid",loginID) == True):
            return False
        else:
            return True
    elif loginRole =="TA":
        if(test("ta","studentid",loginID) == True):
            return False
        else:
            return True
    elif loginRole == "Teacher":
        if(test("faculty","facultyid",loginID) == True):
            return False
        else:
            return True
    else:
        if loginID=="1":
            return True
        else:
            return False
    

def isBatchExist(sBatch):
    cursor.execute("select studentBatch from student where "+sBatch+" in (select distinct(studentBatch) from student) ")
    data = cursor.fetchone()
    if(data == None):
        return False
    else:
        return True

def  getTopFiveStudentsStudent(sBatch):
    cursor.execute(
    "select studentid, firstname, lastname, studentbatch,academicperformance,nonacademicperformance,finalperformance from student natural join performance where studentbatch ="+sBatch+" order by finalperformance desc limit 5 "
    )
    row_headers = [x[0]
                   for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    json_return =  json.dumps(json_data)
    return json_return