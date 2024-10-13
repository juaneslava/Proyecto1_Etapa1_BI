from typing import List
from fastapi import FastAPI, File, Response, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Model import DataModel
from joblib import load, dump
from Pipeline import pipeline

import traceback

import pandas as pd
import json
import os
import io

app = FastAPI()

pipeline2 = load('./assets/pipeline.joblib')

origins = ['http://localhost/8000',
           'http://localhost:3000',
           'http://localhost:3000',
           'http://127.0.0.1:8000',
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.post('/predict_input')
def makePredictionInput(dataModelList : List[DataModel]):
    
    predictions = []
    
    for dataModel in dataModelList:
        data = dataModel.model_dump()
        df = pd.DataFrame([data], columns=dataModel.columns())
        
        pipeline2.named_steps['cleaningPipe'].trainingMode = False
        pipeline2.named_steps['vectorizerPipe'].trainingMode = False
        
        pred_df = pipeline2.predict(df)
        score = max(pred_df.loc[0, 'prob_class_0'], pred_df.loc[0, 'prob_class_1'], pred_df.loc[0, 'prob_class_2'])
        
        prediction_result = {
            'text': data['Textos_espanol'],
            'prediction': int(pred_df.loc[0, 'label']),
            'score': score
        }
        predictions.append(prediction_result)
    
    return {'predictions': predictions}


@app.post('/retrain')
async def retrainModel(file: UploadFile = File(...)):

    _, file_extension = os.path.splitext(file.filename)

    if file_extension not in ['.csv', '.xlsx']:
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a CSV or XLSX file."})

    try:
        # Leer el contenido del archivo subido
        contents = await file.read()
        if file_extension == '.csv':
            new_dataframe = pd.read_csv(io.BytesIO(contents))
        elif file_extension == '.xlsx':
            new_dataframe = pd.read_excel(io.BytesIO(contents))

        # Verificar las columnas necesarias
        if 'Textos_espanol' not in new_dataframe.columns or 'sdg' not in new_dataframe.columns:
            return JSONResponse(status_code=400, content={"message": "The required columns are missing from the uploaded data."})

        # Filtrar filas sin la columna 'sdg'
        new_dataframe = new_dataframe[new_dataframe['sdg'].notnull()]

        # Comprobar si hay datos después del filtrado
        if new_dataframe.empty:
            return JSONResponse(status_code=400, content={"message": "No valid data available for training."})

        # Leer el DataFrame existente
        existing_df = pd.read_excel("./data/ODScat_345.xlsx")

        # Combinar el nuevo DataFrame con el existente
        combined_df = pd.concat([existing_df, new_dataframe], ignore_index=True)

        # Ejecutar el pipeline con el DataFrame combinado
        pipeline(combined_df)

        return JSONResponse(status_code=200, content={"message": "Model retrained successfully!"})

    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file.", "error": str(e)})

@app.get('/report')
def getReport():

    answer = {
              'f1': pipeline2['model'].f1, 
              'precision': pipeline2['model'].precision, 
              'recall': pipeline2['model'].recall}
    
    return Response(content=json.dumps(answer), media_type='application/json', headers={'Access-Control-Allow-Origin': '*'})