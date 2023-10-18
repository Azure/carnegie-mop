# AML Endpoint Deployment troubleshooting

## 1. InferencingClientCallFailed
### simple details description may like below:
```json
(BadRequest) The request is invalid. Code: BadRequest Message: The request is invalid.  
Exception Details: (InferencingClientCallFailed) {
    {
        "errors": {
            {
                "": [
                    "Specified deployment [latest] failed during initial provisioning and is in an unrecoverable state. Delete and re-create."
                ]
            }
        },
        "title": "One or more validation errors occurred."
    }
} Code: InferencingClientCallFailed Message: {
    {
        "errors": {
            {
                "": [
                    "Specified deployment [latest] failed during initial provisioning and is in an unrecoverable state. Delete and re-create."
                ]
            }
        },
        "title": "One or more validation errors occurred."
    }
} Additional Information:Type: ComponentName Info: {
    "value": "managementfrontend"
}Type: Correlation Info: {
    "value": {
        "operation": "92ac12c5481e7f3666f4db7e47faf45e",
        "request": "273525a17208f0f6"
    }
}Type: Environment Info: {
    "value": "eastus"
}Type: Location Info: {
    "value": "eastus"
}Type: Time Info: {
    "value": "2023-03-16T11:10:13.0172602+00:00"
}
```

### Take action:
- Check AML deployment log:   
    Open AML deployment log, and search error to find its details error, and take relative action like below:  
    ![img.png](images/searchDeploymentLog.png)
 
- Check AML environment log:  
    Open AML environment page, open 'Details' tab to see model environment details information, or open "Build log" tab to see environment build log.
   ![img.png](images/amlEnvironmentLog.png) 
 
- Check instance(CPU/GPU) quota limitation exceed or not, and delete useless model.  
   ![](images/deleteUselessModel.png) 
    
- Re-onboarding or upgrade model.

## 2. UserScriptException
### simple details description may like below:
```bash
doc = doc.lower() 
AttributeError: 'NoneType' object has no attribute 'lower' 
The above exception was the direct cause of the following exception: 
Traceback (most recent call last): 
File "/azureml-envs/azureml_e5a841bb5e5f4ad924ef6391789aa059/lib/python3.8/site-packages/azureml_inference_server 
timed_result = main_blueprint.user_script.invoke_run(request, timeout_ms=config.scoring_timeout) 
File "/azureml-envs/azureml_e5a841bb5e5f4ad924ef6391789aa059/lib/python3.8/site-packages/azureml_inference_server 
raise UserScriptException(ex) from ex 
azureml 
inference server http.server.userscrit.UserScritExcetion: Caught an unhandled excetion from the user script
```
![](images/UserScriptException.png)

### Take action:
- Check your deployment log on portal **"Logs->Details"** for more info and then search keyword **"error/fail"** to see error details and then change your **inference.py** codes in your model to fix bug which cause AML endpoint deployment failed, and then re-onboarding model or upgrade model.
