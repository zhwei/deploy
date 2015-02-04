#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Flask
from flask import render_template, request, redirect

import configs
from libs import utils
from libs.events import Events


app = Flask(__name__)
app.debug = configs.debug


@app.context_processor
def pulls():
    return dict(pulls=utils.get_pulls())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/roll", methods=["GET", "POST"])
def rollback():
    version = request.args.get("version")
    if request.method == "POST":
        event = Events("rollback", None)
        event.rollback(version)
        return redirect("/")

    return render_template("roll.html", version=version)


@app.route('/github/webhook', methods=["POST", ])
def web_hook():
    event = request.headers.get("X-Github-Event")  # push, ...
    deliver = json.loads(request.data.decode())
    return "hello"


if __name__ == '__main__':
    app.run()
