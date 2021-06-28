from json.decoder import JSONDecodeError
from os import path
import json

def save_progress(data):
    f = open('progress.json', 'w')
    json.dump(data, f)
    f.close()

def get_progress():
    if path.exists('progress.json'):
        try:
            file = open('progress.json', 'r')
            data = json.load(file)
            file.close()
            return data
        except JSONDecodeError:
            print('Error decoding progress.json!')
    else:
        return {}

def get_read(title):
    progress = get_progress()
    if progress.get(title):
        return progress[title]['chapter']
    return 0

def read_chapter(title, number):
    progress = get_progress()
    if progress.get(title):
        data = progress[title]
        if number > data['chapter']:
            data['chapter'] = number
            save_progress(progress)
    else:
        progress[title] = {'chapter': number}
        save_progress(progress)