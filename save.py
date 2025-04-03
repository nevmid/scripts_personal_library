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
         try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 conn.execute("PRAGMA foreign_keys = ON") #//////////////////////////////////////////////////
                 cursor.execute("""
                     DELETE FROM Books WHERE Name_book = ?
                 """, (name_book,))
         except sqlite3.Error as e:
             raise Exception(f"Ошибка при Удалении книги: {str(e)}")
 
     def add_author(self, firstname, lastname, middlename=None, nickname=None):
         """Добавляет автора или возвращает существующего"""
         try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 # Проверяем существующего автора
                 cursor.execute("""
                     SELECT Id_author FROM Authors 
                     WHERE Name = ? AND Surname = ? 
                     AND (Patronymic = ? OR (? IS NULL AND Patronymic IS NULL))
                     AND (Nickname = ? OR (? IS NULL AND Nickname IS NULL))
                 """, (firstname, lastname, middlename, middlename, nickname, nickname))
 
                 existing_author = cursor.fetchone()
 
                 if existing_author:
                     return existing_author[0]
                 else:
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
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 cursor.execute("""
                     SELECT 1 FROM Books 
                     WHERE LOWER(Name_book) = ?
                 """, (book_name.lower(),))
                 return cursor.fetchone() is not None
         except sqlite3.Error as e:
             raise Exception(f"Ошибка при проверке существования книги: {str(e)}")
 
 
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
