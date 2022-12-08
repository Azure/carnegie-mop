from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any


class InferenceInput:
    def __init__(self, text: Optional[str] = None, image: Optional[str] = None, width: Optional[int] = None,
                 height: Optional[int] = None) -> None:
        self.__text__ = text
        self.__image__ = image
        self.__width__ = width
        self.__height__ = height

    def from_dict(self, input_dict: Dict) -> Any:
        self.__text__ = input_dict.get('text')
        self.__image__ = input_dict.get('image')
        self.__width__ = input_dict.get('width')
        self.__height__ = input_dict.get('height')
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


class InferenceOutput:
    def __init__(self, confidence_scores: Optional[Dict] = None, predicted_labels: Optional[Dict] = None) -> None:
        self.__confidence_scores__: Dict = confidence_scores
        self.__predicted_labels__: Dict = predicted_labels

    def from_dict(self, output_dict: dict) -> Any:
        self.__confidence_scores__ = output_dict.get('confidence_scores', None)
        self.__predicted_labels__ = output_dict.get('predicted_labels', None)
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
    def init(self, model_root: str):
        raise NotImplementedError("init() method is not implemented")

    @abstractmethod
    def inference(self, items: InferenceInput) -> InferenceOutput:
        raise NotImplementedError("inference() method is not implemented")

    @abstractmethod
    def inference_batch(self, items: List[InferenceInput]) -> List[InferenceOutput]:
        raise NotImplementedError("inference_batch() method is not implemented")
