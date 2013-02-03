# daGrevis.lv — My blog on Django 1.4 (Python)

I could use [Tumblr](tumblr.com) or [WordPress](http://wordpress.org/), but that is too easy. :)

## Installation locally

    cd
    mkdir Python
    cd Python
    git clone https://github.com/daGrevis/daGrevis.lv
    virtualenv daGrevis.lv
    cd daGrevis.lv
    bin/pip install -r requirements.txt
    sass dagrevis_lv/core/static/stylesheets/main.scss dagrevis_lv/core/static/stylesheets/main.css
    bin/python dagrevis_lv/manage.py syncdb --noinput

### Run server

    bin/python dagrevis_lv/manage.py runserver

Then open `http://127.0.0.1:8000/` link.

### Run tests

    bin/python dagrevis_lv/manage.py test
