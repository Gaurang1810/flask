import psycopg2

conn = psycopg2.connect(database="railway",
                        host="containers-us-west-112.railway.app",
                        user="postgres",
                        password="lDW5AjH9jkxkfV6ASm2a",
                        port="6494")

cursor = conn.cursor()
