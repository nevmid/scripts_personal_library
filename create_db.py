import sqlite3

# Список жанров
genres_data = [
    ('Природа и животные', 'adv_animal'),
    ('Путешествия и география', 'adv_geo'),
    ('Исторические приключения', 'adv_history'),
    ('Приключения про индейцев', 'adv_indian'),
    ('Морские приключения', 'adv_maritime'),
    ('Вестерн', 'adv_western'),
    ('Прочие приключения', 'adventure'),
    ('Античная литература', 'antique_ant'),
    ('Древневосточная литература', 'antique_east'),
    ('Европейская старинная литература', 'antique_european'),
    ('Мифы. Легенды. Эпос', 'antique_myths'),
    ('Древнерусская литература', 'antique_russian'),
    ('Прочая старинная литература', 'antique'),
    ('Детские приключения', 'child_adv'),
    ('Детские остросюжетные', 'child_det'),
    ('Детская образовательная литература', 'child_education'),
    ('Детская проза', 'child_prose'),
    ('Детская фантастика', 'child_sf'),
    ('Сказка', 'child_tale'),
    ('Детские стихи', 'child_verse'),
    ('Прочая детская литература', 'children'),
    ('Базы данных', 'comp_db'),
    ('Компьютерное "железо" (аппаратное обеспечение)', 'comp_hard'),
    ('ОС и Сети', 'comp_osnet'),
    ('Программирование', 'comp_programming'),
    ('Программы', 'comp_soft'),
    ('Интернет', 'comp_www'),
    ('Прочая околокомпьтерная литература', 'computers'),
    ('Искусство и дизайн', 'design'),
    ('Боевик', 'det_action'),
    ('Классический детектив', 'det_classic'),
    ('Криминальный детектив', 'det_crime'),
    ('Шпионский детектив', 'det_espionage'),
    ('Крутой детектив', 'det_hard'),
    ('Исторический детектив', 'det_history'),
    ('Иронический детектив', 'det_irony'),
    ('Маньяки', 'det_maniac'),
    ('Полицейский детектив', 'det_police'),
    ('Политический детектив', 'det_political'),
    ('Детектив (прочий)', 'detective'),
    ('Драматургия', 'dramaturgy'),
    ('Кулинария', 'home_cooking'),
    ('Хобби и ремесла', 'home_crafts'),
    ('Сделай сам', 'home_diy'),
    ('Развлечения', 'home_entertain'),
    ('Сад и огород', 'home_garden'),
    ('Здоровье', 'home_health'),
    ('Домашние животные', 'home_pets'),
    ('Эротика, Секс', 'home_sex'),
    ('Спорт', 'home_sport'),
    ('Прочие домоводство', 'home'),
    ('Анекдоты', 'humor_anecdote'),
    ('Юмористическая проза', 'humor_prose'),
    ('Юмористические стихи', 'humor_verse'),
    ('Прочий юмор', 'humor'),
    ('Современные любовные романы', 'love_contemporary'),
    ('Остросюжетные любовные романы', 'love_detective'),
    ('Эротика', 'love_erotica'),
    ('Исторические любовные романы', 'love_history'),
    ('Короткие любовные романы', 'love_short'),
    ('Биографии и Мемуары', 'nonf_biography'),
    ('Критика', 'nonf_criticism'),
    ('Публицистика', 'nonf_publicism'),
    ('Прочая документальная литература', 'nonfiction'),
    ('Поэзия', 'poetry'),
    ('Классическая проза', 'prose_classic'),
    ('Современная проза', 'prose_contemporary'),
    ('Контркультура', 'prose_counter'),
    ('Историческая проза', 'prose_history'),
    ('Русская классическая проза', 'prose_rus_classic'),
    ('Советская классическая проза', 'prose_su_classics'),
    ('Словари', 'ref_dict'),
    ('Энциклопедии', 'ref_encyc'),
    ('Руководства', 'ref_guide'),
    ('Справочники', 'ref_ref'),
    ('Прочая справочная литература', 'reference'),
    ('Эзотерика', 'religion_esoterics'),
    ('Религия', 'religion_rel'),
    ('Самосовершенствование', 'religion_self'),
    ('Прочая религиозная литература', 'religion'),
    ('Биология', 'sci_biology'),
    ('Деловая литература', 'sci_business'),
    ('Химия', 'sci_chem'),
    ('Культурология', 'sci_culture'),
    ('История', 'sci_history'),
    ('Юриспруденция', 'sci_juris'),
    ('Языкознание', 'sci_linguistic'),
    ('Математика', 'sci_math'),
    ('Медицина', 'sci_medicine'),
    ('Философия', 'sci_philosophy'),
    ('Психология', 'sci_psychology'),
    ('Физика', 'sci_phys'),
    ('Политика', 'sci_politics'),
    ('Религиоведение', 'sci_religion'),
    ('Технические науки', 'sci_tech'),
    ('Прочая научная литература', 'science'),
    ('Боевая фантастика', 'sf_action'),
    ('Киберпанк', 'sf_cyberpunk'),
    ('Детективная фантастика', 'sf_detective'),
    ('Эпическая фантастика', 'sf_epic'),
    ('Фэнтези', 'sf_fantasy'),
    ('Героическая фантастика', 'sf_heroic'),
    ('Альтернативная история', 'sf_history'),
    ('Ужасы и Мистика', 'sf_horror'),
    ('Юмористическая фантастика', 'sf_humor'),
    ('Социально-психологическая фантастика', 'sf_social'),
    ('Космическая фантастика', 'sf_space'),
    ('Научная Фантастика', 'sf'),
    ('Триллер', 'thriller')
]

# Функция для создания базы данных и подключения к ней
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    return conn

# Функция для создания таблицы книг
def create_books_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            Id_book INTEGER PRIMARY KEY AUTOINCREMENT,
            Name_book TEXT NOT NULL,
            Year_of_publication INTEGER CHECK (Year_of_publication > 0),
            Date_add TEXT DEFAULT CURRENT_DATE
        )
    ''')
    conn.commit()

# Функция для создания таблицы жанров
def create_genres_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Genres (
            ID_genre INTEGER PRIMARY KEY AUTOINCREMENT,
            Name_genre TEXT NOT NULL,
            Code TEXT UNIQUE
        )
    ''')
    conn.commit()

# Функция для создания связующей таблицы Книги_Жанры
def create_books_genres_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books_Genres (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_book INTEGER,
            ID_genre INTEGER,
            FOREIGN KEY (ID_book) REFERENCES Books (Id_book) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (ID_genre) REFERENCES Genres (ID_genre) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')
    conn.commit()

# Функция для создания таблицы тегов
def create_tags_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tags (
            ID_tag INTEGER PRIMARY KEY AUTOINCREMENT,
            Name_tag TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()

# Функция для создания связующей таблицы Книги_Теги
def create_books_tags_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books_Tags (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_book INTEGER,
            ID_tag INTEGER,
            FOREIGN KEY (ID_book) REFERENCES Books (Id_book) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (ID_tag) REFERENCES Tags (ID_tag) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')
    conn.commit()

# Функция для создания таблицы авторов
def create_authors_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            Id_author INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Surname TEXT NOT NULL,
            Patronymic TEXT,
            Nickname TEXT UNIQUE
        )
    ''')
    conn.commit()

# Функция для создания связующей таблицы Книги_Авторы
def create_books_authors_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books_Authors (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_book INTEGER,
            ID_author INTEGER,
            FOREIGN KEY (ID_book) REFERENCES Books (Id_book) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (ID_author) REFERENCES Authors (Id_author) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')
    conn.commit()

# Функция для создания таблицы форматов
def create_formats_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Formats (
            ID_format INTEGER PRIMARY KEY AUTOINCREMENT,
            Name_format TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()

# Функция для создания связующей таблицы Книги_Формат
def create_books_formats_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books_Formats (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_book INTEGER,
            ID_format INTEGER,
            FOREIGN KEY (ID_book) REFERENCES Books (Id_book) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (ID_format) REFERENCES Formats (ID_format) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')
    conn.commit()

# Функция для заполнения таблицы жанров
def populate_genres_table(conn):
    cursor = conn.cursor()
    genres = [
        ('Фантастика', 'FAN'),
        ('Детектив', 'DET'),
        ('Роман', 'ROM'),
        ('Научная литература', 'SCI')
    ]
    cursor.executemany('INSERT INTO Genres (Name_genre, Code) VALUES (?, ?)', genres)
    conn.commit()

# Функция для вставки данных о жанрах
def insert_genres(conn, genres):
    cursor = conn.cursor()
    try:
        cursor.executemany('''
            INSERT INTO Genres (Name_genre, Code)
            VALUES (?, ?)
        ''', genres)
        conn.commit()
        print("Данные успешно добавлены!")
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении данных: {e}")
        conn.rollback()

# Основная функция для создания и настройки базы данных
def setup_database(db_name):
    conn = create_database(db_name)
    create_books_table(conn)
    create_genres_table(conn)
    create_books_genres_table(conn)
    create_tags_table(conn)
    create_books_tags_table(conn)
    create_authors_table(conn)
    create_books_authors_table(conn)
    create_formats_table(conn)
    create_books_formats_table(conn)
    # populate_genres_table(conn)

    insert_genres(conn, genres_data)

    return conn

# Пример использования
if __name__ == "__main__":
    db_name = "library.db"
    conn = setup_database(db_name)
    print("База данных успешно создана и настроена.")
    conn.close()