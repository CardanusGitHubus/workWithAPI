# coding: utf-8
#from distutils.core import setup
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
    setuptools.setup(
        name="testTrelloAPI_CardanusGitHubus",
        version="0.0.1",
        author="CardanusGitHubus",
        author_email="lebedev.free@gmail.com",
        description="A test study package for work with Trello API",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/CardanusGitHubus/workWithAPI",
        packages=setuptools.find_packages(),
        classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent", ], python_requires='>=3.6',
    )
