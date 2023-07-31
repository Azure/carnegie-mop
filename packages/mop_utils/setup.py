from setuptools import setup

setup(
    name='mop_utils',
    version='2.0',
    description='Utilities for MOP',
    packages=['mop_utils'],
    package_dir={'mop_utils': './mop_utils'},
    python_requires='>=3.8.0',
    install_requires=[
        'pyraisdk ~= 0.2',
        'PyYAML >= 6.0',
        'numpy >= 1.22.0',
    ]
)
