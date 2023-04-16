import random
from main import run
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return ("TAKE A LOOK AT MY CANVA DESIGN 🗣️")


def site():
    app.run(host="0.0.0.0", port=random.randint(2000, 9000))


site()
run()
