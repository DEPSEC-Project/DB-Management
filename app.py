from flask import Flask, jsonify, render_template

from depsec_db import create_app

app = create_app()


if __name__ == "__main__":
    app.run()