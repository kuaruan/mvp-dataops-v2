import os
import pandas as pd
from sqlalchemy import create_engine

def load_data():
    # USAMOS LA URL DIRECTA DE SUPABASE
    ## Configuración que debes dejar guardada:
    project_id = "uadctgllvwldvnsfakbe"
    user = f"postgres.{project_id}"
    password = "mvp-dataops-v2"
    host = "aws-0-us-west-2.pooler.supabase.com"
    port = "6543"
    db_url = f"postgresql://{user}:{password}@{host}:{port}/postgres"
        
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "postulaciones.xlsx")
    
    print("--- CARGA USANDO INTERNET DEL CELULAR ---")
    
    try:
        print("1. Leyendo Excel...")
        df = pd.read_excel(file_path)
        
        engine = create_engine(db_url)
        
        print("2. Subiendo a Supabase... (Esto usará unos pocos MB de tu plan de datos)")
        with engine.begin() as connection:
            df.to_sql('postulaciones_demo', connection, if_exists='append', index=False, chunksize=500)
            
        print("--- ¡ÉXITO! Los datos están arriba ---")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    load_data()