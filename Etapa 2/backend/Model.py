import pandas as pd
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from pydantic import BaseModel

class DataModel(BaseModel):
    Textos_espanol: str

    def columns(self):
        return ['Textos_espanol']

class Model():
    def __init__(self):
        self.model = SGDClassifier(alpha=0.001, loss='log_loss', penalty='l2', max_iter=1000, tol=0.001)
        self.precision = None
        self.recall = None
        self.report = None
        self.f1 = None
    
    def fit(self, data, target=None):
        """Entrena el modelo con un conjunto de datos."""
        Y = data['sdg']
        X = data.drop(['sdg'], axis=1)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        self.model.fit(X_train, Y_train)
        self.evaluate(Y_test, X_test)
        return self

    def partial_fit(self, data):
        """Actualiza el modelo con un nuevo conjunto de datos usando partial_fit."""
        Y = data['sdg']
        X = data.drop(['sdg'], axis=1)

        # Si es la primera vez que se llama, inicializa el modelo con las clases.
        if self.model.classes_.size == 0:
            self.model.partial_fit(X, Y, classes=[3, 4, 5])  # Especifica las clases disponibles.
        else:
            self.model.partial_fit(X, Y)  # Actualiza el modelo con los nuevos datos.


    def evaluate(self, Y_test, X_test):
        """Evalúa el modelo y calcula las métricas de rendimiento."""
        Y_test_predict = self.model.predict(X_test)
        self.report = classification_report(Y_test, Y_test_predict)
        self.f1 = f1_score(Y_test, Y_test_predict, average='weighted')
        self.recall = recall_score(Y_test, Y_test_predict, average='weighted')
        self.precision = precision_score(Y_test, Y_test_predict, average='weighted')

    def transform(self, data):
        """Transforma los datos, puedes implementar lógica adicional si es necesario."""
        return data
    
    def predict(self, data):
        """Realiza predicciones sobre nuevos datos."""
        labels = self.model.predict(data)
        probabilities = self.model.predict_proba(data)
        prediction = pd.DataFrame(labels, columns=['label'])
        for i in range(probabilities.shape[1]):
            prediction[f'prob_class_{i}'] = probabilities[:, i]
        return prediction
