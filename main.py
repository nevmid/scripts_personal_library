import sys
import os
import time

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QMimeData, QUrl, QSize, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidgetItem, QWidget, QLabel, \
    QPushButton, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QTextEdit
from create_db import setup_database
from main_window import Ui_MainWindow

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# from save_from_main import DatabaseManager, copy_book_file
from save import DatabaseManager, copy_book_file

from load_data_test import GetData

import shutil
from pathlib import Path  
import sqlite3
from lxml import etree
import xml.etree.ElementTree as ET 

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_tree_loader()

        self.current_edit_book_id = None
        self.current_edit_author_id = None
        self.current_edit_book_name = None

        self.useFirstSound = False

        # Создаем медиаплеер
        self.player = QMediaPlayer()

        self.setWindowIcon(QIcon("app_icon.ico"))  # или .png

        # Устанавливаем имя программы      
        self.setWindowTitle("BookHive")

        # Устанавливаем икноку для программы
        self.setWindowIcon(QIcon("logo.png"))

        # Проверка существования БД
        self.create_db()

        # Иконки
        self.open_eye_icon = QIcon("eye.png")
        self.close_eye_icon = QIcon("close_eye.png")

        self.select_copy = QIcon("select_copy.png")
        self.not_select_copy = QIcon("not_select_copy.png")

        self.select_delete = QIcon("select_delete.png")
        self.not_select_delete = QIcon("not_select_delete.png")


        self.select_edit = QIcon("select_edit.png")
        self.not_select_edit = QIcon("not_select_edit.png")

        # Создание папки для книг
        if not os.path.isdir("books"):
            os.mkdir("books")

        # Загрузка расширений
        db_manager = DatabaseManager()
        db_manager.create_extensions()

        # При запуске отображаем все книги
        self.search_books()

        # При запуске загружаем дерево в главное окно
        self.load_tree_main()

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

        # Кнопка удлаение тегов
        self.window_delete_tag_btn_delete.clicked.connect(self.delete_tags)

        # Добавление обработчиков кликов по дереву
        self.main_window_tags.itemDoubleClicked.connect(self.on_item_double_clicked)

        #
        self.window_edit_book_btn_edit.clicked.connect(self.edit_book)

        self.main_window_button.clicked.connect(self.parse_line)

        ######
        self.tabWidget.currentChanged.connect(self.changeTab)
        self.btn_statistic_tag_genre.clicked.connect(self.show_statistic_book_tags_genre)
        self.btn_statistic_author.clicked.connect(self.show_statistic_book_author)
        self.documentation_text = QTextEdit()
        self.documentation_text.setReadOnly(True)  # Делаем текстовое поле только для чтения

        # Добавляем QTextEdit на вкладку документации
        self.tab_2_layout = QVBoxLayout(self.tab_2)  # Предполагается, что tab_2 - это ваша вкладка документации
        self.tab_2_layout.addWidget(self.documentation_text)

    # Функции открытия окон
    def show_window_add_book(self):
        self.useClick()

        self.load_tags_and_genre_to_window_add_book()

        self.stackedWidget.setCurrentIndex(1)

    def show_window_search_book(self):
        self.useClick()

        self.load_tags_and_genre_to_window_search_book()

        self.stackedWidget.setCurrentIndex(3)

    def show_window_add_category(self):
        self.useClick()


        self.load_tag_to_window_add_tag()

        self.stackedWidget.setCurrentIndex(5)

    def show_window_delete_category(self):
        self.useClick()

        self.load_tag_to_window_delete_tag()

        self.stackedWidget.setCurrentIndex(4)

    def show_main_window(self):
        self.useClick()

        self.load_tree_main()

        self.stackedWidget.setCurrentIndex(0)

    # Функция добавления книги
    def add_book(self, script=False, data=None):

        select_genres = []
        select_tags = []

        if script:
            book_name = data.get('t', '')
            year = data.get('y', '')
            author_firstname = data.get('fn', '')
            author_lastname = data.get('ln', '')
            author_middlename = data.get('mn', '')
            author_nickname = data.get('nn', '')
            path_book = data.get('p', '')
            genres_data = data.get('genres', [])
            tags_data = data.get('tags', [])
            ld = GetData()
            ld.get_connection()
            for tag in tags_data:
                id_tag = ld.get_id_tag(tag)
                if not id_tag:
                    QMessageBox.warning(self, 'Ошибка', f'Тег "{tag}" не найден')
                    return
                select_tags.append(id_tag[0][0])
            for genre in genres_data:
                id_genre = ld.get_id_genre(genre)
                if not id_genre:
                    QMessageBox.warning(self, 'Ошибка', f'Жанр "{genre}" не найден')
                    return
                select_genres.append(id_genre[0][0])
            ld.close_connection()

        else:
            book_name = self.window_add_book_name_book.text().strip()
            year = self.window_add_book_year.text().strip()
            author_firstname = self.window_add_book_firstname.text().strip()
            author_lastname = self.window_add_book_lastname.text().strip()
            author_middlename = self.window_add_book_middlename.text().strip()
            author_nickname = self.window_add_book_nickname.text().strip()
            path_book = self.window_add_file_path.text().strip()
            tags_data, genres_data = self.get_select_tag_and_genre(tree_widget=self.window_add_book_treeWidget)
            select_tags = [tag['id'] for tag in tags_data]
            select_genres = [genre['id'] for genre in genres_data]

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

        if not path_book:
            QMessageBox.warning(self, 'Ошибка', 'Выберите файл книги')
            return

        # Проверка расширения файла
        _, file_extension = os.path.splitext(path_book)
        file_extension = file_extension.lower()
        if file_extension not in ['.fb2', '.pdf', '.txt']:
            QMessageBox.warning(self, 'Ошибка', 'Поддерживаются только файлы с расширениями .fb2, .pdf, .txt')
            return

        db_manager = DatabaseManager()

        try:
            # Проверяем существование книги
            if db_manager.book_exists(book_name):
                QMessageBox.warning(self, 'Ошибка', 'Книга с таким названием уже существует')
                return
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


            for tag in select_tags:
                db_manager.link_book_tags(id_book=book_id, id_tag=tag)

            for genre in select_genres:
                db_manager.link_book_genre(id_book=book_id, id_genre=genre)

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

    def get_select_tag_and_genre(self, tree_widget=None):
        if tree_widget is None:
            tree_widget = self.sender().parent().findChild(QTreeWidget)  # Автопоиск

        selected_tags = []
        selected_genres = []

        root_el_tree = tree_widget.invisibleRootItem()

        for i in range(root_el_tree.childCount()):
            parent = root_el_tree.child(i)
            for j in range(parent.childCount()):
                child = parent.child(j)
                if child.checkState(1) == 2:
                    name = child.text(0)
                    id_value = child.data(0, Qt.UserRole)
                    code = child.data(0, Qt.UserRole + 1)

                    if parent.text(0) == "Пользовательские теги":
                        selected_tags.append({"name": name, "id": id_value})
                    elif parent.text(0) == "Жанры":
                        selected_genres.append({"name": name, "id": id_value, "code": code})

        return selected_tags, selected_genres

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

    # Функция поиска книги
    def search_books(self, script=False, data=None):

        author = []
        tags = []
        genres = []
        loaddata = GetData()

        if script:
            book_name = data.get('t')
            author.append(data.get('fn', ''))
            author.append(data.get('ln', ''))
            author.append(data.get('mn', ''))
            author.append(data.get('nn', ''))
            year = data.get('y')
            tags = data.get('tags', [])
            genres = data.get('genres', [])
            loaddata.get_connection()
            for tag in tags:
                id_tag = loaddata.get_id_tag(tag)
                if not id_tag:
                    QMessageBox.warning(self, 'Ошибка', f'Тег "{tag}" не найден')
                    loaddata.close_connection()
                    return
            for genre in genres:
                id_genre = loaddata.get_id_genre(genre)
                if not id_genre:
                    QMessageBox.warning(self, 'Ошибка', f'Жанр "{genre}" не найден')
                    loaddata.close_connection()
                    return
            loaddata.close_connection()
        else:
            if self.window_search_book_name_book.text() != '':
                book_name = self.window_search_book_name_book.text().lower()
            else:
                book_name = None

            author.append(self.window_search_book_firstname.text())
            author.append(self.window_search_book_lastname.text())
            author.append(self.window_search_book_middlename.text())
            author.append(self.window_search_book_nickname.text())

            if self.window_search_book_year.text() != '':
                year = self.window_search_book_year.text()
            else:
                year = None

            selected_tags, selected_genres = self.get_select_tag_and_genre(tree_widget=self.window_search_book_treeWidget)

            for tag in selected_tags:
                tags.append(tag['name'])
            for genre in selected_genres:
                genres.append(genre['name'])

        # print(tags)
        # print(genres)

        filters = {

            "name": book_name,
            "author": author,
            "year": year,
            "genres": genres,
            "tags": tags

        }

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

        """
        Функция загрузки книг в QListWidget с поддержкой форматирования и кнопок действий.
        :param dict_of_books: Список словарей с информацией о книгах.
        """
        for el in dict_of_books:  # Проходимся по всем книгам
            for format in el["formats"]:  # Проходимся по форматам книги
                item = QListWidgetItem()
                item_widget = QWidget()
                item_widget.setObjectName("itemWidget")  # Для применения стилей

                # Применяем стили
                item_widget.setStyleSheet("""
                    #itemWidget {
                        border-bottom: 2px solid #A264F3;
                        border-top: none;
                        border-left: none;
                        border-right: none;
                        border-radius: 5px;
                        padding: 5px;
                        margin: 2px;            
                    }
                    #itemWidget:hover {
                        border-bottom: 5px solid #A264F3;
                        border-top: none;
                        border-left: none;
                        border-right: none;
                        border-radius: 5px;
                        padding: 5px;
                        margin: 2px;
                    }
                """)

                # Создаем элементы интерфейса
                line_text = QLabel(f'{el["name"].capitalize()}')
                line_empty = QLabel()
                line_format = QLabel(f"{format}")

                # Кнопка "Открыть"
                open_btn = HoverButton(self.close_eye_icon, self.open_eye_icon)
                open_btn.setToolTip("Открыть")
                open_btn.setCursor(Qt.PointingHandCursor)
                open_btn.setMaximumSize(50, 50)
                open_btn.setStyleSheet("border: none;")

                # Кнопка "Скопировать"
                copy_btn = HoverButton(self.not_select_copy, self.select_copy)
                copy_btn.setToolTip("Скопировать")
                copy_btn.setCursor(Qt.PointingHandCursor)
                copy_btn.setMaximumSize(50, 50)
                copy_btn.setStyleSheet("border: none;")

                # Кнопка "Редактировать"
                edit_btn = HoverButton(self.not_select_edit, self.select_edit)
                edit_btn.setToolTip("Редактировать")
                edit_btn.setCursor(Qt.PointingHandCursor)
                edit_btn.setMaximumSize(50, 50)
                edit_btn.setStyleSheet("border: none;")

                # Кнопка "Удалить"
                delete_btn = HoverButton(self.not_select_delete, self.select_delete)
                delete_btn.setToolTip("Удалить")
                delete_btn.setCursor(Qt.PointingHandCursor)
                delete_btn.setMaximumSize(50, 50)
                delete_btn.setStyleSheet("border: none;")

                # Устанавливаем стили для текстовых элементов
                line_text.setStyleSheet("border: none; font: 20px")
                line_empty.setStyleSheet("border: none;")
                line_format.setStyleSheet("border: none; font: 20px")

                # Генерация имени файла
                file_name = "".join("_" if ch == " " else ch for ch in el["name"])
                object_name = f"{file_name}_{format}.{format}"

                # Назначаем имена объектов для кнопок
                open_btn.setObjectName(object_name)
                copy_btn.setObjectName(object_name)
                delete_btn.setObjectName(object_name)

                # Подключаем обработчики событий
                open_btn.clicked.connect(self.clickedLinePB)
                copy_btn.clicked.connect(self.clicked_copy)
                delete_btn.clicked.connect(self.clicked_delete)
                edit_btn.clicked.connect(lambda checked, book_name=el["name"]: self.open_edit_window(book_name))

                # Создаем layout для виджета
                item_layout = QHBoxLayout()
                item_layout.addWidget(line_text)
                item_layout.addWidget(line_empty)
                item_layout.addWidget(line_format)
                item_layout.addWidget(open_btn)
                item_layout.addWidget(copy_btn)
                item_layout.addWidget(edit_btn)
                item_layout.addWidget(delete_btn)
                item_widget.setLayout(item_layout)

                # Устанавливаем размер подсказки и добавляем элемент в QListWidget
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

    def clicked_delete(self, script=False, data=None):

        db_manager = DatabaseManager()

        if script:
            ld = GetData()
            book_name = data.get('t')
            if not book_name:
                QMessageBox.warning(self, 'Ошибка', 'Необходимо указать название книги')
                return
            name, ext = os.path.splitext(book_name)
            if not ext:
                QMessageBox.warning(self, 'Ошибка', 'Необходимо указать формат ([Название].[формат])')
                return
            base_dir = Path(__file__).parent.resolve()
            books_dir = base_dir / "books"
            book_name_in_db = name.replace('_', ' ').lower()
            f = ext[1:].strip()

            ld.get_connection()
            if not ld.get_id_book(book_name_in_db):
                QMessageBox.warning(self, 'Ошибка', 'Книга не найдена')
                ld.close_connection()
                return
            if not ld.get_id_formats(f):
                QMessageBox.warning(self, 'Ошибка', 'Книга с данный форматом не найдена')
                ld.close_connection()
                return
            ld.close_connection()
            if not ld.get_info_about_formats(format_name=f, flag=True, book_name=book_name_in_db):
                QMessageBox.warning(self, 'Ошибка', 'Книга с данный форматом не найдена')
                return
            db_manager.delete_book(book_name_in_db)
            os.remove(books_dir / f"{name}_{f}.{f}")

            QMessageBox.information(self, 'Удаление', 'Книга удалена')
        else:
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

            db_manager.delete_book(book_name_in_db)

            os.remove(books_dir / f"{push_button.objectName()}")

            QMessageBox.information(self, 'Удаление', 'Книга удалена')

        self.load_tree_main()
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

        self.useClick()

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

    def add_tag(self, script=False, data=None):

        ld = GetData()
        dbm = DatabaseManager()
        if script:
            added = False
            name_new_tag = data.get('tags', [])
            ld.get_connection()
            for tag in name_new_tag:
                id_tag = ld.get_id_tag(tag.lower())
                if id_tag:
                    QMessageBox.information(self, 'Добавление тега', f"Тег с названием {tag} уже существует")
                    continue
                else:
                    dbm.add_tag(tag)
                    added = True
            ld.close_connection()
            if added:
                QMessageBox.information(self, 'Добавление тега', f"Теги успешно добавлены")
            else:
                QMessageBox.information(self, 'Добавление тега', f"Теги не добавлены")
        else:
            name_new_tag = self.window_add_tag_name_tag.text()
            # print(ld.get_id_tag(str(name_new_tag).lower()))
            ld.get_connection()

            if ld.get_id_tag(str(name_new_tag).lower()):
                # Вывод сообщения о том что тег с такми название муже сущетвует
                QMessageBox.information(self, 'Добавление тега', f"Тег с названием {name_new_tag} уже существует")
                return
            else:
                dbm.add_tag(str(name_new_tag))

            ld.close_connection()
            # Вывод сообщения о том что тег успешно добавлен
            QMessageBox.information(self, 'Добавление тега', f'Тег с названием {name_new_tag} добавлен')
        self.window_add_tag_name_tag.clear()
        self.load_tag_to_window_add_tag()

    def load_tag_to_window_add_tag(self):

        ld = GetData()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Название тегов'])  # Заголовки столбца

        root_item = self.model.invisibleRootItem()

        main_el = QStandardItem("Пользовательские теги")

        for el in ld.get_info_about_tags(full=True, flag=False):

            children = QStandardItem(f"{el['Name_tag']}")

            main_el.appendRow([children])

        root_item.appendRow([main_el])

        self.window_add_tag_treeView.setModel(self.model)

    def load_tag_to_window_delete_tag(self):

        ld = GetData()

        self.window_delete_tag_treeWidget.clear()

        self.window_delete_tag_treeWidget.setColumnCount(2)
        self.window_delete_tag_treeWidget.setHeaderLabels(["Название Тег", "Статус удаления"])

        tags = ld.get_info_about_tags(full=True, flag=False)

        for tag in tags:
            item = QTreeWidgetItem(self.window_delete_tag_treeWidget)

            item.setText(0 , tag['Name_tag'])

            # Добавляем чекбокс во вторую колонку
            item.setCheckState(1, Qt.Unchecked)  # По умолчанию не выбран

            # Можно сохранить данные тега в item
            item.setData(0, Qt.UserRole, tag["ID_tag"])  # Сохраняем ID тега

    def delete_tags(self, script=False, data=None):

        sv = DatabaseManager()

        if script:
            ld = GetData()
            tags_data = data.get('tags', [])
            selected_tags = []
            deleted = False
            ld.get_connection()
            for tag in tags_data:
                id_tag = ld.get_id_tag(tag.lower())
                if not id_tag:
                    QMessageBox.information(self, 'Удаление тега', f"Тег {tag} не существует")
                    continue
                else:
                    selected_tags.append({
                        'id': id_tag[0][0],
                        'name': tag
                    })

            if selected_tags:
                sv.delete_tags(selected_tags)
                QMessageBox.information(self, 'Удаление тега', f"Теги удалены")
            else:
                QMessageBox.information(self, 'Удаление тега', f"Теги не были удалены")
            ld.close_connection()

        else:
            # Получаем количество элементов в treeWidget
            item_count = self.window_delete_tag_treeWidget.topLevelItemCount()

            # Создаем список для хранения выбранных тегов
            selected_tags = []

            # Перебираем все элементы
            for i in range(item_count):
                item = self.window_delete_tag_treeWidget.topLevelItem(i)

                # Проверяем, отмечен ли чекбокс (вторая колонка)
                if item.checkState(1) == Qt.Checked:
                    # Получаем данные тега
                    tag_id = item.data(0, Qt.UserRole)  # ID тега
                    tag_name = item.text(0)             # Название тега

                    # Добавляем в список выбранных тегов
                    selected_tags.append({
                        'id': tag_id,
                        'name': tag_name
                    })

            print("selected_tags")
            print(selected_tags)

            if selected_tags:
                sv.delete_tags(selected_tags)
            else:
                print("Не выбрано ни одного тега для удаления")

        self.load_tag_to_window_delete_tag()

    # Дерево виджетов в окне добавления книги
    def load_tags_and_genre_to_window_add_book(self):

        self.window_add_book_treeWidget.clear()

        ld = GetData()

        # Полчуение всех тегов
        all_tags = ld.get_info_about_tags(full=True, flag=False)
        # print(all_tags)

        # Получение всех жанров
        all_genres = ld.get_info_about_genres(full=True, flag=False)
        # print(all_genres)

        # Формирование деерва
        self.window_add_book_treeWidget.setHeaderLabels(["Теги и жанры", "Статус добавления"])

        self.window_add_book_treeWidget.setColumnWidth(0, 350)

        root_tags_item = QTreeWidgetItem(self.window_add_book_treeWidget)
        root_tags_item.setText(0, "Пользовательские теги")

        root_genre_item = QTreeWidgetItem(self.window_add_book_treeWidget)
        root_genre_item.setText(0, "Жанры")

        for tag in all_tags:
            tag_in_tree = QTreeWidgetItem(root_tags_item)
            tag_in_tree.setText(0, f"{tag['Name_tag']}")
            tag_in_tree.setCheckState(1, 0)
            tag_in_tree.setData(0, Qt.UserRole, tag["ID_tag"])

        for genre in all_genres:
            genre_in_tree = QTreeWidgetItem(root_genre_item)
            genre_in_tree.setText(0, f"{genre['Name_genre']}")
            genre_in_tree.setCheckState(1, 0)
            genre_in_tree.setData(0, Qt.UserRole, genre["ID_genre"])
            genre_in_tree.setData(0, Qt.UserRole + 1, genre["Code"])

    def load_tags_and_genre_to_window_search_book(self):

        self.window_search_book_treeWidget.clear()

        ld = GetData()

        all_tags = ld.get_info_about_tags(full=True, flag=False)
        # print(all_tags)

        all_genres = ld.get_info_about_genres(full=True, flag=False)
        # print(all_genres)

        self.window_search_book_treeWidget.setHeaderLabels(["Теги и жанры", "Статус поиска"])

        self.window_search_book_treeWidget.setColumnWidth(0, 350)

        root_tags_item = QTreeWidgetItem(self.window_search_book_treeWidget)
        root_tags_item.setText(0, "Пользовательские теги")

        root_genre_item = QTreeWidgetItem(self.window_search_book_treeWidget)
        root_genre_item.setText(0, "Жанры")

        for tag in all_tags:
            tag_in_tree = QTreeWidgetItem(root_tags_item)
            tag_in_tree.setText(0, f"{tag['Name_tag']}")
            tag_in_tree.setCheckState(1, 0)
            tag_in_tree.setData(0, Qt.UserRole, tag["ID_tag"])

        for genre in all_genres:
            genre_in_tree = QTreeWidgetItem(root_genre_item)
            genre_in_tree.setText(0, f"{genre['Name_genre']}")
            genre_in_tree.setCheckState(1, 0)
            genre_in_tree.setData(0, Qt.UserRole, genre["ID_genre"])
            genre_in_tree.setData(0, Qt.UserRole + 1, genre["Code"])

    def load_tags_and_genre_to_window_edit_book(self):
        # self.window_search_book_treeWidget.clear()
        self.window_edit_book_treeWidget.clear()

        ld = GetData()

        all_tags = ld.get_info_about_tags(full=True, flag=False)
        # print(all_tags)

        all_genres = ld.get_info_about_genres(full=True, flag=False)
        # print(all_genres)

        self.window_edit_book_treeWidget.setHeaderLabels(["Теги и жанры", "Статус поиска"])

        self.window_edit_book_treeWidget.setColumnWidth(0, 350)

        root_tags_item = QTreeWidgetItem(self.window_edit_book_treeWidget)
        root_tags_item.setText(0, "Пользовательские теги")

        root_genre_item = QTreeWidgetItem(self.window_edit_book_treeWidget)
        root_genre_item.setText(0, "Жанры")

        for tag in all_tags:
            tag_in_tree = QTreeWidgetItem(root_tags_item)
            tag_in_tree.setText(0, f"{tag['Name_tag']}")
            tag_in_tree.setCheckState(1, 0)
            tag_in_tree.setData(0, Qt.UserRole, tag["ID_tag"])

        for genre in all_genres:
            genre_in_tree = QTreeWidgetItem(root_genre_item)
            genre_in_tree.setText(0, f"{genre['Name_genre']}")
            genre_in_tree.setCheckState(1, 0)
            genre_in_tree.setData(0, Qt.UserRole, genre["ID_genre"])
            genre_in_tree.setData(0, Qt.UserRole + 1, genre["Code"])

    # Главное дерево виджетов
    def on_tree_data_loaded(self, genres, tags, all_years, all_authors):
        self.main_window_tags.setUpdatesEnabled(False)
        ld = GetData()

        all_tags = tags
        # print(all_tags)

        all_genres = genres
        # print(all_genres)


        self.main_window_tags.clear()

        self.main_window_tags.setHeaderLabels(["Категории", "Книги"])
        self.main_window_tags.setColumnWidth(0, 250)

        root_standart_category = QTreeWidgetItem(self.main_window_tags)
        root_standart_category.setText(0, "Стандартные")

        root_standart_category.setIcon(0, QIcon("icon_folder.png"))

        root_user_category = QTreeWidgetItem(self.main_window_tags)
        root_user_category.setText(0,"Пользовательские")

        root_user_category.setIcon(0, QIcon("icon_folder.png"))

        # Обработка для стандартных категорий
        list_standart_category = ["Жанры", "Года", "Автор"]

        for el in list_standart_category:
            standart_category = QTreeWidgetItem(root_standart_category)
            standart_category.setText(0, f"{el}")
            standart_category.setIcon(0, QIcon("icon_folder.png"))

            if el == "Жанры":
                for genre in all_genres:
                    genre_category = QTreeWidgetItem(standart_category)
                    genre_category.setText(0, genre["Name_genre"])
                    genre_category.setIcon(0, QIcon("icon_folder.png"))
                    books_with_this_genre = ld.get_books_by_name_genre(genre["Name_genre"])
                    for book_with_genre in books_with_this_genre:
                        # Получение форматов книги
                        formats_ = ld.get_books({"name": book_with_genre[1]})[0]["formats"]
                        # print(f"formats: {formats_}")
                        for format_ in formats_:
                            book_genre = QTreeWidgetItem(genre_category)
                            book_genre.setText(1, f"{book_with_genre[1]} {format_}")
                            book_genre.setData(1, Qt.UserRole, book_with_genre[0])
                            book_genre.setData(1, Qt.UserRole + 1, book_with_genre[1])
                            book_genre.setData(1, Qt.UserRole + 2, book_with_genre[2])
                            book_genre.setData(1, Qt.UserRole + 3, book_with_genre[3])
                            book_genre.setData(1, Qt.UserRole + 4, format_)
                            book_genre.setIcon(1, QIcon("icon_book.png"))

            elif el == "Года":


                unique_years = all_years
                # Добавляем все года
                for year in unique_years:
                    year_category = QTreeWidgetItem(standart_category)
                    year_category.setText(0, f"{year}")
                    year_category.setIcon(0, QIcon("icon_folder.png"))
                    # Добавляем для текущего года книги
                    books_with_year = ld.get_books_by_year(year)
                    for book_with_year in books_with_year:
                        # Получение форматов книги
                        formats_ = ld.get_books({"name": book_with_year[1]})[0]["formats"]
                        # print(f"formats: {formats_}")
                        for format_ in formats_:
                            book_year = QTreeWidgetItem(year_category)
                            book_year.setText(1, f"{book_with_year[1]} {format_}")
                            book_year.setData(1, Qt.UserRole, book_with_year[0])
                            book_year.setData(1, Qt.UserRole + 1, book_with_year[1])
                            book_year.setData(1, Qt.UserRole + 2, book_with_year[2])
                            book_year.setData(1, Qt.UserRole + 3, book_with_year[3])
                            book_year.setData(1, Qt.UserRole + 4, format_)
                            book_year.setIcon(1, QIcon("icon_book.png"))

            elif el == "Автор":
                authors = all_authors
                for author in authors:
                    author_category = QTreeWidgetItem(standart_category)
                    index = 0
                    name = ""
                    for partname in author:
                        if index == 1 or index == 2 or index == 3:
                            if partname != None:
                                name += partname + " "
                        index += 1
                        author_category.setText(0, f"{name}")
                        author_category.setIcon(0, QIcon("icon_folder.png"))

                    author_filt = []
                    if author[1] != None:
                        author_filt.append(author[1])
                    else:
                        author_filt.append("")

                    if author[2] != None:
                        author_filt.append(author[2])
                    else:
                        author_filt.append("")

                    if author[3] != None:
                        author_filt.append(author[3])
                    else:
                        author_filt.append("")

                    if author[4] != None:
                        author_filt.append(author[4])
                    else:
                        author_filt.append("")

                    filters = {"author": author_filt}
                    books_with_author = ld.get_books(filters)

                    for book_author_ in books_with_author:

                        for formats in book_author_["formats"]:
                            name_book_ = book_author_["name"]
                            formats_ = formats
                            id_book_ = ld.get_id_book(book_author_["name"])[0][0]

                            book_author = QTreeWidgetItem(author_category)
                            book_author.setText(1, f"{name_book_} {formats_}")
                            book_author.setData(1, Qt.UserRole, id_book_)
                            book_author.setData(1, Qt.UserRole + 1, name_book_)

                            # Пусть поля год и автор будут пустыми
                            # book_author.setData(1, Qt.UserRole + 2, formats_)
                            # book_author.setData(1, Qt.UserRole + 3, book_with_year[3])
                            book_author.setData(1, Qt.UserRole + 4, formats_)
                            book_author.setIcon(1, QIcon("icon_book.png"))

        # Обработка для тегов
        for tag in all_tags:
            user_category = QTreeWidgetItem(root_user_category)
            user_category.setText(0, f"{tag['Name_tag'].capitalize()}")
            user_category.setIcon(0, QIcon("icon_folder.png"))
            search_tag = tag['Name_tag']
            books = ld.get_books_by_name_tag(search_tag)
            for book in books:
                # Получение форматов книги
                formats_ = ld.get_books({"name": book[1]})[0]["formats"]
                # print(f"formats tags: {formats_}")
                for format_ in formats_:
                    book_with_tag = QTreeWidgetItem(user_category)
                    book_with_tag.setText(1, f"{book[1].capitalize()} {format_}")
                    book_with_tag.setData(1, Qt.UserRole, book[0])
                    book_with_tag.setData(1, Qt.UserRole + 1, book[1])
                    book_with_tag.setData(1, Qt.UserRole + 2, book[2])
                    book_with_tag.setData(1, Qt.UserRole + 3, book[3])
                    book_with_tag.setData(1, Qt.UserRole + 4, format_)
                    book_with_tag.setIcon(1, QIcon("icon_book.png"))

        self.main_window_tags.setUpdatesEnabled(True)
        # self.load_books_to_list_widgets() # нужно название книги и id - {'name': 'затерянный мир (сборник)', 'formats': ['fb2']}

    def on_item_double_clicked(self, item, column):
        if column == 1 and item.data(1, Qt.UserRole) is not None:
            book_id = item.data(1, Qt.UserRole)
            book_name = item.data(1, Qt.UserRole + 1)
            book_author = item.data(1, Qt.UserRole + 2)
            book_date = item.data(1, Qt.UserRole + 3)
            book_format = item.data(1, Qt.UserRole + 4)

            book = [{'name': book_name, 'formats': [book_format]}]

            self.listWidget.clear()

            self.load_books_to_list_widgets(book)

            # Получать значение по книге название и форматы и вызвать функцию для загрузки книги в основное поле для книг
            print(f"ID: {book_id}")
            print(f"Название: {book_name}")
            print(f"Автор: {book_author}")
            print(f"Год: {book_date}")
            print(f"Формат: {book_format}")

    def parse_line(self):
        # print(self.main_window_LineEdit.text())
        command_types = {
            'rus': {
                'добавить': 'add',
                'удалить': 'delete',
                'редактировать': 'edit',
                'найти': 'search',
                'книгу': 'book',
                'тег': 'tag'
            },
            'eng': {
                'add': 'add',
                'delete': 'delete',
                'edit': 'edit',
                'search': 'search',
                'book': 'book',
                'tag': 'tag'
            }
        }

        KEY_MAP = {
            "rus": {"н": "t", "новн": "newt", "и": "fn", "ф": "ln", "от": "mn", "нн": "nn", "г": "y", "п": "p",
                    "жанры": "genres", "теги": "tags"},
            "eng": {"t": "t","newt": "newt", "fn": "fn", "ln": "ln", "mn": "mn", "nn": "nn", "y": "y", "p": "p",
                    "genres": "genres", "tags": "tags"}
        }

        command = self.main_window_LineEdit.text().strip()
        if not command:
            return
        parts = command.strip().split(' ', 2)


        if len(parts) < 2:
            QMessageBox.warning(self, 'Ошибка', 'Неполная команда')
            return

        command_type = parts[0].lower()
        command_obj = parts[1].lower()
        result = {}

        lang = 'rus' if command_type in command_types['rus'] else 'eng'
        if command_type not in command_types[lang] or command_obj not in command_types[lang]:
            QMessageBox.warning(self, 'Ошибка', 'Неизвестная команда')
            return

        if command_type in ('найти', 'search') and command_obj in ('книгу', 'book'):
            if len(parts) < 3:
                result = {'genres': [], 'tags': []}
                self.search_books(script=True, data=result)
                return

        if len(parts) < 3:
            QMessageBox.warning(self, 'Ошибка', 'Неполная команда')
            return

        params = parts[2]

        # print(params)

        data = {}
        genres = []
        tags = []
        param_parts = []
        current_part = []
        in_quotes = False

        for char in params:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current_part:
                    param_parts.append(''.join(current_part))
                    current_part = []
                continue
            current_part.append(char)

        if current_part:
            param_parts.append(''.join(current_part))
        # print(param_parts)

        for part in param_parts:
            if '=' in part:
                key, value = part.split('=', 1)
                key = key.strip()
                value = value.strip('"').strip()

                # Обработка списков
                if KEY_MAP[lang].get(key) == 'tags':
                    tags = [t.strip().lower() for t in value.split(',') if t.strip()]
                elif KEY_MAP[lang].get(key) == 'genres':
                    genres = [g.strip() for g in value.split(',') if g.strip()]
                else:
                    if value:
                        mapped_key = KEY_MAP[lang].get(key)
                        if mapped_key:
                            data[mapped_key] = value
        # print(data)
        result = {
            **data,
            'genres': genres,
            'tags': tags
        }
        # print(result)

        if (command_types[lang].get(command_type) == "add"
                and command_types[lang].get(command_obj) == "book"):
            self.add_book(script=True, data=result)
        elif (command_types[lang].get(command_type) == "search"
              and command_types[lang].get(command_obj) == "book"):
            self.search_books(script=True, data=result)
        elif (command_types[lang].get(command_type) == "add"
              and command_types[lang].get(command_obj) == "tag"):
            self.add_tag(script=True, data=result)
        elif (command_types[lang].get(command_type) == "delete"
              and command_types[lang].get(command_obj) == "tag"):
            self.delete_tags(script=True, data=result)
        elif (command_types[lang].get(command_type) == "delete"
              and command_types[lang].get(command_obj) == "book"):
            self.clicked_delete(script=True, data=result)
        elif (command_types[lang].get(command_type) == "edit"
              and command_types[lang].get(command_obj) == "book"):
            self.edit_book(script=True, data=result)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неизвестная команда')
            return

    def open_edit_window(self, book_name):
        self.load_tags_and_genre_to_window_edit_book()

        self.current_edit_book_name = book_name
        loaddata = GetData()
        book_info = loaddata.get_info_about_books(flag=True, book_name=book_name)

        if book_info:
            info = book_info[0]
            self.window_edit_book_name_book.setText(info['name_book'])
            self.window_edit_book_year.setText(str(info['year']))
            self.window_edit_book_firstname.setText(info['firstname'])
            self.window_edit_book_lastname.setText(info['lastname'])
            self.window_edit_book_middlename.setText(info['middlename'] if info['middlename'] else "")
            self.window_edit_book_nickname.setText(info['nickname'] if info['nickname'] else "")

            if info['genres']:
                self.set_selected_items_in_tree(self.window_edit_book_treeWidget, info['genres'], parent_name="Жанры‹")
            if info['tags']:
                self.set_selected_items_in_tree(self.window_edit_book_treeWidget, info['tags'],
                                                parent_name="Пользовательские теги")

            self.current_edit_book_id = info['id_book']
            self.current_edit_author_id = info['id_author']
            self.stackedWidget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Не удалось загрузить информацию о книге')

    def set_selected_items_in_tree(self, tree_widget, selected_items, parent_name):
        root = tree_widget.invisibleRootItem()
        for i in range(root.childCount()):
            parent = root.child(i)
            if parent.text(0) == parent_name:
                for j in range(parent.childCount()):
                    child = parent.child(j)
                    item_name = child.text(0)
                    if item_name in selected_items:
                        child.setCheckState(1, Qt.Checked)
                    else:
                        child.setCheckState(1, Qt.Unchecked)
                break

    def edit_book(self, script=True, data=None):

        loaddata = GetData()
        selected_tag_ids = []
        selected_genre_ids = []
        if script:
            self.current_edit_book_name = data.get('t')
            if not self.current_edit_book_name:
                QMessageBox.warning(self, 'Ошибка', 'Введите название книги')
                return
            loaddata.get_connection()
            if not loaddata.get_id_book(self.current_edit_book_name.lower()):
                QMessageBox.warning(self, 'Ошибка', 'Книга не найдена')
                loaddata.close_connection()
                return
            loaddata.close_connection()
            book_info = loaddata.get_info_about_books(flag=True, book_name=self.current_edit_book_name.lower())[0]
            self.current_edit_book_id = book_info['id_book']
            self.current_edit_author_id = book_info['id_author']
            if data.get('newt'):
                new_book_name = data.get('newt').lower()
            else:
                new_book_name = book_info['name_book']
            if data.get('y'):
                year = data.get('y')
            else:
                year = book_info['year']
            if data.get('fn'):
                author_firstname = data.get('fn')
            else:
                author_firstname = book_info['firstname']
            if data.get('ln'):
                author_lastname = data.get('ln')
            else:
                author_lastname = book_info['lastname']
            if data.get('mn'):
                author_middlename = data.get('mn')
            else:
                author_middlename = book_info['middlename']
            if data.get('nn'):
                author_nickname = data.get('nn')
            else:
                author_nickname = book_info['nickname']
            if data.get('tags'):
                selected_tags = data.get('tags', [])
            else:
                selected_tags = book_info.get('tags', [])
            if data.get('genres'):
                selected_genres = data.get('genres', [])
            else:
                selected_genres = book_info.get('genres', [])
            loaddata.get_connection()
            if selected_genres is None:
                selected_genres = []
            if selected_tags is None:
                selected_tags = []
            for tag in selected_tags:
                id_tag = loaddata.get_id_tag(tag)
                if not id_tag:
                    QMessageBox.warning(self, 'Ошибка', f'Тег "{tag}" не найден')
                    loaddata.get_connection()
                    return
                selected_tag_ids.append(id_tag[0][0])
            for genre in selected_genres:
                id_genre = loaddata.get_id_genre(genre)
                if not id_genre:
                    QMessageBox.warning(self, 'Ошибка', f'Жанр "{genre}" не найден')
                    loaddata.get_connection()
                    return
                selected_genre_ids.append(id_genre[0][0])
            loaddata.close_connection()

        else:
            new_book_name = self.window_edit_book_name_book.text().strip()
            year = self.window_edit_book_year.text().strip()
            author_firstname = self.window_edit_book_firstname.text().strip()
            author_lastname = self.window_edit_book_lastname.text().strip()
            author_middlename = self.window_edit_book_middlename.text().strip()
            author_nickname = self.window_edit_book_nickname.text().strip()
            selected_tags, selected_genres = self.get_select_tag_and_genre(
                tree_widget=self.window_edit_book_treeWidget
            )
            selected_genre_ids = [genre['id'] for genre in selected_genres]
            selected_tag_ids = [tag['id'] for tag in selected_tags]

        if not new_book_name:
            QMessageBox.warning(self, 'Ошибка', 'Введите название книги')
            return
        loaddata.get_connection()
        if new_book_name.lower() != self.current_edit_book_name.lower():
            if loaddata.get_id_book(new_book_name.lower()):
                QMessageBox.warning(self, 'Ошибка', 'Книга с таким названием уже существует')
                loaddata.close_connection()
                return
        loaddata.close_connection()
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

        db_manager = DatabaseManager()

        try:
            db_manager.update_book(self.current_edit_book_id, new_book_name, year)
            db_manager.update_author(
                self.current_edit_author_id,
                firstname=author_firstname,
                lastname=author_lastname,
                middlename=author_middlename if author_middlename else None,
                nickname=author_nickname if author_nickname else None
            )

            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Books_Genres WHERE ID_book = ?",
                               (self.current_edit_book_id,))
                for genre_id in selected_genre_ids:
                    cursor.execute(
                        "INSERT INTO Books_Genres (ID_book, ID_genre) VALUES (?, ?)",
                        (self.current_edit_book_id, genre_id)
                    )

                cursor.execute("DELETE FROM Books_Tags WHERE ID_book = ?",
                               (self.current_edit_book_id,))
                for tag_id in selected_tag_ids:
                    cursor.execute(
                        "INSERT INTO Books_Tags (ID_book, ID_tag) VALUES (?, ?)",
                        (self.current_edit_book_id, tag_id)
                    )

                conn.commit()

            book_info = loaddata.get_info_about_books(flag=True, book_name=new_book_name.lower())[0]
            old_formats = book_info['formats']
            if self.current_edit_book_name.lower() != new_book_name.lower():
                base_dir = Path(__file__).parent.resolve()
                books_dir = base_dir / "books"

                for format_name in old_formats:

                    old_safe_name = self.current_edit_book_name.replace(" ", "_").lower()
                    old_filename = f"{old_safe_name}_{format_name}.{format_name}"
                    old_path = books_dir / old_filename

                    new_safe_name = new_book_name.replace(" ", "_").lower()
                    new_filename = f"{new_safe_name}_{format_name}.{format_name}"
                    new_path = books_dir / new_filename

                    if old_path.exists():
                        old_path.rename(new_path)

            QMessageBox.information(self, 'Успех', 'Данные книги обновлены!')
            self.current_edit_book_name = new_book_name
            self.show_main_window()
            self.search_books()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка при обновлении: {str(e)}')

    def useClick(self):
        file_path = "click_1.mp3"

        # Создаем медиа контент из файла
        url = QUrl.fromLocalFile(file_path)
        content = QMediaContent(url)

        # Устанавливаем контент и воспроизводим
        self.player.setMedia(content)
        self.player.play()

    def calculating_statistics(self):
        # Общее количество книг
        ld = GetData()
        count_books = str(len(ld.get_books({})))
        self.count_books.clear()
        self.count_books.setText(f"Общее количество книг: {count_books}")

        # Статистика процента книг по жанрам и тегам
        info_genre_for_statistic = ld.statistic_1()
        use_genre = [genre[1] for genre in info_genre_for_statistic]
        count_book_fro_use_genre = [genre[2] for genre in info_genre_for_statistic]
        info_tag_for_statistic = ld.statistic_1_2()
        use_genre = use_genre + [tag[1] for tag in info_tag_for_statistic]
        count_book_fro_use_genre = count_book_fro_use_genre + [tag[2] for tag in info_tag_for_statistic]
        # Очищаем текущий макет (если есть)
        if self.widget_1.layout():
            layout = self.widget_1.layout()
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            layout = QVBoxLayout(self.widget_1)
        fig = Figure(figsize=(5, 5), dpi=150, facecolor='none')
        ax = fig.add_subplot(111)
        labels = use_genre
        sizes = count_book_fro_use_genre
        # Настройки шрифтов
        font_props = {
            'fontsize': 6,          # Размер шрифта для labels
            'color': 'black',       # Цвет текста
        }
        # Параметры для autopct (процентных значений)
        autopct_props = {
            'fontsize': 5,          # Размер шрифта для процентов
            'color': 'white',       # Цвет текста процентов
            'weight': 'bold'        # Жирный шрифт для лучшей читаемости
        }
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            textprops=font_props,
            pctdistance=0.85
        )
        for autotext in autotexts:
            autotext.set_fontsize(autopct_props['fontsize'])
            autotext.set_color(autopct_props['color'])
            autotext.set_weight(autopct_props['weight'])
        ax.set_title("Процент книг по жанрам и тегам", fontsize=8, pad=10)
        fig.tight_layout()
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        self.widget_1.setLayout(layout)

        # Статистика процента книг по авторам
        info_author_for_statistic = ld.statistic_2()
        use_author = [f"{author[1]} {author[2]} {author[3]} {author[4]}" for author in info_author_for_statistic]
        count_book_for_use_author = [author[5] for author in info_author_for_statistic]
        # Очищаем текущий макет (если есть)
        if self.widget_2.layout():
            layout = self.widget_2.layout()
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            layout = QVBoxLayout(self.widget_2)
        fig = Figure(figsize=(5, 5), dpi=150, facecolor='none')
        ax = fig.add_subplot(111)
        labels = use_author
        sizes = count_book_for_use_author
        # Настройки шрифтов
        font_props = {
            'fontsize': 6,
            'color': 'black',
        }
        autopct_props = {
            'fontsize': 5,
            'color': 'white',
            'weight': 'bold'
        }
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            textprops=font_props,
            pctdistance=0.85
        )
        for autotext in autotexts:
            autotext.set_fontsize(autopct_props['fontsize'])
            autotext.set_color(autopct_props['color'])
            autotext.set_weight(autopct_props['weight'])
        ax.set_title("Процент книг по авторам", fontsize=8, pad=10)
        fig.tight_layout()
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        self.widget_2.setLayout(layout)

        # Статистика добавленных книг по годам и месяцам
        print(ld.statistic_3())
        try:
            # Получаем данные из БД
            book_stats = ld.statistic_3()  # Предполагаем, что это метод, который возвращает данные как в вашем исходном запросе

            if not book_stats:
                print("Нет данных для отображения")
                return

            # Подготовка данных для графика
            dates = [f"{row[0]}-{row[1]}" for row in book_stats]  # Год-месяц
            counts = [row[2] for row in book_stats]  # Количество книг

            # Очищаем текущий макет (если есть)
            if self.widget.layout():
                layout = self.widget.layout()
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
            else:
                layout = QVBoxLayout(self.widget)

            # Создаем фигуру
            fig = Figure(figsize=(5, 3), dpi=100, facecolor='none')
            ax = fig.add_subplot(111)

            # Настройки шрифтов
            font_props = {
                'fontsize': 8,
                'color': 'black'
            }

            # Строим столбчатую диаграмму
            bars = ax.bar(dates, counts, color='skyblue')

            # Добавляем значения на столбцы
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=6)

            # Настройки осей
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(dates, rotation=45, ha='right', fontsize=6)
            ax.set_ylabel('Количество книг', fontdict=font_props)
            ax.set_title("Статистика добавления книг по месяцам", fontsize=10, pad=10)

            # Улучшаем внешний вид
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            fig.tight_layout()

            # Отображаем график
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
            self.widget.setLayout(layout)

        except Exception as e:
            print(f"Ошибка при построении графика: {e}")

    def show_documentation(self):
        # Заполняем текст документации
        documentation_content = r"""
        **Инструкция по использованию приложения BookHive**

        ---

        ### Введение

        Приложение BookHive предназначено для управления библиотекой книг. Оно позволяет добавлять, редактировать, удалять книги и авторов, а также осуществлять поиск по различным критериям.

        ---

        ### Основные функции

        1. **Добавление книги**
           - Нажмите на кнопку "Добавить книгу".
           - Заполните все необходимые поля: название книги, год издания, имя и фамилию автора, выберите файл книги.
           - Выберите теги и жанры, если необходимо.
           - Нажмите "Добавить", чтобы сохранить книгу в базе данных.

        2. **Редактирование книги**
           - Найдите книгу в списке и дважды щелкните по ней.
           - Измените необходимые данные.
           - Нажмите "Редактировать", чтобы сохранить изменения.

        3. **Удаление книги**
           - Найдите книгу в списке и нажмите кнопку "Удалить".
           - Подтвердите удаление, если будет запрошено.

        4. **Поиск книги**
           - Перейдите на вкладку "Поиск книги".
           - Введите критерии поиска: название, автор, год, теги и жанры.
           - Нажмите "Поиск", чтобы отобразить результаты.

        5. **Добавление тегов**
           - Перейдите на вкладку "Добавить тег".
           - Введите название нового тега и нажмите "Добавить".

        6. **Удаление тегов**
           - Перейдите на вкладку "Удалить тег".
           - Выберите теги, которые хотите удалить, и нажмите "Удалить".

        ---

        ### Работа с интерфейсом

        - **Главное окно**: отображает дерево категорий и список книг.
        - **Стековый виджет**: позволяет переключаться между различными окнами (добавление книги, поиск, редактирование и т.д.).
        - **Кнопки действий**: каждая книга в списке имеет кнопки для открытия, копирования, редактирования и удаления.

        ---

        ### Использование командной строки

        Приложение BookHive также поддерживает ввод команд через текстовое поле. Это позволяет пользователям выполнять действия с помощью текстовых команд. Вот список доступных команд и их описание:

        #### Команды

        1. **Добавить книгу**
           - **Команда**: `добавить книгу`
           - **Формат ввода**: 
             ```
             добавить книгу "название" "автор" "год" "путь_к_файлу" жанры="жанр1, жанр2" теги="тег1, тег2"
             ```
           - **Пример**:
             ```
             добавить книгу "Война и мир" "Лев Толстой" "1869" "C:\Books\war_and_peace.pdf" жанры="роман, исторический" теги="классика, русская литература"
             ```

        2. **Удалить книгу**
           - **Команда**: `удалить книгу`
           - **Формат ввода**:
             ```
             удалить книгу "название"
             ```
           - **Пример**:
             ```
             удалить книгу "Война и мир"
             ```

        3. **Редактировать книгу**
           - **Команда**: `редактировать книгу`
           - **Формат ввода**:
             ```
             редактировать книгу "старое_название" "новое_название" "новый_автор" "новый_год" "новый_путь_к_файлу"
             ```
           - **Пример**:
             ```
             редактировать книгу "Война и мир" "Война и мир (издание 2023)" "Лев Толстой" "1869" "C:\Books\war_and_peace_2023.pdf"
             ```

        4. **Найти книгу**
           - **Команда**: `найти книгу`
           - **Формат ввода**:
             ```
             найти книгу "название" автор="имя_автора" год="год" теги="тег1, тег2" жанры="жанр1, жанр2"
             ```
           - **Пример**:
             ```
             найти книгу "Война и мир" автор="Лев Толстой" год="1869" теги="классика" жанры="роман"
             ```

        5. **Добавить тег**
           - **Команда**: `добавить тег`
           - **Формат ввода**:
             ```
             добавить тег "название_тега"
             ```
           - **Пример**:
             ```
             добавить тег "новый_тег"
             ```

        6. **Удалить тег**
           - **Команда**: `удалить тег`
           - **Формат ввода**:
             ```
             удалить тег "название_тега"
             ```
           - **Пример**:
             ```
             удалить тег "старый_тег"
             ```

        ---

        ### Заключение

        Приложение BookHive предоставляет удобный интерфейс для управления вашей библиотекой. Следуйте этой инструкции, чтобы максимально эффективно использовать все функции приложения.
        """

        self.documentation_text.setPlainText(documentation_content)

    def changeTab(self, index):
        if index == 1:
            self.calculating_statistics()
        if index == 2:
            self.show_documentation()

    def show_statistic_book_tags_genre(self):
        self.stackedWidget_2.setCurrentIndex(0)

    def show_statistic_book_author(self):
        self.stackedWidget_2.setCurrentIndex(1)


    def init_tree_loader(self):
        self.tree_loader = DataLoader()
        self.tree_loader.data_ready.connect(self.on_tree_data_loaded)

    def load_tree_main(self):
        if not self.tree_loader.isRunning():
            self.tree_loader.start()

class HoverButton(QPushButton):
    def __init__(self, normal_icon, hover_icon, parent=None):
        super().__init__(parent)
        self.normal_icon = normal_icon
        self.hover_icon = hover_icon
        self.setIconSize(QSize(35, 35))
        self.setIcon(normal_icon)
        
    def enterEvent(self, event):
        self.setIcon(self.hover_icon)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.setIcon(self.normal_icon)
        super().leaveEvent(event)

class DataLoader(QThread):
    data_ready = pyqtSignal(object, object, object, object)

    def run(self):
        ld = GetData()
        genres = ld.get_info_about_genres(full=True, flag=False)
        tags = ld.get_info_about_tags(full=True, flag=False)
        all_years = ld.get_unique_years()
        all_authors = ld.get_info_about_authors(author={}, flag=False)
        self.data_ready.emit(genres, tags, all_years, all_authors)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.showMaximized()
    sys.exit(app.exec_())







