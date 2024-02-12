import pickle
import os

found_books = {}

if os.path.exists('my_data.pickle') and os.path.getsize('my_data.pickle') > 0:
    with open('my_data.pickle', 'rb') as f:
        catalogue_title, catalogue_writer = pickle.load(f)
else:
    catalogue_title = {}
    catalogue_writer = {}

class Book:
    def __init__(self, title, writer):
        self.title = title
        self.writer = writer

    def add(self):
        global catalogue_title
        global catalogue_writer
        
        sequence = self.writer.split(',')
        sequence = list(tuple(elem.strip() for elem in sequence))
        
        catalogue_title[self.title] = sequence
        catalogue_writer[sequence] = self.title

def search(q, b):
    global catalogue_title
    global found_books
    found_books.clear()

    for key.upper in catalogue_title.keys().upper:
        if q in key:
            found_books[key] = catalogue_title[key]

    for t, w in found_books.items():
        print(f'{t}({w})')
    if found_books=={}:
        print(f'Book "{q}" not found in the catalog.')

def delete(q, b):
    global catalogue_title
    global catalogue_writer
    search(q,b)
    action = int(input('Delete the book?([1]Y/[2]N)'))
    if action == 1:
        catalogue_writer.pop(catalogue_title[q])

def input_error(n):
    print(f'Please enter a number between 1 and {n}.')

# start
print('Welcome to the book catalogue!')
while True:
    print()
    print('What do you want to do?')
    print('[0] Exit [1] Add book [2] Search book [3] Delete book [4] Print all books')
    action = int(input('Enter the number: '))
    
    if action == 0:
        break
    elif action == 1:  # add
        print('[Add book:]')
        title = input('Please enter the title of the book: ')
        writer = input('Please enter the writer of the book: ')
        book = Book(title=title, writer=writer)
        book.add()
        
    elif action == 2 or action == 3:  # search/delete
        if action == 2:
            action_text = 'search'
        elif action == 3:
            action_text = 'delete'
        print(f'[{action_text} book:]')
        search_by = int(input('By [1] title or [2] writer? '))
        if search_by == 1:
            search_type = catalogue_title
        elif search_by == 2:
            search_type = catalogue_writer
        else:
            input_error(2)
            continue
        query = input(f'Please enter the {action_text} query: ')
        if action == 2:
            search(query, search_type)
        else:
            delete(query, search_type)
            
    elif action == 4:  # print all book
        for title, writer in catalogue_title.items():
            print(f'{title}({writer})')
    else:
        input_error(4)
        continue

with open('my_data.pickle', 'wb') as f:  # save
    pickle.dump((catalogue_title, catalogue_writer), f)
