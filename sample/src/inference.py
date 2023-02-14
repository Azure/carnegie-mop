import json
import pickle
from typing import List, Dict

import nltk



from mop_utils.base_model_wrapper import BaseModelWrapper, InferenceInput, InferenceOutput


# from base_model_wrapper import  BaseModelWrapper, InferenceInput, InferenceOutput

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
        self.tokenizer = pickle.load(open(model_root + '/tokenizer.pkl', 'rb'))

    def inference(self, item: Dict) -> Dict:
        features = self.tokenizer.transform([item.get('data')])
        score = self.model.predict_proba(features)[0][1]
        # score = 0.9
        return score

    def inference_batch(self, items: List[Dict]) -> List[Dict]:
        print(f'in inference batch, {items}')
        features = self.tokenizer.transform([x.get('data') for x in items])
        predicts = self.model.predict_proba(features)
        scores = [x[1] for x in predicts]
        return scores

    def convert_mop_input_to_model_input(self, mop_input: InferenceInput, **kwargs) -> Dict:
        return  {"data": mop_input.text}

    def convert_model_output_to_mop_output(self, customized_output: Dict, **kwargs) -> InferenceOutput:
        inference_output = InferenceOutput()
        inference_output.confidence_scores = {"identity_hate": customized_output}
        inference_output.predicted_labels = {"identity_hate": customized_output > 0.5}
        return inference_output


if __name__ == "__main__":
    model_wrapper = ModelWrapper()
    model_wrapper.init(model_root='../model')
    customized_input = {"data": "NIGGER PLEASE \n EAT A COCK, LOL HY."}
    c_output = model_wrapper.inference(customized_input)
    print(c_output)

    mop_input = InferenceInput(text="NIGGER PLEASE \n EAT A COCK, LOL HY.")
    customized_input = model_wrapper.convert_mop_input_to_customized_input(mop_input)
    print(customized_input)
    assert mop_input.text == json.loads(customized_input).get('data')

    mop_output = model_wrapper.convert_customized_output_to_mop_output(c_output)
    print(mop_output)

