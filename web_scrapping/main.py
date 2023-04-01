import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top/?sort=ir,desc&mode=simple&page=1'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

movies = soup.select('td.titleColumn')
ratings = soup.select('td.ratingColumn.imdbRating')

for movie, rating in zip(movies, ratings):
    title = movie.select('a')[0].text
    year = movie.select('span')[0].text
    rating = rating.select('strong')[0].text
    print(f'{title} ({year}) - {rating}')
