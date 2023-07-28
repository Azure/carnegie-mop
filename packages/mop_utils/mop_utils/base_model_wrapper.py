from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from util import AcsTextResponse, AcsImageResponse, ImageAnalysisInput, TextAnalysisInput, MopInferenceOutputValidator


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


class InferenceInput(MopInferenceInput):
    """
    Deprecated: This version will be deprecated.
    this is a subclass to be compatible with old version.
    """


class MopInferenceOutput:
    """
    MopInferenceOutput: output example:
    {
        "predicted_labels": {
            "violence": {
                "severity-1": 1,
                "severity-2": 0,
                "severity-3": 0
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
    """
    
    def __init__(self, output_dict: dict) -> None:
        """
        Initialize MopInferenceOutput.
        @param output_dict: output dictionary.
        @type output_dict: Dictionary which have two key: predicted_labels and confidence_scores in it.
                           Refer to class output example as above.
        """
        self.predicted_labels = output_dict.get("predicted_labels", None)
        self.confidence_scores = output_dict.get("confidence_scores", None)
        if not self.__predicted_labels__ or not self.__confidence_scores__:
            raise ValueError(f"MopInferenceOutput from_dict: invalid output_dict: {output_dict}")

        MopInferenceOutputValidator(self).validate()

    def from_dict(self, output_dict: dict) -> Any:
        """
        Deprecated: This version will be deprecated.
        """
        self.__confidence_scores__ = output_dict['confidence_scores']
        self.__predicted_labels__ = output_dict['predicted_labels']
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


class InferenceOutput(MopInferenceOutput):
    """
    Deprecated: This version will be deprecated.
    this is a subclass to be compatible with old version.
    """


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
        It is mandatory if you want to release the model to AACS service.
        @param req: ACS text request
        @type req: TextAnalysisInput
        @return: Model inference input
        @rtype: object
        """
        pass

    def convert_model_inference_output_to_acs_text_response(self, out: object) -> AcsTextResponse:
        """
        Optional implementation: Convert model inference output to ACS text response.
        It is mandatory if you want to release the model to AACS service.
        @param out: Model inference output
        @type out: object
        @return: ACS text response
        @rtype: AcsTextResponse
        """
        pass
    
    def convert_acs_image_request_to_model_inference_input(self, req: ImageAnalysisInput) -> object:
        """
        Optional implementation: Convert ACS image request to model inference input.
        It is mandatory if you want to release the model to AACS service.
        @param req: ACS image request
        @type req: ImageAnalysisInput
        @return: Model inference input
        @rtype: object
        """
        pass
    
    def convert_model_inference_output_to_acs_image_response(self, out: object) -> AcsImageResponse:
        """
        Optional implementation: Convert model inference output to ACS image response.
        It is mandatory if you want to release the model to AACS service.
        @param out: Model inference output
        @type out: object
        @return: ACS image response
        @rtype: AcsImageResponse
        """
        pass
 