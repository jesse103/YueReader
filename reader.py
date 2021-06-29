import utils
import progress_handler

from colorama import Fore

max_on_screen = 5

class ReadingStatus:
    book = None
    chapter = None

def handle_command(book, chapter, command): # TODO: command handler]
    pass

def read(book, chapter):
    utils.clear_screen()

    print(utils.center_text('Press enter to scroll down, or type \'exit\' to go back.'))

    try:

        ReadingStatus.book = book
        ReadingStatus.chapter = chapter

        content = chapter.get_content()

        number = chapter.number

        progress_handler.read_chapter(book.title, number)

        index = 0
        if not chapter.title in content:
            print(utils.center_text(chapter.title))
        for line in content.split('\n'):
            if index >= max_on_screen:
                s = input()
                if s == 'exit':
                    ReadingStatus.chapter = None
                    ReadingStatus.book = None
                    return
                else:
                    handle_command(book, chapter, s)
                index = 0
            index += 1
            print(utils.center_text(line))
        if number != (book.chapter_count-1):
            next_chapter = book.chapters[number]
            read(book, next_chapter)
    except:
        pass
