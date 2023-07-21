"""
Mop-utils some util.
"""

from typing import Dict, Union


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
        
        number = len(self.label_values.keys())
        if 0 == number:
            raise ValueError(f"There must be at least one label in value pairs: {number}")


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
        
        if 0 >= len(self.scores.keys()):
            raise ValueError(f"There must be at least one key in confidence score: {self.scores}")

