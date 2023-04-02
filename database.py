import mysql.connector
from mysql.connector import Error, connect

#connecting to database
try:
    mydb = connect(
        host ="localhost",
        user ="root",
        password = "Gaming.004",
        database = "imdb_movies"
    )
    print("Connected Successfully to MYsql.")

except Error as e:
    print(f"Error Connecting to Mysql: {e}")

#Creating cursor
mycursor = mydb.cursor()