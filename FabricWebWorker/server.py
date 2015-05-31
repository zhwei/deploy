#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os

import flask

import configs
from libs.task import Task
from libs import utils, logger

app = flask.Flask(__name__)
app.secret_key = 'Hello-World'


@app.context_processor
def global_template_variable():
    return {
        'lock_status': utils.get_lock_status
    }


@app.route("/")
def index():
    return flask.render_template("index.html",
                                 projects=utils.get_projects())


@app.route("/p/<name>")
def project(name):
    if name not in os.listdir(configs.PROJECTS_HOME):
        return flask.redirect("/")
    project = {
        'name': name,
        'functions': utils.import_fab(name).actions
    }
    return flask.render_template('project.html', project=project)


@app.route('/task/<action>/<project>/<function>')
def task(action, project, function):
    if action == 'run':
        Task.run(project, function)
        return flask.redirect('/log/{}/{}'.format(project, function))
    elif action == 'stop':
        Task.stop(project, function)

    return flask.redirect(flask.request.referrer or '/')


@app.route("/log/<project>/<function>")
def log(project, function):
    if flask.request.args.get('ajax', None):
        return logger.tail_log_file(project, function)

    if flask.request.args.get('raw', None):
        template = 'log-raw.html'
    else:
        template = 'log.html'

    return flask.render_template(template, project=project, function=function)


if __name__ == '__main__':
    app.debug = configs.debug
    app.run()
