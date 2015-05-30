# -*- coding: utf-8 -*-
# Created by zhangwei7@baixing.com on 2015-05-30 15:14

import os
import signal
import multiprocessing

import fabric.tasks

from libs import utils


class Task(object):
    """ Tasks """

    @classmethod
    def run(cls, project, function, *args, **kwargs):
        """ Run Fabric Single Function
        :param project: project in `PROJECTS_HOME`
        :param function: function name
        :param args: function args
        :param kwargs: function k-v args
        :return: multiprocessing.Process
        """
        def run_fab(*args, **kwargs):
            lock = utils.get_lock(project, function)
            lock.lock(os.getpid())
            fab_function = utils.get_fab(project, function)
            fabric.tasks.execute(fab_function, *args, **kwargs)
            lock.unlock()

        process = multiprocessing.Process(
            target=run_fab,
            args=args,
            kwargs=kwargs
        )
        process.start()
        return process

    @classmethod
    def stop(cls, project, function):
        """ Kill Running Function """
        lock = utils.get_lock(project, function)
        pid = lock.status()
        if not pid:
            return

        try:
            os.kill(int(pid), signal.SIGKILL)
        except OSError:
            pass

        lock.unlock()
