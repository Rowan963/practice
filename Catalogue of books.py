import pickle
import os

catalogue_title = {}
catalogue_writer = {}

if os.path.exists('my_data.pickle') and os.path.getsize('my_data.pickle') > 0:
    with open('my_data.pickle', 'rb') as f:
        catalogue_title, catalogue_writer = pickle.load(f)

class Book:
    def __init__(self, title, writer, original_title=""):
        self.title = title
        self.writer = writer
        self.original_title = original_title

    def add(self):
        catalogue_title[self.title] = {
            "writer": self.writer.split(','),
            "original_title": self.original_title
        }
        for writer in catalogue_title[self.title]["writer"]:
            catalogue_writer.setdefault(writer.strip(), []).append(self.title)

    def edit(self, new_title, new_writer, new_original_title=""):
        if self.title in catalogue_title:
            old_details = catalogue_title.pop(self.title)
            for writer in old_details["writer"]:
                catalogue_writer[writer].remove(self.title)

            catalogue_title[new_title] = {
                "writer": new_writer.split(','),
                "original_title": new_original_title
            }
            for writer in catalogue_title[new_title]["writer"]:
                catalogue_writer.setdefault(writer.strip(), []).append(new_title)

            if new_title != self.title:
                del catalogue_title[self.title]
        else:
            print(f'Book "{self.title}" not found in the catalog.')

def search(q):
    found_books = {title: details for title, details in catalogue_title.items() if q.upper() in title.upper()}
    if found_books:
        for title, details in found_books.items():
            print(f'Title: {title}')
            print(f'Writer: {", ".join(details["writer"])}')
            print(f'Original Title: {details["original_title"]}')
    else:
        print(f'Book "{q}" not found in the catalog.')

def delete(q):
    search(q)
    if q in catalogue_title:
        action = input('Delete the book? ([Y]es/[N]o): ')
        if action.lower() == 'y':
            details = catalogue_title.pop(q)
            for writer in details["writer"]:
                catalogue_writer[writer].remove(q)
            print(f'Book "{q}" deleted successfully.')
    else:
        print(f'Book "{q}" not found in the catalog.')

def print_all_books():
    if catalogue_title:
        for title, details in catalogue_title.items():
            print(f'Title: {title}')
            print(f'Writer: {", ".join(details["writer"])}')
            print(f'Original Title: {details["original_title"]}')
    else:
        print('The catalog is empty.')

print('Welcome to the book catalogue!')
while True:
    print()
    print('What do you want to do?')
    print('[0] Exit [1] Add book [2] Search book [3] Delete book [4] Print all books [5] Edit book')
    action = input('Enter the number: ')

    if action == '0':
        break
    elif action == '1':
        print('[Add book:]')
        title = input('Please enter the title of the book: ')
        writer = input('Please enter the writer of the book: ')
        original_title = input('Please enter the original title of the book: ')
        book = Book(title=title, writer=writer, original_title=original_title)
        book.add()
    elif action in ['2', '3']:
        if action == '2':
            action_text = 'search'
        elif action == '3':
            action_text = 'delete'
        print(f'[{action_text} book:]')
        query = input(f'Please enter the {action_text} query: ')
        if action == '2':
            search(query)
        else:
            delete(query)
    elif action == '4':
        print_all_books()
    elif action == '5':
        print('[Edit book:]')
        old_title = input('Please enter the title of the book you want to edit: ')
        if old_title in catalogue_title:
            new_title = input('Please enter the new title of the book: ')
            new_writer = input('Please enter the new writer of the book: ')
            new_original_title = input('Please enter the new original title of the book: ')
            book = Book(title=old_title, writer="", original_title="")
            book.edit(new_title=new_title, new_writer=new_writer, new_original_title=new_original_title)
            print('Book information edited successfully!')
        else:
            print(f'Book "{old_title}" not found in the catalog.')
    else:
        print(f'Please enter a number between 0 and 5.')

with open('my_data.pickle', 'wb') as f:
    pickle.dump((catalogue_title, catalogue_writer), f)
