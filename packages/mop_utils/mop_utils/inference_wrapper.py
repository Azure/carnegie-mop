import importlib
import json
import logging
from typing import Any, Dict, List, Optional

import numpy as np
from mop_utils.base_model_wrapper import BaseModelWrapper, MopInferenceInput
from mop_utils.constant import CM_MODEL_WRAPPER_NAME
from pyraisdk.dynbatch import BaseModel, DynamicBatchModel

try:
    inference_module = importlib.import_module(CM_MODEL_WRAPPER_NAME)
    ModelWrapper = [getattr(inference_module, i) for i in inference_module.__dict__.keys() if
                    hasattr(inference_module.__dict__.get(i), '__bases__')
                    and BaseModelWrapper in inference_module.__dict__.get(i).__bases__][0]
except Exception as e:
    result = str(e)
    logging.exception(result)
    raise e


class MOPInferenceWrapper:
    def __init__(self, base_model_wrapper: BaseModelWrapper) -> None:
        self.model_wrapper = base_model_wrapper

    def init(self, model_root: str) -> None:
        self.model_wrapper.init(model_root)

    def run(self, item: Dict, triggered_by_mop) -> Dict:
        print(f"function run(), input is {item}, triggered by mop: {triggered_by_mop}")
        logging.info(f"function run(), input is {item}, triggered by mop: {triggered_by_mop}")
        if not triggered_by_mop:
            model_output = self.model_wrapper.inference(item)
            return [model_output]
        else:
            mop_input = MopInferenceInput().from_dict(item)
            model_input = self.model_wrapper.convert_mop_input_to_model_input(mop_input)
            logging.info(f"Converted model input is {model_input}")
            model_output = self.model_wrapper.inference(model_input)
            logging.info(f"Inference model output is {model_output}")
            mop_output = self.model_wrapper.convert_model_output_to_mop_output(model_output)

            return mop_output.output

    def run_batch(self, items: List[dict], triggered_by_mop: bool, batch_size: Optional[int] = None) -> List[dict]:
        print(f"function run_batch(), run_batch is {items}, triggered by mop: {triggered_by_mop}")
        logging.info(f"function run_batch(), run_batch is {items}, triggered by mop: {triggered_by_mop}")
        if not triggered_by_mop:
            model_outputs = self.model_wrapper.inference_batch(items)
            return model_outputs
        else:
            model_inputs = [
                self.model_wrapper.convert_mop_input_to_model_input(MopInferenceInput().from_dict(item)) for item
                in
                items]

            logging.info(f"Converted model inputs is {model_inputs}")
            model_outputs = []
            model_outputs = self.model_wrapper.inference_batch(model_inputs)

            logging.info(f"Inference batch model outputs is {model_outputs}")
            mop_outputs = [self.model_wrapper.convert_model_output_to_mop_output(model_output).output for
                           model_output in model_outputs]
            return mop_outputs


batch_model: Optional[DynamicBatchModel] = None
base_model_wrapper: BaseModelWrapper = ModelWrapper()
inference_wrapper: MOPInferenceWrapper = MOPInferenceWrapper(base_model_wrapper)
batch_size: Optional[int] = None
triggered_by_mop: bool = False


class WrapModel(BaseModel):
    def predict(self, items: List[Any]) -> List[Any]:
        print(f"in predict() function, triggered_by_mop={triggered_by_mop}")
        return inference_wrapper.run_batch(items, triggered_by_mop=triggered_by_mop, batch_size=batch_size)


class NumpyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return json.JSONEncoder.default(self, obj)


"""
This is init function.

Parameters:
    model_root - root where the model file exists

Returns:
    None
"""


def mop_init(model_root, dynamic_batch_args: None):
    global batch_model
    global batch_size
    inference_wrapper.init(model_root)

    # assign batch_model is enabled
    if dynamic_batch_args is not None:
        batch_model = DynamicBatchModel(WrapModel(), **dynamic_batch_args)
        batch_size = dynamic_batch_args.get('max_batch_size')


"""
This is run function.

Parameters:
    raw_data - row input data to do inference
    triggered_by_mop - whether the function is triggered by mop
    **kwargs - dynamic parameter 
    
Returns:
    inference result
    
"""
def mop_run(raw_data: any, is_mop_triggered: bool = False, **kwargs) -> any:
    global triggered_by_mop
    triggered_by_mop = is_mop_triggered
    print(f"in mop_run() function, triggered_by_mop={triggered_by_mop}, is_mop_triggered={is_mop_triggered}")
    if batch_model is not None:
        raw_data = raw_data if isinstance(raw_data, list) else [raw_data]
        inference_result = batch_model.predict(raw_data)
        return inference_result
    if isinstance(raw_data, dict):
        inference_result = inference_wrapper.run(raw_data, triggered_by_mop)
        return inference_result
    if isinstance(raw_data, list):
        inference_result = inference_wrapper.run_batch(raw_data, triggered_by_mop=triggered_by_mop)
        return inference_result
    raise Exception("Invalid input data format")


def build_response(inference_result: any) -> any:
    if isinstance(inference_result, dict):
        output_str = json.dumps(inference_result, cls=NumpyJsonEncoder)
        return json.loads(output_str)
    if isinstance(inference_result, list):
        res = [item.__dict__ if hasattr(inference_result, '__dict__') else item for item in inference_result]
        output_str = json.dumps(res, cls=NumpyJsonEncoder)
        return json.loads(output_str)
    if hasattr(inference_result, '__dict__'):
        output_str = json.dumps(inference_result.__dict__, cls=NumpyJsonEncoder)
        return json.loads(output_str)
    return inference_result


if __name__ == "__main__":
    model_root = "D:\code\carnegie-mop\sample\model"
    # mop_init(model_root, None)
    #
    # text_dict = {"text": "354"}
    # res = mop_run(text_dict, True)
    # print(res)
    # text_dict = [{"text": "354"}]
    # res = mop_run(text_dict, True)
    # print(res)

    dynamic_batch = {
        'enable': True,
        'maxBatchSize': 12,
        'idleBatchSize': 3,
        'maxBatchInterval': 0.2
    }

    mop_init(model_root, dynamic_batch)

    text_dict = {"text": "354"}
    res = mop_run(text_dict, True)
    print(res)
