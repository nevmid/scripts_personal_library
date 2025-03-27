import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from create_db import setup_database
from main_window import Ui_MainWindow
import shutil

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Проверка существования БД
        self.create_db()

        # Создание папки для книг
        if not os.path.isdir("books"):
            os.mkdir("books")
    
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

# Функции открытия окон
    def show_window_add_book(self):
        print("Add book")
        self.stackedWidget.setCurrentIndex(1)
    
    def show_window_search_book(self):
        print("Search book")
        self.stackedWidget.setCurrentIndex(3)
    
    def show_window_add_category(self):
        print("Add category")
        self.stackedWidget.setCurrentIndex(5)
    
    def show_window_delete_category(self):
        print("Delete category")
        self.stackedWidget.setCurrentIndex(4)
    
    def show_main_window(self):
        self.stackedWidget.setCurrentIndex(0)

# Функция добавления книги
    def add_book(self):
        
        # Получение данных о книге
        book_name = self.lineEdit_2.text()
        year = self.lineEdit_3.text()
        author = self.lineEdit_4.text()
        path_book = self.lineEdit_5.text()

        # Проверка
        print(book_name)
        print(year)
        print(author)
        print(path_book)

        # Копирование файла

        # Обработка имени книги для файла
        book_name_for_db = ""
        for ch in book_name:
            if ch == " ":
                book_name_for_db += "_"
            elif ch != " ":
                book_name_for_db += ch
        
        # Получение расширения файла
        book_extension = os.path.splitext(path_book)  

        # print("Расиширение файла: ", book_extension[1])
        # print(book_name_for_db)
        
        book_name_for_db += "_" + book_extension[1][1:]
        print("Имя для файла в папке book: ", book_name_for_db)
        #shutil.copy(source_file, destination_folder + f"{}.pdf")




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
            self.lineEdit_5.setText(f"{file_name}")

# Функция проерки существования файла БД
    def create_db(self):
        if os.path.exists("book_db.db"):
            print("Такой файл есть")
        else:
            setup_database("book_db.db")
            print("Такого файла нет")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.showMaximized()
    sys.exit(app.exec_())