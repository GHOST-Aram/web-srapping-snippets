from selenium import webdriver
from selenium.webdriver.common.by import By

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
    
    


