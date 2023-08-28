import base64
import io
import pickle
from typing import List, Dict
from PIL import Image
import random

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
    
    def mock_inference(self, item: Dict) -> Dict:
        """
         It's a mock inference function: write your own inference logic.
         @param item: A dictionary which have a key named 'images'.
         @type item: Dictionary
         @return: Inference score.
         @rtype: Dictionary
        """
        
        images = item["images"]
        text: str = item["text"]
        length = len(images)
        for i in range(0, length):
            rep_str = '##{image_%d}' % i
            text = text.replace(rep_str, images[i])
    
        img_idx = random.randint(0, length - 1)
        image_data = base64.b64decode(images[img_idx])
        image_stream = io.BytesIO(image_data)
    
        image = Image.open(image_stream)
        width, height = image.size
        image_format = image.format
    
        return {"width": width, "height": height, "format": image_format}
    
    def inference(self, item: Dict) -> Dict:
        """
        Model Inference
        @param item: A dictionary which have a key named 'images'.
        @type item: Dictionary
        @return: Inference score.
        @rtype: Dictionary
        """
        return self.mock_inference(item)
    
    def inference_batch(self, items: List[Dict]) -> List[Dict]:
        return [self.inference(i) for i in items]
    
    def convert_mop_input_to_model_input(self, mop_input: MopInferenceInput, **kwargs) -> Dict:
        images = mop_input.images
        text = mop_input.text
        return {"images": images, "text": text}
    
    def convert_model_output_to_mop_output(self, customized_output: Dict, **kwargs) -> MopInferenceOutput:
        """
         Example function to convert model output to mop-utils output. Write your own logic.
         Parameters
         ----------
         customized_output : your model inference output. It's a dictionary.
         kwargs : other keyword parameters may use by mop-utils

         Returns
         -------
         MopInferenceOutput: mop-utils inference output.
         """
        
        width = customized_output["width"]
        height = customized_output["height"]
        image_format = customized_output["format"]
        
        confidence_scores = dict()
        predicted_labels = dict()
        
        value = width / (width + height)
        score = 1 if width / (width + height) > 0.4 else 0
        score_2 = 0 if score == 1 else 1
        
        predicted_label = {
            "severity_0": score,
            "severity_2": score_2,
            "severity_4": score,
            "severity_6": score_2
        }
        
        confidence_score = {
            "severity_0": value,
            "severity_2": 1 - value,
            "severity_4": value,
            "severity_6": 1 - value
        }
        
        predicted_labels["hate"] = predicted_label
        confidence_scores["hate"] = confidence_score
        
        predicted_labels["sexual"] = predicted_label
        confidence_scores["sexual"] = confidence_score
        
        predicted_labels["violence"] = predicted_label
        confidence_scores["violence"] = confidence_score
        
        predicted_labels["self_harm"] = predicted_label
        confidence_scores["self_harm"] = confidence_score
        
        d = {
            "predicted_labels": predicted_labels,
            "confidence_scores": confidence_scores
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
    
    image_text_input = {
        "text": "This is my test data. Counter It was 7 minutes after midnight. The dog was lying on the grass in the middle of the lawn in front of Mrs Shears’ house. Its eyes were closed. It looked as if it was running on its side, the way dogs run when they think they are chasing a cat in a dream. ##{image_0}\nBut the dog was not running or asleep. The dog was dead. There was a garden fork sticking out of the dog. The points of the fork must have gone all the way through the dog and into the ground because the fork had not fallen over. I decided that the dog was probably killed with the fork because I could not see any other wounds in the dog and I do not think you would stick a garden fork into a dog after it had died for some other reason, like cancer for example, or a road accident. But I could not be certain about this. ##{image_1}\n",
        "images": [
            "iVBORw0KGgoAAAANSUhEUgAAABcAAAAhCAIAAAC9a6dHAAAAJ0lEQVR4nGNkYPjPQDFgotyIUVNGTRk1ZdSUUVNGTRk1ZdQUupoCAC1fAUFdU7NOAAAAAElFTkSuQmCC",
            "iVBORw0KGgoAAAANSUhEUgAAABcAAAANCAIAAADNBWIKAAAAGklEQVR4nGNkYPjPQDFgotyIUVNGTRnxpgAAuWYBGVUzBh4AAAAASUVORK5CYII="
        ]
    }
    
    mop_util_input = MopInferenceInput(text=image_text_input["text"], images=image_text_input["images"])
    model_input = model_wrapper.convert_mop_input_to_model_input(mop_util_input)
    print(model_input)
    
    model_output = model_wrapper.inference(model_input)
    print(model_output)
    
    mop_output = model_wrapper.convert_model_output_to_mop_output(model_output)
    print(mop_output.output)
