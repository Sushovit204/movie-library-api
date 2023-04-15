import mysql.connector, os
from dotenv import load_dotenv
from mysql.connector import Error, connect

#loading environment varibales from env files
load_dotenv()

#Acessing variables vaules
DB_host = os.getenv("HOST")
DB_user = os.getenv("USER")
DB_password = os.getenv("PASSWORD")
DB_name = os.getenv("DATABASE")


#connecting to database
try:
    mydb = connect(
        host =DB_host,
        user =DB_user,
        password = DB_password,
        database = DB_name
    )
    print("Connected Successfully to MYsql.")

except Error as e:
    print(f"Error Connecting to Mysql: {e}")

#Creating cursor
mycursor = mydb.cursor()