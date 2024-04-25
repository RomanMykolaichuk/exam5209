import os
import random
from datetime import datetime, timedelta

# Отримуємо поточний шлях до файлу скрипта
current_path = os.path.dirname(os.path.abspath(__file__))
sql_file_path = os.path.join(current_path, 'generate_data.sql')

# Функція для генерації випадкової дати
def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date

# Відкриваємо файл для запису SQL-запитів у поточній папці
with open(sql_file_path, 'w') as sql_file:
    # Генеруємо SQL-запити для створення таблиць
    sql_file.write('''-- Створення таблиці для даних про техніку
CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Створення таблиці для витрати пального
CREATE TABLE fuel_expense (
    expense_id SERIAL PRIMARY KEY,
    equipment_id INT REFERENCES equipment(equipment_id),
    date DATE NOT NULL,
    liters FLOAT NOT NULL,
    cost NUMERIC(10, 2) NOT NULL,
    mileage FLOAT NOT NULL
);

-- Додавання даних до таблиці "equipment"
INSERT INTO equipment (name)
VALUES
    ('Excavator'),
    ('Bulldozer'),
    ('Crane'),
    ('Loader'),
    ('Backhoe'),
    ('Dump Truck'),
    ('Concrete Mixer'),
    ('Forklift'),
    ('Grader'),
    ('Tractor');
''')

    # Генеруємо SQL-запити для заповнення таблиці "fuel_expense"
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    for _ in range(1000):
        equipment_id = random.randint(1, 10)
        random_date = generate_random_date(start_date, end_date)
        liters = round(random.uniform(1, 100), 1)
        cost = round(random.uniform(1, 200), 2)
        mileage = round(random.uniform(1, 1000), 1)
        sql_file.write(f"INSERT INTO fuel_expense (equipment_id, date, liters, cost, mileage) VALUES ({equipment_id}, '{random_date}', {liters}, {cost}, {mileage});\n")

print(f"SQL-файл 'generate_data.sql' був створений у папці '{current_path}'.")
