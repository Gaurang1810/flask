import psycopg2

conn = psycopg2.connect(database="railway",
                        host="containers-us-west-112.railway.app",
                        user="postgres",
                        password="lDW5AjH9jkxkfV6ASm2a",
                        port="6494")

cursor = conn.cursor()
def test(tablename, columnname, compareValue):
    cursor.execute("select "+columnname+" from "+tablename+" where "+columnname+"="+compareValue+"")
    data =cursor.fetchone()
    #print(data)
    return data == None


#print(test("student","studentid","2020001"))
# #insertion in student
def insertStudent(sid,fname,mname,lname,sbatch,sphonenumber,smail):
    if(test("student","studentid",sid)):
        cursor.execute("insert into student values(?,?,?,?,?,?,?)",(sid,fname,mname,lname,sbatch,sphonenumber,smail))

#updation in student table
#assuming that the studentid is not going to be update.
# But his/her firstname,lastname,middlename,phonenumber,email, batch can be updated!
def updateStudent(sid,fname,mname,lname,sbatch,sphonenumber,smail):
    cursor.execute("update student set firstname = "+fname+", middlename = "+mname+", lastname="+lname+", studentbatch = "+sbatch+", studentphonenumber = "+sphonenumber+", studentemail = "+smail+" where studentid = "+sid+" ")

#updation in faculty table
#assuming that the facultyid is not going to be update.
# But his/her firstname,lastname,middlename,phonenumber,email, address can be updated!
def updateFaculty(fid,fname,lname,mname,fphonenumber,fmail,faddress):
    cursor.execute("update faculty set firstname="+fname+", middlename="+mname+", lastname="+lname+", facultyaddress="+faddress+", facultyemail="+fmail+", facultyphonenumber="+fphonenumber+" where facultyid = "+fid+" ")

#insertion in takes
def insertTakes(sid,cid):
    cursor.execute("insert into takes values (?,?)",(sid,cid))

def updateAcademicactivity():
    pass







