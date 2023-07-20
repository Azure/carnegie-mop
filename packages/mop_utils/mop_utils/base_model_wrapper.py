from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Union


class PredictedLabel:
    """
    Predict label. for example:
      "label_example": {
            "example-1": 1,
            "example-2": 0,
            "example-3": 0
      }
    """

    def __init__(self, label_name: str, label_values: Dict[str, Union[float, int]]):
        self.label_name = label_name
        self.label_value_pairs = label_values
        self.validate()
    
    def get_label_name(self):
        return self.label_name
    
    def get_label_value_paris(self):
        return self.label_value_pairs
        
    def from_dict(self, item: Dict):
        # TODO: need from_dict?
        if not isinstance(item, dict):
            raise ValueError(f"invalid item, must be dict: {item}")

        key = item.keys()
        self.label_name = key
        self.label_value_pairs = item.get(key)
        self.validate()
     
    def validate(self):
        if not self.label_name or not isinstance(self.label_name, str):
            raise ValueError(f"label name must be type str and value must not empty. {self.label_name}")
    
        if not self.label_value_pairs or not isinstance(self.label_value_pairs, dict):
            raise ValueError(f"label scores must be dict. {self.label_value_pairs}")
        
        for k, v in self.label_value_pairs.items():
            if not k or not isinstance(k, str):
                raise ValueError(f"key of label value paris should be str and not empty: {k}")
            if not v or not isinstance(v, (float, int)):
                raise ValueError(f"value of label value pairs should be float or int.")
            
        value_sum = self.value_sum()
        if 1 != value_sum:
            raise ValueError(f"the sum of label values should be 1: {value_sum}")
       
        value_key_pairs_number = self.get_key_number_of_value_pairs()
        if 0 >= value_key_pairs_number:
            raise ValueError(f"there must be at least one label in value pairs: {value_key_pairs_number}")
        
    def value_sum(self):
        value_sum = sum(v for v in self.label_value_pairs.values())
        return value_sum
    
    def get_value_pairs_keys(self):
        return self.label_value_pairs.keys()
    
    def get_key_number_of_value_pairs(self):
        return len(self.get_value_pairs_keys())
    
    
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
        self.label_name: str = label_name
        self.confidence_scores: Dict[str, Union[float, int]] = confidence_scores
        self.validate()
        
    def get_label_name(self):
        return self.label_name
    
    def get_confidence_scores(self):
        return self.confidence_scores
    
    def validate(self):
        if not self.label_name or not isinstance(self.label_name, str):
            raise ValueError(f"label name must be str and not empty: {self.label_name}")
        
        if not self.confidence_scores or isinstance(self.confidence_scores, dict):
            raise ValueError(f"confidence scores must be dict and may not empty: {self.confidence_scores}")
        
        for k, v in self.confidence_scores.items():
            if not k or not isinstance(k, str):
                raise ValueError(f"confidence score key name must be str and not empty: {k}")
            if not v or not isinstance(v, (float, int)):
                raise ValueError(f"confidence score value must be float or int and not empty: {v}")
            
        key_number_confidence_scores = self.get_key_number_of_confidence_scores()
        if 0 >= key_number_confidence_scores:
            raise ValueError(f"there must be at least one key in confidence score: {self.confidence_scores}")
        
    def get_confidence_scores_keys(self):
        return self.confidence_scores.keys()
    
    def get_key_number_of_confidence_scores(self):
        return len(self.get_confidence_scores_keys())
        
        
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
    def __init__(self, confidence_scores: Optional[List[ConfidenceScore]] = None,
                 predicted_labels: Optional[List[PredictedLabel]] = None) -> None:
        self.__confidence_scores__ = dict()
        self.__predicted_labels__ = dict()
        if confidence_scores:
            for score in confidence_scores:
                self.__confidence_scores__[score.get_label_name()] = score.get_confidence_scores()
        
        if predicted_labels:
            for label in predicted_labels:
                self.__predicted_labels__[label.get_label_name()] = label.get_label_value_paris()
                
        self.validate()

    def from_dict(self, output_dict: dict) -> Any:
        predicted_labels: Dict[PredictedLabel] = output_dict["predicted_labels"]
        confidence_scores: Dict[ConfidenceScore] = output_dict["confidence_scores"]
        
        for k, v in predicted_labels.items():
            predict_label = PredictedLabel(k, v)
            self.__predicted_labels__[predict_label.get_label_name()] = predict_label.get_label_value_paris()
        
        for k, v in confidence_scores.items():
            conf_score = ConfidenceScore(k, v)
            self.__confidence_scores__[conf_score.get_label_name()] = conf_score.get_confidence_scores()
            
        return self
    
    def predicted_labels_keys(self):
        return self.__predicted_labels__.keys()
    
    def confidence_scores_keys(self):
        return self.__confidence_scores__.keys()
    
    def if_label_keys_match_score_keys(self):
        if len(self.predicted_labels_keys()) != len(self.confidence_scores_keys()):
            return False
        
        if set(self.predicted_labels_keys()) != set(self.confidence_scores_keys()):
            return False
        
        return True
    
    def if_label_values_keys_match_score_value_keys(self):
        if not self.__predicted_labels__ and not self.__confidence_scores__:
            return True
        
        for key in self.__confidence_scores__.keys():
            conf_score: ConfidenceScore = self.__confidence_scores__[key]
            pre_label: PredictedLabel = self.__predicted_labels__[key]
            
            conf_keys = conf_score.get_confidence_scores_keys()
            pre_keys = pre_label.get_value_pairs_keys()
            if set(conf_keys) != set(pre_keys):
                return False
            
        return True
            
    def validate(self):
        if not self.if_label_keys_match_score_keys():
            raise ValueError(f"predicted_labels labels number should equal to confidence_scores labels number: "
                             f"{self.predicted_labels_keys()}, {self.confidence_scores_keys}")
        
        if not self.if_label_values_keys_match_score_value_keys():
            raise ValueError(f"predicted_labels label values number should equal to confidence_scores "
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
