from setuptools import setup, find_packages

setup(
    name='nlp-service',
    version='0.0.1',
    description='NLP Service',
    packages=find_packages(),
    author='Othmane Zoheir',
    author_email='othmane@rumorz.io',
    install_requires=[
        'nltk',
    ],
)
