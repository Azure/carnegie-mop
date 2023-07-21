from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Union


class PredictedLabel:
    """
    Predict label: for example:
      "label_example": {
            "example-1": 1,
            "example-2": 0,
            "example-3": 0
      }
    """

    def __init__(self, label: str, label_values: Dict[str, int]):
        self.label = label
        self.label_values = label_values
        self.validate()
    
    def get_name(self):
        return self.label
    
    def get_label_values(self):
        return self.label_values
        
    def validate(self):
        if not self.label or not isinstance(self.label, str):
            raise TypeError(f"Label name must be type str and value must not empty. {self.label}")
    
        if not self.label_values or not isinstance(self.label_values, dict):
            raise TypeError(f"Label scores must be dict. {self.label_values}")
        
        for k, v in self.label_values.items():
            if not k or not isinstance(k, str):
                raise TypeError(f"Key of label value paris should be str and not empty: {k}")
            
            if v is None or not isinstance(v, int):
                raise TypeError(f"Value of label value pairs should be int: {k}, {v}, {type(v)}")
            
        number = len(self.get_value_keys())
        if 0 == number:
            raise ValueError(f"There must be at least one label in value pairs: {number}")
        
    def get_value_keys(self):
        return self.label_values.keys()
    
    
class ConfidenceScore:
    """
    Confidence score: for example:
        "label_example": {
            "example-1": 0.3,
            "example-2": 0,
            "example-3": 0.2
        }
    """
    
    def __init__(self, label_name: str, confidence_scores: Dict[str, Union[float, int]]):
        self.label: str = label_name
        self.scores: Dict[str, Union[float, int]] = confidence_scores
        self.validate()
        
    def get_label_name(self):
        return self.label
    
    def get_confidence_scores(self):
        return self.scores
    
    def validate(self):
        if not self.label or not isinstance(self.label, str):
            raise TypeError(f"Label name must be str and not empty: {self.label}")
        
        if not self.scores or not isinstance(self.scores, dict):
            raise TypeError(f"Confidence scores must be dict and may not empty: {self.scores}")
        
        for k, v in self.scores.items():
            if not k or not isinstance(k, str):
                raise TypeError(f"Confidence score key name must be str and not empty: {k}")
            
            if v is None or not isinstance(v, (float, int)):
                raise TypeError(f"Confidence score value must be float or int and not empty: {k}, {v}, {type(v)}")

        if 0 >= len(self.get_confidence_scores_keys()):
            raise ValueError(f"There must be at least one key in confidence score: {self.scores}")
        
    def get_confidence_scores_keys(self):
        return self.scores.keys()
    
    
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
    def __init__(self, confidence_scores: Optional[Dict] = None, predicted_labels: Optional[Dict] = None) -> None:
        self.__confidence_scores__ = dict()
        self.__predicted_labels__ = dict()
        if confidence_scores:
            for k, v in confidence_scores.items():
                conf_score = ConfidenceScore(k, v)
                self.__confidence_scores__[conf_score.get_label_name()] = conf_score.get_confidence_scores()

        if predicted_labels:
            for k, v in predicted_labels.items():
                pre_label = PredictedLabel(k, v)
                self.__predicted_labels__[pre_label.get_name()] = pre_label.get_label_values()
                
        self.validate()

    def from_dict(self, output_dict: dict) -> Any:
        predicted_labels: Dict[PredictedLabel] = output_dict["predicted_labels"]
        confidence_scores: Dict[ConfidenceScore] = output_dict["confidence_scores"]
        
        for k, v in predicted_labels.items():
            predict_label = PredictedLabel(k, v)
            self.__predicted_labels__[predict_label.get_name()] = predict_label.get_label_values()
        
        for k, v in confidence_scores.items():
            conf_score = ConfidenceScore(k, v)
            self.__confidence_scores__[conf_score.get_label_name()] = conf_score.get_confidence_scores()
        
        self.validate()
        return self
    
    def predicted_labels_keys(self):
        return self.__predicted_labels__.keys()
    
    def confidence_scores_keys(self):
        return self.__confidence_scores__.keys()
    
    def if_keys_match(self):
        """
        if label keys match score keys
        """
        if len(self.predicted_labels_keys()) != len(self.confidence_scores_keys()):
            return False
        
        if set(self.predicted_labels_keys()) != set(self.confidence_scores_keys()):
            return False
        
        return True
    
    def if_value_keys_match(self):
        """
        If label value keys match score value keys
        """
        if not self.__predicted_labels__ and not self.__confidence_scores__:
            return True
        
        for key in self.__confidence_scores__.keys():
            conf_score = ConfidenceScore(key, self.__confidence_scores__[key])
            pre_label = PredictedLabel(key, self.__predicted_labels__.get(key, None))
            conf_keys = conf_score.get_confidence_scores_keys()
            pre_keys = pre_label.get_value_keys()
            if set(conf_keys) != set(pre_keys):
                return False
            
        return True
            
    def validate(self):
        # labels name should be match
        if not self.if_keys_match():
            raise ValueError(f"Predicted_labels labels number should equal to scores labels number: "
                             f"{self.predicted_labels_keys()}, {self.confidence_scores_keys()}")
        
        # sub-labels should also be match
        if not self.if_value_keys_match():
            raise ValueError(f"Predicted_labels label values number should equal to scores "
                             f"label values number: {self.__confidence_scores__}, {self.__predicted_labels__}")
        
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
    
    