from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open("README.md", "r") as fh:
    setup(
        name='j2v',
        version='1.1.3',
        author="Michal Zasadzinski",
        author_email="michal.zasadzinski@gmail.com",
        description="A tool to generate Looker views and explores from sample JSONs",
        long_description=long_description,
        long_description_content_type='text/markdown',
        url="https://github.com/Cimpress-MCP/j2v",
        packages=find_packages(),
        install_requires=['PyYAML>=5.1'],
        python_requires='>=3',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
        ],
    )
