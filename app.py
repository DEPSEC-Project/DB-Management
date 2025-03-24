from flask import Flask, jsonify, render_template
<<<<<<< Updated upstream
from app import create_app
=======

from depsec_db import create_app

>>>>>>> Stashed changes
app = create_app()


if __name__ == "__main__":
    app.run()