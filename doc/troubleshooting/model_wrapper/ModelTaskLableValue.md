# Model Task Label Value

## 1. CategoricalTaskLabelValueError
### simple details description may like below:
```html
CategoricalTaskLabelValueError: 1 should only appear once in response predicted_labels. key with value 1 should both in model label and task label. 
error_info: <error_info>, 
               
label_type: <label_type>, 
task_label_info: <task_label_info>, 
               
model_revision_uuid: <model_revision_uuid>, 
response_values: <response_values>.
```

### Take action:
- Check task label and its value rule.  
- Task label and value rule refers to:   
[What format does a model output should be for different task label types?](https://github.com/Azure/carnegie-mop#q-what-format-does-a-model-output-should-be-for-different-task-label-types)


## 2. OrdinalTaskLabelValueError
### simple details description may like below:
```html
OrdinalTaskLabelValueError: 1 must appear in response predicted_labels, in the predicted_labels field, labels before 'medium' (included) should all have 1 as their predicted labels, and labels after 'medium' should all have 0 as their predicted labels.
error_info: <error_info>,
label_type: <label_type>, 
task_label_info: <task_label_info>, 
model_revision_uuid: <model_revision_uuid>,
response_values: <response_values>
```
### Take action:
- Check task label and its value rule.
- Task label and value rule refers to:   
[What format does a model output should be for different task label types?](https://github.com/Azure/carnegie-mop#q-what-format-does-a-model-output-should-be-for-different-task-label-types)