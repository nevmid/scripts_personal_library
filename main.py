import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from main_window import Ui_MainWindow

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
        self.add_book_button.clicked.connect(self.show_window_add_book)
        self.search_book_button.clicked.connect(self.show_window_search_book)
        self.add_category_button.clicked.connect(self.show_window_add_category)
        self.delete_category_button.clicked.connect(self.show_window_delete_category)
        
        self.back_to_main_window_add_book.clicked.connect(self.show_main_window)
        self.back_to_main_window_edit_book.clicked.connect(self.show_main_window)
        self.back_to_main_window_search_bok.clicked.connect(self.show_main_window)
        self.back_to_main_window_delete_category.clicked.connect(self.show_main_window)
        self.back_to_main_window_add_category.clicked.connect(self.show_main_window)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.showMaximized()
    sys.exit(app.exec_())