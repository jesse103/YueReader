import utils
import progress_handler

from colorama import Fore

max_on_screen = 5

class ReadingStatus:
    book = None
    chapter = None

commands = {
    'next': {
        'info': 'Goes to the next chapter if it exists.',
        'returns': True
    },
    'prev': {
        'info': 'Goes to the previous chapter if it exists.',
        'returns': True
    },
    'jump': {
        'info': 'Jump to specified chapter if it exists.',
        'returns': True
    }
}

def handle_command(book, chapter, command): # TODO: command handler
    args = command.split(' ')
    command_name = args[0]

    print(f'args: {str(args)}')

    if command_name == 'next':
        if chapter.number < book.chapter_count:
            next_chapter = book.chapters[chapter.number]
            read(book, next_chapter)
    elif command_name == 'prev':
        if (chapter.number-2) > 0:
            previous_chapter = book.chapters[chapter.number-2]
            read(book, previous_chapter)
    elif command_name == 'jump':
        number = int(args[1])
        if number > 0 and number <= book.chapter_count:
            specified_chapter = book.chapters[number-1]
            read(book, specified_chapter)

def read(book, chapter):
    utils.clear_screen()

    print(utils.center_text('Press enter to scroll down, or type \'exit\' to go back. Check the github page for a list of commands'))
    
    try:
        done = False
        
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
                command = input()
                if command == 'exit':
                    ReadingStatus.chapter = None
                    ReadingStatus.book = None
                    return
                elif len(command) > 1:
                    try:
                        command_data = commands[command.split(' ')[0]]
                        if command_data['returns']: # bad little hack here, fix and ily
                            return handle_command(book, chapter, command)
                        else:
                            handle_command(book, chapter, command)
                    except:
                        pass
                index = 0
            index += 1
            print(utils.center_text(line))
        if number != (book.chapter_count-1):
            next_chapter = book.chapters[number]
            read(book, next_chapter)
    except:
        pass
