#!/usr/bin/env python
# encoding: utf-8

from main import app

if __name__ == "__main__":
    app.debug = app.config['DEBUG']
    app.run(port=8001)
