#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import argparse

import flask

from libs import utils
from libs.model import Task, Item

app = flask.Flask(__name__)
app.secret_key = 'Hello-World'


@app.context_processor
def global_template_variable():
    return {
        'lockStatus': lambda i: utils.Lock(i).status(),
        'itemType': Item.Type,
    }


@app.route("/")
def index():
    return flask.render_template("index.html", projects=Item.get_projects())


@app.route('/task/<action>/<path:path>')
def task(action, path):
    item = Item(path)
    if action == 'run':
        args = flask.request.args.get('args', None)
        if args:
            Task.run(item, *args.split(','))
        else:
            Task.run(item)
        return flask.redirect('/func/{}'.format(path))

    elif action == 'stop':
        Task.stop(item)

    elif action == 'clear':
        Task.clear(item)

    return flask.redirect(flask.request.referrer or '/')



@app.route("/<type>/<path:path>")
def project(type, path):

    item = Item(path)

    if type == 'func':
        if flask.request.args.get('ajax', None):
            return utils.Logger.tail_log_file(item)

        if flask.request.args.get('raw', None):
            template = 'log-raw.html'
        else:
            template = 'log.html'
    else:
        template = 'project.html'

    return flask.render_template(template, item=item)


# parse args
parser = argparse.ArgumentParser(description='Fabric Web Worker')
parser.add_argument('--host', dest='host', type=str, default='127.0.0.1')
parser.add_argument('--port', dest='port', type=int, default=5000)
parser.add_argument('--debug', dest='debug', type=bool, default=False, help='Debug Mode.')
parser.add_argument('--project', dest='project', type=str, default='projects', help='Your Projects Directory.')
args = parser.parse_args()

# init projects path
Item.PROJECT_ROOT_PATH = os.path.join(os.path.abspath(os.curdir), args.project)


def run():
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    run()
