import pandas as pd
import requests
import json
import os

# --- CONFIGURACIÓN ---
PROJECT_ID = "uadctgllvwldvnsfakbe"
URL = f"https://{PROJECT_ID}.supabase.co/rest/v1/postulaciones_demo"
API_KEY = "sb_secret_r68V-kRGv5S9-KQ_Atg0Rw_p3TYQ669" 

def load_data_web():
    print("--- CARGA VÍA API REST (MAPEO AUTOMÁTICO) ---")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "postulaciones.xlsx")
    
    try:
        print(f"1. Leyendo Excel...")
        df = pd.read_excel(file_path)
        
        # --- EL TRUCO MAESTRO: MINÚSCULAS ---
        # Esto hace que 'CARRERA' pase a ser 'carrera' y coincida con Supabase
        df.columns = [c.lower().strip() for c in df.columns]
        
        # --- LIMPIEZA PROFUNDA ---
        df = df.astype(object).where(pd.notnull(df), None)
        
        # Convertir fechas a string si existen
        for col in df.columns:
            if "fecha" in col or "created" in col:
                df[col] = df[col].apply(lambda x: str(x) if x is not None else None)

        records = df.to_dict(orient='records')
        
        headers = {
            "apikey": API_KEY,
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal" 
        }
        
        print(f"2. Enviando {len(records)} registros...")

        batch_size = 500 # Subimos el bloque para terminar más rápido
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            payload = json.dumps(batch, ensure_ascii=False, default=str)
            
            response = requests.post(URL, headers=headers, data=payload.encode('utf-8'))
            
            if response.status_code in [200, 201]:
                print(f"✅ Progreso: {i + len(batch)} / {len(records)}")
            else:
                print(f"❌ Error en bloque {i}: {response.text}")
                return 

        print("\n--- ¡ÉXITO! CARGA COMPLETADA ---")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    load_data_web()