import importlib
import os
import logging
import json

from mop_utils import BaseModelWrapper
from mop_utils.constant import CM_MODEL_WRAPPER_NAME, DYNAMIC_SETTINGS_YAML
from mop_utils.inference_wrapper import MOPInferenceWrapper


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




def mop_init():
    global batch_model
    global batch_size
    inference_wrapper.init(os.path.join(os.getenv("AZUREML_MODEL_DIR"), "../model"))

    # assign batch_model is enabled
    dynamic_batch_args = _get_dynamic_batch_args()
    if dynamic_batch_args is not None:
        batch_model = DynamicBatchModel(WrapModel(), **dynamic_batch_args)
        batch_size = dynamic_batch_args.get('max_batch_size')


def mop_run(raw_data: any, triggered_by_mop) -> dict:
    if batch_model is not None:
        inference_result = batch_model.predict(raw_data, triggered_by_mop if isinstance(raw_data, list) else [raw_data])
        return inference_result
    if isinstance(raw_data, dict):
        inference_result = inference_wrapper.run(raw_data, triggered_by_mop)
        return inference_result
    if isinstance(raw_data, list):
        inference_result = inference_wrapper.run_batch(raw_data, triggered_by_mop)
        return inference_result
    raise Exception("Invalid input data format")


if __name__ == "__main__":
    mop_init()

    data_dict = {"data": "354"}

    res = mop_run(data_dict, False)

    print(res)
    text_dict = {"text": "354"}

    res = mop_run(text_dict, True)
    print(res)


    text_dict = [{"text": "354"}]

    res = mop_run(text_dict, True)
    print(res)


    # test enable dynmaic batch --- move such code to test
