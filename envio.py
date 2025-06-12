import pandas as pd
import requests
import time 

# Cargar el CSV
df = pd.read_csv("data.csv")

# URL de tu API
API_URL = "https://mantenimiento-predictivo.onrender.com/predict"

# Recorre cada fila del DataFrame
for index, row in df.iterrows():
    payload = {
        "date": str(row["date"]),  
        "machine_id": row["machine_id"],
        "assembly_line_no": row["assembly_line_no"],
        "Hydraulic_Pressure_bar": float(row["Hydraulic_Pressure_bar"]),
        "Coolant_Pressure_bar": float(row["Coolant_Pressure_bar"]),
        "Air_System_Pressure_bar": float(row["Air_System_Pressure_bar"]),
        "Coolant_Temperature": float(row["Coolant_Temperature"]),
        "Hydraulic_Oil_Temperature": float(row["Hydraulic_Oil_Temperature"]),
        "Spindle_Bearing_Temperature": float(row["Spindle_Bearing_Temperature"]),
        "Spindle_Vibration": float(row["Spindle_Vibration"]),
        "Tool_Vibration": float(row["Tool_Vibration"]),
        "Spindle_Speed_RPM": int(row["Spindle_Speed_RPM"]),
        "Voltage_volts": int(row["Voltage_volts"]),
        "Torque_Nm": float(row["Torque_Nm"]),
        "Cutting_kN": float(row["Cutting_kN"])
    }

    # Enviar la solicitud POST
    try:
        response = requests.post(API_URL, json=payload)
        print(f"Fila {index + 1}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error en fila {index + 1}: {e}")

    # Esperar un poco para no saturar el servidor
    time.sleep(1)
