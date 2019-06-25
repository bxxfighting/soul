'''
gunicorn application:app -c gunicorn.py
'''
import os
import multiprocessing

CUR_DIR = os.path.dirname(__file__)

bind = "0.0.0.0:18785"
# workers = multiprocessing.cpu_count() * 2 + 1
chdir = CUR_DIR
preload = True
# 去掉daemon，因为要使用supervisor来管理
# daemon = True
