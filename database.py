import pymysql
from pymysql import Error


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='liCannyCat12',
                database='store_db_nik'
            )
        except Error as e:
            print(f"Ошибка соединения: {e}")
            self.connection = None

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def insert_product(self, product_data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = """
                INSERT INTO products (name, quantity, sale_price)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, product_data)
            self.connection.commit()
        except Error as e:
            print(f"Ошибка при вставке продукта: {e}")
        finally:
            self.close_connection()

    def fetch_all_products(self):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = "SELECT * FROM products"
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Ошибка получения продуктов: {e}")
            return None
        finally:
            self.close_connection()

    def update_product(self, product_id, column, new_value):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = f"UPDATE products SET {column} = %s WHERE product_id = %s"
            cursor.execute(query, (new_value, product_id))
            self.connection.commit()
        except Error as e:
            print(f"Ошибка обновления продукта: {e}")
        finally:
            self.close_connection()

    def delete_product(self, product_id):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = "DELETE FROM products WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Ошибка удаления продукта: {e}")
            return False
        finally:
            self.close_connection()

    def save_to_db_products(self, row_values):
        try:
            cursor = self.connection.cursor()
            query = f'''INSERT INTO products (name, quantity, sale_price) VALUES (%s, %s, %s)'''
            cursor.execute(query, row_values)
            self.connection.commit()
        except Error as e:
            print(e)
        finally:
            self.close_connection()

    def insert_order(self, order_data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = """
                INSERT INTO orders (product_id, quantity, purchase_price, total_amount, order_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, order_data)
            self.connection.commit()
        except Error as e:
            print(f"Ошибка при вставке заказа: {e}")
        finally:
            self.close_connection()

    def fetch_all_products_new(self):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = "SELECT product_id, name, quantity FROM products"
            cursor.execute(query)
            records = cursor.fetchall()
            return records  # Возвращает список кортежей: [(product_id, name, quantity), ...]
        except Error as e:
            print(f"Ошибка получения данных о продуктах: {e}")
            return None
        finally:
            self.close_connection()

    def fetch_all_orders(self):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = "SELECT * FROM orders"
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Ошибка получения заказов: {e}")
            return None
        finally:
            self.close_connection()

    def insert_sale(self, sale_data):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = """
                INSERT INTO sales (product_id, sale_date, quantity, total_amount)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, sale_data)
            self.connection.commit()
        except Error as e:
            print(f"Ошибка при вставке записи о продаже: {e}")
        finally:
            self.close_connection()

    def fetch_all_sales(self):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = "SELECT * FROM sales"
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Ошибка получения продаж: {e}")
            return None
        finally:
            self.close_connection()

    def get_last_inserted_id(self):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = "SELECT LAST_INSERT_ID()"
            cursor.execute(query)
            last_id = cursor.fetchone()[0]
            return last_id
        except Error as e:
            print(f"Ошибка получения последнего ID: {e}")
            return None
        finally:
            self.close_connection()

    def fetch_sales_report(self, start_date, end_date):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = """
                SELECT s.product_id, p.name, SUM(s.quantity) AS total_quantity, SUM(s.total_amount) AS total_sales
                FROM sales s
                JOIN products p ON s.product_id = p.product_id
                WHERE s.sale_date BETWEEN %s AND %s
                GROUP BY s.product_id, p.name
            """
            cursor.execute(query, (start_date, end_date))
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Ошибка получения отчета о продажах: {e}")
            return None
        finally:
            self.close_connection()

    # -----------------------
    def fetch_orders_report(self, start_date, end_date):
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = """
                SELECT o.product_id, p.name, SUM(o.quantity) AS total_quantity, SUM(o.total_amount) AS total_amount
                FROM orders o
                JOIN products p ON o.product_id = p.product_id
                WHERE o.order_date BETWEEN %s AND %s
                GROUP BY o.product_id, p.name
            """
            cursor.execute(query, (start_date, end_date))
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Ошибка получения отчета о закупках: {e}")
            return None
        finally:
            self.close_connection()

