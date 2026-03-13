import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, \
    QWidget, QHBoxLayout, QHeaderView
from PyQt5.QtCore import Qt
from addEditCoffeeForm import AddEditCoffeeForm


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информация о кофе")
        self.setGeometry(100, 100, 900, 600)

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создаем вертикальный layout
        layout = QVBoxLayout()

        # Создаем горизонтальный layout для кнопок
        button_layout = QHBoxLayout()

        # Создаем кнопки
        self.add_button = QPushButton("Добавить кофе")
        self.edit_button = QPushButton("Редактировать")
        self.refresh_button = QPushButton("Обновить таблицу")

        # Добавляем кнопки в горизонтальный layout
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()

        # Добавляем горизонтальный layout в вертикальный
        layout.addLayout(button_layout)

        # Создаем таблицу - теперь QTableWidget импортирован!
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Устанавливаем layout
        central_widget.setLayout(layout)

        # Подключаем кнопки
        self.add_button.clicked.connect(self.add_coffee)
        self.edit_button.clicked.connect(self.edit_coffee)
        self.refresh_button.clicked.connect(self.load_coffee)

        # Загружаем данные
        self.load_coffee()

    def load_coffee(self):
        """Загружает данные из базы и отображает в таблице"""
        try:
            conn = sqlite3.connect('coffee.sqlite')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM coffee')
            data = cursor.fetchall()

            self.table.setRowCount(len(data))
            self.table.setColumnCount(7)

            # Устанавливаем заголовки
            headers = ['ID', 'Название', 'Степень обжарки', 'Молотый/В зернах',
                       'Описание вкуса', 'Цена', 'Объем упаковки']
            self.table.setHorizontalHeaderLabels(headers)

            # Заполняем таблицу
            for row, item in enumerate(data):
                for col, value in enumerate(item):
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))

            # Растягиваем столбцы по содержимому
            self.table.resizeColumnsToContents()

            # Растягиваем последний столбец
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(4, QHeaderView.Stretch)  # Растягиваем описание вкуса

            conn.close()
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def add_coffee(self):
        """Открывает форму для добавления нового кофе"""
        form = AddEditCoffeeForm(self)
        if form.exec_():  # Если нажали Сохранить
            self.load_coffee()  # Обновляем таблицу

    def edit_coffee(self):
        """Открывает форму для редактирования выбранного кофе"""
        # Получаем выбранную строку
        current_row = self.table.currentRow()
        if current_row < 0:
            # Ничего не выбрано
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для редактирования")
            return

        # Получаем ID из первой колонки
        coffee_id = int(self.table.item(current_row, 0).text())

        # Открываем форму редактирования
        form = AddEditCoffeeForm(self, coffee_id)
        if form.exec_():  # Если нажали Сохранить
            self.load_coffee()  # Обновляем таблицу


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeApp()
    ex.show()
    sys.exit(app.exec_())
