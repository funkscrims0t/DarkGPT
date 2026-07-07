import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os

DEHASHED_API_KEY = os.getenv("DEHASHED_API_KEY")
DEHASHED_USERNAME = os.getenv("DEHASHED_USERNAME")

def consultar_dominio_dehashed(consulta):
    parametros = {'email': consulta.get("mail"), 'username': consulta.get("nickname")}
    resultados = {}
    headers = {'Accept': 'application/json'}
    for tipo, valor in parametros.items():
        if valor:
            try:
                params = (('query', valor),)
                json_crudo_dehashed = requests.get('https://api.dehashed.com/search',
                                               headers=headers,
                                               params=params,
                                               auth=(DEHASHED_USERNAME, DEHASHED_API_KEY)).text
                resultados[tipo] = convertir_json(json_crudo_dehashed)
            except Exception as e:
                print(f"Error al consultar {tipo}: {e}")
                pass
    resultado_ordenado = ""
    for parametro, entradas in resultados.items():
        for item in entradas:
            fila = f"{item.get('email', 'No disponible')}, "
            fila += f"{item.get('username', 'No disponible')}, "
            fila += f"{item.get('password', 'No disponible')}, "
            fila += f"{item.get('hashed_password', 'No disponible')}, "
            fila += f"{item.get('phone', 'No disponible')}, "
            fila += f"{item.get('database_name', 'No disponible')}\n"
            resultado_ordenado += fila
    return resultado_ordenado

def convertir_json(raw_json):
    datos_json = json.loads(raw_json)
    entradas = datos_json.get('entries', [])
    return entradas
