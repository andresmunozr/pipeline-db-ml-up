import os
import joblib
import pandas as pd

from src.contexts.api.models import PredictorRequest



class TrainModelController:
    def execute(self, request: PredictorRequest):
        print(request)
        model_path = os.getenv("MODELO_ENTRENADO")
        model = joblib.load(model_path)
        input_data = pd.DataFrame([{
            "email_type": request.email_type,
            "country": request.country,
            "city": request.city,
        }])
        prediction = model.predict(input_data)[0]

        print(f"Predicción de género musical: {prediction}")
        return {"status": "OK", "result": prediction}

    
