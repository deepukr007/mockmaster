import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="mockmaster",
    version="0.0.2",
    author="Deepu Krishnareddy , Harish Mohan",
    author_email="deepukreddy007@gmail.com , Harishmohan1598@gmail.com",
    description=("A CLI tool to generate dummy data "),
    license="MIT",
    keywords="data dummy",
    packages=['mockmaster'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',


    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
    ],
    install_requires=['openai', 'pandas',
                      "jsonschema", "python-dotenv", "pyfiglet", "tabulate", "termcolor"],
    entry_points={
        'console_scripts': [
            'mockmaster = mockmaster.cli:main',
        ],
    }
)
