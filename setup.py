"""
Fichier setup pour rendre le projet installable via pip
"""
from setuptools import find_packages, setup

setup(
    name="depsec_models",
    version="0.1",
    packages=["depsec_db"],
    package_dir={"depsec_db": "app"},
    install_requires=["flask_sqlalchemy"],
)
