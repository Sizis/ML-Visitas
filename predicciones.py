
# Crear el modelo de Holt-Winters
model = ExponentialSmoothing(df['Users'], trend='add', seasonal='add', seasonal_periods=7)
fit_model = model.fit(damping_slope=0.8)

# Solicitar al usuario ingresar una fecha futura
while True:
    try:
        input_date = input("Ingresa una fecha futura en formato YYYY-DD-MM: ")
        forecast_date = pd.to_datetime(input_date)
        break
    except ValueError:
        print("Por favor, ingresa una fecha válida en el formato correcto.")

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

# Realizar el pronóstico para la fecha ingresada y la cantidad de pasos
forecast = fit_model.forecast(steps=forecast_steps)
forecast_values = forecast[:forecast_steps].astype(int)

print(f"Predicción de visitas para la fecha {forecast_date.date()}:")
for i in range(forecast_steps):
    print(f"{i+1} {forecast_values[i]}")

    # Crear un DataFrame con los resultados
forecast_df = pd.DataFrame({'Fecha': pd.date_range(start=forecast_date, periods=forecast_steps),
                            'Predicción': forecast_values})

# Mostrar el DataFrame de resultados
print("\nResultados de la Predicción:")
forecast_df