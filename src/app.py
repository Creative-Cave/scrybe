import time
import random
import urllib
from main import run
from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route("/")
def home():
  return ("TAKE A LOOK AT MY CANVA DESIGN 🗣️")


def site():
  app.run(host="0.0.0.0", port=random.randint(2000, 9000))


def stay_alive():
  while True:
    start = time.time()

    while True:
      end = time.time()

      # This 15 is for the amount of minutes you change it and take it upto 30 minutes at most
      if ((end - start) >= (15 * 60)):
        urllib.request.urlopen("https://scrybe.writerscave.repl.co")
        break


site_thread = Thread(target=site)
ping_thread = Thread(target=stay_alive)

site_thread.start()
ping_thread.start()

run()
