from setuptools import find_packages, setup


def find_required():
    required = []
    with open("requirements.txt") as f:
        required = f.read().splitlines()
    return required


setup(
    name="molotov-ext",
    description="",
    version="0.6",
    url="https://gitlab.2gis.ru/pychapter/molotov-ext",
    author="Nikita Tsvetkov",
    author_email="n.tsvetkov@2gis.ru",
    packages=find_packages(),
    install_requires=find_required(),
)
