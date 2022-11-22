import psycopg2

conn = psycopg2.connect(database="railway",
                        host="containers-us-west-112.railway.app",
                        user="postgres",
                        password="lDW5AjH9jkxkfV6ASm2a",
                        port="6494")

cursor = conn.cursor()

#getmarks
sql = '''create or replace function getmarks(string character varying)
returns double precision
as
$$ 
declare
	marks double precision;
begin
	select activitypercentage into marks 
	from activity
	where activityname = string;
	return marks;
end;
$$
language plpgsql;'''

cursor.execute(sql)

#insert_student_fun

sql = '''create or replace function insert_student_fun()
returns trigger
as
$insert_student_trg$
BEGIN
	insert into nonacademicactivity values(new.studentid);
	insert into performance values(new.studentid);
	return new;
end
$insert_student_trg$
language 'plpgsql'; '''

cursor.execute(sql)

#insert_takes_fun
sql = '''create or replace function insert_takes_fun()
returns trigger
as
$$
BEGIN
	if (new.subjectid not in (select subjectid from course) or 
		new.studentid not in (select studentid from student))
	then 
		raise notice '% or % not exist', new.studentid, new.subjectid;
		return old;
	elsif ((new.studentid, new.subjectid) in (select studentid,subjectid from takes) )
	then 
		raise notice '% , % entry already exist!' , new.studentid, new.subjectid;
		return old;
	else
		insert into academicactivity values(new.studentid,new.subjectid);
		return new;
	end if;
end
$$
language 'plpgsql' ;'''

cursor.execute(sql)


#before_update_academicactivity_fun
sql = '''create or replace function before_update_academicactivity_fun()
returns trigger
as
$$
declare 
	exammarks double precision;
	practicalmarks double precision;
	projectmarks double precision;
	quizzesmarks double precision;
	attendencemarks double precision;
	marks double precision;
BEGIN
	if(new.exam > 100 or new.practical>100 or new.project > 100 or new.quizzes>100 or new.attendence>100 or new.exam <0 or new.practical<0 or new.project < 0 or new.quizzes<0 or new.attendence<0)
	then 
		raise notice 'Marks should be less then 100 and grater than 0';
		return old;
	else
		select getmarks('exam') into exammarks;
		select getmarks('practical') into practicalmarks;
		select getmarks('project') into projectmarks;
		select getmarks('quizzes') into quizzesmarks;
		select getmarks('attendence') into attendencemarks;

		exammarks := ((exammarks * new.exam)/100);
 		practicalmarks:=((practicalmarks* new.practical)/100);
 		projectmarks:=((projectmarks*new.project)/100) ;
		quizzesmarks:=((quizzesmarks*new.quizzes)/100);
		attendencemarks:=((attendencemarks*new.attendence)/100);
		marks := exammarks + practicalmarks + projectmarks + quizzesmarks + attendencemarks;
		new.totalscore := marks;
		return new;
	end if;
end;
$$
language 'plpgsql';'''

cursor.execute(sql)

#after_update_academicactivity_fun
sql = '''create or replace function after_update_academicactivity_fun()
returns trigger
as
$$
declare 
finalscore double precision;
BEGIN
	select sum(totalscore) into finalscore
	from academicactivity
	where studentid = new.studentid;

-- 	finalscore = finalscore/cn;
	update performance
	set academicperformance = finalscore
	where studentid = new.studentid;
	return new;
end;
$$
language 'plpgsql';'''

cursor.execute(sql)

#before_update_nonacademicactivity_fun

sql = '''create or replace function before_update_nonacademicactivity_fun()
returns trigger
as
$$
declare 
	artmarks double precision;
	techinicalmarks double precision;
	sportmarks double precision;
	culturalmarks double precision;
	othermarks double precision;
	marks double precision;
BEGIN
	if(new.techinical > 100 or new.art>100 or new.cultural > 100 or new.sport>100 or new.techinical<0 or new.other>100 or new.art <0 or new.cultural<0 or new.sport < 0 or new.other<0)
	then 
		raise notice 'Marks should be less then 100 and grater than 0';
		return old;
	else
		select getmarks('art') into artmarks;
		select getmarks('cultural') into culturalmarks;
		select getmarks('techinical') into techinicalmarks;
		select getmarks('sport') into sportmarks;
		select getmarks('other') into othermarks;

		artmarks := ((artmarks * new.art)/100);
 		culturalmarks:=((culturalmarks* new.cultural)/100);
 		sportmarks:=((sportmarks*new.sport)/100) ;
		techinicalmarks:=((techinicalmarks*new.techinical)/100);
		othermarks:=((othermarks*new.other)/100);
		marks := techinicalmarks+ othermarks + culturalmarks + sportmarks +artmarks;
		new.totalscore := marks;
		return new;
	end if;
end;
$$
language 'plpgsql';'''

cursor.execute(sql)

#after_update_nonacademicactivity_fun
sql = '''create or replace function after_update_nonacademicactivity_fun()
returns trigger
as
$$
BEGIN
	update performance
	set nonacademicperformance = new.totalscore
	where studentid = new.studentid;
	return new;
end;
$$
language 'plpgsql';'''

cursor.execute(sql)

#before_update_performance_fun
sql = '''create or replace function before_update_performance_fun()
returns trigger
as
$$
declare 
	academicmarks double precision;
	nonacademicmarks double precision;
	marks double precision;
BEGIN
	select getmarks('academicactivity') into academicmarks;
	select getmarks('nonacademicactivity') into nonacademicmarks;

	academicmarks := ((academicmarks * new.academicperformance)/100);
	nonacademicmarks:=((nonacademicmarks* new.nonacademicperformance)/100);
	marks := academicmarks+ nonacademicmarks;
	new.finalperformance := marks;
	return new;
end;
$$
language 'plpgsql';'''

cursor.execute(sql)



conn.commit()
# cursor.execute("insert into student values(2020444,'Gaurang','Gajendrabhai','Parmar','2020','9999999999','gaurang@gmail.com')")
# conn.commit()
