from json.decoder import JSONDecodeError
from os import path
import json

def get_bookmarks():
    if path.exists('bookmarks.json'):
        file = open('bookmarks.json', 'r', encoding='utf-8')
        try:
            content = json.load(file)
            file.close()
            return content
        except JSONDecodeError:
            print('Error decoding bookmarks.json!')
    else:
        return []

def save_bookmarks(bookmarks):
    try:
        file = open('bookmarks.json', 'w', encoding='utf-8')
        json.dump(bookmarks, file)
        file.close()
    except:
        print('An error occured while trying to save bookmarks!')

def is_bookmarked(title, bookmarks):
    for bookmark in bookmarks:
        if bookmark['title'] == title:
            return True
    return False

def add_bookmark(title):
    bookmarks = get_bookmarks()
    if not is_bookmarked(title, bookmarks):
        bookmarks.append({'title': title})
        save_bookmarks(bookmarks)

def remove_bookmark(title):
    bookmarks = get_bookmarks()
    index = 0
    for bookmark in bookmarks:
        if bookmark['title'] == title:
            bookmarks.pop(index)
            break
        index += 1
    save_bookmarks(bookmarks)