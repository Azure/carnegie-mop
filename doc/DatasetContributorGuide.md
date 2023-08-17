# MOP Evaluation Dataset Contributor Guide

For each verified evaluation dataset, MOP will automatically generate evaluation results for all models that can be used to resolve the associated task(s). MOP and model contributor will benefit from these datasets when there are new models/model versions onboarded to MOP, and dataset contributors can continuously get evaluation results for their datasets on latest models.

This guide will walk you through the process of onboarding your datasets to MOP.

## Prerequisites
### Understand MOP Concepts
Please read [MOP Documentation](../README.md) to understand the concepts of MOP.

### Azure Resource
You need an available **Azure Storage Account** to store your dataset files. If you don't have one, please follow [this guide](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal) to create one.

MOP uses Service Principal for authentication. Users should grant the **Storage Blob Data Reader** role to our system (
service principal: **cm-model-onboarding-prod-sp**).
See [Azure RBAC documentation](https://learn.microsoft.com/en-us/azure/role-based-access-control/conditions-role-assignments-portal)

### Prepare Dataset File
You should prepare your dataset csv file in a **Blob Container**:
```
<Your Dataset Folder Name>
│
└─── dataset.csv     # Required
```

The dataset file should be in csv format. Each csv file should contain data columns and one or more label columns. 

For different modalities, we have different format requirements for the dataset file. 

Please visit **[sample datasets](../sample/dataset)** for more details.

#### Text
- The csv file name should be **dataset.csv**.
- The content in the csv should be in **utf-8** encoding.
- There should be only one data column with the header **text**. Each cell in the column should be a sample of text.
- There should be one or more label columns with customised headers. Each cell in the column should be a label for the corresponding sample in the **text** column. Valid label values are different for different label types:
  - If this column is for binary classification (and there are positive and negative labels), the valid label values are `0` and `1`.
  - If this column is for multi-class classification (or binary classification, but you do not have predefined positive and negative labels), the valid label values can be any string. **However, the set of valid label values should be a subset of labels in the task(s) that this dataset will be used for.**
- **No duplicate header name in the csv file.**
- **No null/empty/NaN values are allowed.**
- Using **\t** as the delimiter.
    
#### Image
- The csv file name should be **dataset.csv**.      
- The content in the csv should be in **utf-8** encoding.
- There should be four columns with headers "base64_image", "file_name", "image_width_pixels", "image_height_pixels".  Values for these columns represents sample images in the dataset.
  - The content of column "base64_image" should be the **base64 encoded string** of the image.
  - The content of column " file_name " should include **file name extension**.
  - The content of column "image_width_pixels" and "image_height_pixels" should be positive integer.
- There should be one or more label columns with customised headers. Each cell in the column should be a label for the corresponding sample in the **base64_image** column. Valid label values are different for different label types:
  - If this column is for binary classification (and there are positive and negative labels), the valid label values are `0` and `1`.
  - If this column is for multi-class classification (or binary classification, but you do not have predefined positive and negative labels), the valid label values can be any string. **However, the set of valid label values should be a subset of labels in the task(s) that this dataset will be used for.**
- **No duplicate header name in the csv file.**
- **No null/empty/NaN values are allowed.**
- Using **\t** as the delimiter.

#### ImageAndText
- The csv file name should be **dataset.csv**.
- The content in the csv should be in **utf-8** encoding.
- There should be One column with header "text", representing the text of sample.
- **Up to 20 placeholders** in format `##{image_0}, ##{image_1}, ..., ##{image_19}` are allowed in the text. Placeholders in one text should be in order (from 0) and should not be duplicated. **Text without placeholders is also allowed.**
- **Up to 20 columns** with header "image_0", "image_1", ..., "image_19", representing the images of sample.
- The content of images columns should be the base64 encoded string of an image.
- Image columns should be in order (from 0) and consecutive.
- There should be one or more label columns with customised headers. Each cell in the column should be a label for the corresponding sample in the **text** column. Valid label values are different for different label types:
  - If this column is for binary classification (and there are positive and negative labels), the valid label values are `0` and `1`.
  - If this column is for multi-class classification (or binary classification, but you do not have predefined positive and negative labels), the valid label values can be any string. **However, the set of valid label values should be a subset of labels in the task(s) that this dataset will be used for.**
- **No duplicate header name in the csv file.**
- **No null/empty/NaN values are allowed in the Text column**
- Using **\t** as the delimiter.

## Onboard Your Dataset
### Create Dataset
Go to [MOP portal](https://carnegie-mop.azurewebsites.net), click "Evaluation Datasets" on the left navigation bar, and then click "Add Datasets" button in the top left corner. 

Fill in the form  in the pop-up window:
* **Select dataset modality**: Select the modality of your dataset. There are three valid options: _Text_, _Image_, _ImageAndText_. The modality of your dataset should be consistent with the format of your dataset file.
* **Team**: The team that owns this dataset. **It cannot be changed after the dataset is created.**
* Source Type: The source type of your dataset. There is only one valid option for now: _Blob_.
* **Dataset url**: The url of your dataset file. It should be in the format of `https://<storage account name>.blob.core.windows.net/<container name>/<dataset folder name>`. For example, if your dataset file is in the container `mop` in the storage account `mop`, and the dataset folder name is `sample`, the url should be `https://mop.blob.core.windows.net/mop/sample`. **It cannot be changed after the dataset is created.**
* **Language**: The language of your dataset. **This option is for _Text_ and _ImageAndText_ dataset only. It cannot be changed after the dataset is created.**

  > There might be multiple label columns in the dataset.csv file. Each label column represents a dataset (together with the sample data). 
  > 
  > MOP provides a convenient way to create multiple datasets from one dataset.csv file by mapping each label column to a dataset.
   
* **Label header**: The header of the label column (in the dataset.csv) that you want to map to a dataset. **It cannot be changed after the dataset is created.**
* **Dataset name**: The name of the dataset. It should be unique in MOP. **It cannot be changed after the dataset is created.**
* **Label type**: There are two valid options:
  * _Binary_: The label column is for binary classification and there are positive and negative labels. Selecting this option means that the valid label values in the label column are `0` and `1`.
  * _Multi-label_: The label column is for multi-class classification or binary classification, but you do not have predefined positive and negative labels. Selecting this option means that the valid label values in the label column can be any string.
* **Label size**: The number of classes in the label column. It is a positive integer (>=2), and only valid for _Multi-label_ labels. **It cannot be changed after the dataset is created.**
* **Connected tasks**: The tasks that this dataset will be used for. It is a multi-select option. MOP will provide candidate tasks based on the label type and label size you provided. 
  * _Binary_: This dataset can be used for ordinal tasks, or categorical tasks with two labels `0` and `1`.
  * _Multi-label_: This dataset can be used for categorical tasks with the number of labels you provided.
  > Labels in the label column should be a subset of labels in the tasks that this dataset will be used for.

* **Description**: The description of the dataset. It can be changed after the dataset is created.

> You can click "➕" button on the bottom of the page to add more label columns and datasets. 
> 
> You can also click "🗑" button on the right of each dataset to remove it in your submission.
 
Click `Submit` button to create datasets.

## Manage Your Dataset
> In MOP, the evaluation datasets are stored in a storage account with limited access. Users will only see the dataset metadata in MOP portal. 
> 
> **No sample data and label data will be accessible to users after the dataset is created (even the user who created the dataset).**

### Find Your Evaluation Dataset on MOP
Go to [MOP portal](https://carnegie-mop.azurewebsites.net), click "Evaluation Datasets" on the left navigation bar. You can see a list of datasets, including those that you jsut created, and all other datasets.

#### Using Status filter
MOP supports dataset status filter for users to find datasets that they want to view. Using the dropdown list in the top right corner to filter datasets by status. The default status is _All except outdated and verifyFailed_. So you may need to change the status filter to view all datasets.

#### Using Search box
MOP supports dataset search for users to find datasets that they want to view. Using the search box in the top right corner to search datasets by name.

### Dataset metadata
Click the dataset name to view the metadata of the dataset. The metadata includes:
* **Dataset name**: The name of the dataset.
* **Dataset description**: The description of the dataset. Change it by clicking the "✏️" button.
* Team: The team that owns this dataset.
* Created time: The time when the dataset is created.
* Created by: The user who created the dataset.
* Size (MB): The size of the dataset file in megabytes.
* Modality: The modality of the dataset.
* Related datasets: The datasets that are created from the same dataset file.
* **Status**: MOP will verify the dataset format and content after you submit the dataset. The status describes the status of the dataset during the process. There are following valid status:
  * _created_: The dataset submission is received by MOP. It is the initial status of a dataset.
  * _verified_: The dataset format and content are verified by MOP. A dataset with this status is ready to be used for evaluation.
  * _verifyFailed_: The dataset format and content are verified by MOP. However, the dataset does not meet the requirements. There will be a message in the status description to describe the reason. 
    
    If you can locate the issue in your dataset.csv file, you can fix it and put the dataset.csv file in the same location as the original one. Then click _retry_ button to submit the dataset again. MOP will verify the dataset again.
  * Status description: The description of the status. If the status is _verifyFailed_, it will describe the reason why the dataset verification failed.
  * Dataset source type: The source type of the dataset. There is only one valid option for now: _Blob_.
  * Dataset path: The Azure Blob url of the dataset file when you submit your dataset.
  * Label header: The header of the label column (in the dataset.csv) that you want to map to this dataset.
  * Connected tasks: The tasks that this dataset will be used for.
  * Sample number: The number of samples in the dataset.
  * Label ratio: The ratio of each label in the dataset.
  * Language: The language of the dataset. It is only valid for _Text_ and _ImageAndText_ dataset.

### Update bound task
Click the `Update bound task` button to update the tasks that this dataset will be used for. You can select tasks from the dropdown list. The tasks are filtered based on the label type and label size of the dataset. Your current operation will cover the existing tasks that this dataset is bound to.

## View Evaluation Metrics on MOP
See [Model Testing results](./doc/ModelTestingResults.md).