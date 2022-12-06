import re
import pickle
import re
import string
from typing import List
import dill
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import json

from mop_utils import BaseModelWrapper, InferenceInput, InferenceOutput


class ModelWrapper(BaseModelWrapper):
    def __init__(self) -> None:
        super().__init__()
        self.model = None
        self.tokenizer = None

    def init(self, model_root: str) -> None:
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        print(model_root)
        self.model = pickle.load(open(model_root + '/xgboost.pkl', 'rb'))
        self.tokenizer = dill.load(open(model_root + '/tokenizer.dill', 'rb'))

    @staticmethod
    def __convert__inference_output(model_output):
        inference_output = InferenceOutput()
        inference_output.confidence_score = {"identity_hate": model_output}
        inference_output.predicted_labels = {"identity_hate": model_output > 0.5}
        return inference_output

    def inference(self, item: InferenceInput) -> InferenceOutput:
        print(item.text)
        features = self.tokenizer.transform([item.text])
        score = self.model.predict_proba(features)[0][1]
        return self.__convert__inference_output(score)

    def inference_batch(self, items: List[InferenceInput]) -> List[InferenceOutput]:
        print(items)
        features = self.tokenizer.transform([x.text for x in items])
        print(features)
        predicts = self.model.predict_proba(features)
        scores = [x[1] for x in predicts]
        print(scores)
        return [self.__convert__inference_output(x) for x in scores]


if __name__ == "__main__":
    model_wrapper = ModelWrapper()
    model_wrapper.init(model_root='../model')
    model_input = InferenceInput(text="NIGGER PLEASE \n EAT A COCK, LOL HY.")
    output = model_wrapper.inference(model_input)
    print(output)
