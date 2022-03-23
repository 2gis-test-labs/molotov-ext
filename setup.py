from setuptools import find_packages, setup


def find_required():
    required = []
    with open("requirements.txt") as f:
        required = f.read().splitlines()
    return required


setup(
    name="molotov-ext",
    description="Library for collecting metrics for Molotov",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version="1.0.0",
    url="https://github.com/2gis-test-labs/molotov-ext",
    license="Apache-2.0",
    author="2GIS Test Labs",
    author_email="test-labs@2gis.ru",
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=find_required(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
