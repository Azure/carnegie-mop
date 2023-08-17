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

MOP asks model contributors to organize their models (file structure, input/output contract, implementations, .etc) in a particular way, see [Model Contributor Guide](./doc/ModelContributorGuide.md) for more details.

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

Dataset contributors can upload their datasets to MOP by following the [Dataset Contributor Guide](./doc/DatasetContributorGuide.md).

### DSAT Cases
DSAT stands for "Dissatisfaction". DSAT cases are usually collected from the downstream responsible AI services. They are the cases that the downstream responsible AI services are not satisfied with the model's performance. Each case is associated with a task. It contains information including the input, trace id, the ground truth label and other information that can help model owners to debug their models. Please refer to [DSAT Case Contributor Guide](./DSATCaseContributorGuide.md) for more details.

## Role-based documentation
If you are a model contributor and want to onboard your model to MOP, please refer to [Model Contributor Guide](./doc/ModelContributorGuide.md).

If you are a dataset contributor and want to upload your dataset to MOP, please refer to [Dataset Contributor Guide](./doc/DatasetContributorGuide.md).

If you want to provide DSAT cases and track its resolution, please refer to [DSAT Case Contributor Guide](./DSATCaseContributorGuide.md).

If you are a downstream responsible AI service admin and want to use MOP to track models that are released to your service, please refer to [Downstream Responsible AI Service Admin Guide](./DownstreamResponsibleAIServiceAdminGuide.md).

If you want to go through model testing results in general, please refer to [Model Testing Results Guide](./doc/ModelTestingResults.md).

## FAQ
### Q: What metrics does MOP use for model evaluation?
- Precision: tp / (tp + fp)
- Recall: tp / (tp + fn)
- F1_score: 2 * (precision * recall) / (precision + recall)
- Averaging methods: macro-average, micro-average, weighted-average

<!--
### Q: How to calculate the average rank percentile of a metric?

A: For a version of a model (i.e. a model revision), MOP will evaluate it on all the datasets connected to a task.
There might be multiple models (and different versions) that are connected to the same task.

The average rank percentile of a metric for a model version is calculated as below (we use f1_score as an example):

1. For all model revisions and all datasets that are connected to the task, calculate the f1_score for each model
   revision on each dataset.
2. Rank the f1_score of each model revision on each dataset from high to low.
3. For a model revision, the average rank percentile of f1_score is the average of the rank percentile of f1_score on
   all datasets.

For example, if there are 3 datasets (D1, D2, D3), and each dataset has 3 model revisions (M1, M2, M3), and the f1_score
of each model revision on each dataset is as below:

```
M1 on D1: 0.90   M1 on D2: 0.92   M1 on D3: 0.91
M2 on D1: 0.91   M2 on D2: 0.73   M2 on D3: 0.93
M3 on D1: 0.90   M3 on D2: 0.89   M3 on D3: 0.88
```

Now we can calculate the average rank percentile of f1_score for M1:

On dataset D1, M1 has the second highest f1_score (out of 3 model revisions), so the rank percentile D1 is 2/3 = 0.67;

On dataset D2, M1 has the highest f1_score (out of 3 model revisions), so the rank percentile D2 is 1/3 = 0.33;

On dataset D3, M1 has the second highest f1_score (out of 3 model revisions), so the rank percentile D3 is 2/3 = 0.67;

The average rank percentile of f1_score for M1 is (0.67 + 0.33 + 0.67) / 3 = 55%.
-->

### Q: How to do the load test?

A: MOP deploys verified model as a service (on a single machine), and MOP will use http client to send requests to the
service.
MOP will gradually increase the number of clients, and each client will send a new request to the service as soon as it
received the response of the previous request.

User failed means MOP get 4xx error code when doing load test. Usually it refers to 429 Too Many Request.

System Failed means MOP get 5xx error code when doing load test.

### Q: Why I cannot see the evaluation results?

We have access control for evaluation results on each dataset for a model. By default, only model owner can see them.

If you are not the owner of the model, you can ask the model owner to publish these results so that others can see them
on MOP. Published evaluation results will be shown on `Tasks -> Evaluation by datasets`
page, `Models -> Your Model -> Evaluation by datasets` page and `Dataset -> <related dataset> -> Evaluation result`
page for all MOP users.

A model owner can go to `Models -> Your Model -> Evaluation by datasets`, choose the results that you want to publish,
and select `Public evaluation result` to publish them.

If you are the model owner, and you cannot see the expected evaluation results, please contact us via
**[Teams Channel](https://teams.microsoft.com/l/channel/19%3aff909a78aec9400198fd23ff2f870b7b%40thread.tacv2/User%2520Support%2520and%2520Feedback?groupId=65192cc8-6d82-48d6-8fb7-109cf913f4f9&tenantId=72f988bf-86f1-41af-91ab-2d7cd011db47)**.

### Q: Why do I fail to install mop-utils package?
The package mop-utils depends on python which version is no lower than 3.8.

### Q: Why the model onboarding status is verifyFailed？
- check provided error message. 
- check logs to get detailed error message and update a new model revision to fix the problem.
- check whether your packages are right using the conda_verify.bat tool. Note, your private package should be no large then 2.5G.

### Q: What is the difference between the load test (perRPS) and load test (perConcurrency)?
- **perRPS**: 

    PerRPS is a type of load test that focuses on testing the system's capacity to handle a given number of 
requests per second. This type of testing is particularly useful when you want to identify the maximum number of 
requests that the system can handle without degrading its performance. 

    The platform uses python async mechanism to send requests to the service, gradually increasing the "target RPS" from 
1 using step 10 ([1,10,20,30,40, ...]). For each target RPS, the platform runs the load test for 5 minutes, and the requests are randomly sent.
  (detailed implementation for randomness: if the target RPS = 5, the platform starts 5 threads at the beginning of each second, and asks each 
thread to send a request right now. In each thread, it will wait a random time between 0 and 1000 millisecond before 
actually sending the request. This is to make sure that the requests are not sent at the same time in each second, but
are sent randomly in each second.)

    The key metrics provided by the platform include the actual RPS, latency percentile, successful request count, 
failed request count, and infrastructure utilization percentage (cpu, memory, gpu, gpu memory, and disk). The 
platform will stop the load test if the failure rate is over 1 percent, and provide the result in graphs with 
the x-axis representing target RPS.

    -  _Recommended scenarios for PerRPS:_

    PerRPS is ideal for scenarios where you need to measure the maximum number of requests that the system can handle
 **(i.e. measure other metrics trending with RPS, such as latency, cpu utilization, etc.)**
before degrading its performance. This type of testing is particularly useful for predicting how the system will 
perform under peak traffic conditions. It's also helpful when you need to identify potential bottlenecks in the system, 
such as high CPU or memory usage, and optimize system resources accordingly.


- **PerConcurrency**:

    PerConcurrency is a type of load test that focuses on testing the system's capacity to handle a given number of 
concurrent users. This type of testing is particularly useful when you want to identify the maximum number of users 
that the system can handle without degrading its performance.

    The platform gradually increases the "concurrency count" from 1, using step 10. For each concurrency count, the 
platform uses the specified number of single-thread clients to send requests. For example, if the concurrency count 
is 3, the platform will have 3 single-thread clients, and each client will send requests continuously. Each client 
is independent of each other, sends a request, gets the response, and then sends the next request with no waiting time.

    The key metrics provided by the platform include the actual RPS, latency percentile, successful request 
count, failed request count, and infrastructure utilization percentage (cpu, memory, gpu, gpu memory, and disk). The 
platform will stop the load test after 5 minutes and provide the result in graphs with the x-axis representing the concurrency count.

    - _Recommended scenarios for PerConcurrency:_

    PerConcurrency is ideal for scenarios where you need to measure the maximum number of concurrent users that the 
system can handle before degrading its performance. This type of testing is particularly useful for predicting how 
the system will perform under peak user conditions. It's also helpful when you need to identify potential bottlenecks 
in the system, such as high CPU or memory usage, and optimize system resources accordingly.