
"""
Fichier setup pour rendre le projet installable via pip
"""

from setuptools import setup, find_packages

setup(
    name="depsec_models",
    version="0.1",
    packages=find_packages(),
    install_requires=["flask_sqlalchemy"],
)

