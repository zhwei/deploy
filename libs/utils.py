# Created by zhangwei@baixing.net on 2015-02-04 13:26

import os
import importlib

import configs

LOCK_PATH = configs.TEMP_PATH + 'lock/'
os.system('mkdir -p {}'.format(LOCK_PATH))

class Lock(object):
    """ file lock """

    def __init__(self, name):
        self.name = name
        self.lock_file = LOCK_PATH + str(self.name)

    def lock(self, msg='lock'):
        if os.path.isfile(self.lock_file):
            raise Exception('locked before, please unlock')

        with open(self.lock_file, "w") as fi:
            fi.write(str(msg))
        return True

    def unlock(self):
        if not os.path.isfile(self.lock_file):
            return False
        os.remove(self.lock_file)
        return True

    def status(self):
        if not os.path.isfile(self.lock_file):
            return False
        with open(self.lock_file) as fi:
            return fi.read()


def get_lock(project, function):
    return Lock('{}.{}'.format(project, function))


def get_lock_status(project, function):
    """ shotcut function """
    return get_lock(project, function).status()


def get_fab(project, function=None):
    """ get fabric module or function """
    fab = importlib.import_module('projects.{}.fabfile'.format(project))
    if function:
        return getattr(fab, function, None)
    return fab


def get_projects():
    for i in os.listdir(configs.PROJECTS_HOME):
        if i not in ('__init__.py', '__init__.pyc'):
            yield i
