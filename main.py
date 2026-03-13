import sqlite3
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem,
                             QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
                             QHeaderView, QMessageBox, QDialog)
from PyQt5.QtCore import Qt
from UI.main import Ui_MainWindow
from UI.addEditCoffeeForm import Ui_Dialog


class AddEditCoffeeForm(QDialog, Ui_Dialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        self.setupUi(self)

        self.coffee_id = coffee_id

        self.button_save.clicked.connect(self.save_coffee)
        self.button_cancel.clicked.connect(self.reject)

        self.db_path = self.get_db_path()

        if self.coffee_id:
            self.load_coffee_data()
            self.setWindowTitle("Редактирование кофе")
        else:
            self.setWindowTitle("Добавление кофе")

    def get_db_path(self):
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        db_path = os.path.join(application_path, 'data', 'coffee.sqlite')
        return db_path

    def load_coffee_data(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM coffee WHERE id = ?', (self.coffee_id,))
            coffee = cursor.fetchone()

            if coffee:
                self.lineEdit_name.setText(coffee[1])

                index = self.comboBox_roast.findText(coffee[2])
                if index >= 0:
                    self.comboBox_roast.setCurrentIndex(index)

                index = self.comboBox_type.findText(coffee[3])
                if index >= 0:
                    self.comboBox_type.setCurrentIndex(index)

                self.textEdit_taste.setText(coffee[4])
                self.lineEdit_price.setText(str(coffee[5]))
                self.lineEdit_volume.setText(str(coffee[6]))

            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")

    def save_coffee(self):
        if not self.lineEdit_name.text():
            QMessageBox.warning(self, "Предупреждение", "Введите название кофе")
            return

        try:
            name = self.lineEdit_name.text()
            roast = self.comboBox_roast.currentText()
            coffee_type = self.comboBox_type.currentText()
            taste = self.textEdit_taste.toPlainText()
            price = float(self.lineEdit_price.text()) if self.lineEdit_price.text() else 0
            volume = int(self.lineEdit_volume.text()) if self.lineEdit_volume.text() else 0

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if self.coffee_id:
                cursor.execute('''
                    UPDATE coffee 
                    SET name=?, roast_level=?, ground_or_beans=?, 
                        taste_description=?, price=?, package_volume=?
                    WHERE id=?
                ''', (name, roast, coffee_type, taste, price, volume, self.coffee_id))
            else:
                cursor.execute('''
                    INSERT INTO coffee (name, roast_level, ground_or_beans, taste_description, price, package_volume)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, roast, coffee_type, taste, price, volume))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Данные сохранены!")
            self.accept()

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Проверьте правильность ввода цены и объема")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {e}")


class CoffeeApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Добавляем кнопки, так как в UI их нет
        self.add_button = QPushButton("Добавить кофе")
        self.edit_button = QPushButton("Редактировать")
        self.refresh_button = QPushButton("Обновить таблицу")

        # Создаем горизонтальный layout для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()

        # Добавляем кнопки в вертикальный layout
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.tableWidget)

        # Устанавливаем layout для центрального виджета
        self.centralwidget.setLayout(layout)

        self.add_button.clicked.connect(self.add_coffee)
        self.edit_button.clicked.connect(self.edit_coffee)
        self.refresh_button.clicked.connect(self.load_coffee)

        self.db_path = self.get_db_path()
        self.load_coffee()

    def get_db_path(self):
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        db_path = os.path.join(application_path, 'data', 'coffee.sqlite')
        return db_path

    def load_coffee(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM coffee')
            data = cursor.fetchall()

            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(7)

            headers = ['ID', 'Название', 'Степень обжарки', 'Молотый/В зернах',
                       'Описание вкуса', 'Цена', 'Объем упаковки']
            self.tableWidget.setHorizontalHeaderLabels(headers)

            for row, item in enumerate(data):
                for col, value in enumerate(item):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

            self.tableWidget.resizeColumnsToContents()
            header = self.tableWidget.horizontalHeader()
            header.setSectionResizeMode(4, QHeaderView.Stretch)

            conn.close()
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def add_coffee(self):
        form = AddEditCoffeeForm(self)
        if form.exec_():
            self.load_coffee()

    def edit_coffee(self):
        current_row = self.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для редактирования")
            return

        coffee_id = int(self.tableWidget.item(current_row, 0).text())
        form = AddEditCoffeeForm(self, coffee_id)
        if form.exec_():
            self.load_coffee()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeApp()
    ex.show()
    sys.exit(app.exec_())