
"""
Fichier setup pour rendre le projet installable via pip
"""

from setuptools import setup, find_packages

setup(
    name="depsec_models",
<<<<<<< Updated upstream
    version="0.1",
    packages=find_packages(),
=======
    version="0.3",
    packages=find_packages(),
    package_dir={"depsec_db": "app"},
>>>>>>> Stashed changes
    install_requires=["flask_sqlalchemy"],
)

