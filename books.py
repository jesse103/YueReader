from bs4 import BeautifulSoup
import requests

base_url = 'https://lightnovel.world' # Site URL

def scrape_page(url):
    r = requests.get(url)
    r.encoding = 'utf-8' # Force Encoding
    return r.text # Return Data

def search_title(title):
    url = f'{base_url}/search?keyword={title}'
    data = scrape_page(url) 

    soup = BeautifulSoup(data, 'html.parser') # Parse HTML
    
    content = soup.find('div', {'id': 'contnet'}) # Find the terribly misspelled content

    book = content.find('div', {'id': 'book_info'}) # Book found!

    if book:
        title_text = book.find('li', {'class': 'text1 textC000'}).text.split('\n')[0] # Title of book

        links = book.find_all('a') # All chapters
        for link in links:
            if 'book' in link['href']: # Found a chapter
                return {
                    'link': base_url + link['href'], # base_url + '/book/...html'
                    'title': title_text
                }

def get_chapters(url):
    data = scrape_page(url)

    soup = BeautifulSoup(data, 'html.parser')

    chapters = soup.find('div', {'class': 'chapter_content'})

    links = chapters.find_all('a') # Chapters

    chapter_list = []

    n = 0
    
    for link in links:
        n += 1
        chapter_list.append(
            {
                'link': base_url + link['href'],
                'title': link.text,
                'number': n
            }
         )
    return chapter_list

def get_chapter_content(url):
    data = scrape_page(url)

    soup = BeautifulSoup(data, 'html.parser')

    content = soup.find('div', {'id': 'content_detail'})
    for br in content.find_all('br'):
        br.replace_with('\n')
    return content.text