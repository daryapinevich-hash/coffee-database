import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загружаем интерфейс
        uic.loadUi('main.ui', self)
        # Подключаем кнопку к функции
        self.pushButton.clicked.connect(self.load_coffee)
        # Загружаем данные при запуске
        self.load_coffee()

    def load_coffee(self):
        # Подключаемся к базе данных
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()

        # Получаем все записи из таблицы coffee
        cursor.execute('SELECT * FROM coffee')
        data = cursor.fetchall()

        # Настраиваем таблицу
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(7)

        # Устанавливаем заголовки столбцов
        headers = ['ID', 'Название', 'Степень обжарки', 'Молотый/В зернах',
                   'Описание вкуса', 'Цена', 'Объем упаковки']
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # Заполняем таблицу данными
        for row, item in enumerate(data):
            for col, value in enumerate(item):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

        # Закрываем соединение с базой
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeApp()
    ex.show()
    sys.exit(app.exec_())
