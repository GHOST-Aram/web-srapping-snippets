from bs4 import BeautifulSoup
import requests as rq
import pandas as pd

header = {"Accept-Language": "en-US, en:q=0.5"}
url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
response = rq.get(url, headers=header)

soup = BeautifulSoup(response.text, 'lxml')

titles = []
genres = []
years = []
time = []
imdb_ratings = []
meta_scores= []
votes = []
us_gross = []

# Movie divs
movie_divs = soup.find_all('div', class_='lister-item-content')

for movie in  movie_divs:
    titles.append(movie.h3.a.text)
    genres.append(movie.find('span', class_='genre').text)
    years.append(movie.find('span', class_='lister-item-year text-muted unbold').text)
    time.append(movie.find('span', class_='runtime').text)
    imdb_ratings.append(movie.strong.text)

    
    meta_score = movie.find('span', class_='metascore').text if movie.find('span', class_='metascore') else '-'
   
    meta_scores.append(meta_score)

    # Votes and Gross
    nv = movie.find_all('span', attrs={'name':'nv'})

    votes.append(nv[0].text)

    gross = nv[1].text if len(nv) > 1 and '#' not in nv[1].text else '-'
    us_gross.append(gross)


    
# Data Frames
movies = pd.DataFrame({
   'Movie':titles,
   'Year':years,
   'Length (Minutes)':time,
   'Rating':imdb_ratings,
   'Metascore':meta_scores,
   'votes':votes,
   'Gross(Millions)':us_gross 
})

#Cleaning data
movies['Year'] = movies['Year'].str.extract('(\d+)').astype(int)
movies['Length (Minutes)'] = movies['Length (Minutes)'].str.extract('(\d+)').astype(int)
movies['Metascore'] = pd.to_numeric(movies['Metascore'], errors='coerce') 
movies['votes'] = movies['votes'].str.replace(',','').astype(int)
movies['Gross(Millions)'] = movies['Gross(Millions)'].map(lambda gross: gross.lstrip('$').rstrip('M'))
movies['Gross(Millions)'] = pd.to_numeric(movies['Gross(Millions)'], errors='coerce')


movies.to_csv('movies.csv')


