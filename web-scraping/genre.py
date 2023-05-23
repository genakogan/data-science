import requests
import re
from bs4 import BeautifulSoup

url = "https://knigogo.net/knigi/palata-6/#lib_book_download"

response = requests.get(url)
html_text = response.text

genre_names = re.findall(r'Жанры:\s*(.*?)</li>', html_text)

if genre_names:
    genre_names = [genre.strip() for genre in genre_names[0].split(',')]
    #print(genre_names)
else:
    print("No genres found.")

filtered_data = []
for item in genre_names:
    soup = BeautifulSoup(item, 'html.parser')
    if soup.find('a'):
        text = soup.a.text
        filtered_data.append(text)

print(filtered_data)
