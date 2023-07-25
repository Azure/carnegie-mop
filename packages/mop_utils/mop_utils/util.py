"""
Mop-utils some util.
"""

from typing import Dict, Union


class ImageAnalysisInput:
    data: bytes = b''


class TextAnalysisInput:
    text: str = ""


class AnalysisResult:
    harmful_score: float = 0.0
    severity_level: int = 0


class AcsImageResponse:
    hate = AnalysisResult()
    self_harm = AnalysisResult()
    sexual = AnalysisResult()
    violence = AnalysisResult()


class AcsTextResponse:
    hate = AnalysisResult()
    self_harm = AnalysisResult()
    sexual = AnalysisResult()
    violence = AnalysisResult()


class PredictedLabel:
    """Predict label:
    for example:
      "label_name": {
            "label_value_name-1": 1,
            "label_value_name-2": 0,
            "label_value_name-3": 0
      }
    """
    
    def __init__(self, label_name: str, label_values: Dict[str, int]):
        """
        Initialize label and label values
        @param label_name: label name.
        @type label_name: str
        @param label_values: label values
        @type label_values: Dictionary which key type is str, value type is int, its 'value' should be 1 or 0.
        """
        self.label_name = label_name
        self.label_values = label_values
        # self.validate()
        
    def output(self):
        """
        Output of predictedLabel. For example:
        "identity_hate": {
            "positive": 1,
            "negative": 0
        }
        @return:
        @rtype:
        """
        return {self.label_name: self.label_values}
    
    def validate(self):
        """
        Validates label name, type and label value name, type and value type.
        @return:
        @rtype:
        """
        if not self.label_name or not isinstance(self.label_name, str):
            raise TypeError(f"Label name must be type str and value must be not empty. {self.label_name}")
        
        if not self.label_values or not isinstance(self.label_values, dict):
            raise TypeError(f"Label scores must be dict. {self.label_values}")
        
        for k, v in self.label_values.items():
            if not k or not isinstance(k, str):
                raise TypeError(f"Key of label value should be type str and not empty: {k}")
            
            if v is None or not isinstance(v, int) or v not in (1, 0):
                raise TypeError(f"The value of label value should be int( 1 or 0 ): "
                                f"key: {k}, value: {v}, type: {type(v)}")
        
        number = len(self.label_values.keys())
        if 0 == number:
            raise ValueError(f"There must be at least one label in value: {number}")


class ConfidenceScore:
    """Confidence score:
    for example:
        "label_name": {
            "label_value_name-1": 0.3,
            "label_value_name-2": 0,
            "label_value_name-3": 0.2
        }
    """
    
    def __init__(self, label_name: str, confidence_score: Dict[str, Union[float, int]]):
        """
        Initial confidence score.
        @param label_name: label name
        @type label_name: str
        @param confidence_score: confidence score
        @type confidence_score: Dictionary which key type is str, and value type is a float or int,
                                its 'value' should between 0 and 1.
        """
        self.label_name: str = label_name
        self.scores: Dict[str, Union[float, int]] = confidence_score
        # self.validate()
    
    def output(self) -> dict:
        """
        Output of ConfidenceScore. For example:
        "identity_hate": {
            "positive": 0.713,
            "negative": 0.287
        }
        @return:
        @rtype:
        """
        
        return {self.label_name: self.scores}
    
    def validate(self):
        """
        Validates label name, type and label value name, type and value type.
        @return:
        @rtype:
        """
        if not self.label_name or not isinstance(self.label_name, str):
            raise TypeError(f"Label name must be str and not empty: {self.label_name}")
        
        if not self.scores or not isinstance(self.scores, dict):
            raise TypeError(f"Confidence scores must be dict and may not empty: {self.scores}")
        
        for k, v in self.scores.items():
            if not k or not isinstance(k, str):
                raise TypeError(f"Confidence score key name must be str and not empty: {k}")
            
            if v is None or not isinstance(v, (float, int)):
                raise TypeError(f"Confidence score value must be float or int and not empty: "
                                f"key: {k}, value: {v}, type: {type(v)}")
        
        if 0 == len(self.scores.keys()):
            raise ValueError(f"There must be at least one key in confidence score: {self.scores}")
