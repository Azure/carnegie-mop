# RAI Model Onboarding Pipeline Documentation
> **Note:** This document is a work in progress. Please feel free to contribute to it by submitting a pull request.
> Any questions please contact [David Liang](mailto:liangze@microsoft.com).

## Overview
- MOP link (AAD required): **[https://carnegie-mop.azurewebsites.net](https://carnegie-mop.azurewebsites.net)**

RAI Model Onboarding Pipeline (MOP) is a platform for responsible AI model onboarding. It provides **an automation pipeline to help data scientists and engineers to onboard their models** for Azure responsible AI services including Azure AI Content Safety (AACS) and RAI Orchestrator (RAIO). 

For now MOP **supports classification models only**.

## Getting Started
There are several concepts on MOP that you need to know before you start using it.

### Tasks
A Task on MOP defines a classification problem. It contains the following information:
- **Name**: A unique name for the task.
- **Description**: A description for the task. Usually it will explain the classification problem in detail, including the business scenario, the data source, definition of labels, etc.
- Group: The team that owns the task.
- Created time: The time when the task is created.
- Created by: The user who created the task.
- **Modality name**: Modality refers to a particular way in which information is processed and stored. Now MOP supports 3 different modality: 
  - Text: the input is a piece of text. 
  - Image: the input is a base64 encoded image.
  - ImageAndText: the input is a piece of text and a base64 encoded image. Images will be inserted into the text at the position of the corresponding placeholders.
- **Taxonomy**: Taxonomy here sometimes is also called "category". It refers to the structured classification within a particular domain. Each taxonomy should be independent and mutually exclusive. MOP supports following taxonomy types:
  - Hate
  - Self-harm
  - Violence
  - Sexual
  - Jailbreak
  - Defensive

- **Labels**: Labels represent the classification categories. For example, if the task is to classify whether a piece of text is toxic, the labels could be `toxic` and `non-toxic`; if the task is to classify the level of toxicity, the labels could be `non-toxic`, 'slightly toxic', `toxic`, `very toxic`, and `extremely toxic`. Number of labels should be at least 2 and at most 20;
- **Label type**: Label type defines the type of the labels. For now MOP supports 2 different label types:
  - Categorical: each sample can have only one label; labels are independent and mutually exclusive. There should be at least 2 labels for a categorical task.
  - Ordinal: each sample can have only one label; labels are in ascending order. There should be at least **3** labels for an ordinal task.

> To note that **only MOP administrators can create/modify the definition of a Task.**


### Models
A model on MOP represents a trained classification model that can be used for specific MOP task(s). Therefore, a model contributor should specify which task(s) their model can resolve. All users can be a model contributor as long as they have an available model to onboard.

Model owners can sue MOP to manage versions of their models, get various testing results, and release their models to downstream responsible AI services. 

MOP asks model contributors to organize their models (file structure, input/output contract, implementations, .etc) in a particular way, see [Model Contributor Guide](./ModelContributorGuide.md) for more details.

### Evaluation Datasets
MOP stores abundant evaluation datasets for model owners to test their models. Each evaluation dataset is associated with one or more tasks. To avoid potential over-fitting, MOP will not provide the dataset content and ground truth labels of the evaluation datasets. Instead, MOP will provide the evaluation metrics of the models on the evaluation datasets.

There are two types of evaluation datasets on MOP:
- **Binary dataset**: A binary dataset contains only two labels `0` and `1`. It can be used to evaluate:
  - Ordinal tasks: since labels for an ordinal task are in ascending order, MOP will automatically convert the ordinal labels to multiple set of binary labels and generate corresponding evaluation results. 
  
    For example, if the ordinal labels are `0`, `1`, `2`, `3`, MOP will convert them to:
    - `0` vs `1, 2, 3`
    - `0, 1` vs `2, 3`
    - `0, 1, 2` vs `3`
    
    MOP will generate (three sets of) evaluation results for each set of binary labels.
  - Categorical task with 2 labels `0` and `1`: MOP will generate evaluation results for the binary labels `0` and `1`.
- **Multi-label dataset**: A multi-label dataset contains at least two labels. It can be used to evaluate:
  - Categorical tasks with 2 or more labels: The labels in the dataset should be a subset (or equal to) of the labels of the task. MOP will generate evaluation results for each label in the dataset.

Dataset contributors can upload their datasets to MOP by following the [Dataset Contributor Guide](./DatasetContributorGuide.md).

### DSAT Cases
DSAT stands for "Dissatisfaction". DSAT cases are usually collected from the downstream responsible AI services. They are the cases that the downstream responsible AI services are not satisfied with the model's performance. Each case is associated with a task. It contains information including the input, trace id, the ground truth label and other information that can help model owners to debug their models. Please refer to [DSAT Case Contributor Guide](./DSATCaseContributorGuide.md) for more details.

## Role-based documentation
If you are a model contributor and want to onboard your model to MOP, please refer to [Model Contributor Guide](./ModelContributorGuide.md).

If you are a dataset contributor and want to upload your dataset to MOP, please refer to [Dataset Contributor Guide](./DatasetContributorGuide.md).

If you want to provide DSAT cases and track its resolution, please refer to [DSAT Case Contributor Guide](./DSATCaseContributorGuide.md).

If you are a downstream responsible AI service admin and want to use MOP to track models that are released to your service, please refer to [Downstream Responsible AI Service Admin Guide](./DownstreamResponsibleAIServiceAdminGuide.md).

If you want to go through model testing results in general, please refer to [Model Testing Results Guide](./ModelTestingResultsGuide.md).

## FAQ
