import sys
import os

from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QMimeData, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidgetItem, QWidget, QLabel, QPushButton, QHBoxLayout, QTreeWidget, QTreeWidgetItem
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

        # Кнопка удлаение тегов
        self.window_delete_tag_btn_delete.clicked.connect(self.delete_tags)

        # Добавление обработчиков кликов по дереву
        self.main_window_tags.itemClicked.connect(self.on_item_clicked)
        self.main_window_tags.itemDoubleClicked.connect(self.on_item_double_clicked)




# Функции открытия окон
    def show_window_add_book(self):
        # print("Add book")

        # self.load_tree_main()

        self.load_tags_and_genre_to_window_add_book()

        self.stackedWidget.setCurrentIndex(1)
    
    def show_window_search_book(self):
        # print("Search book")
        self.load_tags_and_genre_to_window_search_book()

        self.stackedWidget.setCurrentIndex(3)
    
    def show_window_add_category(self):
        # print("Add category")

        self.load_tag_to_window_add_tag()
        
        self.stackedWidget.setCurrentIndex(5)
    
    def show_window_delete_category(self):
        # print("Delete category")

        self.load_tag_to_window_delete_tag()

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

            # 7. Получение выбранных тегов и жанров
            select_tags, select_genre = self.get_select_tag_and_genre(tree_widget=self.window_add_book_treeWidget)

            for tag in select_tags:
                db_manager.link_book_tags(id_book=book_id, id_tag=tag["id"])

            for genre in select_genre:
                db_manager.link_book_genre(id_book=book_id, id_genre=genre["id"])

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

        # print("Выбранные теги:", selected_tags)
        # print("Выбранные жанры:", selected_genres)



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

        selected_tags, selected_genres = self.get_select_tag_and_genre(tree_widget=self.window_search_book_treeWidget)
        tags = []
        genres = []
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
        ld.get_connection()

        if ld.get_id_tag(str(name_new_tag).lower()):
            # Вывод сообщения о том что тег с такми название муже сущетвует
            QMessageBox.information(self, 'Добавление ткга', f"Тэг с названием {name_new_tag} уже существует")
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

    def delete_tags(self):

        sv = DatabaseManager()

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

    # Главное дерево виджетов
    def load_tree_main(self):
        
        self.main_window_tags.clear()

    def on_item_double_clicked(self):
        print(2)
    
    def on_item_clicked(self):
        print(1)





        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.showMaximized()
    sys.exit(app.exec_())
