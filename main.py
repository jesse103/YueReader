from colorama import Fore
import os

import utils
import bookmark_handler
import progress_handler
import reader
import books

def read_input(title, chapters, bookmarked):
    utils.clear_screen()

    chapters_read = progress_handler.get_read(title)

    try:
        if chapters_read > 0:
            print(utils.color_text(f'[{title}]', Fore.LIGHTBLUE_EX))
            print('\n'.join(['1. Resume Reading', '2. Pick Chapter']))
            option = int(input('> '))
            if option == 1:
                chapter = chapters[chapters_read-1]
                content = books.get_chapter_content(chapter['link'])
                reader.read(title, chapter, chapters, content)
                return
            else:
                pass
    except:
        read_input()
        return

    utils.clear_screen()

    print(utils.color_text(f'[{title}]', Fore.LIGHTBLUE_EX))
    print('Enter a chapter number, or type \'exit\' to exit.')

    option = input('> ')

    try:
        number = int(option)
        if number <= len(chapters) and number > 0:
            chapter = chapters[number-1]
            content = books.get_chapter_content(chapter['link'])
            reader.read(title, chapter, chapters, content)
    except:
        if option == 'exit':
            return book_input(title, chapters, bookmarked)
        else:
            return read_input(title, chapters, bookmarked)

def book_input(title, chapters, bookmarked):
    print('\n=- Options -=')
    options = ['1. Read', f'2. {"Remove Bookmark" if bookmarked else "Bookmark"}', '3. Download', '4. Exit']
    print('\n'.join(options))

    try:
        option = int(input('> '))
        print(option)
        if option == 1:
            read_input(title, chapters, bookmarked)
        elif option == 2:
            if bookmarked:
                bookmark_handler.remove_bookmark(title)
            else:
                bookmark_handler.add_bookmark(title)
        elif option == 3:
            books.download_chapters(title, chapters)
        elif option == 4:
            return
        else:
            book_input(title, chapters, bookmarked)
    except:
        book_input(title, chapters, bookmarked)

def book_menu(data):
    utils.clear_screen()

    title = data['title']
    chapters = books.get_chapters(data['link'])

    chapters_read = progress_handler.get_read(title)

    bookmarked = bookmark_handler.is_bookmarked(title, bookmark_handler.get_bookmarks())

    # Book Info
    print(f'=- Book Info -=\
    \nTitle: {utils.color_text(title, Fore.LIGHTBLUE_EX)} \
    \nChapters: {utils.color_text(len(chapters), Fore.GREEN)} \
    \nProgress: {utils.color_text(f"{chapters_read}/{len(chapters)}", Fore.GREEN)}')

    book_input(title, chapters, bookmarked)
    

def bookmark_menu():
    bookmarks = bookmark_handler.get_bookmarks()
    if len(bookmarks) > 0:
        n = 0
        for bookmark in bookmarks:
            n += 1
            title = bookmark['title']
            print(f'{n}. {title}')
        def bookmark_input():
            print('Type a number to see book info, or type \'exit\' to exit.')
            option = input('> ')
            try:
                option = int(option)
                if option <= len(bookmarks) and option > 0:
                    utils.clear_screen()
                    return book_menu(books.search_title(bookmarks[option-1]['title']))
            except:
                if option == 'exit':
                    utils.clear_screen()
                    return main()
                else:
                    return bookmark_input()
        bookmark_input()
    else:
        print('You don\'t have any bookmarks! :(')
        return main()

def search_menu():
    print(utils.color_text('Search Books', Fore.LIGHTYELLOW_EX))
    title = input('title> ')

    try:
        data = books.search_title(title)
        if data != None:
            book_menu(data)
        else:
            print('Book not found!')
            search_menu()
    except:
        search_menu()

def print_art():

    print(utils.color_text("""
\t\t__  __           ____                 __         
\t\t\ \/ /_  _____  / __ \___  ____ _____/ /__  _____
\t\t \  / / / / _ \/ /_/ / _ \/ __ `/ __  / _ \/ ___/
\t\t / / /_/ /  __/ _, _/  __/ /_/ / /_/ /  __/ /    
\t\t/_/\__,_/\___/_/ |_|\___/\__,_/\__,_/\___/_/\n""", Fore.LIGHTCYAN_EX))


def main():
    utils.clear_screen()
    print_art()

    options = ['1. Search Book', '2. Bookmarks', '3. Exit']
    print('\n'.join(options))

    try:
        option = int(input('> '))

        utils.clear_screen()

        if option == 1:
            search_menu()
        elif option == 2:
            bookmark_menu()
        elif option == 3:
            exit()
        else:
            utils.clear_screen()
    except:
        pass
    main()
    

os.system('')
main()
