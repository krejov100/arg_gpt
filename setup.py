from setuptools import setup

setup(
    name='arg-gpt',
    version='0.0.1',
    description="A package to help you build a GPT interface for your python code",
    author="Philip Krejov",
    packages=['arg_gpt'],
    # load from requirements.txt
    install_requires=[line.strip() for line in open("requirements.txt", "r").readlines()]
)