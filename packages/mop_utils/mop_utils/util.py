"""
Utilities for Mop-utils.
"""


class ImageAnalysisInput:
    data: bytes = b''


class TextAnalysisInput:
    text: str = ""


class AnalysisResult:
    harmful_score: float = 0.0
    severity_level: int = 0


class AcsImageResponse:
    """
    All four fields "hate", "self_harm", "sexual" and "violence" are required.
    """
    hate = AnalysisResult()
    self_harm = AnalysisResult()
    sexual = AnalysisResult()
    violence = AnalysisResult()


class AcsTextResponse:
    """
    All four fields "hate", "self_harm", "sexual" and "violence" are required.
    """
    hate = AnalysisResult()
    self_harm = AnalysisResult()
    sexual = AnalysisResult()
    violence = AnalysisResult()


class MopInferenceOutputValidator:
    """
    MOP inference output validator.
    """

    def __init__(self, mop_inference_output):
        self.predicted_labels = mop_inference_output.predicted_labels
        self.confidence_scores = mop_inference_output.confidence_scores
        if not self.predicted_labels or not self.confidence_scores:
            raise ValueError(f"Invalid predicted_labels and confidence_scores. "
                             f"Current value: {self.confidence_scores}, {self.predicted_labels}")
    
    def _check_predicted_labels(self):
        """
           Validate predicted label name, type, and validate its value's key name, key type and key value.
           @return:
           @rtype:
       """
        if self.predicted_labels:
            for key, value in self.predicted_labels.items():
                if not key or not isinstance(key, str):
                    raise TypeError(f"The label name must be type str and its value must be not empty. "
                                    f"Current value: {key}, type: {type(key)}")
            
                if not value or not isinstance(value, dict):
                    raise TypeError(f"The label scores must be dict type. Current value: {value}, type: {type(value)}")
            
                for k, v in value.items():
                    if not k or not isinstance(k, str):
                        raise TypeError(f"The key should be type str and not empty. "
                                        f"Current value: {k}, type: {type(k)}")
                
                    if v is None or not isinstance(v, int) or v not in (1, 0):
                        raise TypeError(f"The value should be int ( 1 or 0 ): "
                                        f"Current key: {k}, value: {v}, type: {type(v)}")
            
                if len(value.keys()) == 0:
                    raise ValueError(f"There must be at least one value. ")
            
    def _check_confidence_scores(self):
        """
            Validate confidence score label name, type, and validate its value's key name, key type, key value.
        """
        if self.confidence_scores:
            for key, value in self.confidence_scores.items():
                if not key or not isinstance(key, str):
                    raise TypeError(f"The label name must be str and not empty. "
                                    f"Current value: {key}, type: {type(key)}")
            
                if not value or not isinstance(value, dict):
                    raise TypeError(f"The confidence scores must be dict and also not empty. "
                                    f"Current value: {value}, type: {type(value)}")
            
                for k, v in value.items():
                    if not k or not isinstance(k, str):
                        raise TypeError(f"The confidence score key name must be str and also not empty. "
                                        f"Current value: {k}, type: {type(k)}")
                
                    if v is None or not isinstance(v, (float, int)):
                        raise TypeError(f"The confidence score value must be float or int and not empty. "
                                        f"Current key: {k}, value: {v}, type: {type(v)}")
            
                if len(value.keys()) == 0:
                    raise ValueError(f"There must be at least one key in confidence score.")
            
    def _check_keys_match(self) -> bool:
        """
        Check if predict labels keys match confidence score keys.
        """
        if len(self.predicted_labels.keys()) != len(self.confidence_scores.keys()):
            return False
        
        if set(self.predicted_labels.keys()) != set(self.confidence_scores.keys()):
            return False
        
        return True
    
    def _check_value_keys_match(self) -> bool:
        """
        Check if the keys of predict label value match the keys of confidence score value.
        """
        if not self.predicted_labels and not self.confidence_scores:
            return True
        
        for key in self.confidence_scores.keys():
            conf_score = self.confidence_scores[key]
            pre_label = self.predicted_labels.get(key, None)
            conf_keys = conf_score.keys()
            pre_keys = pre_label.keys()
            if set(conf_keys) != set(pre_keys):
                return False
        
        return True
    
    def validate(self):
        """
        Validate if label name, type, the numbers of label match between confidence score and predicted labels.
        """
        
        self._check_predicted_labels()
        self._check_confidence_scores()
        
        if not self._check_keys_match():
            raise ValueError(f"The keys of predicted labels should match the keys of confidence scores. Current: "
                             f"{self.predicted_labels.keys()}, {self.confidence_scores.keys()}")
        
        if not self._check_value_keys_match():
            raise ValueError(f"The keys of predicted labels values should match the keys of confidence score values. "
                             f"Current: {self.confidence_scores}, {self.predicted_labels}")
