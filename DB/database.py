import os
import sqlite3
import pandas as pd

db_path = 'daily_visits.db'
csv_path = '../data/users_web.csv'

def create_table():
    # conectar a la base de datos, si no existe crea una nueva
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # crear tabla con numero de usuarios por día
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visit_quant (
            Date DATE PRIMARY KEY,
            Users INTEGER
        )
    ''')
    conn.commit()

    cursor.close()
    conn.close()


def update_table():
    conn = sqlite3.connect(db_path)

    # leer del csv
    df_csv = pd.read_csv(csv_path)
    df_csv['Date'] = pd.to_datetime(df_csv['Date'], dayfirst=True)
    # leer de la db (TODO funcion a parte)
    df_sql = pd.read_sql("SELECT * from visit_quant", conn)

    # quitar duplicados antes de insertar
    df_new = pd.merge(df_sql, df_csv, indicator=True, how='outer')
    df_new = df_new[df_new['_merge'] == 'right_only'].drop('_merge', axis=1)
    
    # añadir nuevas filas a la db
    df_new.to_sql('visit_quant', conn, if_exists='append', index=False)

    conn.close()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    create_table()
    update_table()

main()
