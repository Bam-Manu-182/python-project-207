import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

def init_database():
    database_url = os.getenv('DATABASE_URL')
    print("Conectando a la base de datos de Render...")

    try:
        with open('database.sql', 'r') as f:
            sql_script = f.read()

        conn = psycopg2.connect(database_url)
        with conn.cursor() as curr:
            curr.execute(sql_script)
            conn.commit()
        conn.close()

        print("¡Éxito total! Las tablas se crearon correctamente en Render.")

    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")


if __name__ == '__main__':
    init_database()
