import os
import utils
import bookmark_handler
import progress_handler
import reader
import threading
import asyncio

from colorama import Fore
from pypresence import Presence
from books import Book
from time import sleep

discord_thread = None

def read_input(book):
    utils.clear_screen()

    chapters_read = progress_handler.get_read(book.title)

    try:
        if chapters_read > 0:
            print(utils.color_text(f'[{book.title}]', Fore.LIGHTBLUE_EX))
            print('\n'.join(['1. Resume Reading', '2. Pick Chapter']))
            option = int(input('> '))
            if option == 1:
                chapter = book.chapters[chapters_read-1]
                reader.read(book, chapter)
                return
            else:
                pass
    except:
        return read_input()

    utils.clear_screen()

    print(utils.color_text(f'[{book.title}]', Fore.LIGHTBLUE_EX))
    print('Enter a chapter number, or type \'exit\' to exit.')

    option = input('> ')

    try:
        number = int(option)
        if number <= book.chapter_count and number > 0:
            chapter = book.chapters[number-1]
            reader.read(book, chapter)
    except:
        if option == 'exit':
            book_input(book)
        else:
            read_input(book)

def book_input(book):
    options = ['1. Read', '2. List Chapters', f'3. {"Remove Bookmark" if book.bookmarked else "Bookmark"}', '4. Download', '5. Exit']
    print('\n'.join(options))

    try:
        option = int(input('> '))
        print(option)
        if option == 1:
            read_input(book)
        elif option == 2:
            book.list_chapters()
            utils.clear_screen()
            book_input(book)
        elif option == 3:
            if book.bookmarked:
                bookmark_handler.remove_bookmark(book.title)
            else:
                bookmark_handler.add_bookmark(book.title)
        elif option == 4:
            book.download_chapters()
        elif option == 5:
            return
        else:
            book_input(book)
    except:
        book_input(book)

def book_menu(book):
    utils.clear_screen()

    chapters_read = progress_handler.get_read(book.title)

    # Book Info
    print(f'[{utils.color_text(book.title, Fore.LIGHTBLUE_EX)}]\
    \nChapters: {utils.color_text(book.chapter_count, Fore.GREEN)} \
    \nProgress: {utils.color_text(f"{chapters_read}/{book.chapter_count}", Fore.GREEN)}')

    book_input(book)
    

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
                    book_menu(Book(bookmarks[option-1]['title']))
            except:
                if option == 'exit':
                    pass
                else:
                    bookmark_input()
        bookmark_input()
    else:
        print('You don\'t have any bookmarks! :(')

def search_menu():
    print(utils.color_text('Search Books', Fore.LIGHTYELLOW_EX))
    title = input('title> ')

    try:
        book = Book(title)
        if book.valid:
            book_menu(book)
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
            return
        else:
            utils.clear_screen()
    except:
        pass
    main()

def discord_rpc():
    asyncio.set_event_loop(asyncio.new_event_loop())
    try:
        client_id = 859508506687176764 # YueReader
        rpc = Presence(client_id)
        rpc.connect() # Connect to discord

        while True:
            if reader.ReadingStatus.chapter:
                book = reader.ReadingStatus.book
                chapter = reader.ReadingStatus.chapter
                rpc.update(state=f'Reading {book.title} - {chapter.title}', large_image='moon')
            else:
                rpc.update(state="Idle", large_image='moon')
            sleep(10)
    except:
        pass
    

os.system('')

discord_thread = threading.Thread(target=discord_rpc) # Discord Rich Presence support, feel free to remove
discord_thread.daemon = True
discord_thread.start()

main()
