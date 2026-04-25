import os
import pandas as pd
from sqlalchemy import create_engine

# Datos confirmados por tus capturas:
project_id = "uadctgllvwldvnsfakbe"
user = f"postgres.{project_id}"
password = "mvp-dataops-v2"
host = "aws-0-us-west-2.pooler.supabase.com" # Oregon
port = "6543"

db_url = f"postgresql://{user}:{password}@{host}:{port}/postgres"

def load():
    print("--- INICIANDO CARGA MASIVA ---")
    try:
        df = pd.read_excel("data/postulaciones.xlsx")
        engine = create_engine(db_url)
        print("Conectando y subiendo registros...")
        df.to_sql('postulaciones_demo', engine, if_exists='append', index=False, chunksize=500)
        print("--- ¡ÉXITO! Verifica tu dashboard ahora ---")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    load()

