import importlib
import os

from azureml.contrib.services.aml_response import AMLResponse

from mop_utils import BaseModelWrapper
from mop_utils.constant import CM_MODEL_WRAPPER_NAME, DYNAMIC_SETTINGS_YAML
from mop_utils.inference_wrapper import MOPInferenceWrapper

#todo: for quick test

# from inference import ModelWrapper

try:
    inference_module = importlib.import_module(CM_MODEL_WRAPPER_NAME)
    ModelWrapper = [getattr(inference_module, i) for i in inference_module.__dict__.keys() if
                    hasattr(inference_module.__dict__.get(i), '__bases__')
                    and BaseModelWrapper in inference_module.__dict__.get(i).__bases__][0]



except Exception as e:
    result = str(e)
    # logging.exception(result)
    raise e
import numpy as np
import json

import yaml
from typing import Any, Dict, List, Optional

from pyraisdk.dynbatch import BaseModel, DynamicBatchModel

batch_model: Optional[DynamicBatchModel] = None
base_model_wrapper: BaseModelWrapper = ModelWrapper()
inference_wrapper: MOPInferenceWrapper = MOPInferenceWrapper(base_model_wrapper)
batch_size: Optional[int] = None


class WrapModel(BaseModel):
    def predict(self, items: List[Any], triggered_by_mop=False) -> List[Any]:
        return inference_wrapper.run_batch(items, triggered_by_mop, batch_size=batch_size)


def _get_dynamic_batch_args() -> Optional[Dict]:
    """ if dynamic batch not enable, return None
    """
    if not os.path.exists(DYNAMIC_SETTINGS_YAML):
        return None

    # load settings.yml
    with open(DYNAMIC_SETTINGS_YAML) as dynamic_settings_file:
        try:
            settings = yaml.safe_load(dynamic_settings_file)
        except yaml.YAMLError:
            raise Exception("Load Dynamic Setting Yaml Fail")

    # check enable
    dynamic_batch = settings.get('dynamicBatch', {})
    enable = dynamic_batch.get('enable', None)
    if enable is None:
        return None
    if not (isinstance(enable, bool) and enable):
        return None

    # get args
    args = {
        'max_batch_size': dynamic_batch.get('maxBatchSize'),
        'idle_batch_size': dynamic_batch.get('idleBatchSize'),
        'max_batch_interval': dynamic_batch.get('maxBatchInterval'),
    }
    return {k: v for k, v in args.items() if v is not None}


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


# def inference_output(inference_result):
#     # return json.loads(json.dumps(inference_result, cls=NumpyJsonEncoder))
#     return json.dumps(inference_result, cls=NumpyJsonEncoder)

def generate_response(inference_result: Dict) -> AMLResponse:
    output_json = json.dumps(inference_result, cls=NumpyJsonEncoder)
    return AMLResponse(output_json, 200, {'Content-Type': 'application/json'})


# todo: add a string response

def mop_init():
    global batch_model
    global batch_size
    inference_wrapper.init(os.path.join(os.getenv("AZUREML_MODEL_DIR"), "../model"))

    # assign batch_model is enabled
    dynamic_batch_args = _get_dynamic_batch_args()
    if dynamic_batch_args is not None:
        batch_model = DynamicBatchModel(WrapModel(), **dynamic_batch_args)
        batch_size = dynamic_batch_args.get('max_batch_size')


# todo: think more, whether any or anything else, need to talk with congrui

# better be a dict



def mop_run(raw_data: str, triggered_by_mop) -> AMLResponse:
    # print("Request: [{0}]".format(request))
    #
    # raw_data = request.get_data(False)
    # if raw_data is None:
    #     raise Exception("No input data provided")
    # encoding = 'utf-8'
    # raw_data_json = str(raw_data, encoding)
    # raw_data = json.loads(raw_data_json)
    # print(f"raw_data: {raw_data}")

    # triggered_by_mop = True
    # raw_header = request.get_header(False)
    # print(f"raw_header： {raw_header}" )
    # encoding = 'utf-8'
    # raw_header_str = str(raw_header, encoding)
    # print(f"raw_header_str： {raw_header_str}")



    if batch_model is not None:
        inference_result = batch_model.predict(raw_data, triggered_by_mop if isinstance(raw_data, list) else [raw_data])
        return generate_response(inference_result)
    if isinstance(raw_data, str):
        inference_result = inference_wrapper.run(raw_data, triggered_by_mop)
        return generate_response(inference_result)
    if isinstance(raw_data, dict):
        inference_result = inference_wrapper.run(raw_data, triggered_by_mop)
        return generate_response(inference_result)
    if isinstance(raw_data, list):
        inference_result = inference_wrapper.run_batch(raw_data, triggered_by_mop)
        return generate_response(inference_result)
    raise Exception("Invalid input data format")


# if __name__ == "__main__":
#     mop_init()
#
#     data_dict = {"data": "354"}
#     data_str = json.dumps(data_dict)
#     res = mop_run(data_str, False)
#
#     print(res)
#     text_dict = {"text": "354"}
#     text_str = json.dumps(text_dict)
#     res = mop_run(text_str, True)
#     print(res)
#
#
#     text_dict = [{"text": "354"}]
#     text_str = json.dumps(text_dict)
#     res = mop_run(text_str, True)
#     print(res)


    # test enable dynmaic batch --- move such code to test
