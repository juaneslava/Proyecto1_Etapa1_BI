import pandas as pd
from sklearn.pipeline import Pipeline
from joblib import dump
from CleaningPipe import CleaningPipe
from VectorizerPipe import VectorizerPipe
from Model import Model


def pipeline(data):
    pipeline = Pipeline([
        ('cleaningPipe', CleaningPipe(trainingMode=True)),
        ('vectorizerPipe', VectorizerPipe(trainingMode=True)),
        ('model', Model())
    ])

    pipeline.fit(data)  
    
    dump(pipeline, './assets/pipeline.joblib', compress=True)

if __name__ == "__main__":
    print("[Pipeline] ¡Pipeline iniciado!")
    
    df = pd.read_excel("./data/ODScat_345.xlsx")
    
    pipeline(df)
    
    print("[Pipeline] ¡Pipeline finalizado!")
