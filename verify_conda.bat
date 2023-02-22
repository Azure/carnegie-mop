set environment=%1
set python=%2
call conda env remove -n %environment%
call conda create -n %environment% python=%python% -y
call conda activate %environment%
call pip install -r src/requirements.txt

if exist privatepkgs\ (
	for %%f in (.\privatepkgs\*.whl) do (
		echo %%f
		call pip install %%f
	)
) else (
	echo "No private packages"
)

pip install azureml-defaults
pip install PyYAML
pip install pyraisdk
