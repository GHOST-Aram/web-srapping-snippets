from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Create webdriver
driver  = webdriver.Chrome()

# get response
url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
driver.get(url)

# Initializing lists
titles = []
genres = []
years = []
time = []
imdb_ratings = []
meta_scores= []
votes = []
us_gross = []

def collect_data(container):
    for movie in  container:
        titles.append(movie.find_element(By.CSS_SELECTOR, 'h3 a').text)
        genres.append(movie.find_element(By.CLASS_NAME, 'genre').text)
        years.append(movie.find_element(By.CLASS_NAME, 'lister-item-year').text)
        time.append(movie.find_element(By.CLASS_NAME, 'runtime').text)
        imdb_ratings.append(movie.find_element(By.TAG_NAME, 'strong').text)

        # collect metascore
        try:
            meta_score = movie.find_element(By.CLASS_NAME, 'metascore').text
        except:
            meta_score = '-' 
    
        meta_scores.append(meta_score)

        # Votes
        votes_container = movie.find_element(By.CLASS_NAME, 'sort-num_votes-visible')
        
        nv = votes_container.find_elements(By.TAG_NAME, 'span')
        votes.append(nv[1].text)

        # gross

        gross = nv[4].text if len(nv) == 5 and '#' not in nv[4].text else '-'
        us_gross.append(gross)

#Cleaning data
def clean_data(dataframe):
    dataframe['Year'] = dataframe['Year'].str.extract('(\d+)').astype(int)
    dataframe['Length (Minutes)'] = dataframe['Length (Minutes)'].str.extract('(\d+)').astype(int)
    dataframe['Metascore'] = pd.to_numeric(dataframe['Metascore'], errors='coerce') 
    dataframe['votes'] = dataframe['votes'].str.replace(',','').astype(int)
    dataframe['Gross(Millions)'] = dataframe['Gross(Millions)'].map(lambda gross: gross.lstrip('$').rstrip('M'))
    dataframe['Gross(Millions)'] = pd.to_numeric(dataframe['Gross(Millions)'], errors='coerce')

    return data_frame

# Create data frames
def create_data_frame():
    # Data Frames
    movies = pd.DataFrame({
    'Movie':titles,
    'Genre':genres,
    'Year':years,
    'Length (Minutes)':time,
    'Rating':imdb_ratings,
    'Metascore':meta_scores,
    'votes':votes,
    'Gross(Millions)':us_gross 
    })

    return movies

def scrap():
    while True:
        # get movie divs on current page
        movie_divs = driver.find_elements(By.CLASS_NAME, 'lister-item-content')

        # collect data
        collect_data(movie_divs)
        #Find next
        try:
            next_page_element = driver.find_element(By.CLASS_NAME, 'next-page')
            next_page_element.click()    
        except:
            break   
    
    
if __name__ == '__main__':
    scrap()
    data_frame = create_data_frame()
    data_frame = clean_data(data_frame)
    data_frame.to_csv('movies.csv')

