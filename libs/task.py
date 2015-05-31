# -*- coding: utf-8 -*-
# Created by zhangwei7@baixing.com on 2015-05-30 15:14

import os
import signal
import multiprocessing

import fabric.tasks

from libs import utils, logger


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
        log = logger.Logger(project, function)
        lock = utils.get_lock(project, function)

        def run_fab(*args, **kwargs):
            lock.lock(os.getpid())
            fab_function = utils.import_fab(project, function)
            logger.redirect_stdout_to_file(project, function)
            fabric.tasks.execute(fab_function, *args, **kwargs)
            lock.unlock()
            log.log('Task:: {}.{} finished.'.format(project, function))

        if lock.status():
            log.log('Task:: {}.{} stated before. pid: {}'.format(
                project, function, lock.status()))
            return

        log.log('=' * 50)
        log.log('Task:: {}.{} start.'.format(project, function))
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
        log = logger.Logger(project, function)
        if not pid:
            log.log('Task:: {}.{} has stop.'.format(project, function))
            return

        try:
            os.kill(int(pid), signal.SIGKILL)
        except OSError:
            pass

        lock.unlock()
        log.log('Task:: {}.{} has been killed.'.format(project, function))