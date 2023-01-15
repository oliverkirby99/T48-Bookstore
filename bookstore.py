# Import SQLite3
import sqlite3

# Create database and setup cursor:
db = sqlite3.connect('bookstore_db')
cursor = db.cursor()

default_stock_list = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                      (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                      (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
                      (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
                      (3005, "Alice in Wonderland", "Lewis Carroll", 12)]


# Function to set up default stock list:
def setup_table():
    cursor.execute('''
             CREATE TABLE Bookstore_Table(id INTEGER PRIMARY KEY, title STRING, author STRING, qty INTEGER)''')
    db.commit()
    print("Table 'Bookstore_Table' has been created.")
    # Add the default stock to the table
    cursor.executemany('''
    INSERT INTO Bookstore_Table(id, title, author, qty) VALUES(?, ?, ?, ?)''', default_stock_list)
    db.commit()
    print("Default Values Loaded.")
    input("Press ENTER to start the program.")


# Function that is run to check if the 'books_table' exists.
def check_table(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    data = cursor.fetchall()
    # If table already exists:
    if len(data) > 0:
        pass
        # Table 'Bookstore_Table' already exists.
    else:
        print("Table 'Bookstore_Table' does not exist.")
        setup_table()


# Call this to open the starting menu and make choices
def start_app():
    while True:
        while True:
            try:
                choice = int(input("""-------- * --------
Welcome to the bookstore app!
Please type a number to make a choice:
1. Enter Book
2. Update Book
3. Delete Book
4. Search Books
5. View Stock
0. Quit
- """).lower())
                break
            # If not number input:
            except ValueError:
                input("Invalid Input. Press 'ENTER' to try again.")

        if choice == 1:
            enter_book()
        elif choice == 2:
            update_book()
        elif choice == 3:
            delete_book()
        elif choice == 4:
            search_book()
        elif choice == 5:
            view_stock()
            input("Press ENTER to continue...")
        elif choice == 0:
            break


def enter_book():
    # Get input for ID, Title, Author, Qty
    get_id = input("Enter ID: ")
    get_title = input("Enter Title: ")
    get_author = input("Enter Author: ")
    get_qty = input("Enter Quantity: ")
    # Insert the values to the table.
    cursor.execute('''INSERT INTO Bookstore_Table(id, title, author, qty) VALUES(:id, :title, :author, :qty)''',
                   {'id': get_id, 'title': get_title, 'author': get_author, 'qty': get_qty})
    db.commit()


def update_book():
    book_id = input("Enter the ID for the book that you want to update: ")
    cursor.execute('''SELECT * FROM Bookstore_Table WHERE id=?''', (book_id,))
    entry = cursor.fetchone()

    while True:
        # Loop until yes/no value given
        confirm = input(f"Would you like to update:\n{entry}\nyes/no: ").lower()
        if confirm == "yes":
            while True:
                # Get the value that the user wants to update
                print("Which value do you want to update?")
                choose_value = input("ID, Title, Author, Quantity? ").lower()
                if choose_value == "id":
                    change = input("Enter the new ID value: ")
                    # Update the value of ID to the new value
                    cursor.execute('''UPDATE Bookstore_Table SET id = ? WHERE id = ?''', (change, book_id,))
                    db.commit()
                    # Get the updated version and print it out.
                    cursor.execute('''SELECT * FROM Bookstore_Table WHERE id=?''', (book_id,))
                    entry = cursor.fetchone()
                    print("ID, Title, Author, Quantity")
                    print(entry)
                    input("Changes have been made. Press ENTER to continue...")
                    break
                elif choose_value == "title":
                    change = input("Enter the new Title value: ")
                    # Update the value of Title to the new value
                    cursor.execute('''UPDATE Bookstore_Table SET title = ? WHERE id = ?''', (change, book_id,))
                    db.commit()
                    # Get the updated version and print it out.
                    cursor.execute('''SELECT * FROM Bookstore_Table WHERE id=?''', (book_id,))
                    entry = cursor.fetchone()
                    print("ID, Title, Author, Quantity")
                    print(entry)
                    input("Changes have been made. Press ENTER to continue...")
                    break
                elif choose_value == "author":
                    change = input("Enter the new Author value: ")
                    # Update the value of Author to the new value
                    cursor.execute('''UPDATE Bookstore_Table SET author = ? WHERE id = ?''', (change, book_id,))
                    db.commit()
                    # Get the updated version and print it out.
                    cursor.execute('''SELECT * FROM Bookstore_Table WHERE id=?''', (book_id,))
                    entry = cursor.fetchone()
                    print("ID, Title, Author, Quantity")
                    print(entry)
                    input("Changes have been made. Press ENTER to continue...")
                    break
                elif choose_value == "quantity":
                    change = input("Enter the new Quantity value: ")
                    # Update the value of Qty to the new value
                    cursor.execute('''UPDATE Bookstore_Table SET qty = ? WHERE id = ?''', (change, book_id,))
                    db.commit()
                    # Get the updated version and print it out.
                    cursor.execute('''SELECT * FROM Bookstore_Table WHERE id=?''', (book_id,))
                    entry = cursor.fetchone()
                    print("ID, Title, Author, Quantity")
                    print(entry)
                    input("Changes have been made. Press ENTER to continue...")
                    break
                else:
                    print("Invalid input. Please try again.")
            break
        elif confirm == "no":
            # Cancel out of the function.
            input("Request Cancelled. Press ENTER to continue...")
            break
        else:
            print("Invalid Input.")


def delete_book():
    # Get value from the user
    book_id = input("Enter the ID for the book that you want to delete: ")
    # Get the value and store it in a variable
    cursor.execute('''SELECT * FROM Bookstore_Table WHERE id=?''', (book_id,))
    entry = cursor.fetchone()

    while True:
        # Loop until yes/no value is given
        confirm = input(f"Are you sure that you want to delete:\n{entry}\nyes/no: ").lower()
        if confirm == "yes":
            # Delete the given value from the table
            cursor.execute('''DELETE FROM Bookstore_Table WHERE id = ?''', (book_id,))
            db.commit()
            break
        elif confirm == "no":
            # Cancel out of this function
            input("Request Cancelled. Press ENTER to continue...")
            break
        else:
            print("Invalid Input.")


def search_book():
    while True:
        # Find out if user wants to search for ID, Title or Author
        search_key = input("Do you want to search by ID, Title or Author? ").lower()
        if search_key == "id":
            # Get the ID input and store it in variable
            book_search = input("Enter the ID of the book that you want to search: ")
            # Search where id = the book_search input
            cursor.execute('''SELECT * FROM Bookstore_Table WHERE id = ?''', (book_search,))
            # There should only be one, so return that value
            result = cursor.fetchone()
            print("ID, Title, Author, Quantity")
            print(result)
            break
        elif search_key == "title":
            # Get the title the user wants to search
            book_search = input("Enter the Title of the book that you want to search: ")
            # Search where title is LIKE the book_search input
            cursor.execute('''SELECT * FROM Bookstore_Table WHERE title LIKE ?''', (f"%{book_search}%",))
            # Return all possible results
            result = cursor.fetchall()
            print("ID, Title, Author, Quantity")
            for i in result:
                print(i)
            break
        elif search_key == "author":
            # Get the author that the user wants to search
            book_search = input("Enter the Author of the book that you want to search: ")
            # Search where author is LIKE the book_search input
            cursor.execute('''SELECT * FROM Bookstore_Table WHERE author LIKE ?''', (f"%{book_search}%",))
            # return all results
            result = cursor.fetchall()
            print("ID, Title, Author, Quantity")
            for i in result:
                print(i)
            break
        else:
            print("Invalid Input. Please Try again.")

    input("Press ENTER to continue...")


def view_stock():
    # Get all entries and print them
    cursor.execute('SELECT * FROM Bookstore_Table')
    books = cursor.fetchall()
    print("List of all stock:")
    print("ID, TITLE, AUTHOR, QTY")
    for book in books:
        print(book)


# Check if table exists:
check_table("Bookstore_Table")

# App starts here:
start_app()