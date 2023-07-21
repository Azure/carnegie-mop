"""
Mop-utils some util.
"""

from typing import Dict, Union


class PredictedLabel:
    """Predict label:
    for example:
      "label_taxonomy": {
            "label_name-1": 1,
            "label_name-2": 0,
            "label_name-3": 0
      }
    """
    
    def __init__(self, label: str, label_values: Dict[str, int]):
        """
        Initialize label and label values
        @param label: label (taxonomy) name.
        @type label: str
        @param label_values: label values
        @type label_values: Dict which key type is str, value type is int.
        """
        self.label = label
        self.label_values = label_values
        self.validate()
    
    def validate(self):
        """
        validate taxonomy name, type and label name, type and value type.
        @return:
        @rtype:
        """
        if not self.label or not isinstance(self.label, str):
            raise TypeError(f"Label name must be type str and value must be not empty. {self.label}")
        
        if not self.label_values or not isinstance(self.label_values, dict):
            raise TypeError(f"Label scores must be dict. {self.label_values}")
        
        for k, v in self.label_values.items():
            if not k or not isinstance(k, str):
                raise TypeError(f"Key of label value should be str and not empty: {k}")
            
            if v is None or not isinstance(v, int):
                raise TypeError(f"Value of label value should be int: {k}, {v}, {type(v)}")
        
        number = len(self.label_values.keys())
        if 0 == number:
            raise ValueError(f"There must be at least one label in value: {number}")


class ConfidenceScore:
    """Confidence score:
    for example:
        "label_taxonomy": {
            "label_name-1": 0.3,
            "label_name-2": 0,
            "label_name-3": 0.2
        }
    """
    
    def __init__(self, label_name: str, confidence_score: Dict[str, Union[float, int]]):
        """
        Initial confidence score.
        @param label_name: label (taxonomy) name
        @type label_name: str
        @param confidence_score: confidence score
        @type confidence_score: Dict which key type is str, and value type is a float or int.
        """
        self.label: str = label_name
        self.scores: Dict[str, Union[float, int]] = confidence_score
        self.validate()
    
    def validate(self):
        """
        validate taxonomy name, type and label name, type and value type.
        @return:
        @rtype:
        """
        if not self.label or not isinstance(self.label, str):
            raise TypeError(f"Label name must be str and not empty: {self.label}")
        
        if not self.scores or not isinstance(self.scores, dict):
            raise TypeError(f"Confidence scores must be dict and may not empty: {self.scores}")
        
        for k, v in self.scores.items():
            if not k or not isinstance(k, str):
                raise TypeError(f"Confidence score key name must be str and not empty: {k}")
            
            if v is None or not isinstance(v, (float, int)):
                raise TypeError(f"Confidence score value must be float or int and not empty: {k}, {v}, {type(v)}")
        
        if 0 == len(self.scores.keys()):
            raise ValueError(f"There must be at least one key in confidence score: {self.scores}")
