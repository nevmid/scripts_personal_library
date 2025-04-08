import sys
import os

from PyQt5.QtGui import QIcon #
from PyQt5.QtCore import Qt, QMimeData, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidgetItem, QWidget, QLabel, QPushButton, QHBoxLayout
from create_db import setup_database
from main_window import Ui_MainWindow
from save import DatabaseManager, copy_book_file
from load_data import GetData
import shutil
from pathlib import Path  
import sqlite3 ##############

# для fb2
from lxml import etree
import xml.etree.ElementTree as ET 

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon("app_icon.ico"))  # или .png

        # Устанавливаем имя программы      
        self.setWindowTitle("BookHive")
        
        # Устанавливаем икноку для программы
        self.setWindowIcon(QIcon("logo.png"))

        # Проверка существования БД
        self.create_db()

        # Создание папки для книг
        if not os.path.isdir("books"):
            os.mkdir("books")

        # Загрузка расширений
        db_manager = DatabaseManager()
        db_manager.create_extensions()

        # При запуске отображаем все книги
        self.search_books()
    
        self.add_book_button.clicked.connect(self.show_window_add_book)
        self.search_book_button.clicked.connect(self.show_window_search_book)
        self.add_category_button.clicked.connect(self.show_window_add_category)
        self.delete_category_button.clicked.connect(self.show_window_delete_category)
        
        self.back_to_main_window_add_book.clicked.connect(self.show_main_window)
        self.back_to_main_window_edit_book.clicked.connect(self.show_main_window)
        self.back_to_main_window_search_book.clicked.connect(self.show_main_window)
        self.back_to_main_window_delete_tag.clicked.connect(self.show_main_window)
        self.back_to_main_window_add_tag.clicked.connect(self.show_main_window)

        # Кнопка добавления книги
        self.window_add_book_btn_add.clicked.connect(self.add_book)
        self.window_add_book_btn_choose.clicked.connect(self.open_file_dialog)

        # Кнопка поиска книги
        self.window_search_book_btn_search.clicked.connect(self.search_books)

        # Кнопка добавления тега
        self.window_add_tag_btn_add.clicked.connect(self.add_tag)


# Функции открытия окон
    def show_window_add_book(self):
        # print("Add book")
        self.stackedWidget.setCurrentIndex(1)
    
    def show_window_search_book(self):
        # print("Search book")
        self.stackedWidget.setCurrentIndex(3)
    
    def show_window_add_category(self):
        # print("Add category")
        self.stackedWidget.setCurrentIndex(5)
    
    def show_window_delete_category(self):
        # print("Delete category")
        self.stackedWidget.setCurrentIndex(4)
    
    def show_main_window(self):
        self.stackedWidget.setCurrentIndex(0)

#-------------------------------#
# Функция добавления книги
    def add_book(self):
        # Получение данных из полей ввода
        book_name = self.window_add_book_name_book.text().strip()
        year = self.window_add_book_year.text().strip()
        author_firstname = self.window_add_book_firstname.text().strip()
        author_lastname = self.window_add_book_lastname.text().strip()
        author_middlename = self.window_add_book_middlename.text().strip()
        author_nickname = self.window_add_book_nickname.text().strip()
        path_book = self.window_add_file_path.text().strip()

        # Валидация данных
        if not book_name:
            QMessageBox.warning(self, 'Ошибка', 'Введите название книги')
            return
        try:
            year = int(year)
            if year <= 0 or year >= 3000:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректный год издания (от 1 до 2999)')
            return

        if not author_firstname or not author_lastname:
            QMessageBox.warning(self, 'Ошибка', 'Введите имя и фамилию автора')
            return

        if len(author_firstname) < 2:
            QMessageBox.warning(self, 'Ошибка', 'Имя автора должно содержать минимум 2 символа')
            return

        if len(author_lastname) < 2:
            QMessageBox.warning(self, 'Ошибка', 'Фамилия автора должна содержать минимум 2 символа')
            return

        if not path_book:
            QMessageBox.warning(self, 'Ошибка', 'Выберите файл книги')
            return

        # Проверка расширения файла
        _, file_extension = os.path.splitext(path_book)
        file_extension = file_extension.lower()
        if file_extension not in ['.fb2', '.pdf', '.txt']:
            QMessageBox.warning(self, 'Ошибка', 'Поддерживаются только файлы с расширениями .fb2, .pdf, .txt')
            return

        # Создаем экземпляр менеджера БД
        db_manager = DatabaseManager()

        try:
            # Проверяем существование книги
            if db_manager.book_exists(book_name):
                QMessageBox.warning(self, 'Ошибка', 'Книга с таким названием уже существует')
                return

            # Проблема при удаленни книги из дб
            # так как в бд хранится название как Computer Science
            # а в папке books как computer_science_pdf.pdf
            # при нажатии на кнопку мы полчаем computer_science_pdf.pdf
            # удаляем такой файл из папки books
            # потом убираем _pdf.pdf и получаем computer_science
            # и по этому имени ищем в БД НО В БД хранится Computer Science


            # #////////
            # file_extension = os.path.splitext(source_path)[1].lower()
            # safe_book_name = book_name.replace(" ", "_").lower()
            # new_filename = f"{safe_book_name}_{format_name}{file_extension}"
            # #////////

            # 1. Добавляем книгу
            book_id = db_manager.add_book(book_name, year)

            # 2. Добавляем автора
            author_id = db_manager.add_author(
                firstname=author_firstname,
                lastname=author_lastname,
                middlename=author_middlename if author_middlename else None,
                nickname=author_nickname if author_nickname else None
            )

            # 3. Связываем книгу и автора
            db_manager.link_book_author(book_id, author_id)

            # 4. Получаем ID формата
            format_name = file_extension[1:]  # Убираем точку (.fb2 → fb2)
            format_id = db_manager.get_format_id(format_name)

            if not format_id:
                QMessageBox.critical(self, 'Ошибка', f'Формат {format_name} не поддерживается')
                return

            # 5. Связываем книгу и формат
            db_manager.link_book_format(book_id, format_id)

            # 6. Копируем файл книги
            copy_book_file(path_book, book_name, format_name)

            QMessageBox.information(self, 'Успех', 'Книга и автор успешно добавлены')

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка: {str(e)}')

        # Очищаем поля ввода
        self.window_add_book_name_book.clear()
        self.window_add_book_year.clear()
        self.window_add_book_firstname.clear()
        self.window_add_book_lastname.clear()
        self.window_add_book_middlename.clear()
        self.window_add_book_nickname.clear()
        self.window_add_file_path.clear()

        # Возвращаемся на главный экран
        self.show_main_window()

# Функция получения пути до файла
    def open_file_dialog(self):
        # Открываем диалоговое окно выбора файла
        file_name, _ = QFileDialog.getOpenFileName(
            self,                  # Родительское окно
            "Выберите файл",       # Заголовок окна
            "",                    # Начальная директория
            "All Files (*);;Text Files (*.txt);;Python Files (*.py)"  # Фильтры файлов
        )
        
        # Если файл выбран (не нажата отмена)
        if file_name:

            # Проверяем расширение файла
            _, file_extension = os.path.splitext(file_name)
            file_extension = file_extension.lower()
            if file_extension == ".fb2":
                # Если fb2 то заполняем из метаданных
                self.parse_fb2_metadata(file_name)

            self.window_add_file_path.setText(f"{file_name}")

# Функция проерки существования файла БД
    def create_db(self):
        if os.path.exists("book_db.db"):
            print("Такой файл есть")
        else:
            setup_database("book_db.db")
            print("Такого файла нет")

#   Функция поиска книги
    def search_books(self):
        
        if self.window_search_book_name_book.text() != '':
            book_name = self.window_search_book_name_book.text().lower()
        else:
            book_name = None

        author = []

        author.append(self.window_search_book_firstname.text())
        author.append(self.window_search_book_lastname.text())
        author.append(self.window_search_book_middlename.text())
        author.append(self.window_search_book_nickname.text())

        if self.window_search_book_year.text() != '':
            year = self.window_search_book_year.text()
        else:
            year = None

        filters = {

            "name": book_name,
            "author": author,
            "year": year,
            "genres": [],
            "tags": []

        }

        loaddata = GetData()
        books = loaddata.get_books(filters)

        self.window_search_book_name_book.clear()
        self.window_search_book_firstname.clear()
        self.window_search_book_lastname.clear()
        self.window_search_book_middlename.clear()
        self.window_search_book_nickname.clear()
        self.window_search_book_year.clear()

        self.listWidget.clear()

        self.load_books_to_list_widgets(books)

        self.stackedWidget.setCurrentIndex(0)  ##### Поменять на вызов функции

    def load_books_to_list_widgets(self, dict_of_books):

        for el in dict_of_books:  # Проходимся по всем книгам
            for format in el["formats"]:  # Проходимся по форматам книги
                item = QListWidgetItem()
                item_widget = QWidget()
                item_widget.setStyleSheet("color: black; border: 0px; font: 20px")
                line_text = QLabel(f'{el["name"].capitalize()}')
                line_empty = QLabel()
                line_format = QLabel(f"{format}")
                open_btn = QPushButton("От")
                open_btn.setToolTip("Открыть")
                open_btn.setCursor(Qt.PointingHandCursor)
                open_btn.setMaximumSize(50, 50)
                copy_btn = QPushButton("Ск")
                copy_btn.setToolTip("Скопировать")
                copy_btn.setMaximumSize(50, 50)
                copy_btn.setCursor(Qt.PointingHandCursor)
                edit_btn = QPushButton("Ред")
                edit_btn.setToolTip("Редактировать")
                edit_btn.setMaximumSize(50, 50)
                edit_btn.setCursor(Qt.PointingHandCursor)
                delete_btn = QPushButton("Уд")
                delete_btn.setToolTip("Удалить")
                delete_btn.setMaximumSize(50, 50)
                delete_btn.setCursor(Qt.PointingHandCursor)
                file_name = ""
                for ch in el["name"]:
                    if ch == " ":
                        file_name += "_"
                    else:
                        file_name += ch
                open_btn.setObjectName(str(f"{file_name}_{format}.{format}"))
                open_btn.clicked.connect(self.clickedLinePB)
                delete_btn.setObjectName(str(f"{file_name}_{format}.{format}"))
                delete_btn.clicked.connect(self.clicked_delete)
                
                copy_btn.setObjectName(str(f"{file_name}_{format}.{format}"))
                copy_btn.clicked.connect(self.clicked_copy)
                
                item_layout = QHBoxLayout()
                item_layout.addWidget(line_text)
                item_layout.addWidget(line_empty)
                item_layout.addWidget(line_format)
                item_layout.addWidget(open_btn)
                item_layout.addWidget(copy_btn)
                item_layout.addWidget(edit_btn)
                item_layout.addWidget(delete_btn)
                item_widget.setLayout(item_layout)
                item.setSizeHint(item_widget.sizeHint())
                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item, item_widget)

    def clickedLinePB(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())

        # Получаем путь до текущей директории
        base_dir = Path(__file__).parent.resolve()
        books_dir = base_dir / "books"

        # Запускаем файл
        os.startfile(books_dir / f"{push_button.objectName()}" )
    
    def clicked_delete(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())

        # Получаем путь до текущей директории
        base_dir = Path(__file__).parent.resolve()
        books_dir = base_dir / "books"

        full_dir = books_dir / f"{push_button.objectName()}"
        
        book_name_in_db = push_button.objectName()

        book_name_in_db.lower()

        book_name_in_db = book_name_in_db[:-8]

        print(book_name_in_db)
        print(full_dir)

        db_manager = DatabaseManager()

        db_manager.delete_book(book_name_in_db)

        os.remove(books_dir / f"{push_button.objectName()}")

        # Выводсообщения о том что книги скопирована
        QMessageBox.information(self, 'Удаление', 'Книга удалена')

        self.search_books()
    
    def clicked_copy(self):
         sender = self.sender()
         push_button = self.findChild(QPushButton, sender.objectName())
 
         base_dir = Path(__file__).parent.resolve()
         books_dir = base_dir / "books"
 
         full_dir = books_dir / f"{push_button.objectName()}"
 
         mime_data = QMimeData()
         mime_data.setUrls([QUrl.fromLocalFile(str(full_dir))])
 
         clipboard = QApplication.clipboard()
         clipboard.setMimeData(mime_data)

        # Вывод сообщения о том что книги скопирована
         QMessageBox.information(self, 'Копирование', 'Книга скопирована')

    def parse_fb2_metadata(self, path):
        try:
            # 1. Парсим XML-структуру FB2
            tree = ET.parse(path)  # Загружаем файл
            root = tree.getroot()  # Получаем корневой элемент
            # 2. Указываем namespace (пространство имён FB2)
            ns = {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
            # 3. Ищем блок <title-info> (метаданные книги)
            title_info = root.find('.//fb2:title-info', ns)
            # 4. Извлекаем автора
            if title_info is not None:
                author_elem = title_info.find('fb2:author', ns)
                if author_elem is not None:
                    first_name = author_elem.find('fb2:first-name', ns).text if author_elem.find('fb2:first-name', ns) is not None else ""
                    last_name = author_elem.find('fb2:last-name', ns).text if author_elem.find('fb2:last-name', ns) is not None else ""
                    author = f"{first_name} {last_name}".strip()
                else:
                    author = "Не указан"
                # 5. Извлекаем название книги
                book_title = title_info.find('fb2:book-title', ns).text if title_info.find('fb2:book-title', ns) is not None else "Не указано"
                # 6. Извлекаем дату написания книги (атрибут value)
                book_date = title_info.find('fb2:date', ns).get('value') if title_info.find('fb2:date', ns) is not None else "Не указана"
            else:
                author, book_title, book_date = "Не найдено", "Не найдено", "Не найдено"
            # 7. Ищем блок <document-info> (метаданные файла FB2)
            doc_info = root.find('.//fb2:document-info', ns)
            if doc_info is not None:
                fb2_date = doc_info.find('fb2:date', ns).get('value') if doc_info.find('fb2:date', ns) is not None else "Не указана"
            else:
                fb2_date = "Не найдена"

            # Устанавливаем название книги
            self.window_add_book_name_book.clear()
            self.window_add_book_name_book.setText(f"{book_title}")

            # Устанавливаем дату книги
            self.window_add_book_year.clear()
            if book_date:
                self.window_add_book_year.setText(f"{book_date[:4]}")
            elif fb2_date:
                self.window_add_book_year.setText(f"{fb2_date[:4]}")

            # Устанавливаем имя автора книги
            self.window_add_book_firstname.clear()
            self.window_add_book_firstname.setText(f"{first_name}")

            # Устанавливаем Фамилию автора книги
            self.window_add_book_lastname.clear()
            self.window_add_book_lastname.setText(f"{last_name}")

            # Очищаем остальные поля
            self.window_add_book_nickname.clear()
            self.window_add_book_middlename.clear()

        except Exception as e:
            return {"Ошибка": str(e)}
            
    def add_tag(self):
        name_new_tag = self.window_add_tag_name_tag.text()
        dbm = DatabaseManager()
        ld = GetData()
        # print(ld.get_id_tag(str(name_new_tag).lower()))
        if ld.get_id_tag(str(name_new_tag).lower()):
            # Вывод сообщения о том что тег с такми название муже сущетвует
            QMessageBox.information(self, 'Добавление ткга', f"Тэг с названием {name_new_tag} уже существует")
            return
        else:
            dbm.add_tag(str(name_new_tag))
        # Вывод сообщения о том что тег успешно добавлен
        QMessageBox.information(self, 'Добавление тега', f'Тег с названием {name_new_tag} добавлен')
        self.window_add_tag_name_tag.clear()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.showMaximized()
    sys.exit(app.exec_())
