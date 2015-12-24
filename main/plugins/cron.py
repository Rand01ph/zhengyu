#!/usr/bin/env python
# encoding: utf-8

import requests
from .. import celery, app

@celery.task(name='access_token.update')
def update_access_token():
    """定时更新微信 access_token"""
    requests.get(app.config['HOST_URL'] +
                 app.config['UPDATE_ACCESS_TOKEN_URL_ROUTE'])
