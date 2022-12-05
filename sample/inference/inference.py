import re
import pickle
import re
import string
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import json

from mop_utils import BaseModelWrapper, InferenceInput, InferenceOutput


def tokenize(text):
    '''
    Tokenize text and return a non-unique list of tokenized words found in the text. 
    Normalize to lowercase, strip punctuation, remove stop words, filter non-ascii characters.
    Lemmatize the words and lastly drop words of length < 3.
    '''
    text = text.lower()
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)
    words = nopunct.split(' ')
    # remove any non ascii
    words = [word.encode('ascii', 'ignore').decode('ascii') for word in words]
    lmtzr = WordNetLemmatizer()
    words = [lmtzr.lemmatize(w) for w in words]
    words = [w for w in words if len(w) > 2]
    return words

class ModelWrapper(BaseModelWrapper):
    def __init__(self) -> None:
        self.model = None
        self.tokenizer = None

    def init(self, model_root:str) -> None:
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        model = pickle.load(open(model_root + '/xgboost.pkl', 'rb'))
        tokenizer = pickle.load(open(model_root + '/tokenizer.pkl', 'rb'))

    
    def inference(self, item: InferenceInput)->InferenceOutput:
         features =self.tokenizer.transform([item.text])
         score = self.model.predict_proba(features)[0][1]
         inference_output = InferenceOutput()
         inference_output.confidence_score = {"identity_hate": score}
         inference_output.predicted_labels = {"identity_hate": score > 0.5}   
         return inference_output

if __name__ == "__main__":
    model_wrapper = ModelWrapper()
    model_wrapper.init(model_root='./model')
    inference_input = InferenceInput()
    inference_input.text = "NIGGER PLEASE \n EAT A COCK, LOL HY."
    inference_output = model_wrapper.inference(inference_input)
    print(inference_output)