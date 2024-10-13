import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class VectorizerPipe:

    def __init__(self, trainingMode = False):
        self.vectorizer = TfidfVectorizer()
        self.trainingMode = trainingMode
        self.vector = None
        self.data = None

    def getVectorWeights(self, data):
        vectorizer = TfidfVectorizer()
        vector = vectorizer.fit_transform(data['Textos_espanol'])
        vectorizer.get_feature_names_out()
        vect_score = np.asarray(vector.mean(axis=0)).ravel().tolist()
        vect_array = pd.DataFrame({'term': vectorizer.get_feature_names_out(), 'weight': vect_score})
        vect_array.sort_values(by='weight',ascending=False,inplace=True)
        return vect_array

    def setImpact(self, df):
        df3 = df[df['sdg'] == 3]
        df4 = df[df['sdg'] == 4]
        df5 = df[df['sdg'] == 5]

        self.impact3 = self.getVectorWeights(df3)
        self.impact4 = self.getVectorWeights(df4)
        self.impact5 = self.getVectorWeights(df5)
    
    def fit(self, data , target = None):
        self.setImpact(data)
        X =  self.vectorizer.fit_transform(data['Textos_espanol'])
        self.data = pd.DataFrame(X.todense())
        self.data['sdg'] = data['sdg']
        return self

    def transform(self, data):
        self.vector = self.vectorizer.transform(data['Textos_espanol'])
        transformed_data = pd.DataFrame(self.vector.todense(), columns=self.vectorizer.get_feature_names_out())
        if self.trainingMode:
            transformed_data['sdg'] = data['sdg'].values
        return transformed_data
        
    def predict(self, data):
        return self 
