import json
from typing import Dict, List

from mop_utils import BaseModelWrapper, InferenceInput


class MOPInferenceWrapper:
    def __init__(self, base_model_wrapper: BaseModelWrapper) -> None:
        self.model_wrapper = base_model_wrapper

    def init(self, model_root: str) -> None:
        self.model_wrapper.init(model_root)

    def run(self, item: str, triggered_by_mop: False) -> List[str]:
        if not triggered_by_mop:
            customized_output = self.model_wrapper.inference(item)
            return [customized_output]
        else:
            # todo: check is validate input, other wise, throw exception
            item_json = json.loads(item)

            if isinstance(item_json, dict):
                mop_input = InferenceInput().from_dict(item_json)
                customized_input = self.model_wrapper.convert_mop_input_to_customized_input(mop_input)
                customized_output = self.model_wrapper.inference(customized_input)
                mop_output = self.model_wrapper.convert_customized_output_to_mop_output(customized_output)
                #todo, add json decoder
                return [json.dumps(mop_output.output)]
            if isinstance(item_json, list):
                # by batch?
                customized_inputs = [
                    self.model_wrapper.convert_mop_input_to_customized_input(
                        InferenceInput().from_dict(item)) for item in item_json]

                customized_outputs = self.model_wrapper.inference_batch(customized_inputs)

                # todo, add json decoder
                mop_outputs = [
                    json.dumps(self.model_wrapper.convert_customized_output_to_mop_output(customized_output).output) for
                    customized_output in customized_outputs]
                return mop_outputs

    def run_batch(self, items: List[str], triggered_by_mop: False) -> List[str]:
        if not triggered_by_mop:
            customized_outputs = self.model_wrapper.inference_batch(items)
            return customized_outputs
        else:
            # todo: check is validate input, other wise, throw exception
            customized_inputs = [
                self.model_wrapper.convert_mop_input_to_customized_input(InferenceInput().from_dict( json.load(item))) for item in
                items]

            customized_outputs = self.model_wrapper.inference_batch(customized_inputs)

            # todo, add json decoder
            mop_outputs = [json.dumps(self.model_wrapper.convert_customized_output_to_mop_output(customized_output).output) for
                           customized_output in customized_outputs]
            return mop_outputs
