from abc import ABC, abstractmethod
from typing import List, Dict

class InferenceInput:
    def __init__(self, input_dict: dict) -> None:
        self.__input__ = input_dict
        self.__text__ = None
        self.__image__ = None
        self.__width__ = None
        self.__height__  = None

    def __str__(self) -> str:
        return str(self.input)

    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def input(self) -> dict:
        return self.__input__ 

    @property
    def text(self) -> str:
        return self.input.get('text', None)
    
    @text.setter
    def text(self, text: str) -> None:
        self.__text__ = text
    
    @property
    def image(self) -> str:
        return self.input.get('image', None)
    
    @image.setter
    def image(self, image: str) -> None:
        self.__image__ = image
    
    @property
    def width(self) -> int:
        return self.input.get('width', None)
    
    @width.setter
    def width(self, width: int) -> None:
        self.__width__ = width

    @property
    def height(self) -> int:
        return self.input.get('height', None)
    
    @height.setter
    def height(self, height: int) -> None:
        self.__height__ = height

class InferenceOutput:
    def __init__(self) -> None:
        self.__confidence_score__: Dict = None
        self.__predicted_labels__: Dict = None


    def __str__(self) -> str:
        return str(self.output)

    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def confidence_score(self) -> Dict:
        return self.output.get('confidence_score', None)
    
    @confidence_score.setter
    def confidence_score(self, confidence_score: Dict) -> None:
        self.output['confidence_score'] = confidence_score
    
    @property
    def predicted_labels(self) -> Dict:
        return self.output.get('predicted_labels', None)
    
    @predicted_labels.setter
    def predicted_labels(self, predicted_labels: Dict) -> None:
        self.output['predicted_labels'] = predicted_labels

    @property
    def output(self) -> dict:
        return {'confidence_score': self.confidence_score, 'predicted_labels': self.predicted_labels}


class BaseModelWrapper(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def init(self, model_root:str) -> None:
        raise NotImplementedError( "Should have implemented this" )

    @abstractmethod
    def inference(self, items: InferenceInput)->InferenceOutput:
        raise NotImplementedError( "Should have implemented this" )

    @abstractmethod
    def inference_batch(self, items: List[InferenceInput])->List[InferenceOutput]:
        raise NotImplementedError( "Should have implemented this" )