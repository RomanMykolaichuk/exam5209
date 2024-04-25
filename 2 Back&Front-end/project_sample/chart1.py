import matplotlib.pyplot as plt
import pandas as pd
import os



def generate_chart(equipment_id, name, conn):
    try:
        # Виконуємо SQL-запит для отримання даних про заправку для обраної техніки за місяць
       
        query = f"""
            SELECT EXTRACT(MONTH FROM date) AS month, SUM(liters) AS total_liters
            FROM fuel_expense
            WHERE equipment_id = {equipment_id}
            GROUP BY month
            ORDER BY month
        """
        df = pd.read_sql_query(query, conn)

        

        # Побудова графіку
        plt.figure(figsize=(10, 6))
        plt.bar(df['month'], df['total_liters'])
        plt.xlabel('Місяць')
        plt.ylabel('Заправка (літри)')
        plt.title('Заправка за місяць ('+ name+')')
        plt.xticks(range(1, 13), ['Січ', 'Лют', 'Бер', 'Квіт', 'Трав', 'Черв', 'Лип', 'Серп', 'Вер', 'Жовт', 'Лист', 'Груд'])
         # Створення шляху до папки "static/img" у вашому проекті
        static_img_dir = os.path.join(os.path.dirname(__file__), 'static', 'img')
        
        # Перевірка, чи існує папка "static/img"; якщо ні, то створюємо її
        if not os.path.exists(static_img_dir):
            os.makedirs(static_img_dir)
        
        chart_name = 'chart.png'

        # Зберігаємо графік у файл у папці "static/img"
        chart_path = os.path.join(static_img_dir, chart_name)
        plt.savefig(chart_path)

        # Закриваємо графік, щоб звільнити ресурси Matplotlib
        plt.close()
    except Exception as e:
        print(str(e))
    finally:
        conn.close()
    return chart_name