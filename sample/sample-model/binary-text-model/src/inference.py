import json
import base64
import pickle
from typing import List, Dict

import nltk
from mop_utils.base_model_wrapper import BaseModelWrapper, MopInferenceInput, MopInferenceOutput
from mop_utils.util import TextAnalysisInput, ImageAnalysisInput, AcsTextResponse, AcsImageResponse, AnalysisResult


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
    customized_input = {"data": "NIGGER PLEASE \n EAT A COCK, LOL HY."}
    c_output = model_wrapper.inference(customized_input)
    print(c_output)

    mop_input = MopInferenceInput(text="NIGGER PLEASE \n EAT A COCK, LOL HY.")
    customized_input = model_wrapper.convert_mop_input_to_model_input(mop_input)
    print(customized_input)
    assert mop_input.text == customized_input.get('data')

    mop_output = model_wrapper.convert_model_output_to_mop_output(c_output)
    print(mop_output)
    
    acs_txt_req = TextAnalysisInput()
    acs_txt_req.text = "NIGGER PLEASE \n EAT A COCK, LOL HY."
    model_input = model_wrapper.convert_acs_text_request_to_model_inference_input(acs_txt_req)
    print(model_input)
    
    model_inference_output = {
        "violence": {
            "scores": [
                0.9343945384025574,
                0.016118334606289865,
                0.024537162855267526,
                0.024950077757239343
            ],
            "class": 0
        },
        "self-harm": {
            "scores": [
                0.9265221357345581,
                0.02502666786313057,
                0.02527506835758686,
                0.02317621186375618
            ],
            "class": 0
        },
        "hate": {
            "scores": [
                0.1400328278541565,
                0.02049916982650757,
                0.024420715868473054,
                0.8150473237037659
            ],
            "class": 6
        },
        "sexual": {
            "scores": [
                0.882838249206543,
                0.02585785463452339,
                0.02786555513739586,
                0.06343831121921539
            ],
            "class": 0
        }
    }
    
    acs_text_response = model_wrapper.convert_model_inference_output_to_acs_text_response(model_inference_output)
    print(acs_text_response.hate.harmful_score, acs_text_response.hate.severity_level,
          acs_text_response.sexual.harmful_score, acs_text_response.sexual.severity_level,
          acs_text_response.self_harm.harmful_score, acs_text_response.self_harm.severity_level,
          acs_text_response.violence.harmful_score, acs_text_response.violence.severity_level)

    acs_image_req = ImageAnalysisInput()
    image_data = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC'
    decoded_data = base64.b64decode(image_data)

    print(decoded_data)
    acs_image_req.data = decoded_data
    model_input = model_wrapper.convert_acs_image_request_to_model_inference_input(acs_image_req)
    assert image_data == model_input["data"]
    
    acs_image_response = model_wrapper.convert_model_inference_output_to_acs_image_response(model_inference_output)
    print(acs_image_response.hate.harmful_score, acs_image_response.hate.severity_level,
          acs_image_response.sexual.harmful_score, acs_image_response.sexual.severity_level,
          acs_image_response.self_harm.harmful_score, acs_image_response.self_harm.severity_level,
          acs_image_response.violence.harmful_score, acs_image_response.violence.severity_level)
    
    