
# Crear el modelo de Holt-Winters
model = ExponentialSmoothing(df['Users'], trend='add', seasonal='add', seasonal_periods=7)
fit_model = model.fit(damping_slope=0.8)

# Solicitar al usuario ingresar una fecha futura
while True:
    try:
        input_date = input("Ingresa una fecha futura en formato YYYY-MM-DD: ")
        forecast_date = pd.to_datetime(input_date)
        break
    except ValueError:
        print("Por favor, ingresa una fecha válida en el formato correcto YYYY-MM-DD.")

# Solicitar al usuario elegir la opción de pronóstico
while True:
    try:
        forecast_option = input("¿Deseas predecir para 1 semana, o para 1 mes? Elija semana, o mes): ")
        if forecast_option.lower() not in ['semana', 'mes']:
            raise ValueError()
        break
    except ValueError:
        print("Por favor, ingresa una opción válida ('semana' o 'mes').")

# Calcular el número de pasos de pronóstico según la opción seleccionada
if forecast_option.lower() == 'semana':
    forecast_steps = 7
else:
    forecast_steps = 30  # Asumiendo un mes de 30 días

# LLamar a la base de datos y sacar última fecha
# cargar los datos de la db
conn = sqlite3.connect('DB/daily_visits.db')
df = pd.read_sql("SELECT * FROM visit_quant", conn, parse_dates='Date', index_col='Date')
conn.close()

# Obtener la última fecha del DataFrame
last_date = df.index.max()

# Realizar el pronóstico para la fecha ingresada y la cantidad de pasos
forecast = fit_model.predict(forecast_steps + (forecast_date - last_date).days)
forecast_values = forecast[:forecast_steps].astype(int)

# Crear un DataFrame con los resultados
forecast_df = pd.DataFrame({'Fecha': pd.date_range(start=forecast_date, periods=forecast_steps),
                            'Predicción': forecast_values})

# Restablecer el índice y convertir la columna "Fecha" en el nuevo índice
forecast_df.reset_index(drop=True, inplace=True)
forecast_df.set_index('Fecha', inplace=True)

# Mostrar el DataFrame de resultados
print("\nResultados de la Predicción:")
forecast_df