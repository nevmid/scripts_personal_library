import sqlite3

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
    populate_genres_table(conn)
    return conn

# Пример использования
if __name__ == "__main__":
    db_name = "library.db"
    conn = setup_database(db_name)
    print("База данных успешно создана и настроена.")
    conn.close()