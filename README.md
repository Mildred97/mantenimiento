# 🛠️ API de Predicción de Downtime

Esta API permite predecir la probabilidad de *downtime* (tiempo de paro) en maquinaria industrial a partir de variables como la presión hidráulica, la velocidad del husillo (RPM), y otras características del sistema. El objetivo es asistir en la toma de decisiones para mantenimiento preventivo o ajustes operativos.

## 🚀 Tecnologías utilizadas

- Python 3.10
- FastAPI
- Uvicorn
- XGBoost
- Pandas / NumPy

El modelo fue entrenado utilizando datos históricos de sensores industriales. Se incluyeron variables como:
- "Hydraulic_Pressure(bar)", "Coolant_Pressure(bar)" y "Air_System_Pressure(bar)" - mediciones de presión en diferentes puntos de la máquina.
- "Coolant_Temperature", "Hydraulic_Oil_Temperature" y "Spindle_Bearing_Temperature" - mediciones de temperatura (en Celsius) en diferentes puntos de la máquina.
- "Spindle_Vibration", "Tool_Vibration" y "Spindle_Speed(RPM)" - mediciones de vibración (en micrómetros) y velocidad de rotación del husillo y la herramienta.
- "Voltage(volts)" - el voltaje suministrado a la máquina.
- "Torque(Nm)" - el torque generado por la máquina.
- "Cutting(KN)" - la fuerza de corte de la herramienta.
- "Downtime" - indicador de si la máquina estuvo fuera de servicio o no en el día registrado.
