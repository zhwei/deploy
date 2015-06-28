# -*- coding: utf-8 -*-
# Created by zhangwei7@baixing.com on 2015-05-30 15:14

import os
import imp
import signal
import multiprocessing

import fabric.tasks

from . import utils


class Task(object):
    """ Tasks """

    @classmethod
    def test(cls):
        print(Item.PROJECT_ROOT_PATH)

    @classmethod
    def run(cls, item, *args, **kwargs):
        """ Run Fabric Single Function
        :param project: project in `PROJECTS_HOME`
        :param function: function name
        :param args: function args
        :param kwargs: function k-v args
        :return: multiprocessing.Process
        """
        log = utils.Logger(item)
        lock = utils.Lock(item)

        def run_fab(*args, **kwargs):
            lock.lock(os.getpid())
            fab_function = item.load_function()
            utils.Logger.redirect_to_file(item)
            fabric.tasks.execute(fab_function, *args, **kwargs)
            lock.unlock()
            log.log('Task:: {} finished.'.format(item.unit_name))

        if lock.status():
            log.log('Task:: {} stated before. pid: {}'.format(
                item.unit_name, lock.status()))
            return

        log.log('=' * 50)
        log.log('Task:: {} start.'.format(item.unit_name))
        process = multiprocessing.Process(
            target=run_fab,
            args=args,
            kwargs=kwargs
        )
        process.start()
        return process

    @classmethod
    def stop(cls, item):
        """ Kill Running Function """
        lock = utils.Lock(item)
        pid = lock.status()
        log = utils.Logger(item)
        if not pid:
            log.log('Task:: {} has stop.'.format(item.unit_name))
            return

        try:
            os.kill(int(pid), signal.SIGKILL)
        except OSError:
            pass

        lock.unlock()
        log.log('Task:: {} has been killed.'.format(item.unit_name))


class Item(object):
    class Type:
        Directory = 'Directory'
        File = 'File'
        Function = 'Function'

    PROJECT_ROOT_PATH = None

    @classmethod
    def get_projects(cls):
        return [Item(f) for f in os.listdir(cls.PROJECT_ROOT_PATH)]

    def __init__(self, path, parent=None):

        self.path = path
        self.parent = parent
        if ':' in path:
            self.name = path.rsplit(':')[-1]
            self.type = Item.Type.Function
            self.abs_path = self._get_abs_path()
        else:
            self.path = self._merge_path(path)
            self.name = self.path.rsplit('/', 1)[-1]
            self.abs_path = self._get_abs_path()
            self.type = self._get_type()

        # self.abs_path = self._get_abs_path()
        # self.type = self._get_type()
        self.unit_name = self.path.replace('/', '.')

    def _merge_path(self, path):
        if isinstance(self.parent, Item):
            path = self.parent.path + '/' + path
        return path

    def _get_abs_path(self):
        p = os.path.join(Item.PROJECT_ROOT_PATH, self.path.rsplit(':')[0])
        return p

    def _get_type(self):
        # if self.type:
        #     return self.type

        if os.path.isdir(self.abs_path):
            t = Item.Type.Directory
        elif os.path.isfile(self.abs_path):
            t = Item.Type.File
        else:
            t = Item.Type.Function
        return t

    def _validate_type(self, is_type):
        if is_type != self.type:
            raise RuntimeError('type should be `{}`'.format(is_type))

    def get_tree(self):
        if self.parent is None:
            return None
        return self.parent.get_tree()

    def get_children(self):
        if self.type == Item.Type.Directory:
            for f in os.listdir(self.abs_path):
                item = Item(f, parent=self)
                if item.type == Item.Type.File and not f.endswith('.py'):
                    continue
                yield item

        elif self.type == Item.Type.File:
            for i in self.fab().ALL:
                yield Item('{}:{}'.format(self.path, i))

    def load_parent(self):
        s = ':' if self.type == Item.Type.Function else '/'
        return Item(self.path.rsplit(s, 1)[0])

    def load_function(self):
        self._validate_type(Item.Type.Function)
        func_name = self.name
        if self.parent:
            fab = self.parent.fab()
        else:
            fab = self.fab(self.abs_path)
        return getattr(fab, func_name)

    # For File

    def fab(self, path=None):
        if not path:
            self._validate_type(Item.Type.File)
            name, path = self.name, self.abs_path
        else:
            name = path.rsplit('/', 1)[-1]
        return imp.load_source(name, path)

    def __iter__(self):
        for i in self.get_children():
            yield i

    def __str__(self):
        return self.name + ('/' if self.type == Item.Type.Directory else '')
