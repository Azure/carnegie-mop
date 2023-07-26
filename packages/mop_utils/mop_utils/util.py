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


class MopInferenceOutputValidator:
    """
    MOP inference output validator
    """
    
    def __init__(self, predicted_label: dict, confidence_scores: dict):
        self.predicted_label = predicted_label
        self.confidence_scores = confidence_scores
    
    def _if_valid_predicted_label(self):
        """
           Validates label name, type and label value name, type and value type.
           @return:
           @rtype:
       """
        if self.predicted_label:
            for key, value in self.predicted_label.items():
                label_name, label_values = key, value
                if not label_name or not isinstance(label_name, str):
                    raise TypeError(f"Label name must be type str and value must be not empty. {label_name}")
            
                if not label_values or not isinstance(label_values, dict):
                    raise TypeError(f"Label scores must be dict: {label_values}")
            
                for k, v in label_values.items():
                    if not k or not isinstance(k, str):
                        raise TypeError(f"Key of label value should be type str and not empty: {k}")
                
                    if v is None or not isinstance(v, int) or v not in (1, 0):
                        raise TypeError(f"The value of label value should be int( 1 or 0 ): "
                                        f"key: {k}, value: {v}, type: {type(v)}")
            
                number = len(label_values.keys())
                if number == 0:
                    raise ValueError(f"There must be at least one label in value: {number}")
            
    def _if_valid_confidence_scores(self):
        """
            Validates label name, type and label value name, type and value type.
            @return:
            @rtype:
        """
        if self.confidence_scores:
            for key, value in self.confidence_scores.items():
                label_name, scores = key, value
                if not label_name or not isinstance(label_name, str):
                    raise TypeError(f"Label name must be str and not empty: {label_name}")
            
                if not scores or not isinstance(scores, dict):
                    raise TypeError(f"Confidence scores must be dict and may not empty: {scores}")
            
                for k, v in scores.items():
                    if not k or not isinstance(k, str):
                        raise TypeError(f"Confidence score key name must be str and not empty: {k}")
                
                    if v is None or not isinstance(v, (float, int)):
                        raise TypeError(f"Confidence score value must be float or int and not empty: "
                                        f"key: {k}, value: {v}, type: {type(v)}")
            
                if len(scores.keys()) == 0:
                    raise ValueError(f"There must be at least one key in confidence score: {scores}")
            
    def _if_keys_match(self):
        """
        Check if label_name keys match score keys
        """
        if len(self.predicted_label.keys()) != len(self.confidence_scores.keys()):
            return False
        
        if set(self.predicted_label.keys()) != set(self.confidence_scores.keys()):
            return False
        
        return True
    
    def _if_value_keys_match(self):
        """
        Check if label_name value keys match score value keys
        """
        if not self.predicted_label and not self.confidence_scores:
            return True
        
        for key in self.confidence_scores.keys():
            conf_score = self.confidence_scores[key]
            pre_label = self.predicted_label.get(key, None)
            conf_keys = conf_score.keys()
            pre_keys = pre_label.keys()
            if set(conf_keys) != set(pre_keys):
                return False
        
        return True
    
    def validate(self):
        """
        Validate if label name, type, the numbers of and value within predicted_labels
        and confidence_scores match.
        @return:
        @rtype:
        """
        
        self._if_valid_predicted_label()
        self._if_valid_confidence_scores()
        
        if not self._if_keys_match():
            raise ValueError(f"Predicted_labels labels number should equal to scores labels number: "
                             f"{self.predicted_label.keys()}, {self.confidence_scores.keys()}")
        
        if not self._if_value_keys_match():
            raise ValueError(f"Predicted_labels the label value keys should match score value keys: "
                             f"{self.confidence_scores}, {self.predicted_label}")
