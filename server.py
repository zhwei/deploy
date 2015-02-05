#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import tailer
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


@app.route("/pull")
def pull():
    Events("push")
    return redirect("/")


@app.route("/roll", methods=["GET", "POST"])
def rollback():
    version = request.args.get("version")
    if request.method == "POST":
        Events("rollback", version=version)
        return redirect("/")

    return render_template("roll.html", version=version)


@app.route("/log")
def deploy_log():
    return render_template("log.html")



@app.route('/github/webhook', methods=["POST", ])
def web_hook():
    event = request.headers.get("X-Github-Event")  # push, ...
    deliver = json.loads(request.data.decode())
    return "hello"


@app.route("/ajax/log")
def tail_log():
    with open("/tmp/Deploy.log") as fi:
        return "\n".join(tailer.tail(fi, 1000))


if __name__ == '__main__':
    app.run()
