#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import importlib

import tailer
from flask import Flask
from flask import render_template, request, redirect

import configs
from libs import utils
from libs.events import Events
from libs.dataobject import DataObject


app = Flask(__name__)
app.debug = configs.debug


@app.context_processor
def global_template_variable():
    result = {}
    return result

@app.route("/")
def index():
    projects = os.listdir(configs.PROJECT_HOME)
    return render_template("index.html", projects=projects)

def get_fab(name, func_name=None):
    fab = importlib.import_module('projects.{}.fabfile'.format(name))
    if func_name:
        return getattr(fab, func_name, None)
    return fab

@app.route("/p/<name>")
def project(name):
    if name not in os.listdir(configs.PROJECT_HOME):
        return redirect("/")
    project = {
        'name': name,
        'functions': get_fab(name).actions
    }
    return render_template('project.html', project=project)

@app.route("/roll", methods=["GET", "POST"])
def rollback():
    version = request.args.get("version")
    if request.method == "POST":
        Events("rollback", version=version)
        return redirect("/log")

    return render_template("roll.html", version=version)


@app.route("/log")
def log():
    if request.args.get('ajax', None):
        with open("/tmp/Deploy.log") as fi:
            return "\n".join(tailer.tail(fi, 1000))
    return render_template("log.html")


if __name__ == '__main__':
    app.run()
