# daGrevis.lv — My blog on Django 1.5 (Python)

I could use Tumblr or WordPress, but that is too easy. :)

## Installation locally

    git clone https://github.com/daGrevis/daGrevis.lv
    cd daGrevis.lv
    virtualenv .
    bin/pip install -r requirements.txt
    sass dagrevis_lv/core/static/stylesheets/main.scss dagrevis_lv/core/static/stylesheets/main.css
    bin/python dagrevis_lv/manage.py syncdb

(`git`, `virtualenv` and `sass` are required)

### Running server

    bin/python dagrevis_lv/manage.py runserver

Then <http://127.0.0.1:8000/>.

### Running tests

    bin/python dagrevis_lv/manage.py test

[![Build Status](https://travis-ci.org/daGrevis/daGrevis.lv.png?branch=master)](https://travis-ci.org/daGrevis/daGrevis.lv)

## On production

Currently, I'm using Nginx and Gunicorn.
