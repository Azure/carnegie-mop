import base64
import io
import pickle
from typing import List, Dict
from PIL import Image

import nltk
from mop_utils.base_model_wrapper import BaseModelWrapper, MopInferenceInput, MopInferenceOutput
from mop_utils.util import AcsImageResponse, ImageAnalysisInput


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
       It's a mock inference function: use your own inference logic.
       @param item: A dictionary which have a key named 'data'.
       @type item: Dictionary
       @return: Inference score.
       @rtype: Dictionary
       """

        base64_string: str = item["data"]
        if base64_string.startswith("data:image"):
            base64_string = base64_string.split(",", 1)[1]

        image_data = base64.b64decode(base64_string)
        image_stream = io.BytesIO(image_data)

        image = Image.open(image_stream)
        width, height = image.size

        image_format = image.format
        return {"width": width, "height": height, "format": image_format}
        
    def inference(self, item: Dict) -> Dict:
        """
        Model Inference
        @param item: A dictionary which have a key named 'data'.
        @type item: Dictionary
        @return: Inference score.
        @rtype: Dictionary
        """
        return self.mock_inference(item)
    
    def inference_batch(self, items: List[Dict]) -> List[Dict]:
        return [self.inference(i) for i in items]
    
    def convert_mop_input_to_model_input(self, mop_input: MopInferenceInput, **kwargs) -> Dict:
        image_base64 = mop_input.image
        return {"data": image_base64}
    
    def convert_model_output_to_mop_output(self, customized_output: Dict, **kwargs) -> MopInferenceOutput:
        """
        Example function to convert model output to mop-utils output.
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
        
        confidence_scores = dict()
        predicted_labels = dict()
        
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
    
    def convert_acs_image_request_to_model_inference_input(self, req: ImageAnalysisInput) -> object:
        """
        Optional implementation: Convert ACS image request to model inference input.
        But it is mandatory if you want to release the model to AACS service.
        @param req: ACS image request
        @type req: ImageAnalysisInput
        @return: Model inference input
        @rtype: object
        """
        encoded_data = base64.b64encode(req.data)
        encoded_string = encoded_data.decode('utf-8')
        return {"data": encoded_string}
    
    def convert_model_inference_output_to_acs_image_response(self, out: object) -> AcsImageResponse:
        """
        Optional implementation: Convert model inference output to ACS image response.
        But it is mandatory if you want to release the model to AACS service.
        @param out: Model inference output
        @type out: object
        @return: ACS image response
        @rtype: AcsImageResponse
        """
        width = out["width"]
        height = out["height"]
        image_format = out["format"]
        
        score = 1 if width / (width + height) > 0.4 else 0
        
        acs_image_resp = AcsImageResponse()
        acs_image_resp.violence.harmful_score = score
        acs_image_resp.violence.severity_level = int(score * 7)
        
        acs_image_resp.self_harm.harmful_score = score
        acs_image_resp.self_harm.severity_level = int(score * 7)
        
        acs_image_resp.hate.harmful_score = score
        acs_image_resp.hate.severity_level = int(score * 7)
        
        acs_image_resp.sexual.harmful_score = score
        acs_image_resp.sexual.severity_level = int(score * 7)
        return acs_image_resp


if __name__ == "__main__":
    model_wrapper = ModelWrapper()
    model_wrapper.init(model_root='../model')
    
    base64_str = "iVBORw0KGgoAAAANSUhEUgAAABcAAAANCAIAAADNBWIKAAAAGklEQVR4nGNkYPjPQDFgotyIUVNGTRnxpgAAuWYBGVUzBh4AAAAASUVORK5CYII="
    mop_util_input = MopInferenceInput(image=base64_str)
    model_input = model_wrapper.convert_mop_input_to_model_input(mop_util_input)
    print(model_input)
    assert mop_util_input.image == model_input.get('data')
    
    model_output = model_wrapper.inference(model_input)
    print(model_output)
    
    mop_output = model_wrapper.convert_model_output_to_mop_output(model_output)
    print(mop_output)
    
    acs_image_req = ImageAnalysisInput()
    decoded_data = base64.b64decode(base64_str)
    print(decoded_data)
    acs_image_req.data = decoded_data
    model_input = model_wrapper.convert_acs_image_request_to_model_inference_input(acs_image_req)
    assert base64_str == model_input["data"]
    
    acs_model_output = model_wrapper.inference(model_input)
    acs_image_response = model_wrapper.convert_model_inference_output_to_acs_image_response(acs_model_output)
    print(acs_image_response.hate.harmful_score, acs_image_response.hate.severity_level,
          acs_image_response.sexual.harmful_score, acs_image_response.sexual.severity_level,
          acs_image_response.self_harm.harmful_score, acs_image_response.self_harm.severity_level,
          acs_image_response.violence.harmful_score, acs_image_response.violence.severity_level)
