#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Flask, request, render_template

from libs.github import GitHub
from libs.dataobject import DataObject

app = Flask(__name__)


@app.route("/")
def index():

    pulls_data = DataObject("pulls")
    if not pulls_data.all():
        github = GitHub()
        pulls = github.get_pull_requests("all")
        pulls_data.init(pulls)

    return render_template("index.html", pulls=pulls_data.all())


@app.route('/github/webhook', methods=["POST", ])
def web_hook():

    event = request.headers.get("X-Github-Event")  # push, ...
    deliver = json.loads(request.data.decode())
    return ""


if __name__ == '__main__':
    app.run()
