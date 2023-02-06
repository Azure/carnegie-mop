from setuptools import setup
from setuptools import find_packages

setup(
   name='mop_utils',
   version='1.6',
   description='Utilities for MOP',
   packages=['mop_utils'],
   package_dir={'mop_utils': './mop_utils'},
   python_requires='>=3.8.0',
   install_requires = [
      'azureml-contrib-services==1.48',
      'pyraisdk==0.1.0'
   ]
)