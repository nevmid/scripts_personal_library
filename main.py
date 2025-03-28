import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidgetItem, QWidget, QLabel, QPushButton, QHBoxLayout
from create_db import setup_database
from main_window import Ui_MainWindow
from save import add_book, create_extension, connect_book_extension
from load_data import GetData
import shutil
from pathlib import Path  
import sqlite3 ##############

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Проверка существования БД
        self.create_db()

        # Создание папки для книг
        if not os.path.isdir("books"):
            os.mkdir("books")

        # Загрузка расширений
        create_extension()
    
        self.add_book_button.clicked.connect(self.show_window_add_book)
        self.search_book_button.clicked.connect(self.show_window_search_book)
        self.add_category_button.clicked.connect(self.show_window_add_category)
        self.delete_category_button.clicked.connect(self.show_window_delete_category)
        
        self.back_to_main_window_add_book.clicked.connect(self.show_main_window)
        self.back_to_main_window_edit_book.clicked.connect(self.show_main_window)
        self.back_to_main_window_search_bok.clicked.connect(self.show_main_window)
        self.back_to_main_window_delete_category.clicked.connect(self.show_main_window)
        self.back_to_main_window_add_category.clicked.connect(self.show_main_window)

        # Кнопка добавления книги
        self.pushButton_3.clicked.connect(self.add_book)
        self.pushButton_2.clicked.connect(self.open_file_dialog)

        # Кнопка поиска книги
        self.pushButton_5.clicked.connect(self.search_books)


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
        
        # Получение данных о книге
        book_name = self.lineEdit_2.text()
        year = self.lineEdit_3.text()
        author_firstname = self.window_add_book_firstname.text()
        author_lastname = self.window_add_book_lastname.text()
        author_middlename = self.window_add_book_middlename.text()
        author_nikname= self.window_add_book_nikname.text()        
        # author = self.lineEdit_4.text()
        path_book = self.window_add_file_path.text()

        # Проверка
        # print("Имя книги: ", book_name)
        # print("Год: ", year)
        # print("Имя автора: ", author_firstname)
        # print("Фаммилия автора: ", author_lastname)
        # print("Отчество автора: ", author_middlename)
        # print("Псевдоним автора: ", author_nikname)
        # print("Путь до файла: ", path_book)

        # Копирование файла

        # Обработка имени книги для файла
        book_name_for_db = ""
        for ch in book_name:
            if ch == " ":
                book_name_for_db += "_"
            elif ch != " ":
                book_name_for_db += ch
        
        # Получение расширения и пути до файла
        book_path = os.path.splitext(path_book)[0]
        book_extension = os.path.splitext(path_book)[1] 

        # Проверка расширения файла для книг
        if book_extension != '.fb2' and book_extension != '.pdf' and book_extension != '.txt':
            QMessageBox.information(self, 'Сообщение', 'Выберите файл с расширением для книги')
            return

        # Проверка корректности года
        try:
            int(year)
        except ValueError:
            QMessageBox.information(self, 'Сообщение', 'Дата должна быть целым числом')
            return

        if int(year) <= 0 or int(year) >= 3000:
            QMessageBox.information(self, 'Сообщение', 'Введите дату от 0 до 3000')
            return

        # Проверка автора
        if author_firstname == "" or author_lastname == "":
            QMessageBox.information(self, 'Сообщение', 'Ведите имя и фамилию автора')
            return

        if len(author_firstname) < 2:
            QMessageBox.information(self, 'Сообщение', 'Имя не может состоить из 1 буквы')
            return

        if len(author_lastname) < 5:
            QMessageBox.information(self, 'Сообщение', 'Фамили не может состять из 4 и меньше букв')
            return

        if book_name == "":
            QMessageBox.information(self, 'Сообщение', 'Введите название книги')
            return

        # Создание имени для файла для папки books
        book_name_for_db += "_" + book_extension[1:]

        # Добавление книги
        if add_book(book_name.lower(), int(year)):
            QMessageBox.information(self, 'Сообщение', 'Книга добавлена')
        else:
            QMessageBox.information(self, 'Сообщение', 'Книга не добавлена')

        # Проверка на существование данной книги в БД

        # Получение id добавленной книги
        loaddata = GetData()
        loaddata.conn = sqlite3.connect("book_db.db") ################ ТУТ НЕ НАДО ТАК
        id_book = loaddata.get_id_book(book_name.lower()) # Вывод (id, )
        id_extension = loaddata.get_id_formats(book_extension[1:]) # Вывод (id, )
 
        # Копируем файл в папку books
        base_dir = Path(__file__).parent.resolve()
        books_dir = base_dir / "books"
        dest_path = books_dir / f"{book_name_for_db.lower()}{book_extension}"
        shutil.copy(path_book, dest_path)

        # Связываем книгу и формат
        connect_book_extension(id_book[0][0], id_extension[0][0])

        # Очищение полей ввода
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.window_add_book_firstname.clear()
        self.window_add_book_lastname.clear()
        self.window_add_book_middlename.clear()
        self.window_add_book_nikname.clear()     
        self.window_add_file_path.clear()



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
        
        if self.window_search_name_book.text() != '':
            book_name = self.window_search_name_book.text()
        else:
            book_name = None

        author = []

        author.append(self.window_search_last_name.text())
        author.append(self.window_search_first_name.text())
        author.append(self.window_search_middle_name.text())
        author.append(self.window_search_nikname.text())

        if self.window_search_year.text() != '':
            year = self.window_search_year.text()
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

        self.window_search_name_book.clear()
        self.window_search_first_name.clear()
        self.window_search_last_name.clear()
        self.window_search_middle_name.clear()
        self.window_search_nikname.clear()
        self.window_search_year.clear()

        self.listWidget.clear()

        self.load_books_to_list_widgets(books)

        self.stackedWidget.setCurrentIndex(0)  ##### Поменять на вызов функции

    def load_books_to_list_widgets(self, dict_of_books):

        for el in dict_of_books:  # Проходимся по всем книгам
            for format in el["formats"]:  # Проходимся по форматам книги
                item = QListWidgetItem()
                item_widget = QWidget()
                line_text = QLabel(f'{el["name"].capitalize()}')
                line_empty = QLabel()
                line_format = QLabel(f"{format}")
                line_push_button = QPushButton("Открыть")
                file_name = ""
                for ch in el["name"]:
                    if ch == " ":
                        file_name += "_"
                    else:
                        file_name += ch
                line_push_button.setObjectName(str(f"{file_name}_{format}.{format}"))
                line_push_button.clicked.connect(self.clickedLinePB)
                item_layout = QHBoxLayout()
                item_layout.addWidget(line_text)
                item_layout.addWidget(line_empty)
                item_layout.addWidget(line_format)
                item_layout.addWidget(line_push_button)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.showMaximized()
    sys.exit(app.exec_())