from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database

from docx import Document
from docx.shared import Inches


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(508, 346)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.login = QtWidgets.QLineEdit(self.page)
        self.login.setObjectName("login")
        self.verticalLayout_3.addWidget(self.login)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.page)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.password = QtWidgets.QLineEdit(self.page)
        self.password.setObjectName("password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verticalLayout_4.addWidget(self.password)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.GoInSistemB = QtWidgets.QPushButton(self.page)
        self.GoInSistemB.setObjectName("GoInSistemB")
        self.verticalLayout.addWidget(self.GoInSistemB, 0, QtCore.Qt.AlignRight)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AddB = QtWidgets.QPushButton(self.page_2)
        self.AddB.setObjectName("AddB")
        self.horizontalLayout.addWidget(self.AddB)
        self.SellB = QtWidgets.QPushButton(self.page_2)
        self.SellB.setObjectName("SellB")
        self.horizontalLayout.addWidget(self.SellB)
        self.ReportB = QtWidgets.QPushButton(self.page_2)
        self.ReportB.setObjectName("ReportB")
        self.horizontalLayout.addWidget(self.ReportB)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tableWidget1W = QtWidgets.QTableWidget(self.page_2)
        self.tableWidget1W.setObjectName("tableWidget1W")
        self.tableWidget1W.setColumnCount(0)
        self.tableWidget1W.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget1W)
        self.RedactB = QtWidgets.QPushButton(self.page_2)
        self.RedactB.setObjectName("RedactB")
        self.verticalLayout_2.addWidget(self.RedactB)
        self.stackedWidget.addWidget(self.page_2)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.formLayout = QtWidgets.QFormLayout(self.page_5)
        self.formLayout.setObjectName("formLayout")
        self.AddProdB = QtWidgets.QPushButton(self.page_5)
        self.AddProdB.setObjectName("AddProdB")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.AddProdB)
        self.DelProdB = QtWidgets.QPushButton(self.page_5)
        self.DelProdB.setObjectName("DelProdB")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.DelProdB)
        self.tableWidget2W = QtWidgets.QTableWidget(self.page_5)
        self.tableWidget2W.setObjectName("tableWidget2W")
        self.tableWidget2W.setColumnCount(0)
        self.tableWidget2W.setRowCount(0)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.tableWidget2W)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.GoToMainB2W = QtWidgets.QPushButton(self.page_5)
        self.GoToMainB2W.setObjectName("GoToMainB2W")
        self.horizontalLayout_4.addWidget(self.GoToMainB2W)
        self.SaveB2W = QtWidgets.QPushButton(self.page_5)
        self.SaveB2W.setObjectName("SaveB2W")
        self.horizontalLayout_4.addWidget(self.SaveB2W)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout_4)
        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.comboBox3W = QtWidgets.QComboBox(self.page_6)
        self.comboBox3W.setObjectName("comboBox3W")
        self.verticalLayout_5.addWidget(self.comboBox3W)
        self.tableWidget3W = QtWidgets.QTableWidget(self.page_6)
        self.tableWidget3W.setObjectName("tableWidget3W")
        self.tableWidget3W.setColumnCount(4)
        self.tableWidget3W.setHorizontalHeaderLabels(["Название", "Количество", "Цена закупа", "Общая стоимость"])
        self.verticalLayout_5.addWidget(self.tableWidget3W)
        self.lineEdit3W = QtWidgets.QLineEdit(self.page_6)
        self.lineEdit3W.setAutoFillBackground(False)
        self.lineEdit3W.setDragEnabled(False)
        self.lineEdit3W.setReadOnly(True)
        self.lineEdit3W.setObjectName("lineEdit3W")
        self.verticalLayout_5.addWidget(self.lineEdit3W)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.NoB3W = QtWidgets.QPushButton(self.page_6)
        self.NoB3W.setObjectName("NoB3W")
        self.horizontalLayout_2.addWidget(self.NoB3W)
        self.YesB3W = QtWidgets.QPushButton(self.page_6)
        self.YesB3W.setObjectName("YesB3W")
        self.horizontalLayout_2.addWidget(self.YesB3W)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.stackedWidget.addWidget(self.page_6)
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_7)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.comboBox_24W = QtWidgets.QComboBox(self.page_7)
        self.comboBox_24W.setObjectName("comboBox_24W")
        self.verticalLayout_6.addWidget(self.comboBox_24W)
        self.tableWidgetW4 = QtWidgets.QTableWidget(self.page_7)
        self.tableWidgetW4.setObjectName("tableWidgetW4")
        self.tableWidgetW4.setColumnCount(4)
        self.tableWidgetW4.setHorizontalHeaderLabels(["Название", "Количество", "Цена за единицу", "Общая стоимость"])
        self.verticalLayout_6.addWidget(self.tableWidgetW4)
        self.lineEdit_24W = QtWidgets.QLineEdit(self.page_7)
        self.lineEdit_24W.setReadOnly(True)
        self.lineEdit_24W.setObjectName("lineEdit_24W")
        self.verticalLayout_6.addWidget(self.lineEdit_24W)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.NoB4W = QtWidgets.QPushButton(self.page_7)
        self.NoB4W.setObjectName("NoB4W")
        self.horizontalLayout_5.addWidget(self.NoB4W)
        self.YesBW4 = QtWidgets.QPushButton(self.page_7)
        self.YesBW4.setObjectName("YesBW4")
        self.horizontalLayout_5.addWidget(self.YesBW4)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.stackedWidget.addWidget(self.page_7)
        self.page_8 = QtWidgets.QWidget()
        self.page_8.setObjectName("page_8")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_8)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.page_8)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(self.label_5)
        self.StertdateEdit = QtWidgets.QDateEdit(self.page_8)
        self.StertdateEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # -------
        self.StertdateEdit.setObjectName("StertdateEdit")
        self.verticalLayout_7.addWidget(self.StertdateEdit)
        self.gridLayout_2.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.page_8)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_8.addWidget(self.label_6)
        self.EnddateEdit = QtWidgets.QDateEdit(self.page_8)
        self.EnddateEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # ----
        self.EnddateEdit.setObjectName("EnddateEdit")
        self.verticalLayout_8.addWidget(self.EnddateEdit)
        self.gridLayout_2.addLayout(self.verticalLayout_8, 0, 1, 1, 1)
        self.tableWidget_25W = QtWidgets.QTableWidget(self.page_8)
        self.tableWidget_25W.setObjectName("tableWidget_25W")
        self.tableWidget_25W.setColumnCount(0)
        self.tableWidget_25W.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget_25W, 1, 0, 1, 2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.BackB5W = QtWidgets.QPushButton(self.page_8)
        self.BackB5W.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BackB5W.sizePolicy().hasHeightForWidth())
        self.BackB5W.setSizePolicy(sizePolicy)
        self.BackB5W.setObjectName("BackB5W")
        self.gridLayout.addWidget(self.BackB5W, 0, 0, 1, 1)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.CreateB5W = QtWidgets.QPushButton(self.page_8)
        self.CreateB5W.setObjectName("CreateB5W")
        self.verticalLayout_9.addWidget(self.CreateB5W)
        self.SaveDocxB5W = QtWidgets.QPushButton(self.page_8)
        self.SaveDocxB5W.setObjectName("SaveDocxB5W")
        self.verticalLayout_9.addWidget(self.SaveDocxB5W)
        self.gridLayout.addLayout(self.verticalLayout_9, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 2)
        self.stackedWidget.addWidget(self.page_8)
        self.verticalLayout_10.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Убедитесь, что это отсутствует в вашем коде
        self.StertdateEdit.setReadOnly(False)
        self.EnddateEdit.setReadOnly(False)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Магазин канцтоваров"))
        self.label.setText(_translate("MainWindow", "Логин"))
        self.label_2.setText(_translate("MainWindow", "Пароль"))
        self.GoInSistemB.setText(_translate("MainWindow", "Войти"))
        self.AddB.setText(_translate("MainWindow", "Поступление товара"))
        self.SellB.setText(_translate("MainWindow", "Продажа товара"))
        self.ReportB.setText(_translate("MainWindow", "Сформировать отчет"))
        self.RedactB.setText(_translate("MainWindow", "Редактор"))
        self.AddProdB.setText(_translate("MainWindow", "+"))
        self.DelProdB.setText(_translate("MainWindow", "-"))
        self.GoToMainB2W.setText(_translate("MainWindow", "Возврат в главное окно"))
        self.SaveB2W.setText(_translate("MainWindow", "Сохранить изменения"))
        self.NoB3W.setText(_translate("MainWindow", "Отмена операции"))
        self.YesB3W.setText(_translate("MainWindow", "Подтвердить операцию"))
        self.NoB4W.setText(_translate("MainWindow", "Отмена операции"))
        self.YesBW4.setText(_translate("MainWindow", "Подтвердить операцию"))
        self.label_5.setText(_translate("MainWindow", "Начало периода"))
        self.label_6.setText(_translate("MainWindow", "Конец периода"))
        self.BackB5W.setText(_translate("MainWindow", "Возврат в главное окно"))
        self.CreateB5W.setText(_translate("MainWindow", "Сформировать"))
        self.SaveDocxB5W.setText(_translate("MainWindow", "Сохранить в .docx"))


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)

        self.center_window()

        self.comboBox3W.currentIndexChanged.connect(self.add_selected_product)
        self.comboBox_24W.currentIndexChanged.connect(self.add_selected_product_to_sell_table)

        self.GoInSistemB.clicked.connect(self.show_main_window)
        self.RedactB.clicked.connect(self.show_window_editor)
        self.AddB.clicked.connect(self.show_window_add)
        self.SellB.clicked.connect(self.show_window_sell)
        self.ReportB.clicked.connect(self.show_window_report)

        self.GoToMainB2W.clicked.connect(self.show_main_window)
        self.BackB5W.clicked.connect(self.show_main_window)
        self.NoB3W.clicked.connect(self.cancel_order)
        self.NoB4W.clicked.connect(self.cancel_order_sell)
        self.AddProdB.clicked.connect(self.add_product)
        self.DelProdB.clicked.connect(self.delete_row)
        self.SaveB2W.clicked.connect(self.save_changes)

        self.YesB3W.clicked.connect(self.confirm_order)
        self.YesBW4.clicked.connect(self.confirm_product_sale)

        self.CreateB5W.clicked.connect(self.create_report)

        self.SaveDocxB5W.clicked.connect(self.save_report_to_docx)

        self.old_values = []

    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def show_main_window(self):
        if self.login.text() == "1" and self.password.text() == "1":
            self.stackedWidget.setCurrentIndex(1)
            self.resize(1900, 980)
            self.center_window()
            self.load_products()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Некорректный логин или пароль.")

    def show_window_editor(self):
        self.stackedWidget.setCurrentIndex(2)
        self.load_products_to_editor()
        self.center_window()

    def load_products_to_editor(self):
        db = Database()
        products = db.fetch_all_products()
        self.tableWidget2W.setColumnCount(3)
        self.tableWidget2W.setHorizontalHeaderLabels(
            ["Название", "Количество", "Цена за единицу"])

        if products:
            self.tableWidget2W.setRowCount(len(products))
            self.old_values = []
            for row_index, product in enumerate(products):
                self.tableWidget2W.setItem(row_index, 0, QtWidgets.QTableWidgetItem(product[1]))
                self.tableWidget2W.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(product[2])))
                self.tableWidget2W.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(product[3])))


                self.old_values.append({
                    'product_id': product[0],
                    'name': product[1],
                    'quantity': product[2],
                    'price': product[3]
                })

            self.tableWidget2W.resizeColumnsToContents()
        else:
            self.tableWidget2W.setRowCount(0)

    def delete_row(self):
        selected_items = self.tableWidget2W.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")
            return

        row_to_delete = selected_items[0].row()
        db = Database()
        db.connect()
        product_id = self.old_values[row_to_delete]['product_id']  # Получаем ID продукта для удаления
        if db.delete_product(product_id):
            self.tableWidget2W.removeRow(row_to_delete)
            del self.old_values[row_to_delete]
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось удалить запись из базы данных.")

    def add_product(self):
        db = Database()
        db.connect()

        base_name = 'Товар'
        price = 0.00
        quantity = 0

        name = base_name
        existing_names = {product['name'] for product in self.old_values}
        index = 1

        while name in existing_names:
            name = f"{base_name}{index}"
            index += 1

        row_position = self.tableWidget2W.rowCount()
        self.tableWidget2W.insertRow(row_position)
        self.tableWidget2W.setItem(row_position, 0, QtWidgets.QTableWidgetItem(name))
        self.tableWidget2W.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(quantity)))
        self.tableWidget2W.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(price)))

        row_values = [name, quantity, price]
        db.save_to_db_products(row_values)

        print(1)

        self.old_values.append({
            'product_id': db.get_last_inserted_id(),
            'name': name,
            'quantity': quantity,
            'price': price
        })
        self.tableWidget2W.resizeColumnsToContents()

        db = Database()
        products = db.fetch_all_products()
        if products:
            self.old_values = []
            for row_index, product in enumerate(products):
                self.old_values.append({
                    'product_id': product[0],
                    'name': product[1],
                   'quantity': product[2],
                    'price': product[3]
                })
            print(':)')
        else:
            print(':(')

    def on_item_changed(self, item):
        if not self.flag:
            row = item.row()
            column = item.column()

            new_value = item.text()

            if column == 0:
                if new_value == '':
                    item.setText(self.old_values[row]['name'])
                else:
                    self.old_values[row]['name'] = new_value

            elif column == 1:
                if not new_value.isdigit():
                    item.setText(str(self.old_values[row]['quantity']))
                else:
                    self.old_values[row]['quantity'] = int(new_value)

            elif column == 2:
                try:
                    new_price = float(new_value)
                    self.old_values[row]['price'] = new_price
                except ValueError:
                    item.setText(str(self.old_values[row]['price']))

    def save_changes(self):
        db = Database()
        existing_names = {product['name'] for product in self.old_values}

        for row in range(self.tableWidget2W.rowCount()):
            product_id = self.old_values[row]['product_id']

            item_name = self.tableWidget2W.item(row, 0)
            if item_name is None or item_name.text().strip() == "":
                QtWidgets.QMessageBox.warning(self, "Ошибка",
                                              f"На строке {row + 1} поле 'Название' не может быть пустым.")
                return
            name = item_name.text().strip()

            try:
                quantity_item = self.tableWidget2W.item(row, 1)
                if quantity_item is None:
                    raise ValueError("Количество не указано.")
                quantity_text = quantity_item.text().strip()
                quantity = int(quantity_text)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"На строке {row + 1} количество должно быть числом.")
                return

            try:
                price_item = self.tableWidget2W.item(row, 2)
                if price_item is None:
                    raise ValueError("Цена не указана.")
                price_text = price_item.text().strip()
                price = float(price_text)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"На строке {row + 1} цена должна быть числом.")
                return

            if quantity < 0:
                QtWidgets.QMessageBox.warning(self, "Ошибка",
                                              f"На строке {row + 1} количество не может быть отрицательным.")
                return
            if price < 0:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"На строке {row + 1} цена не может быть отрицательной.")
                return

            if name in existing_names and name != self.old_values[row]['name']:
                QtWidgets.QMessageBox.warning(self, "Ошибка",
                                              f"На строке {row + 1} название продукта должно быть уникальным.")
                return

            db.update_product(product_id, 'name', name)
            db.update_product(product_id, 'quantity', quantity)
            db.update_product(product_id, 'sale_price', price)

            self.old_values[row]['name'] = name
            self.old_values[row]['quantity'] = quantity
            self.old_values[row]['price'] = price

        QtWidgets.QMessageBox.information(self, "Успех", "Изменения сохранены.")
        self.tableWidget2W.resizeColumnsToContents()
        self.load_products_to_editor()

    def show_window_add(self):
        self.stackedWidget.setCurrentIndex(3)
        self.center_window()
        self.load_products_to_combobox()

    def load_products_to_combobox(self):
        db = Database()
        products = db.fetch_all_products()
        self.comboBox3W.clear()

        self.comboBox3W.addItem("")
        if products:
            for product in products:
                self.comboBox3W.addItem(product[1], userData=product)
        self.comboBox3W.setCurrentIndex(0)

    def add_selected_product(self):
        selected_product = self.comboBox3W.currentData()

        if selected_product is None:
            return

        product_id = selected_product[0]
        product_name = selected_product[1]

        for row in range(self.tableWidget3W.rowCount()):
            if self.tableWidget3W.item(row, 0).text() == product_name:

                try:
                    quantity, ok = QtWidgets.QInputDialog.getInt(self, "Количество", "Введите количество:", 1, 1, 1000)
                    if not ok:
                        return

                    current_quantity = int(self.tableWidget3W.item(row, 1).text())
                    new_quantity = current_quantity + quantity
                    purchase_price = float(self.tableWidget3W.item(row, 2).text())
                    total_price = purchase_price * new_quantity

                    self.tableWidget3W.item(row, 1).setText(str(new_quantity))
                    self.tableWidget3W.item(row, 3).setText(str(total_price))

                    self.update_total_price()

                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите корректное количество.")
                    return

                return

        try:
            quantity, ok = QtWidgets.QInputDialog.getInt(self, "Количество", "Введите количество:", 1, 1, 1000)
            if not ok:
                return

            purchase_price, ok = QtWidgets.QInputDialog.getDouble(self, "Цена закупа", "Введите цену закупа:", 0, 0,
                                                                  10000, 2)
            if not ok:
                return

            total_price = purchase_price * quantity
            row_position = self.tableWidget3W.rowCount()
            self.tableWidget3W.insertRow(row_position)
            self.tableWidget3W.setItem(row_position, 0, QtWidgets.QTableWidgetItem(product_name))
            self.tableWidget3W.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(quantity)))
            self.tableWidget3W.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(purchase_price)))
            self.tableWidget3W.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(total_price)))

            self.tableWidget3W.item(row_position, 0).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget3W.item(row_position, 1).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget3W.item(row_position, 2).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget3W.item(row_position, 3).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.update_total_price()

        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите корректное количество и цену.")
            return

    def cancel_order(self):
        self.tableWidget3W.setRowCount(0)
        self.lineEdit3W.clear()
        self.stackedWidget.setCurrentIndex(1)
        self.center_window()

    def update_total_price(self):
        total_price = 0
        for row in range(self.tableWidget3W.rowCount()):
            total_price += float(self.tableWidget3W.item(row, 3).text())
        self.lineEdit3W.setText(f"Общая стоимость: {total_price:.2f}")

    def show_window_sell(self):
        self.stackedWidget.setCurrentIndex(4)
        self.center_window()
        self.load_products_to_sell_combobox()
        self.tableWidgetW4.setRowCount(0)

    def load_products_to_sell_combobox(self):
        db = Database()
        products = db.fetch_all_products()
        self.comboBox_24W.clear()

        self.comboBox_24W.addItem("")
        if products:
            for product in products:
                self.comboBox_24W.addItem(product[1], userData=product)
        self.comboBox_24W.setCurrentIndex(0)

    def add_selected_product_to_sell_table(self):
        selected_product = self.comboBox_24W.currentData()

        if selected_product is None:
            return

        product_id = selected_product[0]
        product_name = selected_product[1]
        product_price = selected_product[3]

        quantity, ok = QtWidgets.QInputDialog.getInt(self, "Количество", "Введите количество:", 1, 1, 1000)
        if not ok or quantity <= 0:
            return

        print(product_id)
        print(product_name)
        print(selected_product[2])
        print(product_price)
        print(quantity)
        print(self.tableWidgetW4.rowCount())

        for row in range(self.tableWidgetW4.rowCount()):

            if self.tableWidgetW4.item(row, 0).text() == product_name:
                current_quantity = int(self.tableWidgetW4.item(row, 1).text())
                new_quantity = current_quantity + quantity
                total_price = product_price * new_quantity

                self.tableWidgetW4.item(row, 1).setText(str(new_quantity))
                self.tableWidgetW4.item(row, 3).setText(str(total_price))
                self.update_total_price_sell()
                return

        row_position = self.tableWidgetW4.rowCount()
        self.tableWidgetW4.insertRow(row_position)
        self.tableWidgetW4.setItem(row_position, 0, QtWidgets.QTableWidgetItem(product_name))
        self.tableWidgetW4.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(quantity)))
        self.tableWidgetW4.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(product_price)))
        self.tableWidgetW4.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(product_price * quantity)))
        self.tableWidgetW4.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(product_id)))

        for column in [0, 1, 2, 3]:
            self.tableWidgetW4.item(row_position, column).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        self.update_total_price_sell()

        self.tableWidgetW4.viewport().update()

    def cancel_order_sell(self):
        self.tableWidgetW4.setRowCount(0)
        self.lineEdit_24W.clear()
        self.stackedWidget.setCurrentIndex(1)

    def update_total_price_sell(self):
        total_price = 0
        for row in range(self.tableWidgetW4.rowCount()):
            total_price += float(self.tableWidgetW4.item(row, 3).text())
        self.lineEdit_24W.setText(f"Общая стоимость: {total_price:.2f}")

    def confirm_order(self):
        order_data_list = []
        db = Database()

        for row in range(self.tableWidget3W.rowCount()):
            product_name = self.tableWidget3W.item(row, 0).text()
            quantity = int(self.tableWidget3W.item(row, 1).text())
            purchase_price = float(self.tableWidget3W.item(row, 2).text())
            total_amount = float(self.tableWidget3W.item(row, 3).text())

            products = db.fetch_all_products()
            product_id = next((product[0] for product in products if product[1] == product_name), None)

            if product_id is not None:
                order_data = (product_id, quantity, purchase_price, total_amount,
                              QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss'))
                order_data_list.append(order_data)

                current_product = next((product[2] for product in products if product[0] == product_id), None)
                if current_product is not None:
                    new_quantity = current_product + quantity
                    db.update_product(product_id, 'quantity', new_quantity)

        for order_data in order_data_list:
            db.insert_order(order_data)

        QtWidgets.QMessageBox.information(self, "Успех", "Заказ успешно оформлен.")
        self.load_products()
        self.cancel_order()

    def confirm_product_sale(self):
        db = Database()
        sales_data_list = []

        for row in range(self.tableWidgetW4.rowCount()):
            product_name = self.tableWidgetW4.item(row, 0).text()
            quantity = int(self.tableWidgetW4.item(row, 1).text())
            sale_price = float(self.tableWidgetW4.item(row, 2).text())
            total_amount = float(self.tableWidgetW4.item(row, 3).text())

            products = db.fetch_all_products()
            product_id = next((product[0] for product in products if product[1] == product_name), None)

            if product_id is not None:

                sale_data = (
                    product_id, QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss'), quantity,
                    total_amount)
                sales_data_list.append(sale_data)


                current_product = next((product[2] for product in products if product[0] == product_id), None)
                if current_product is not None:
                    new_quantity = current_product - quantity
                    if new_quantity < 0:
                        QtWidgets.QMessageBox.warning(self, "Ошибка",
                                                      f"Недостаточно товара на складе для {product_name}.")
                        return
                    db.update_product(product_id, 'quantity', new_quantity)


        for sale_data in sales_data_list:
            db.insert_sale(sale_data)

        QtWidgets.QMessageBox.information(self, "Успех", "Продажа успешно оформлена.")
        self.load_products()
        self.cancel_order_sell()

    def show_window_report(self):
        self.stackedWidget.setCurrentIndex(5)
        self.center_window()

        self.StertdateEdit.setDateTime(
            QtCore.QDateTime(2000, 1, 1, 0, 0, 0))
        self.EnddateEdit.setDateTime(
            QtCore.QDateTime.currentDateTime())

    def merge_reports(self, products_data, orders_report, sales_report):
        report_data = {}


        for product_id, product in products_data.items():
            report_data[product_id] = {
                'name': product[0],
                'current_quantity': product[1],
                'total_purchase_cost': 0,
                'total_sales_amount': 0
            }

        for order in orders_report:
            product_id = order[0]
            if product_id in report_data:
                report_data[product_id]['total_purchase_cost'] += order[3]

        for sale in sales_report:
            product_id = sale[0]
            if product_id in report_data:
                report_data[product_id]['total_sales_amount'] += sale[3]

        result = []
        for product_id, data in report_data.items():
            result.append((
                product_id,
                data['name'],
                data['current_quantity'],
                data['total_purchase_cost'],
                data['total_sales_amount']
            ))
        return result

    def create_report(self):
        start_date = self.StertdateEdit.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        end_date = self.EnddateEdit.dateTime().toString('yyyy-MM-dd HH:mm:ss')

        db = Database()

        try:
            products = db.fetch_all_products_new()
            if not products:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Нет данных о продуктах.")
                return

            products_data = {product[0]: (product[1], product[2]) for product in products}

            orders_report = db.fetch_orders_report(start_date, end_date)

            sales_report = db.fetch_sales_report(start_date, end_date)

            report_data = self.merge_reports(products_data, orders_report, sales_report)

            self.update_report_table(report_data)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"ERROR - Произошла ошибка при создании отчета: {str(e)}")

    def update_report_table(self, report_data):
        self.tableWidget_25W.setColumnCount(5)
        self.tableWidget_25W.setHorizontalHeaderLabels(
            ["ID товара", "Название", "Текущее количество", "Затраты на покупки", "Общая сумма продаж"])
        self.tableWidget_25W.setRowCount(len(report_data))

        for row_index, row in enumerate(report_data):
            self.tableWidget_25W.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget_25W.setItem(row_index, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget_25W.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tableWidget_25W.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tableWidget_25W.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(row[4])))

        self.tableWidget_25W.resizeColumnsToContents()

    def load_products(self):
        db = Database()
        products = db.fetch_all_products()
        self.tableWidget1W.setColumnCount(3)
        self.tableWidget1W.setHorizontalHeaderLabels(
            ["Название", "Количество", "Цена за единицу"])

        if products:
            self.tableWidget1W.setRowCount(len(products))
            for row_index, product in enumerate(products):
                self.tableWidget1W.setItem(row_index, 0, QtWidgets.QTableWidgetItem(product[1]))
                self.tableWidget1W.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(product[2])))
                self.tableWidget1W.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(product[3])))

                for column_index in range(3):
                    item = self.tableWidget1W.item(row_index, column_index)
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

            self.tableWidget1W.resizeColumnsToContents()
        else:
            self.tableWidget1W.setRowCount(0)

    def save_report_to_docx(self):

        report_data = []
        for row in range(self.tableWidget_25W.rowCount()):
            row_data = []
            for column in range(self.tableWidget_25W.columnCount()):
                item = self.tableWidget_25W.item(row, column)
                row_data.append(item.text() if item else "")
            report_data.append(row_data)


        file_name = "report.docx"
        self.generate_docx(file_name, report_data)

        QtWidgets.QMessageBox.information(self, "Успех", f"Отчет сохранен в файл {file_name}")

    def generate_docx(self, file_name, data):
        doc = Document()


        doc.add_heading('Отчет по товарам', 0)


        table = doc.add_table(rows=1, cols=5)
        table.style = 'Table Grid'


        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'ID товара'
        hdr_cells[1].text = 'Название'
        hdr_cells[2].text = 'Текущее количество'
        hdr_cells[3].text = 'Затраты на покупки'
        hdr_cells[4].text = 'Общая сумма продаж'


        for row in data:
            row_cells = table.add_row().cells
            row_cells[0].text = str(row[0])
            row_cells[1].text = row[1]
            row_cells[2].text = str(row[2])
            row_cells[3].text = str(row[3])
            row_cells[4].text = str(row[4])

        doc.save(file_name)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


