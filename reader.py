import utils
import shutil
import progress_handler
import books

from colorama import Fore

max_on_screen = 5

def read(title, chapter, chapter_list, content):
    utils.clear_screen()

    print(utils.color_text('Press any key to scroll down, or type \'exit\' to go back.', Fore.LIGHTCYAN_EX))

    try:
        number = chapter['number']

        progress_handler.read_chapter(title, chapter['number'])

        index = 0
        if not chapter['title'] in content:
            print(utils.center_text(chapter['title']))
        for line in content.split('\n'):
            if index >= max_on_screen:
                s = input()
                if s == 'exit':
                    return
                index = 0
            index += 1
            print(utils.center_text(line))
        if number != (len(chapter_list)-1):
            next_chapter = chapter_list[number]
            read(title, next_chapter, chapter_list, books.get_chapter_content(next_chapter['link']))
    except:
        print('nooo')
