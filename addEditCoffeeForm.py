import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox


class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        # Загружаем интерфейс
        uic.loadUi('addEditCoffeeForm.ui', self)

        # Запоминаем ID кофе (если None - это добавление, если есть - редактирование)
        self.coffee_id = coffee_id

        # Подключаем кнопки
        self.button_save.clicked.connect(self.save_coffee)
        self.button_cancel.clicked.connect(self.reject)

        # Если редактируем - загружаем данные
        if self.coffee_id:
            self.load_coffee_data()
            self.setWindowTitle("Редактирование кофе")
        else:
            self.setWindowTitle("Добавление кофе")

    def load_coffee_data(self):
        """Загружает данные кофе для редактирования"""
        try:
            conn = sqlite3.connect('coffee.sqlite')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM coffee WHERE id = ?', (self.coffee_id,))
            coffee = cursor.fetchone()

            if coffee:
                # Заполняем поля
                self.lineEdit_name.setText(coffee[1])  # name

                # Выбираем степень обжарки в комбобоксе
                index = self.comboBox_roast.findText(coffee[2])
                if index >= 0:
                    self.comboBox_roast.setCurrentIndex(index)

                # Выбираем тип в комбобоксе
                index = self.comboBox_type.findText(coffee[3])
                if index >= 0:
                    self.comboBox_type.setCurrentIndex(index)

                self.textEdit_taste.setText(coffee[4])  # taste_description
                self.lineEdit_price.setText(str(coffee[5]))  # price
                self.lineEdit_volume.setText(str(coffee[6]))  # package_volume

            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")

    def save_coffee(self):
        """Сохраняет данные в базу"""
        # Проверяем, что все поля заполнены
        if not self.lineEdit_name.text():
            QMessageBox.warning(self, "Предупреждение", "Введите название кофе")
            return

        try:
            # Получаем данные из полей
            name = self.lineEdit_name.text()
            roast = self.comboBox_roast.currentText()
            coffee_type = self.comboBox_type.currentText()
            taste = self.textEdit_taste.toPlainText()
            price = float(self.lineEdit_price.text()) if self.lineEdit_price.text() else 0
            volume = int(self.lineEdit_volume.text()) if self.lineEdit_volume.text() else 0

            conn = sqlite3.connect('coffee.sqlite')
            cursor = conn.cursor()

            if self.coffee_id:  # Редактирование
                cursor.execute('''
                    UPDATE coffee 
                    SET name=?, roast_level=?, ground_or_beans=?, 
                        taste_description=?, price=?, package_volume=?
                    WHERE id=?
                ''', (name, roast, coffee_type, taste, price, volume, self.coffee_id))
            else:  # Добавление
                cursor.execute('''
                    INSERT INTO coffee (name, roast_level, ground_or_beans, taste_description, price, package_volume)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, roast, coffee_type, taste, price, volume))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Данные сохранены!")
            self.accept()  # Закрываем форму с успехом

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Проверьте правильность ввода цены и объема")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {e}")