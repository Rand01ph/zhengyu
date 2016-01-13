#!/usr/bin/env python
# encoding: utf-8

# 绑定的端口
bind='127.0.0.1:8001'
# worker数量
workers=3
backlog=2048
# sync, gevent,meinheld
# worker_class='gevent'
debug=True
proc_name='zhengyu.pid'
pidfile='/home/tan/log/gunicorn/zhengyu.log'
loglevel='debug'
