from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from langdetect import detect, DetectorFactory
import string


class CleaningPipe:

    def __init__(self, trainingMode = False):
        self.translateTable = str.maketrans(' ', ' ', string.punctuation)
        self.stopwords = set(stopwords.words('spanish'))
        self.lemmatizer = WordNetLemmatizer()
        self.trainingMode = trainingMode
        DetectorFactory.seed = 42
        self.df = None
    
    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return None

    def fix_codification(self, text:str):
        utf8_to_ansi = {"Ã": "Á","Ã¡": "á","Ã‰": "É","Ã©": "é","Ã": "Í","Ã­": "í","Ã“": "Ó",
                        "Ã³": "ó","Ãš": "Ú","Ãº": "ú","Ã‘": "Ñ","Ã±": "ñ","Â¿": "¿"}
        for utf8, ansi in utf8_to_ansi.items():
            text = text.replace(utf8, ansi)
        return text
    
    def to_lowercase(self, text:str):
        return text.lower()
    
    def replace_accents(self, text:str):
        accents = {'á': 'a','é': 'e','í': 'i','ó': 'o','ú': 'u'}
        for accented, unaccented in accents.items():
            text = text.replace(accented, unaccented)
        return text
    
    def remove_characters(self, text:str):
        return text.translate(self.translateTable)
    
    def remove_stopwords(self, text:str):
        return [word.strip() for word in text.split(' ') if word not in self.stopwords and len(word) > 2]

    def remove_no_alphabetics(self, words:list[str]):
        return [word for word in words if word.isalpha()]
    
    def lemmatize(self, words:list[str]):
        lemas = []
        for word in words:
            if len(word) > 4:
                lemas.append(self.lemmatizer.lemmatize(word, pos = 'v'))
            else:
                lemas.append(word)
        return lemas

    def remove_routes(self, words:list[str]):
        return [word for word in words if (('http' not in word) and ('https' not in word) and  ('www' not in word))]
    
    def preprocessing(self, text:str):
        text = self.fix_codification(text)
        text = self.to_lowercase(text)
        text = self.replace_accents(text)
        text = self.remove_characters(text)
        words = self.remove_stopwords(text)
        words = self.remove_no_alphabetics(words)
        words = self.lemmatize(words)
        words = self.remove_routes(words)
        return ' '.join(words)
    
    def fit(self, data, target=None):
        self.df = data
        if self.trainingMode:
            self.df['Language'] = self.df['Textos_espanol'].apply(self.detect_language)
        self.df['Textos_espanol'] = data['Textos_espanol'].apply(self.preprocessing)
        if self.trainingMode:
            self.df = self.df[self.df['Language']=='es']
            self.df = self.df.drop(['Language'], axis = 1)
        return self
    
    def transform(self, data):
        del self.df
        self.df = data
        self.df['Textos_espanol'] = data['Textos_espanol'].apply(self.preprocessing)
        if self.trainingMode:
            self.df = self.df[self.df['Language']=='es']
            self.df = self.df.drop(['Language'], axis = 1)
        print('[CleaningTrain] Transformation Finished!!')
        return self.df
    
    def predict(self, data):
        return self
