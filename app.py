import sys
import os

import certifi

from Network_Security.constants.training_pipepline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME
from Network_Security.utils.ml_utils.model.estimator import NetworkModel
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mango_db_url = os.getenv("MONGO_DB_URL")
print(mango_db_url)

import pymongo
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from Network_Security.utils.main_utils.utils import load_object

def get_latest_artifact_dir(base_dir="Artifacts"):
    folders = [
        os.path.join(base_dir, d)
        for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d))
    ]
    latest_dir = max(folders, key=os.path.getmtime)
    return latest_dir

client = pymongo.MongoClient(mango_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is Successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        print("✅ Predict route called")

        df = pd.read_csv(file.file)
        print("Data loaded, shape:", df.shape)

        latest_artifact_dir = get_latest_artifact_dir()
        print("📦 Using artifacts from:", latest_artifact_dir)

        preprocessor_path = os.path.join(
            latest_artifact_dir,
            "data_transformation",
            "transformed_object",
            "preprocessing.pkl"
        )

        model_path = os.path.join(
            latest_artifact_dir,
            "model_trainer",
            "trained_model",
            "model.pkl"
        )

        preprocessor = load_object(preprocessor_path)
        model = load_object(model_path)

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=model
        )

        y_pred = network_model.predict(df)
        df["predicted_column"] = y_pred

        os.makedirs("prediction_output", exist_ok=True)
        output_path = "prediction_output/output.csv"
        df.to_csv(output_path, index=False)

        print("✅ Prediction saved at:", output_path)

        table_html = df.to_html(classes="table table-striped")

        return templates.TemplateResponse(
            "table.html",
            {
                "request": request,
                "table_html": table_html
            }
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.get("/predict")
async def predict_form(request: Request):
        return templates.TemplateResponse(
            "table.html",
            {"request": request}
        )
    
if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)