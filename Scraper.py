import bs4
import requests

url = 'https://www.nytimes.com/'
r = requests.get(url)
soup = bs4.BeautifulSoup(r.content, "lxml")

titles = ''

titles_h3 = soup.find_all('h3')  # The NYT uses exclusively <h2> and <h3> tags for their titles. I collect these first
titles_h2 = soup.find_all('h2')

for title in titles_h3:  # This loop iterates over all these tags and extracts the text, leaving only the title.
    titles += title.get_text() + '\n'

for title in titles_h2:
    titles += title.get_text() + '\n'

print(titles)