# Environment conda troubleshooting

## 1. CondaDependencyError
### A simplified description might resemble the following:
```bash
Step 8/21 : RUN ldconfig /usr/local/cuda/lib64/stubs && conda env create -p /azureml-envs/azureml_e57c376e843ed0524af2f71285901817 -f azureml-environment-setup/mutated_conda_dependencies.yml && rm -rf "$HOME/.cache/pip" && conda clean -aqy && CONDA_ROOT_DIR=$(conda info --root) && rm -rf "$CONDA_ROOT_DIR/pkgs" && find "$CONDA_ROOT_DIR" -type d -name __pycache__ -exec rm -rf {} + && ldconfig
---> Running in 4de347f830e7
[91m/opt/miniconda/bin/python: /opt/miniconda/bin/../lib/./libtinfow.so.6: no version information available (required by /opt/miniconda/bin/../lib/libpypy3-c.so)
[0m[91m/opt/miniconda/bin/python: /opt/miniconda/bin/../lib/./libtinfow.so.6: no version information available (required by /opt/miniconda/bin/../lib/libpypy3-c.so)
[0mRetrieving notices: ...working... done
Collecting package metadata (repodata.json): ...working... [91m/opt/miniconda/bin/python: /opt/miniconda/bin/../lib/./libtinfow.so.6: no version information available (required by /opt/miniconda/bin/../lib/libpypy3-c.so)
[0m[91m/opt/miniconda/bin/python: /opt/miniconda/bin/../lib/./libtinfow.so.6: no version information available (required by /opt/miniconda/bin/../lib/libpypy3-c.so)
[0m
done
Solving environment: ...working... [91mWARNING conda.resolve:_get_sat_solver_cls(70): Could not run SAT solver through interface 'pycosat'.
[0mfailed
[91m
CondaDependencyError: Cannot run solver. No functioning SAT implementations available.

[0mThe command '/bin/sh -c ldconfig /usr/local/cuda/lib64/stubs && conda env create -p /azureml-envs/azureml_e57c376e843ed0524af2f71285901817 -f azureml-environment-setup/mutated_conda_dependencies.yml && rm -rf "$HOME/.cache/pip" && conda clean -aqy && CONDA_ROOT_DIR=$(conda info --root) && rm -rf "$CONDA_ROOT_DIR/pkgs" && find "$CONDA_ROOT_DIR" -type d -name __pycache__ -exec rm -rf {} + && ldconfig' returned a non-zero code: 1
2023/06/21 07:29:25 Container failed during run: acb_step_0. No retries remaining.
failed to run step ID: acb_step_0: exit status 1

Run ID: cap5 failed after 3m57s. Error: failed during run, err: exit status 1
```

### Take appropriate action:
- Verify whether there are issues with the Docker image. If issues are found, utilize an alternative Docker image and then attempt to re-onboard or upgrade the model.

- Examine the AML image build log to determine if any errors were encountered. Open the <uuid>.txt file to access detailed information.
![img.png](images/amlBuildImageLog.png) 

## 2. CondaEnvException
### A simplified description might resemble the following:
```bash
Downloading mop_utils-1.8-py3-none-any.whl (4.4 k8) 
0[91 mPip subprocess error: 
ERROR: Could not find a version that satisfies the requirement numpy==5.22.0 (from versions: 1.3.O, 1.4.1, l.s.o, 1.5.1, 1.6.C 
ERROR: No matching distribution found for 
CondaEnvException: Pip failed 
2023/06/26 03:34:48 Container failed during run: acb_step_O. No retries remaining. 
failed to run step ID: acb_step_O: exit status 1 
Run ID: ca3b6 failed after 2m19s. Error. failed during run, err: exit status 1 
ev 1 / 6 Next) 
```

### Take appropriate action:
- Examine the AML deployment log:
    Open the AML deployment log, search for errors to find detailed error information, and take appropriate actions as outlined below:
    ![img.png](images/searchDeploymentLog.png)
 
- Verify the AML image build log for errors:
    Open the <uuid>.txt file to access detailed information about encountered errors.
![img.png](images/amlBuildImageLog.png)  
 
- Review the AML image build log for comprehensive details:
   Refer to [Image build failure](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-troubleshoot-online-endpoints?view=azureml-api-2&tabs=python#error-imagebuildfailure)  
 
- Consider re-onboarding or upgrading the model.

