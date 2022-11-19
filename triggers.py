import psycopg2
from functions import *

conn = psycopg2.connect(database="railway",
                        host="containers-us-west-112.railway.app",
                        user="postgres",
                        password="lDW5AjH9jkxkfV6ASm2a",
                        port="6494")

cursor = conn.cursor()

#insert_student_trg

sql = '''create trigger insert_student_trg 
after INSERT
on student
for each row
execute procedure insert_student_fun(); '''
cursor.execute(sql)

#insert_takes_trg
sql = '''create trigger insert_takes_trg 
before INSERT 
on takes
for each row
execute procedure insert_takes_fun()'''

cursor.execute(sql)


#before_update_academicactivity_trg
sql = '''create trigger before_update_academicactivity_trg
before update 
on academicactivity
for each row
execute procedure before_update_academicactivity_fun()'''

cursor.execute(sql)

#after_update_academicactivity_trg
sql = '''create trigger after_update_academicactivity_trg
after update 
on academicactivity
for each row
execute procedure after_update_academicactivity_fun()'''

cursor.execute(sql)

#before_update_nonacademicactivity_trg

sql = '''create trigger before_update_nonacademicactivity_trg
before update 
on nonacademicactivity
for each row
execute procedure before_update_nonacademicactivity_fun()'''

cursor.execute(sql)

#after_update_nonacademicactivity_trg
sql = '''create trigger after_update_nonacademicactivity_trg
after update 
on nonacademicactivity
for each row
execute procedure after_update_nonacademicactivity_fun() '''

cursor.execute(sql)

#before_update_performance_trg
sql = '''create trigger before_update_performance_trg
before update 
on performance
for each row
execute procedure before_update_performance_fun() '''
cursor.execute(sql)
conn.commit()


