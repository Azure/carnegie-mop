import pickle
from typing import List, Dict

import nltk
from mop_utils.base_model_wrapper import BaseModelWrapper, MopInferenceInput, MopInferenceOutput
from mop_utils.util import TextAnalysisInput, AcsTextResponse, AnalysisResult


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
        """
        Model Inference
        @param item: A dictionary which have a key named 'data'.
        @type item: Dictionary
        @return: Inference score.
        @rtype: Dictionary
        """
        return self.mock_inference(item)
    
    def mock_inference(self, item: Dict) -> Dict:
        """
        It's a mock inference function: write your own inference logic.
        @param item: A dictionary which have a key named 'data'.
        @type item: Dictionary
        @return: Inference score.
        @rtype: Dictionary
        """
        features = self.tokenizer.transform([item.get('data')])
        score = self.model.predict_proba(features)[0][1]
        return {'score': score}

    def inference_batch(self, items: List[Dict]) -> List[Dict]:
        print(f'in inference batch, {items}')
        features = self.tokenizer.transform([x.get('data') for x in items])
        predicts = self.model.predict_proba(features)
        scores = [{'score': x[1]} for x in predicts]
        return scores

    def convert_mop_input_to_model_input(self, mop_input: MopInferenceInput, **kwargs) -> Dict:
        return {"data": mop_input.text}

    def convert_model_output_to_mop_output(self, customized_output: Dict, **kwargs) -> MopInferenceOutput:
        """
        Example function to convert model output to mop-utils output. Write your own logic.
        @param customized_output : Your model inference output. It's a dictionary.
        @type customized_output: A dictionary.
        @param kwargs : Other necessary keyword parameters.
        @return: Mop-utils inference output
        @rtype: MopInferenceOutput
         """
        
        probability = float(customized_output.get('score'))
        print(f'model probability: {probability}')
        positive = 1 if probability > 0.5 else 0
        d = {
            "confidence_scores": {
                "identity_hate": {
                    "positive": positive,
                    "negative": 1 - positive
                }
            },
            "predicted_labels": {
                "identity_hate": {
                    "positive": 1,
                    "negative": 0
                }
            }
        }
        mop_inference_output = MopInferenceOutput(d)
        return mop_inference_output

    def convert_acs_text_request_to_model_inference_input(self, req: TextAnalysisInput) -> object:
        """
        Optional implementation: Convert ACS text request to model inference input.
        But it is mandatory if you want to release the model to AACS service.
        @param req: ACS text request
        @type req: TextAnalysisInput
        @return: Model inference input
        @rtype: object
        """
        return {"data": req.text}

    def convert_model_inference_output_to_acs_text_response(self, out: object) -> AcsTextResponse:
        """
        Optional implementation: Convert model inference output to ACS text response.
        But it is mandatory if you want to release the model to AACS service.
        @param out: Model inference output
        @type out: object
        @return: ACS text response
        @rtype: AcsTextResponse
        """
      
        score = out["score"]
        analysis_result = AnalysisResult()
        analysis_result.harmful_score = score
        analysis_result.severity_level = int(score * 7)
        
        acs_text_resp = AcsTextResponse()
        acs_text_resp.violence = analysis_result
        acs_text_resp.self_harm = analysis_result
        acs_text_resp.hate = analysis_result
        acs_text_resp.sexual = analysis_result
        
        return acs_text_resp


if __name__ == "__main__":
    model_wrapper = ModelWrapper()
    model_wrapper.init(model_root='../model')

    mop_util_input = MopInferenceInput(text="NIGGER PLEASE \n EAT A COCK, LOL HY.")
    model_input = model_wrapper.convert_mop_input_to_model_input(mop_util_input)
    print(model_input)
    assert mop_util_input.text == model_input.get('data')

    model_output = model_wrapper.inference(model_input)
    print(model_output)
    
    mop_output = model_wrapper.convert_model_output_to_mop_output(model_output)
    print(mop_output)
    
    acs_txt_req = TextAnalysisInput()
    acs_txt_req.text = "NIGGER PLEASE \n EAT A COCK, LOL HY."
    model_input = model_wrapper.convert_acs_text_request_to_model_inference_input(acs_txt_req)
    print(model_input)
    
    acs_text_response = model_wrapper.convert_model_inference_output_to_acs_text_response(model_output)
    print(acs_text_response.hate.harmful_score, acs_text_response.hate.severity_level,
          acs_text_response.sexual.harmful_score, acs_text_response.sexual.severity_level,
          acs_text_response.self_harm.harmful_score, acs_text_response.self_harm.severity_level,
          acs_text_response.violence.harmful_score, acs_text_response.violence.severity_level)
    
