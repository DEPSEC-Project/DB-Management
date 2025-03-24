"""
Fichier qui lance l'application
"""
from flask import Flask, jsonify, render_template
from depsec_db import create_app


app = create_app()

"""
Lance l'application
"""

if __name__ == "__main__":
    app.run()
