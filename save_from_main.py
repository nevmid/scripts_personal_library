import sqlite3
from pathlib import Path
import shutil
import os
import load_data
 
 
class DatabaseManager:
     def __init__(self, db_name="book_db.db"):
         self.db_name = db_name
 
     def _get_connection(self):
         return sqlite3.connect(self.db_name)
 
     def add_book(self, book_name, year):
         """Добавляет книгу в таблицу Books и возвращает ID"""
         # Сохранение имени книги в БД приводим у нижнему регистру 
         book_name = book_name.lower()
         print(book_name)
         try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 cursor.execute("""
                     INSERT INTO Books (Name_book, Year_of_publication)
                     VALUES (?, ?)
                 """, (book_name, year))
                 return cursor.lastrowid
         except sqlite3.Error as e:
             raise Exception(f"Ошибка при добавлении книги: {str(e)}")
    
     def delete_book(self, name_book):
         """Удаление книги из БД"""
      
         # Так как в папке books имена файлов храняться с знаками _
         # то вместо них ставим пробелы
         # print("old: ", name_book)
         correct_name_book = "" 
         for ch in name_book:
            if ch != "_":
                correct_name_book += ch
            else:
                correct_name_book += " "
         # print("new: ", correct_name_book)
         try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 conn.execute("PRAGMA foreign_keys = ON") #//////////////////////////////////////////////////
                 cursor.execute("""
                     DELETE FROM Books WHERE Name_book = ?
                 """, (correct_name_book,))
         except sqlite3.Error as e:
             raise Exception(f"Ошибка при Удалении книги: {str(e)}")
 
     def add_author(self, firstname, lastname, middlename=None, nickname=None):
         """Добавляет автора или возвращает существующего"""
         try:
             author_params = {
                 'Name': firstname,
                 'Surname': lastname,
                 'Patronymic': middlename,
                 'Nickname': nickname
             }
             ld = load_data.GetData()
             ld.get_connection()
             existing_authors = ld.get_id_author(author_params)
             ld.close_connection()

             if existing_authors:
                 return existing_authors[0][0]

             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 cursor.execute("""
                             INSERT INTO Authors (Name, Surname, Patronymic, Nickname)
                             VALUES (?, ?, ?, ?)
                         """, (firstname, lastname, middlename, nickname))
                 return cursor.lastrowid
         except sqlite3.Error as e:
             raise Exception(f"Ошибка при добавлении автора: {str(e)}")
 
     def link_book_author(self, book_id, author_id):
         """Связывает книгу с автором"""
         try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 cursor.execute("""
                     INSERT INTO Books_Authors (ID_book, ID_author)
                     VALUES (?, ?)
                 """, (book_id, author_id))
         except sqlite3.Error as e:
             raise Exception(f"Ошибка при связывании книги и автора: {str(e)}")
 
     def create_extensions(self):
         """Создает необходимые расширения файлов в БД"""
         try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 formats_to_add = ["txt", "pdf", "fb2"]
 
                 for format_name in formats_to_add:
                     cursor.execute("""
                         INSERT OR IGNORE INTO Formats (Name_format) 
                         VALUES (?)
                     """, (format_name,))
                 conn.commit()
         except sqlite3.Error as e:
             raise Exception(f"Ошибка при создании расширений: {str(e)}")
 
     def get_format_id(self, format_name):
         """Возвращает ID формата по его названию"""
         try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 cursor.execute("""
                     SELECT ID_format FROM Formats 
                     WHERE Name_format = ?
                 """, (format_name,))
                 result = cursor.fetchone()
                 return result[0] if result else None
         except sqlite3.Error as e:
             raise Exception(f"Ошибка при получении ID формата: {str(e)}")
 
     def link_book_format(self, book_id, format_id):
         """Связывает книгу с форматом"""
         try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 cursor.execute("""
                     INSERT INTO Books_Formats (ID_book, ID_format)
                     VALUES (?, ?)
                 """, (book_id, format_id))
         except sqlite3.Error as e:
             raise Exception(f"Ошибка при связывании книги и формата: {str(e)}")
 
     def book_exists(self, book_name):
         """Проверяет, существует ли книга с таким названием"""
         try:
             ld = load_data.GetData()
             ld.get_connection()
             result = ld.get_id_book(book_name.lower())
             ld.close_connection()
             return result
         except sqlite3.Error as e:
             raise Exception(f"Ошибка при проверке существования книги: {str(e)}")
          
     def add_tag(self, tag_name):
        """Добавление тега"""
        try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 
                 conn.execute("PRAGMA foreign_keys = ON")
                 
                 cursor.execute("""INSERT INTO Tags (Name_tag)
                 VALUES (?)""", (tag_name.lower(),))
                
                 conn.commit()

        except sqlite3.Error as e:
             raise Exception(f"Ошибка при добавлении тега: {str(e)}")

     def delete_tags(self, list_tags):
        """Удаление тега"""
        try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 
                 conn.execute("PRAGMA foreign_keys = ON")
                 for tag in list_tags:
                    id_tag = tag['id']

                    cursor.execute("""DELETE FROM Tags WHERE ID_tag = ?""", (id_tag,))
                 
                 conn.commit()

        except sqlite3.Error as e:
             raise Exception(f"Ошибка при добавлении тега: {str(e)}")

     def link_book_tags(self, id_book, id_tag):
        """Связка книги с тегом"""
        try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 
                 conn.execute("PRAGMA foreign_keys = ON")
                 cursor.execute("""INSERT INTO Books_Tags (ID_book, ID_tag)
                 VALUES (?, ?)""", (id_book, id_tag,))
                 
                 conn.commit()

        except sqlite3.Error as e:
             raise Exception(f"Ошибка при связывании тега и книги: {str(e)}")

     def link_book_genre(self, id_book, id_genre):
        """Связка книги с жанром"""
        try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 
                 conn.execute("PRAGMA foreign_keys = ON")
                 cursor.execute("""INSERT INTO Books_Genres (ID_book, ID_genre)
                 VALUES (?, ?)""", (id_book, id_genre,))
                 
                 conn.commit()

        except sqlite3.Error as e:
             raise Exception(f"Ошибка при связывании тега и книги: {str(e)}")

 
def copy_book_file(source_path, book_name, format_name, books_dir="books"):
     """Копирует файл книги в целевую директорию"""
     try:
         file_extension = os.path.splitext(source_path)[1].lower()
         safe_book_name = book_name.replace(" ", "_").lower()
         new_filename = f"{safe_book_name}_{format_name}{file_extension}"
 
         target_dir = Path(__file__).parent / books_dir
         target_dir.mkdir(exist_ok=True)
         dest_path = target_dir / new_filename
 
         shutil.copy2(source_path, dest_path)
         return dest_path
     except Exception as e:
         raise Exception(f"Ошибка при копировании файла: {str(e)}")
