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
        cursor.execute("insert into student values(?,?,?,?,?,?,?)",
                       (sid, fname, mname, lname, sbatch, sphonenumber, smail))

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


def updateFaculty(fid, fname, lname, mname, fphonenumber, fmail, faddress):
    cursor.execute("update faculty set firstname="+fname+", middlename="+mname+", lastname="+lname+", facultyaddress=" +
                   faddress+", facultyemail="+fmail+", facultyphonenumber="+fphonenumber+" where facultyid = "+fid+" ")

#insertion in takes


def insertTakes(sid, cid):
    cursor.execute("insert into takes values (?,?)", (sid, cid))

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
