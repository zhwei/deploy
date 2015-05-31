# Created by zhangwei@baixing.net on 2015-02-03 13:54

debug = True


import os
ROOT = os.path.abspath(__file__).rsplit('/', 1)[0]
get_path = lambda x: os.path.join(ROOT, x)


PROJECTS_HOME = get_path('projects')
TEMP_PATH = '/tmp/'
