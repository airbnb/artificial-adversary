from setuptools import setup

setup(
    name='Adversary',
    version='1.1',
    packages=['tests', 'Adversary'],
    url='https://github.com/airbnb/artificial-adversary',
    license='MIT',
    author='Devin Soni',
    author_email='devinsoni1010@gmail.com',
    description='Creates adversarial text examples for machine learning models',
    install_requires=[
        'pandas',
        'nltk',
        'textblob'
    ],
)
