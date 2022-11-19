import psycopg2

conn = psycopg2.connect(database="railway",
                        host="containers-us-west-112.railway.app",
                        user="postgres",
                        password="lDW5AjH9jkxkfV6ASm2a",
                        port="6494")

cursor = conn.cursor()

#Creating table as per requirement
sql ='''CREATE TABLE student
(
    studentid integer NOT NULL,
    firstname character varying NOT NULL,
    middlename character varying NOT NULL,
    lastname character varying NOT NULL,
    studentbatch integer NOT NULL,
    studentphonenumber character varying(10) NOT NULL,
    studentemail character varying NOT NULL,
    PRIMARY KEY (studentid)
)
'''
cursor.execute(sql)
print("Table created successfully........")

#table2
sql ='''CREATE TABLE faculty
(
    facultyid integer NOT NULL,
    firstname character varying NOT NULL,
    middlename character varying NOT NULL,
    lastname character varying NOT NULL,
    facultyaddress character varying NOT NULL,
    facultyemail character varying NOT NULL,
    facultyphonenumber character varying(10) NOT NULL,
    PRIMARY KEY (facultyid)
)
'''
cursor.execute(sql)
print("Table created successfully........")

#table3
sql ='''CREATE TABLE course
(
    subjectid integer NOT NULL,
    subjectname character varying NOT NULL,
    facultyid integer DEFAULT 0,
    PRIMARY KEY (subjectid),
    CONSTRAINT facultyid FOREIGN KEY (facultyid)
        REFERENCES faculty (facultyid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET DEFAULT
        NOT VALID
)
'''
cursor.execute(sql)
print("Table created successfully........")
#table4
sql ='''CREATE TABLE takes
(
    studentid integer NOT NULL,
    subjectid integer NOT NULL,
    PRIMARY KEY (studentid, subjectid),
    CONSTRAINT studentid FOREIGN KEY (studentid)
        REFERENCES student (studentid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT subjectid FOREIGN KEY (subjectid)
        REFERENCES course (subjectid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
)
'''
cursor.execute(sql)
print("Table created successfully........")
#table5
sql ='''CREATE TABLE subjectmarksforta
(
    subjectid integer NOT NULL,
    tamarks integer NOT NULL DEFAULT 0,
    PRIMARY KEY (subjectid),
    CONSTRAINT subjectid FOREIGN KEY (subjectid)
        REFERENCES course (subjectid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
)
'''
cursor.execute(sql)
print("Table created successfully........")
#table6
sql ='''CREATE TABLE ta
(
    studentid integer NOT NULL,
    subjectid integer NOT NULL,
    assignedbatch integer NOT NULL,
    PRIMARY KEY (studentid),
    CONSTRAINT studentid FOREIGN KEY (studentid)
        REFERENCES student (studentid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT subjectid FOREIGN KEY (subjectid)
        REFERENCES subjectmarksforta (subjectid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
)
'''
cursor.execute(sql)
print("Table created successfully........")
#table7
sql ='''CREATE TABLE activity
(
    activityname character varying NOT NULL,
    activitypercentage double precision NOT NULL DEFAULT 0,
    PRIMARY KEY (activityname)
)
'''
cursor.execute(sql)
print("Table created successfully........")
#table8
sql ='''CREATE TABLE academicactivity
(
    studentid integer NOT NULL,
    subjectid integer NOT NULL,
    exam integer NOT NULL DEFAULT 0,
    practical integer NOT NULL DEFAULT 0,
    project integer NOT NULL DEFAULT 0,
    quizzes integer NOT NULL DEFAULT 0,
    attendence integer NOT NULL DEFAULT 0,
    totalscore double precision NOT NULL DEFAULT 0,
    PRIMARY KEY (studentid, subjectid),
    CONSTRAINT studentid FOREIGN KEY (studentid)
        REFERENCES student (studentid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT subjectid FOREIGN KEY (subjectid)
        REFERENCES course (subjectid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
)
'''
cursor.execute(sql)
print("Table created successfully........")
#table9
sql ='''CREATE TABLE nonacademicactivity
(
    studentid integer NOT NULL,
    techinical integer NOT NULL DEFAULT 0,
    art integer NOT NULL DEFAULT 0,
    cultural integer NOT NULL DEFAULT 0,
    sport integer NOT NULL DEFAULT 0,
    other integer NOT NULL DEFAULT 0,
    totalscore double precision NOT NULL DEFAULT 0,
    PRIMARY KEY (studentid),
    CONSTRAINT studentid FOREIGN KEY (studentid)
        REFERENCES student (studentid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
)
'''
cursor.execute(sql)
print("Table created successfully........")
#table10
sql ='''CREATE TABLE performance
(
    studentid integer NOT NULL,
    academicperformance double precision NOT NULL DEFAULT 0,
    nonacademicperformance double precision NOT NULL DEFAULT 0,
    finalperformance double precision NOT NULL DEFAULT 0,
    PRIMARY KEY (studentid),
    CONSTRAINT studentid FOREIGN KEY (studentid)
        REFERENCES student (studentid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
)
'''
cursor.execute(sql)
print("Table created successfully........")

conn.commit()
