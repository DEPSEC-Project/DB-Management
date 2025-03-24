"""
Fichier setup pour rendre le projet installable via pip
"""
from setuptools import find_packages, setup

__version__ ="0.5.0"
setup(
    name="depsec_models",
    version=__version__,
    packages=find_packages(),
    install_requires=["flask_sqlalchemy"],
)
