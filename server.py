#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os

import flask
import tailer

import configs
from libs.task import Task
from libs import utils

app = flask.Flask(__name__)



@app.context_processor
def global_template_variable():
    return {
        'lock_status': utils.get_lock_status
    }


@app.route("/")
def index():
    return flask.render_template("index.html", projects=get_projects())


@app.route("/p/<name>")
def project(name):
    if name not in os.listdir(configs.PROJECTS_HOME):
        return flask.redirect("/")
    project = {
        'name': name,
        'functions': utils.get_fab(name).actions
    }
    return flask.render_template('project.html', project=project)

@app.route('/task/<action>/<project>/<function>')
def task(action, project, function):
    if action == 'run':
        Task.run(project, function)
    elif action == 'stop':
        Task.stop(project, function)
    return flask.redirect(flask.request.referrer)

@app.route("/log")
def log():
    if flask.request.args.get('ajax', None):
        with open("/tmp/Deploy.log") as fi:
            return "\n".join(tailer.tail(fi, 1000))
    return flask.render_template("log.html")


if __name__ == '__main__':
    app.debug = configs.debug
    app.run()
