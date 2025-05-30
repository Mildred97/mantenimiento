import os
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import psycopg2
from datetime import date

# Carga el modelo
modelo = joblib.load("modelo.pkl")

# Columnas que el modelo espera
features = [
    "Hydraulic_Pressure_bar",
    "Coolant_Pressure_bar",
    "Air_System_Pressure_bar",
    "Coolant_Temperature",
    "Hydraulic_Oil_Temperature",
    "Spindle_Bearing_Temperature",
    "Spindle_Vibration",
    "Tool_Vibration",
    "Spindle_Speed_RPM",
    "Voltage_volts",
    "Torque_Nm",
    "Cutting_kN"
]

# Configuración de conexión a PostgreSQL 
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}


# API
app = FastAPI(title="Modelo de Predicción de Fallas")
class InputData(BaseModel):
    date: date
    machine_id: str
    assembly_line_no: str
    Hydraulic_Pressure_bar: float
    Coolant_Pressure_bar: float
    Air_System_Pressure_bar: float
    Coolant_Temperature: float
    Hydraulic_Oil_Temperature: float
    Spindle_Bearing_Temperature: float
    Spindle_Vibration: float
    Tool_Vibration: float
    Spindle_Speed_RPM: int
    Voltage_volts: int
    Torque_Nm: float
    Cutting_kN: float

@app.post("/predict")
def predict(input_data: InputData):
    df = pd.DataFrame([input_data.dict()])

    # Datos para predicción
    datos_modelo = df[features]
    pred = int(modelo.predict(datos_modelo)[0])
    df["downtime"] = pred

    # Convierte a valores nativos de Python
    values = []
    for val in df.iloc[0]:
        if hasattr(val, 'item'):
            values.append(val.item())  
        else:
            values.append(val)

    # Insertar en PostgreSQL
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        insert_query = """
            INSERT INTO machine_data (
                date, machine_id, assembly_line_no,
                hydraulic_pressure_bar, coolant_pressure_bar, air_system_pressure_bar,
                coolant_temperature, hydraulic_oil_temperature,
                spindle_bearing_temperature, spindle_vibration, tool_vibration,
                spindle_speed_rpm, voltage_volts, torque_nm, cutting_kn,
                downtime
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, tuple(values))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return {"error": str(e)}

    return {"prediction": pred}
