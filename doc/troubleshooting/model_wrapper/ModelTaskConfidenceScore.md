# Model Task Confidence Score

## 1. CategoricalTaskLabelConfidenceScoreSumError
### simple details description may like below:
```html
CategoricalTaskLabelConfidenceScoreSumError: the sum of all confidence scores of a taxonomy should be 1
score_sum: <score_sum>,
label_type: <self.label_type>, 
task_label_info: <task_label_info>, 
model_revision_uuid: <model_revision_uuid>, 
response_values: <response_values>.
```
### Take action:
- Check task label confidence score value.
- Task label confidence score value, please refer to: [What format does a model output should be for different task label types?](https://github.com/Azure/carnegie-mop#q-what-format-does-a-model-output-should-be-for-different-task-label-types)

## 2. OrdinalTaskLabelConfidenceScoreValueError
### simple details description may like below:
```html
OrdinalTaskLabelConfidenceScoreValueError: confidence score for each label should be cumulative.
error_info: <score_cumulative>, 
label_type: <label_type>, 
task_label_info: <task_label_info>, 
model_revision_uuid: <model_revision_uuid>,
response_values: <response_values>"
```

### Take action:
- Check task label confidence score value.
- Task label confidence score value, please refer to: [What format does a model output should be for different task label types?](https://github.com/Azure/carnegie-mop#q-what-format-does-a-model-output-should-be-for-different-task-label-types)

