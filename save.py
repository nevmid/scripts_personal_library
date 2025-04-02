import sqlite3

def add_book(book_name, year):
    # print(book_name)
    # print(year)
    try:
        con = sqlite3.connect("book_db.db")
        cursor = con.cursor()
        cursor.execute("""INSERT INTO Books (Name_book, Year_of_publication) VALUES (?, ?);""", (book_name, year))
        con.commit()
        con.close()
        return True
    except:
        return False 

def create_extension():
    try:
        con = sqlite3.connect("book_db.db")
        cursor = con.cursor()
        
        # Список форматов для добавления
        formats_to_add = ["txt", "pdf", "fb2"]
        
        for format_name in formats_to_add:
            # Проверяем, существует ли уже такой формат
            cursor.execute("""
                SELECT 1 FROM Formats 
                WHERE Name_format = ? 
                LIMIT 1
            """, (format_name,))
            
            # Если запись не найдена - добавляем
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO Formats (Name_format) 
                    VALUES (?)
                """, (format_name,))
        
        con.commit()
        return True
        
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return False
    finally:
        if con:
            con.close()

def connect_book_extension(id_book, id_extension):
    try:
        con = sqlite3.connect("book_db.db")
        cursor = con.cursor()
        cursor.execute("""INSERT INTO Books_Formats (ID_book, ID_format) VALUES (?, ?);""", (int(id_book), int(id_extension)))
        con.commit()
        con.close()
        return True
    except:
        return False 