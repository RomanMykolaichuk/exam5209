
from flask import Flask, render_template, request, Response
from chart1 import generate_chart
import psycopg2, os

app = Flask(__name__)

db_params = {
    'dbname': 'exam1',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}

# Підключення до бази даних
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Вибірка даних з бази даних (приклад)
cursor.execute("SELECT * FROM equipment")
equipment_options = cursor.fetchall()

# Закриваємо з'єднання з базою даних
cursor.close()
conn.close()

def found_name(id): 
    name = 'not found'
    print(id)
    for option in equipment_options:       
        if option[0] == id:
            name = option[1]
            print(name)
    return name
    


@app.route('/')
def index():
    return render_template('index.html', equipment_options=equipment_options, result=None)

@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    sql_query = request.form['sql_query']
    result = None

    try:
        # Виконуємо SQL-запит у базі даних
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.commit()
    except Exception as e:
        result = str(e)
    finally:
        cursor.close()
        conn.close()

    return render_template('index.html', equipment_options=equipment_options, result=result)

@app.route('/chart', methods=['POST'])
def display_chart():
    equipment_id = request.form['equipment_id']

    conn = psycopg2.connect(**db_params)

    # Викликаємо функцію generate_chart з generate_chart.py
    chart_name = generate_chart(equipment_id, found_name(int(equipment_id)),conn)

      
    chart_path = os.path.join('static/img', chart_name)

    # Виводимо графік у веб-інтерфейсі
    return render_template('chart.html', chart_path=chart_path)

@app.route('/add_fuel_expense', methods=['POST'])
def add_fuel_expense():
    if request.method == 'POST':
        # Отримуємо дані з форми
        equipment_id = request.form['equipment_id']
        date = request.form['date']
        liters = request.form['liters']
        cost = request.form['cost']
        mileage = request.form['mileage']

        try:
            # Підключення до бази даних
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()

            # SQL-запит для вставки даних в таблицю fuel_expenses
            sql = """
            INSERT INTO fuel_expense (equipment_id, date, liters, cost, mileage)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (equipment_id, date, liters, cost, mileage))

            # Зберігаємо зміни та закриваємо підключення
            conn.commit()
            conn.close()

            # Після збереження перенаправляємо користувача на іншу сторінку (наприклад, головну)
            return render_template('index.html', equipment_options=equipment_options, result="None")

        except Exception as e:
            # Обробка помилок підключення або запиту
            return "Помилка при додаванні витрат на пальне: " + str(e)

if __name__ == '__main__':
    app.run(debug=True)
