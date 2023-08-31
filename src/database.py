import os
import sqlite3
import pandas as pd

db_path = '../DB/daily_visits.db'
csv_path = '../data/'

def create_table(db_path):
    # conectar a la base de datos, si no existe crea una nueva
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # crear tabla de numero de usuarios por día si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visit_quant (
            Date DATE PRIMARY KEY,
            Users INTEGER
        )
    ''')
    conn.commit()

    cursor.close()
    conn.close()


def update_table(df_csv):
    conn = sqlite3.connect(db_path)

    # añadir los datos nuevos a la tabla
    df_csv.to_sql('visit_quant', conn, if_exists='append', index=False)

    conn.close()
