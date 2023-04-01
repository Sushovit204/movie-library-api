import requests
from bs4 import BeautifulSoup
import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Gaming.004",
  database="imdb_movies"
)

mycursor = mydb.cursor()

# Create table to store movie data
mycursor.execute("CREATE TABLE IF NOT EXISTS movies (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), year VARCHAR(4), rating FLOAT)")

url = 'https://www.imdb.com/chart/top/?sort=ir,desc&mode=simple&page=1'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

movies = soup.select('td.titleColumn')
ratings = soup.select('td.ratingColumn.imdbRating')

# Iterate over movies and insert data into table
for movie, rating in zip(movies, ratings):
    title = movie.select('a')[0].text
    year = movie.select('span')[0].text[1:-1]
    rating = float(rating.select('strong')[0].text)
    
    # Insert movie data into table
    sql = "INSERT INTO movies (title, year, rating) VALUES (%s, %s, %s)"
    val = (title, year, rating)
    mycursor.execute(sql, val)
    mydb.commit()

print("Movies added to database!")
