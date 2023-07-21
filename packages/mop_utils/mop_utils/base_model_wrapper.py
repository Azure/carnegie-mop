from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Union
from util import PredictedLabel, ConfidenceScore, AcsResponse, ImageAnalysisInput, TextAnalysisInput


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
    """this is a subclass to be compatible with old version"""


class MopInferenceOutput:
    """
    MopInferenceOutput: output example:
    {
        "predicted_labels": {
            "violence": {
                "severity-1": 1,
                "helloworld": 0,
                "severity-2": 0
            },
            "hate": {
                "severity-1": 0,
                "hello": 0,
                "severity-2": 1
            }
        },
        "confidence_scores": {
            "violence": {
                "severity-1": 0.525,
                "helloworld": 0,
                "severity-2": 0.5485
            },
            "hate": {
                "severity-1": 0.225,
                "hello": 0.225,
                "severity-2": 0.26544
            }
        }
    }
    """
    
    def __init__(self, output_dict: Optional[Dict] = None) -> None:
        """
        Initialize MopInferenceOutput
        @param output_dict: output dictionary.
        @type output_dict: Dictionary which have two key: predicted_labels and confidence_scores in it.
                           Refer to class output example as above.
        """
        self.__confidence_scores__ = dict()
        self.__predicted_labels__ = dict()
        if output_dict:
            self.from_dict(output_dict)
        # self._validate()

    def from_dict(self, output_dict: dict) -> Any:
        """
        Copy from other dict.
        @param output_dict: output dictionary.
        @type output_dict: Dictionary which have two key: predicted_labels and confidence_scores in it.
                           Refer to class output example as above.
        @return:
        @rtype:
        """
        predicted_labels: Dict[PredictedLabel] = output_dict["predicted_labels"]
        confidence_scores: Dict[ConfidenceScore] = output_dict["confidence_scores"]
        
        for k, v in predicted_labels.items():
            predict_label = PredictedLabel(k, v)
            self.__predicted_labels__[predict_label.label_name] = predict_label.label_values
        
        for k, v in confidence_scores.items():
            conf_score = ConfidenceScore(k, v)
            self.__confidence_scores__[conf_score.label_name] = conf_score.scores
        
        # self._validate()
        return self
    
    def _if_keys_match(self):
        """
        Check if label_name keys match score keys
        """
        if len(self.__predicted_labels__.keys()) != len(self.__confidence_scores__.keys()):
            return False
        
        if set(self.__predicted_labels__.keys()) != set(self.__confidence_scores__.keys()):
            return False
        
        return True
    
    def _if_value_keys_match(self):
        """
        Check if label_name value keys match score value keys
        """
        if not self.__predicted_labels__ and not self.__confidence_scores__:
            return True
        
        for key in self.__confidence_scores__.keys():
            conf_score = ConfidenceScore(key, self.__confidence_scores__[key])
            pre_label = PredictedLabel(key, self.__predicted_labels__.get(key, None))
            conf_keys = conf_score.scores.keys()
            pre_keys = pre_label.label_values.keys()
            if set(conf_keys) != set(pre_keys):
                return False
            
        return True
            
    def _validate(self):
        """
        Validate if label name, type, numbers and value within predicted_labels
        and confidence_scores match.
        @return:
        @rtype:
        """
        # taxonomy name should be match
        if not self._if_keys_match():
            raise ValueError(f"Predicted_labels labels number should equal to scores labels number: "
                             f"{self.__predicted_labels__.keys()}, {self.__confidence_scores__.keys()}")
        
        # labels should also be match
        if not self._if_value_keys_match():
            raise ValueError(f"Predicted_labels label values number should equal to scores label values number: "
                             f"{self.__confidence_scores__}, {self.__predicted_labels__}")
        
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
    Deprecated:
    this is a subclass to be compatible with old version
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
   
    # def convert_acs_input_to_model_input(self, acs_input: AcsResponse, **kwargs) -> Dict:
    #     pass
    #
    # def convert_model_output_to_acs_output(self, customized_output: Dict, **kwargs) -> AcsResponse:
    #     pass

    # TODO: consult Chenglong
    # optional
    def convert_acs_request_to_model_inference_input(self, req: Union[TextAnalysisInput, ImageAnalysisInput]) -> object:
        pass
    
    # optional
    def convert_model_inference_output_to_acs_response(self, out: object) -> AcsResponse:
        pass
