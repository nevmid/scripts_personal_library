import sqlite3

def add_book(book_name, year):
    print(book_name)
    print(year)
    try:
        con = sqlite3.connect("book_db.db")
        cursor = con.cursor()
        cursor.execute("""INSERT INTO Books (Name_book, Year_of_publication) VALUES (?, ?);""", (book_name, year))
        con.commit()
        con.close()
        return True
    except:
        return False           
