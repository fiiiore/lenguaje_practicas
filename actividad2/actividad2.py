
from datetime import datetime
from collections import Counter, defaultdict
import csv
import json
import os

# -------------------------------------
#  Crear carpeta de salida
# -------------------------------------
os.makedirs("salida", exist_ok=True)

# -------------------------------------
#  Inicializar estructuras para acumular información
# -------------------------------------
contador_dias = Counter()
contador_campeones = Counter()      
contador_finde = Counter()          
resumen_dias = defaultdict(lambda: defaultdict(int))  
fechas = []                        

fines_de_semana = ['Saturday', 'Sunday']

# -------------------------------------
#  Función para convertir fecha según formato
# -------------------------------------
def parse_fecha(fecha_str):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(fecha_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Formato de fecha no reconocido: {fecha_str}")

# -------------------------------------
# Leer el CSV y procesar todo en una sola pasada
# -------------------------------------
with open("actividad_2.csv", newline="", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    
    for fila in lector:
        # Parsear y extraer datos útiles de la fila
        fecha = parse_fecha(fila["timestamp"])
        dia_semana = fecha.strftime("%A")
        campeon = fila["campeon"]

        # Actualizar contadores
        contador_dias[dia_semana] += 1
        contador_campeones[campeon] += 1
        resumen_dias[dia_semana][campeon] += 1
        
        # Contar fines de semana
        if dia_semana in fines_de_semana:
            contador_finde[campeon] += 1
        
        # Registrar fecha para calcular rango después
        fechas.append(fecha)

# Día/s con más sesiones
max_sesiones = max(contador_dias.values())
dias_mas_sesiones = [dia for dia, cant in contador_dias.items() if cant == max_sesiones]

# Rango entre primer y último entrenamiento
dias_transcurridos = (max(fechas) - min(fechas)).days

# Campeón que más entrenó
campeon_top = contador_campeones.most_common(1)[0][0]

# Promedio de entrenamientos por día
num_semanas = dias_transcurridos / 7 if dias_transcurridos >= 7 else 1
promedio_por_dia = {d: round(c / num_semanas, 2) for d, c in contador_dias.items()}

# Campeón que más entrena fines de semana
if contador_finde:
    campeon_finde = contador_finde.most_common(1)[0][0]
else:
    campeon_finde = "No hay entrenamientos en fin de semana"

# -------------------------------------
#  Mostrar resultados
# -------------------------------------
print("Cantidad total de registros:", sum(contador_dias.values()))
print("Día/s con más sesiones:", dias_mas_sesiones)
print("Días entre primer y último entrenamiento:", dias_transcurridos)
print("Campeón que más entrenó:", campeon_top)
print("Promedio entrenamientos por día:", promedio_por_dia)
print("Campeón que más entrena fines de semana:", campeon_finde)

# -------------------------------------
#  Exportar resultados
# -------------------------------------
# CSV
with open("salida/entrenamientos_por_campeon.csv", "w", newline="", encoding="utf-8") as archivo_salida:
    writer = csv.writer(archivo_salida)
    writer.writerow(["campeon", "cantidad"])
    writer.writerows(contador_campeones.items())

# JSON
resumen = {
    "total_registros": sum(contador_dias.values()),
    "dias_mas_sesiones": dias_mas_sesiones,
    "dias_transcurridos": dias_transcurridos,
    "campeon_mas_entreno": campeon_top,
    "promedios_por_dia": promedio_por_dia,
    "campeon_finde": campeon_finde,
}
resumen.update(resumen_dias)

with open("salida/resumen.json", "w", encoding="utf-8") as archivo_json:
    json.dump(resumen, archivo_json, indent=4)

print("\n✅ Archivos generados en la carpeta 'salida':")
print("- entrenamientos_por_campeon.csv")
print("- resumen.json")
