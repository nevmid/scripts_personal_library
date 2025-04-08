import sqlite3


class GetData:

    def __init__(self):
        self.conn = None

    def get_connection(self):
        self.conn = sqlite3.connect('book_db.db')

    def close_connection(self):
        self.conn.close()

    def get_books(self, filters):
        try:
            self.get_connection()
            cursor = self.conn.cursor()
            query = """
            SELECT b.Name_book, GROUP_CONCAT(DISTINCT f.Name_format) AS formats
            FROM Books b
            JOIN Books_Formats bf ON bf.ID_book = b.Id_book
            JOIN Formats f ON bf.ID_format = f.ID_format
            WHERE 1=1
            """

            params = []

            for key, value in filters.items():
                if value:
                    if key == "name":
                        query += " AND b.Name_book LIKE ?"
                        params.append(f"%{value}%")

                    elif key == "author":
                        query += """ AND b.Id_book IN
                        (SELECT ba.ID_book FROM Books_Authors ba
                        JOIN Authors a ON ba.ID_author = a.Id_author
                        WHERE 1=1
                        """
                        if value[0] != '':
                            query += " AND a.Name = ?"
                            params.append(value[0])

                        if value[1] != '':
                            query += " AND a.Surname = ?"
                            params.append(value[1])

                        if value[2] != '':
                            query += " AND a.Patronymic = ?"
                            params.append(value[2])

                        if value[3] != '':
                            query += " AND a.Nickname = ?"
                            params.append(value[3])

                        query += ")"

                    elif key == "year":
                        query += " AND b.Year_of_publication = ?"
                        params.append(value)

                    elif key == "genres":
                        query += """ AND b.Id_book IN
                        (SELECT bg.ID_book FROM Books_Genres bg
                        JOIN Genres g ON g.ID_genre = bg.ID_genre
                        WHERE g.Name_genre IN ({}))
                        """.format(",".join(["?"]*len(value)))
                        params.append(value)

                    elif key == "tags":
                        query += """ AND b.Id_book IN
                        (SELECT bt.ID_book FROM Books_Tags bt
                        JOIN Tags t ON t.ID_tag = bt.ID_tag
                        WHERE t.Name_tag IN ({}))
                        """.format(",".join(["?"]*len(value)))
                        params.append(value)

            query += " GROUP BY b.Name_book"
            result = cursor.execute(query, params)
            books = []

            for row in result:
                book = {
                    'name': row[0],
                    'formats': [item.strip() for item in row[1].split(',')]
                }
                books.append(book)

            return books

        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.close_connection()

    def get_id_book(self, book_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT Id_book FROM Books WHERE Name_book = ?", (book_name, ))
            result = cursor.fetchall()

            return result
        except Exception as e:
            print(e)

    def get_id_author(self, author):
        try:
            cursor = self.conn.cursor()
            query = "SELECT Id_author FROM Authors WHERE 1=1"

            params = []

            for key, value in author.items():
                if value:
                    query += f" AND {key} = ?"
                    params.append(value)

            cursor.execute(query, params)
            result = cursor.fetchall()

            return result
        except Exception as e:
            print(e)

    def get_id_tag(self, tag_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_tag FROM Tags WHERE Name_tag = ?", (tag_name, ))
            result = cursor.fetchall()

            return result
        except Exception as e:
            print(e)

    def get_id_genre(self, genre_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_genre FROM Genres WHERE Name_genre = ?", (genre_name, ))
            result = cursor.fetchall()

            return result
        except Exception as e:
            print(e)

    def get_id_formats(self, format_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_format FROM Formats WHERE Name_format = ?", (format_name, ))
            result = cursor.fetchall()

            return result
        except Exception as e:
            print(e)

    def get_info_about_books(self, flag=False, book_name=None):
        try:
            self.get_connection()
            cursor = self.conn.cursor()
            if flag:
                id_book = self.get_id_book(book_name)
                cursor.execute("""SELECT 
                                        b.Id_book, b.Name_book, b.Year_of_publication, a.Id_author, a.Name,
                                        a.Surname, a.Patronymic, a.Nickname,
                                        GROUP_CONCAT(DISTINCT g.Name_genre),
                                        GROUP_CONCAT(DISTINCT t.Name_tag),
                                        GROUP_CONCAT(DISTINCT f.Name_format)
                                        FROM Books b
                                    JOIN Books_Authors ba ON b.Id_book = ba.ID_book
                                    JOIN Authors a ON ba.ID_author = a.Id_author
                                    LEFT JOIN Books_Genres bg ON b.Id_book = bg.ID_book
                                    LEFT JOIN Genres g ON bg.ID_genre = g.ID_genre
                                    LEFT JOIN Books_Tags bt ON b.Id_book = bt.ID_book
                                    LEFT JOIN Tags t ON bt.ID_tag = t.ID_tag
                                    LEFT JOIN Books_Formats bf ON b.Id_book = bf.ID_book
                                    LEFT JOIN Formats f ON f.ID_format = bf.ID_format
                                    WHERE 
                                        b.Id_book = ?
                                    GROUP BY b.Id_book, b.Name_book, b.Year_of_publication, a.Id_author, a.Name, 
                                        a.Surname, a.Patronymic, a.Nickname""", id_book[0])
                result = cursor.fetchall()
                info = []

                for row in result:
                    if row[8] is None:
                        genres = None
                    else:
                        genres = [item.strip() for item in row[8].split(',')]
                    if row[9] is None:
                        tags = None
                    else:
                        tags = [item.strip() for item in row[9].split(',')]

                    d = {

                        "id_book": row[0],
                        "name_book": row[1],
                        "year": row[2],
                        "id_author": row[3],
                        "firstname": row[4],
                        "lastname": row[5],
                        "middlename": row[6],
                        "nickname": row[7],
                        "genres": genres,
                        "tags": tags,
                        "formats": [item.strip() for item in row[10].split(',')]

                    }
                    info.append(d)
            else:
                cursor.execute("SELECT * FROM Books")
                info = cursor.fetchall()
            return info

        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.close_connection()

    def get_info_about_authors(self, author, flag, book_name=None):
        try:
            self.get_connection()
            cursor = self.conn.cursor()

            if flag:

                id_book = self.get_id_book(book_name)
                id_author = self.get_id_author(author)

                cursor.execute("SELECT ID FROM Books_Authors WHERE ID_book = ? AND ID_author = ?",
                               [id_book, id_author])

            else:
                query = "SELECT * FROM Authors WHERE 1=1"

                params = []

                for key, value in author.items():
                    if value:
                        query += f" AND {key} = ?"
                        params.append(value)

                cursor.execute(query, params)

            result = cursor.fetchall()

            return result

        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.close_connection()

    def get_info_about_tags(self, full, flag, book_name=None, tag_name=None):
        try:
            self.get_connection()
            cursor = self.conn.cursor()
            if flag:

                id_book = self.get_id_book(book_name)
                id_tag = self.get_id_tag(tag_name)

                cursor.execute("SELECT ID FROM Books_Tags WHERE ID_book = ? AND ID_tag = ?",
                               [id_book, id_tag])

                result = cursor.fetchall()

            elif full:
                query = "SELECT * FROM Tags"
                cursor.execute(query)

                columns = [column[0] for column in cursor.description]
                tags = cursor.fetchall()

                result = [dict(zip(columns, row)) for row in tags]

            else:
                query = "SELECT * FROM Tags WHERE Name_tag = ?"
                cursor.execute(query, tag_name)
                result = cursor.fetchall()



            return result

        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.close_connection()

    def get_info_about_genres(self, full, flag, genre_name=None, book_name=None):
        try:
            self.get_connection()
            cursor = self.conn.cursor()
            if flag:

                id_book = self.get_id_book(book_name)
                id_genre = self.get_id_genre(genre_name)

                cursor.execute("SELECT ID FROM Books_Genres WHERE ID_book = ? AND ID_genre = ?",
                               [id_book, id_genre])
            elif full:
                query = "SELECT * FROM Genres"
                cursor.execute(query)

                columns = [column[0] for column in cursor.description]

                genres = cursor.fetchall()

                result = [dict(zip(columns, row)) for row in genres]


            else:
                query = "SELECT * FROM Genres WHERE Name_genre = ?"
                cursor.execute(query, genre_name)

                result = cursor.fetchall()

            return result

        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.close_connection()

    def get_info_about_formats(self, format_name, flag, book_name=None):
        try:
            self.get_connection()
            cursor = self.conn.cursor()
            if flag:

                id_book = self.get_id_book(book_name)
                id_format = self.get_id_formats(format_name)

                cursor.execute("SELECT ID FROM Books_Formats WHERE ID_book = ? AND ID_format = ?",
                               [id_book, id_format])

            else:
                query = "SELECT * FROM Formats WHERE Name_format = ?"
                cursor.execute(query, format_name)

            result = cursor.fetchall()

            return result

        except Exception as e:
            print('Error: ', e)
        finally:
            if self.conn:
                self.close_connection()

