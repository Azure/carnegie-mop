from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from .util import AcsTextResponse, AcsImageResponse, ImageAnalysisInput, TextAnalysisInput, MopInferenceOutputValidator


class MopInferenceInput:
    def __init__(self, text: Optional[str] = None, image: Optional[str] = None,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 images: Optional[List] = None) -> None:
        self.__text__ = text
        self.__image__ = image
        self.__width__ = width
        self.__height__ = height
        self.__images__ = images

    def from_dict(self, input_dict: Dict) -> Any:
        self.__text__ = input_dict.get('text', None)
        self.__image__ = input_dict.get('image', None)
        self.__width__ = input_dict.get('width', None)
        self.__height__ = input_dict.get('height', None)
        self.__images__ = input_dict.get('images', None)
        if self.__text__ is None and self.__image__ is None and self.__images__ is None:
            raise ValueError('Either text or image must be provided')
        return self

    def __str__(self) -> str:
        return str(vars(self))

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def text(self) -> str:
        return self.__text__

    @text.setter
    def text(self, text: str) -> None:
        self.__text__ = text

    @property
    def image(self) -> str:
        return self.__image__

    @image.setter
    def image(self, image: str) -> None:
        self.__image__ = image

    @property
    def width(self) -> int:
        return self.__width__

    @width.setter
    def width(self, width: int) -> None:
        self.__width__ = width

    @property
    def height(self) -> int:
        return self.__height__

    @height.setter
    def height(self, height: int) -> None:
        self.__height__ = height

    @property
    def images(self) -> str:
        return self.__images__

    @images.setter
    def images(self, images: str) -> None:
        self.__images__ = images


class MopInferenceOutput:
    """
    MopInferenceOutput: output example:
    
    The key name below for taxonomy 'violence' and 'hate', for example 'severity-1', 'severity-2', 'severity-3'
    or 'sev-1', 'sev-2', 'sev-3' is just for example, please write your own key names relevant to your model,
    the key names are variable by your model.
    
    The key value below for taxonomy 'violence' and 'hate', for example value for key 'severity-1' is just for sample,
    its value will be updated by your model.
    
    Please make sure the key names for taxonomy 'violence' and 'hate', for example 'severity-1', 'severity-2',
    'severity-3', 'sev-1', 'sev-2', 'sev-3' must be both appear in 'predicted_labels' and 'confidence_scores' and
    its key name is same.
    
    1, For categorical task:
    Value 1 only appears once in predicted_labels,  and its key name should both appear in model label and task label.
    
    For example:
    
    {
        "predicted_labels": {
            "violence": {
                "severity-1": 0,
                "severity-2": 0,
                "severity-3": 1
            },
            "hate": {
                "sev-1": 0,
                "sev-2": 0,
                "sev-3": 1
            }
        },
        "confidence_scores": {
            "violence": {
                "severity-1": 0.525,
                "severity-2": 0,
                "severity-3": 0.5485
            },
            "hate": {
                "sev-1": 0.225,
                "sev-2": 0.225,
                "sev-3": 0.26544
            }
        }
    }
    
    2, For ordinal task:
    Value 1 must in model predicted_labels, and if 1 appears in model response predicted_labels,
    then all other values after this 1 will be also 1.
    
    For example:
    
    {
        "predicted_labels": {
            "violence": {
                "severity-1": 1,
                "severity-2": 1,
                "severity-3": 1
            },
            "hate": {
                "sev-1": 1,
                "sev-2": 1,
                "sev-3": 1
            }
        },
        "confidence_scores": {
            "violence": {
                "severity-1": 0.525,
                "severity-2": 0,
                "severity-3": 0.5485
            },
            "hate": {
                "sev-1": 0.225,
                "sev-2": 0.225,
                "sev-3": 0.26544
            }
        }
    }
    """
    
    def __init__(self, raw_data_dict: dict) -> None:
        """
        Initialize MopInferenceOutput.
        @param raw_data_dict: raw data dictionary.
        @type raw_data_dict: A dictionary which have two keys: "predicted_labels" and "confidence_scores".
                           Refer the class output example above.
        """
        self.predicted_labels = raw_data_dict.get("predicted_labels", None)
        self.confidence_scores = raw_data_dict.get("confidence_scores", None)
        if not self.__predicted_labels__ or not self.__confidence_scores__:
            raise ValueError(f"MopInferenceOutput: invalid raw data dict: Current value: {raw_data_dict}")

        MopInferenceOutputValidator(self).validate()

    def from_dict(self, raw_data_dict: dict) -> Any:
        """
        Deprecated: This method will be deprecated.
        """
        self.__confidence_scores__ = raw_data_dict['confidence_scores']
        self.__predicted_labels__ = raw_data_dict['predicted_labels']
        MopInferenceOutputValidator(self).validate()
        return self
    
    def __str__(self) -> str:
        return str(vars(self))

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def confidence_scores(self) -> Dict:
        return self.__confidence_scores__

    @confidence_scores.setter
    def confidence_scores(self, confidence_scores: Dict) -> None:
        self.__confidence_scores__ = confidence_scores

    @property
    def predicted_labels(self) -> Dict:
        return self.__predicted_labels__

    @predicted_labels.setter
    def predicted_labels(self, predicted_labels: Dict) -> None:
        self.__predicted_labels__ = predicted_labels

    @property
    def output(self) -> Dict:
        return {'confidence_scores': self.confidence_scores, 'predicted_labels': self.predicted_labels}


class BaseModelWrapper(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def init(self, model_root: str, **kwargs):
        raise NotImplementedError("init() method is not implemented")

    @abstractmethod
    def inference(self, item: Dict, **kwargs) -> Dict:
        raise NotImplementedError("inference() method is not implemented")

    @abstractmethod
    def inference_batch(self, item: List[Dict], **kwargs) -> List[Dict]:
        raise NotImplementedError("inference_batch() method is not implemented")

    @abstractmethod
    def convert_mop_input_to_model_input(self, mop_input: MopInferenceInput, **kwargs) -> Dict:
        raise NotImplementedError("convert_mop_input_to_model_input() method is not implemented")

    @abstractmethod
    def convert_model_output_to_mop_output(self, customized_output: Dict, **kwargs) -> MopInferenceOutput:
        raise NotImplementedError("convert_model_output_to_mop_output() method is not implemented")
   
    def convert_acs_text_request_to_model_inference_input(self, req: TextAnalysisInput) -> object:
        """
        Optional implementation: Convert ACS text request to model inference input.
        But it is mandatory if you want to release the model to AACS service.
        @param req: ACS text request
        @type req: TextAnalysisInput
        @return: Model inference input
        @rtype: object
        """
        pass

    def convert_model_inference_output_to_acs_text_response(self, out: object) -> AcsTextResponse:
        """
        Optional implementation: Convert model inference output to ACS text response.
        But it is mandatory if you want to release the model to AACS service.
        @param out: Model inference output
        @type out: object
        @return: ACS text response
        @rtype: AcsTextResponse
        """
        pass
    
    def convert_acs_image_request_to_model_inference_input(self, req: ImageAnalysisInput) -> object:
        """
        Optional implementation: Convert ACS image request to model inference input.
        But it is mandatory if you want to release the model to AACS service.
        @param req: ACS image request
        @type req: ImageAnalysisInput
        @return: Model inference input
        @rtype: object
        """
        pass
    
    def convert_model_inference_output_to_acs_image_response(self, out: object) -> AcsImageResponse:
        """
        Optional implementation: Convert model inference output to ACS image response.
        But it is mandatory if you want to release the model to AACS service.
        @param out: Model inference output
        @type out: object
        @return: ACS image response
        @rtype: AcsImageResponse
        """
        pass
 