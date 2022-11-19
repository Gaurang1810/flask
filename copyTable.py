import psycopg2

conn = psycopg2.connect(database="railway",
                        host="containers-us-west-112.railway.app",
                        user="postgres",
                        password="lDW5AjH9jkxkfV6ASm2a",
                        port="6494")

cursor = conn.cursor()
#table1
with open('C:/Users/Public/CaseStudy_CSV/student.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'student', sep=',')
#table2
with open('C:/Users/Public/CaseStudy_CSV/faculty.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'faculty', sep=',')
#table3
with open('C:/Users/Public/CaseStudy_CSV/course.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'course', sep=',')
#table4
with open('C:/Users/Public/CaseStudy_CSV/takes.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'takes', sep=',')
#table5
with open('C:/Users/Public/CaseStudy_CSV/subjectmarksforta.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'subjectmarksforta', sep=',')
#table6
with open('C:/Users/Public/CaseStudy_CSV/ta.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'ta', sep=',')
#table7
with open('C:/Users/Public/CaseStudy_CSV/activity.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'activity', sep=',')
#table8
with open('C:/Users/Public/CaseStudy_CSV/academicactivity.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'academicactivity', sep=',')
#table9
with open('C:/Users/Public/CaseStudy_CSV/nonacademicactivity.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'nonacademicactivity', sep=',')
#table10
with open('C:/Users/Public/CaseStudy_CSV/performance.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'performance', sep=',')
conn.commit()
# sql = '''COPY student FROM 'C:/Users/Public/CaseStudy_CSV/student.csv' DELIMITER ',' CSV HEADER'''
# cursor.execute(sql)
# #table2
# sql = '''COPY faculty FROM 'C:/Users/Public/CaseStudy_CSV/faculty.csv' DELIMITER ',' CSV HEADER
# '''
# cursor.execute(sql)
# #table3
# sql = '''COPY course FROM 'C:/Users/Public/CaseStudy_CSV/course.csv' DELIMITER ',' CSV HEADER'''
# cursor.execute(sql)
# #table4
# sql = '''COPY takes FROM 'C:/Users/Public/CaseStudy_CSV/takes.csv' DELIMITER ',' CSV HEADER'''
# cursor.execute(sql)
# #table5
# sql = '''COPY subjectmarksforta FROM 'C:/Users/Public/CaseStudy_CSV/subjectmarksforta.csv' DELIMITER ',' CSV HEADER'''
# cursor.execute(sql)
# #table6
# sql = '''COPY ta FROM 'C:/Users/Public/CaseStudy_CSV/ta.csv' DELIMITER ',' CSV HEADER'''
# cursor.execute(sql)
# #table7
# sql = '''COPY activity FROM 'C:/Users/Public/CaseStudy_CSV/activity.csv' DELIMITER ',' CSV HEADER'''
# cursor.execute(sql)
# #table8
# sql = '''COPY academicactivity FROM 'C:/Users/Public/CaseStudy_CSV/academicactivity.csv' DELIMITER ',' CSV HEADER'''
# cursor.execute(sql)
# #table9
# sql = '''COPY nonacademicactivity FROM 'C:/Users/Public/CaseStudy_CSV/nonacademicactivity.csv' DELIMITER ',' CSV HEADER'''
# cursor.execute(sql)
# #table10
# sql = '''COPY performance FROM 'C:/Users/Public/CaseStudy_CSV/performance.csv' DELIMITER ',' CSV HEADER'''
# cursor.execute(sql)

# conn.commit()