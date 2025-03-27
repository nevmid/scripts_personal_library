import sqlite3


class GetData:

    def __init__(self):
        self.conn = None

    def get_books(self, filters):
        try:
            self.conn = sqlite3.connect('book_db.db')
            cursor = self.conn.cursor()
            query = """
            SELECT b.Name_book, GROUP_CONCAT(DISTINCT f.Name_format, ', ') AS formats
            FROM Books b
            JOIN Books_Formats bf ON bf.ID_book = b.Id_book
            JOIN Formats f ON bf.ID_format = f.ID_format
            WHERE 1=1
            """

            params = []

            for key, value in filters.items():
                if value:
                    if key == "name":
                        query += " AND b.Name_book LIKE %s"
                        params.append(f"%{value}%")

                    elif key == "author":
                        query += """ AND b.Id_book IN
                        (SELECT ba.ID_book FROM Books_Authors ba
                        JOIN Authors a ON ba.ID_author = a.Id_author
                        WHERE 1=1
                        """
                        if value[0] != '':
                            query += " AND a.Name = %s"
                            params.append(value[0])

                        if value[1] != '':
                            query += " AND a.Surname = %s"
                            params.append(value[1])

                        if value[2] != '':
                            query += " AND a.Patronymic = %s"
                            params.append(value[2])

                        if value[3] != '':
                            query += " AND a.Nickname = %s"
                            params.append(value[3])

                        query += ")"

                    elif key == "year":
                        query += " AND b.Year_of_publication = %s"
                        params.append(value)

                    elif key == "genres":
                        query += """ AND b.Id_book IN
                        (SELECT bg.ID_book FROM Books_Genres bg
                        JOIN Genres g ON g.ID_genre = bg.ID_genre
                        WHERE g.Name_genre IN ({}))
                        """.format(",".join(["%s"]*len(value)))
                        params.append(value)

                    elif key == "tags":
                        query += """ AND b.Id_book IN
                        (SELECT bt.ID_book FROM Books_Tags bt
                        JOIN Tags t ON t.ID_tag = bt.ID_tag
                        WHERE t.Name_tag IN ({}))
                        """.format(",".join(["%s"]*len(value)))
                        params.append(value)

            query += " GROUP BY b.Name_book"
            result = cursor.execute(query, params)
            books = []

            for row in result:
                book = {
                    'name': row[0],
                    'formats': row[1].split(', ') if row[1] else []
                }
                books.append(book)

            return books

        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def get_id_book(self, book_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT Id_book FROM Books WHERE Name_book = %s", book_name)
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
                    query += f" AND {key} = %s"
                    params.append(value)

            cursor.execute(query, params)
            result = cursor.fetchall()

            return result
        except Exception as e:
            print(e)

    def get_id_tag(self, tag_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_tag FROM Tags WHERE Name_tag = %s", tag_name)
            result = cursor.fetchall()

            return result
        except Exception as e:
            print(e)

    def get_id_genre(self, genre_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_genre FROM Genres WHERE Name_genre = %s", genre_name)
            result = cursor.fetchall()

            return result
        except Exception as e:
            print(e)

    def get_id_formats(self, format_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_format FROM Formats WHERE Name_format = %s", format_name)
            result = cursor.fetchall()

            return result
        except Exception as e:
            print(e)

    def get_info_about_books(self, flag, book_name=None):
        try:
            self.conn = sqlite3.connect('book_db.db')
            cursor = self.conn.cursor()
            if flag:
                cursor.execute("SELECT * FROM Books WHERE Name_book = %s", book_name)
            else:
                cursor.execute("SELECT * FROM Books")
            result = cursor.fetchall()

            return result

        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def get_info_about_authors(self, author, flag, book_name=None):
        try:
            self.conn = sqlite3.connect('book_db.db')
            cursor = self.conn.cursor()

            if flag:

                id_book = self.get_id_book(book_name)
                id_author = self.get_id_author(author)

                cursor.execute("SELECT ID FROM Books_Authors WHERE ID_book = %s AND ID_author = %s",
                               [id_book, id_author])

            else:
                query = "SELECT * FROM Authors WHERE 1=1"

                params = []

                for key, value in author.items():
                    if value:
                        query += f" AND {key} = %s"
                        params.append(value)

                cursor.execute(query, params)

            result = cursor.fetchall()

            return result

        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def get_info_about_tags(self, tag_name, flag, book_name=None):
        try:
            self.conn = sqlite3.connect('book_db.db')
            cursor = self.conn.cursor()
            if flag:

                id_book = self.get_id_book(book_name)
                id_tag = self.get_id_tag(tag_name)

                cursor.execute("SELECT ID FROM Books_Tags WHERE ID_book = %s AND ID_tag = %s",
                               [id_book, id_tag])

            else:
                query = "SELECT * FROM Tags WHERE Name_tag = %s"
                cursor.execute(query, tag_name)

            result = cursor.fetchall()

            return result

        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def get_info_about_genres(self, genre_name, flag, book_name=None):
        try:
            self.conn = sqlite3.connect('book_db.db')
            cursor = self.conn.cursor()
            if flag:

                id_book = self.get_id_book(book_name)
                id_genre = self.get_id_genre(genre_name)

                cursor.execute("SELECT ID FROM Books_Genres WHERE ID_book = %s AND ID_genre = %s",
                               [id_book, id_genre])

            else:
                query = "SELECT * FROM Genres WHERE Name_genre = %s"
                cursor.execute(query, genre_name)

            result = cursor.fetchall()

            return result

        except Exception as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    def get_info_about_formats(self, format_name, flag, book_name=None):
        try:
            self.conn = sqlite3.connect('book_db.db')
            cursor = self.conn.cursor()
            if flag:

                id_book = self.get_id_book(book_name)
                id_format = self.get_id_formats(format_name)

                cursor.execute("SELECT ID FROM Books_Formats WHERE ID_book = %s AND ID_format = %s",
                               [id_book, id_format])

            else:
                query = "SELECT * FROM Formats WHERE Name_format = %s"
                cursor.execute(query, format_name)

            result = cursor.fetchall()

            return result

        except Exception as e:
            print('Error: ', e)
        finally:
            if self.conn:
                self.conn.close()
