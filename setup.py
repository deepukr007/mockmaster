import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ddgen",
    version="0.0.1",
    author="Deepu Krishnareddy , Harish M",
    author_email="deepukreddy007@gmail.com",
    description=("A CLI tool to generate dummy data "),
    license="Apache 2.0",
    keywords="data dummy",
    packages=['ddgen'],
    long_description=read('README.md'),

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache 2.0",
    ],
    install_requires=['openai', 'pandas',
                      "jsonschema", "python-dotenv", "pyfiglet", "tabulate", "termcolor"],
    entry_points={
        'console_scripts': [
            'ddgen = ddgen.cli:main',
        ],
    }
)
