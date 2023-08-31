import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from pmdarima.arima import ARIMA

import database

picklename = 'model_arima_users.pkl'

def train_with_all_data(filename, df_new):

    # aplicar log y quitar los -inf para evitar errores
    df_logScale = np.log(df_new)
    df_logScale[df_logScale.index.isin(np.isfinite(df_logScale[['Users']]).query('not Users').index)] = 0

    # entrenar modelo con hyperparametros conseguidos en el analisis
    users_log = df_logScale['Users'].values
    model_new = ARIMA(order=(9, 1, 6))
    model_new.fit(users_log)
        
    with open(filename, "wb") as output_file:
        pickle.dump(model_new, output_file)

def update_model(filename, df_new):
    # cargar modelo
    with open(filename, 'rb') as input_file:
        model = pickle.load(input_file)

    # actualizar modelo con la data nueva
    df_logScale = np.log(df_new)
    df_logScale[df_logScale.index.isin(np.isfinite(df_logScale[['Users']]).query('not Users').index)] = 0
    model_updated = model.update(df_logScale.values)

    with open(filename, "wb") as output_file:
        pickle.dump(model_updated, output_file)
    

def main():
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # si no existe la db (o la tabla) crearla
    if not os.path.isfile(database.db_path):
        database.create_table(database.db_path)

    # pedir csv para añadir a la db
    while True:
        try:
            filename = input("Indique el nombre del csv con la data nueva: ")
            csv_path = database.csv_path + filename
            if not os.path.isfile(csv_path):
                raise ValueError()
            break
        except ValueError:
            print("Ese csv no existe")
    
    # leer del csv
    df_csv = pd.read_csv(csv_path)
    # formatear la fecha a AAAA-MM-DD
    df_csv['Date'] = pd.to_datetime(df_csv['Date'], dayfirst=True)
    # actualizar la db
    database.update_table(df_csv)

    # entrenar o actualizar modelo
    df_csv = df_csv.set_index(df_csv['Date']).drop('Date', axis=1)
    if os.path.isfile(picklename):
        update_model(picklename, df_csv)
    else:
        train_with_all_data(picklename, df_csv)


main()
