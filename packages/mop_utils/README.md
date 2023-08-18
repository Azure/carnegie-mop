# mop-utils

## Overview

This project is made for model contributor to onboard their models to RAI Model Onboarding Pipeline (MOP). The SDK provides a set of APIs to load model checkpoints, perform inference (single and batch) and convert model input/output contracts so that MOP can parse its conferencing results and give evaluation metrics.

## Integrate the SDK with your model

> You may want to check the [MOP Model Contributor Guide](https://github.com/Azure/carnegie-mop/blob/main/doc/ModelContributorGuide.md) for more details.

Follow the steps below to integrate the SDK with your model.

1. In the requirements.txt file of your model in the /src, add the latest [mop-utils](https://github.com/Azure/carnegie-mop/blob/main/packages/mop_utils/setup.py#L5) as a dependency.

2. Import resources from mop-utils:
```
# Required
from mop_utils.base_model_wrapper import BaseModelWrapper, MopInferenceInput, MopInferenceOutput

# Optional. If you want to use release your model to AACS, you can import them as well.
from mop_utils.util import TextAnalysisInput, AcsTextResponse, AnalysisResult
```
3. Inherit your model class from `BaseModelWrapper` and implement the abstract methods, 5 of which are required and the rest are optional. You can check the [samples](https://github.com/Azure/carnegie-mop/tree/main/sample) for more details.

```
class MyOwnModel(BaseModelWrapper):
    def init(self, model_root: str, **kwargs):
        """
        Load model checkpoint and initialize the model.
        """
        
    def inference(self, item: Dict, **kwargs) -> Dict:
        """
        Perform inference on a single item.
        """
        
    def def inference_batch(self, item: List[Dict], **kwargs) -> List[Dict]:
        """
        Perform inference on a batch of items.
        """
        
    def convert_mop_input_to_model_input(self, mop_input: MopInferenceInput, **kwargs) -> Dict:
        """
        Convert MOP inference input to model input.
        """
        
    def convert_model_output_to_mop_output(self, customized_output: Dict, **kwargs) -> MopInferenceOutput:
        """
        Convert model output to MOP inference output.
        """
        
    def convert_acs_text_request_to_model_inference_input(self, req: TextAnalysisInput) -> object:
        """
        Optional. Only required if you want to release your model to AACS.
        Convert ACS text request to model inference input.
        """
        
    def convert_model_inference_output_to_acs_text_response(self, out: object) -> AcsTextResponse:
        """
        Optional. Only required if you want to release your model to AACS.
        Convert model inference output to ACS text response.
        """
        
    def convert_acs_image_request_to_model_inference_input(self, req: ImageAnalysisInput) -> object:
        """
        Optional. Only required if you want to release your model to AACS.
        Convert ACS image request to model inference input.
        """
        
    def convert_model_inference_output_to_acs_image_response(self, out: object) -> AcsImageResponse:
        """
        Optional. Only required if you want to release your model to AACS.
        Convert model inference output to ACS image response.
        """
```