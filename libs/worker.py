# Created by zhangwei@baixing.net on 2015-02-05 13:33
# Thread Worker

import threading


class _Worker(object):

    lock = threading.Lock()

    def run(self, func, *args, **kwargs):
        with self.lock:
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()


worker_instance = _Worker()
