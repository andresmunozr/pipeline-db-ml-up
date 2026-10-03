import joblib
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv


from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

class TrainModel:

    def entrenarModelo():

        #se usaron las credeciales para ingresar de manera ocacional (Transaction pooler)
        load_dotenv("/app/.env")
        USER = os.getenv("SUPABASE_USER")
        PASSWORD = os.getenv("SUPABASE_PASSWORD")
        HOST = os.getenv("SUPABASE_HOST")
        PORT = os.getenv("SUPABASE_PORT")
        DBNAME = os.getenv("SUPABASE_DBNAME")
        

        if(PORT== None):
            print("no se lee el env")
            return
        else:
            print("si se lee en env")


        try:
            with psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                dbname=DBNAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'SELECT email_type, country, city, genre FROM "Dataset";'
                    )
                    rows = cursor.fetchall()
                    
                    print(f"Filas recuperadas: {len(rows)}")

        except Exception as e:
            print(f"Error al conectar o recuperar datos: {e}")
            return
        
        if not rows:
            print("No se recuperaron filas de la base de datos. Abortando entrenamiento.")
            return
        else:
            print(rows[:2])
            

        data = pd.DataFrame(rows, columns=["email_type", "country", "city", "genre"])
        features = ["email_type", "country", "city"]
        model = Pipeline([
            ("encoder", ColumnTransformer([
                ("categorical", OneHotEncoder(handle_unknown="ignore"), features),
            ])),
            ("classifier", LogisticRegression(max_iter=1000)),
        ])
        model.fit(data[features], data["genre"])
        joblib.dump(model, os.getenv("MODELO_ENTRENADO"))
        print("modelo entrenado")
        
