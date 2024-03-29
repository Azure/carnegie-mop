# Model Task Confidence Score

## 1. CategoricalTaskLabelConfidenceScoreSumError
### A simplified description might resemble the following:
```html
CategoricalTaskLabelConfidenceScoreSumError: the sum of all confidence scores of a taxonomy should be 1
score_sum: <score_sum>,
label_type: <self.label_type>, 
task_label_info: <task_label_info>, 
model_revision_uuid: <model_revision_uuid>, 
response_values: <response_values>.
```
### Take appropriate action:
- Verify the confidence score value for the task label.
- For details on the task label confidence score value, please consult: [What format does a model output should be for different task label types?](https://github.com/Azure/carnegie-mop#q-what-format-does-a-model-output-should-be-for-different-task-label-types)

## 2. OrdinalTaskLabelConfidenceScoreValueError
### A simplified description might resemble the following:
```html
OrdinalTaskLabelConfidenceScoreValueError: confidence score for each label should be cumulative.
error_info: <score_cumulative>, 
label_type: <label_type>, 
task_label_info: <task_label_info>, 
model_revision_uuid: <model_revision_uuid>,
response_values: <response_values>"
```

### Take appropriate action:
- Verify the confidence score value for the task label.
- For details on the task label confidence score value, please consult: [What format does a model output should be for different task label types?](https://github.com/Azure/carnegie-mop#q-what-format-does-a-model-output-should-be-for-different-task-label-types)

