import mysql.connector

#connecting to database
mydb = mysql.connector.connect(
    host ="localhost",
    user ="root",
    password = "Gaming.004",
    database = "imdb_movies"
)

#Creating cursor
mycursor = mydb.cursor()