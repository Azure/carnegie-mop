from setuptools import setup

setup(
    name='mop_utils',
    version='2.1',
    description='Utility SDK for RAI Model Onboarding Pipeline (MOP) model contributor.',
    packages=['mop_utils'],
    package_dir={'mop_utils': './mop_utils'},
    python_requires='>=3.8.0',
    install_requires=[
        'pyraisdk ~= 0.3.7',
        'PyYAML >= 6.0',
        'numpy >= 1.22.0',
    ]
)
