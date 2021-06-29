from bs4 import BeautifulSoup
import requests
import os
import bookmark_handler

base_url = 'https://lightnovel.world' # Site URL

class Chapter:
    def __init__(self, title, link, number):
        self.title = title
        self.link = link
        self.number = number

    def get_content(self):
        return get_chapter_content(self.link)

class Book:
    def __init__(self, title):
        self.valid = False

        book_data = search_title(title)
        if book_data:
            self.valid = True

            self.title = book_data['title']
            self.chapters = get_chapters(book_data['link'])

            self.chapter_count = len(self.chapters)

            self.bookmarked = bookmark_handler.is_bookmarked(self.title, bookmark_handler.get_bookmarks())
            
    def download_chapters(self):
        if not os.path.exists('downloads'):
            os.mkdir('downloads') 

        book_path = f'downloads/{self.title}'

        if os.path.exists(book_path):
            for f in os.listdir(book_path):
                os.remove(os.path.join(book_path, f))
        else:
            os.mkdir(book_path)

        i = 1
        for chapter in self.chapters:
            print(f'Downloading chapter {i}..')
            content = chapter.get_content()
            f = open(f'{book_path}/{i}.txt', 'w', encoding='utf-8')
            f.write(content)
            f.close()
            i += 1
        print(f'Downloaded all chapters for [{self.title}]!')

def scrape_page(url):
    r = requests.get(url)
    r.encoding = 'utf-8' # Force Encoding
    return r.text # Return Data

def search_title(title):
    url = f'{base_url}/search?keyword={title}'
    data = scrape_page(url) 

    soup = BeautifulSoup(data, 'html.parser') # Parse HTML
    
    content = soup.find('div', {'id': 'contnet'}) # Find the terribly misspelled content

    book = content.find('div', {'id': 'book_info'}) # Book info found!

    if book:
        title_text = book.find('li', {'class': 'text1 textC000'}).text.split('\n')[0] # Title of book

        links = book.find_all('a') # All links
        for link in links:
            if 'book' in link['href']: # If the book link is found, return the data
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

    n = 1
    
    for link in links:
        title = link.text
        chapter_link = base_url + link['href']
        chapter_list.append(Chapter(title, chapter_link, n))
        n += 1
    return chapter_list

def get_chapter_content(url):
    data = scrape_page(url)

    soup = BeautifulSoup(data, 'html.parser')

    content = soup.find('div', {'id': 'content_detail'})
    for br in content.find_all('br'):
        br.replace_with('\n')
    return content.text

def download_chapters(title, chapters):
    if not os.path.exists('downloads'):
        os.mkdir('downloads') 

    book_path = f'downloads/{title}'

    if os.path.exists(book_path):
        for f in os.listdir(book_path):
            os.remove(os.path.join(book_path, f))
    else:
        os.mkdir(book_path)

    i = 0
    for chapter in chapters:
        i += 1
        print(f'Downloading chapter {i}..')
        content = chapter.get_content()
        f = open(f'{book_path}/{i}.txt', 'w', encoding='utf-8')
        f.write(content)
        f.close()
    print(f'Downloaded all chapters for [{title}]!')
