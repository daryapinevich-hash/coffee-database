import sqlite3

# Создаем подключение к базе данных
conn = sqlite3.connect('coffee.sqlite')
cursor = conn.cursor()

# Создаем таблицу
cursor.execute('''
CREATE TABLE IF NOT EXISTS coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roast_level TEXT,
    ground_or_beans TEXT,
    taste_description TEXT,
    price REAL,
    package_volume INTEGER
)
''')

# Добавляем данные
coffee_data = [
    ('Эфиопия Сидамо', 'Светлая', 'Молотый', 'Цитрусовые нотки, ягодный аромат', 850, 250),
    ('Колумбия Супремо', 'Средняя', 'В зернах', 'Карамель, орехи, шоколад', 780, 500),
    ('Бразилия Сантос', 'Темная', 'Молотый', 'Горький шоколад, орехи', 650, 500),
    ('Гватемала', 'Средняя', 'В зернах', 'Фруктовый букет, вино', 950, 300),
    ('Кения', 'Светлая', 'Молотый', 'Ягоды, цитрус, кислинка', 890, 250)
]

cursor.executemany('''
INSERT INTO coffee (name, roast_level, ground_or_beans, taste_description, price, package_volume)
VALUES (?, ?, ?, ?, ?, ?)
''', coffee_data)

# Сохраняем изменения
conn.commit()
conn.close()

print("База данных создана успешно!")